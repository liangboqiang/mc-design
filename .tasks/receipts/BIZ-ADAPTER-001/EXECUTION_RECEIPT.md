# BIZ-ADAPTER-001 执行回执

## 结论

已新增 `tool.design_flow` 业务适配工具组，并接入 Python client 本地工具目录、Tjuae inline plugin HTTP executor、静态工具资产和设计技能流程。该工具组不在 NX plugin 中，不执行 NX 写入、保存或 TC 上传，只输出结构化业务状态和 NX 写入前建模计划。

本次未修改 `mc-design-ai-service`，因此不需要项目负责人手动更新 K8s 才能验证本次新增的本地业务适配工具。`query_ipm_list`、`connect_qpp`、`query_ecr_list` 仍保留为 K8s 动态 connector catalog 返回的原子 connector。

## 改动文件清单

- `mc-design-nx/client/src/mc_design_client/tools/design_flow_provider.py`
- `mc-design-nx/client/src/mc_design_client/tools/registry.py`
- `mc-design-nx/client/src/mc_design_client/app.py`
- `mc-design-nx/client/src/mc_design_client/runtime/tjuae_runtime_adapter.py`
- `mc-design-nx/client/resources/tool_execution_map.json`
- `mc-design-nx/assets/source/tools/tool.design_flow/TOOL.md`
- `mc-design-nx/assets/source/tools/INDEX.md`
- `mc-design-nx/assets/source/agents/design_agent/runtime.md`
- `mc-design-nx/assets/source/skills/part-design/SKILL.md`
- `mc-design-nx/assets/source/skills/logic-expression-design/SKILL.md`
- `mc-design-nx/assets/source/skills/parameter-mapping/SKILL.md`
- `mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md`
- `mc-design-nx/assets/source/skills/external-connector-adapter/SKILL.md`
- `mc-design-nx/client/tests/test_design_flow_tools.py`
- `mc-design-nx/client/tests/test_tool_registry.py`
- `.tasks/receipts/BIZ-ADAPTER-001/EXECUTION_RECEIPT.md`

## 新增/修改工具

工具组：`tool.design_flow`

执行位置：`mc_design_client.tools.design_flow_provider.DesignFlowToolProvider`

Executor namespace：

- `design_flow`
- `tool.design_flow`

### design_task_normalize

用途：把 IPM/ECMS/QPP 返回、用户直接输入任务编号、用户描述统一成 `task_candidates`。

入参：

- `source_results`: object，可含 `ipm`、`ecms`、`qpp`
- `ipm_result` / `ecms_result` / `qpp_result`: object/string/list
- `items`: array
- `source`: string
- `task_id`: string
- `user_input` / `description`: string

出参：

- `ok`
- `task_candidates`
- `candidate_count`
- `external_interface_issues`
- `state`
- `next_actions`

QPP 不通、超时或返回 `ok=false` 时返回：

- `external_interface_issues[].category = "external_interface_unavailable"`
- `external_interface_issues[].mc_design_failure = false`

### design_task_select

用途：根据用户选择的任务编号或候选序号生成 `selected_task_context`，并按 `conversation_id` 持久保存多轮上下文。

入参：

- `conversation_id`: string
- `task_candidates`: array
- `selection`: string
- `task_id`: string
- `confirmed`: boolean

出参：

- `ok`
- `selected_task_context`
- `task_candidates`
- `state`
- `selection_source`

### design_input_classify

用途：按五类参数输出统一参数表。

分类：

- `design_parameter`
- `boundary_parameter`
- `template_parameter`
- `drive_parameter`
- `associated_parameter`

入参：

- `parameters`: array
- `parameter_classes`: object
- `user_input`: string

出参：

- `ok`
- `parameter_classes`
- `parameters`
- `counts`
- `unclassified`
- `warnings`
- `state`

### design_parameter_prepare

用途：执行四类参数分支判定。

分支：

- `parameters_complete`: 参数齐全
- `parameters_missing`: 参数不全/无参数
- `boundary_only`: 仅边界参数
- `mixed_parameters`: 混合参数

入参：

- `classified_parameters`: object
- `parameters`: array
- `template_required_parameters`: array
- `required_parameters`: array

出参：

- `ok`
- `branch`
- `branch_label_cn`
- `state`
- `parameters`
- `parameter_classes`
- `template_required_parameters`
- `covered_template_parameters`
- `missing_parameters`
- `counts`
- `question_prompts`
- `next_actions`
- `nx_write_gate`

### design_modeling_plan_build

用途：生成 NX 写入前建模计划，只输出计划，不直接写 NX。

入参：

- `conversation_id`: string
- `selected_task_context`: object
- `template_context`: object
- `prepared_parameters`: object
- `parameters`: array
- `parameter_mappings`: array
- `drive_parameters`: array

出参：

- `ok`
- `state`
- `modeling_plan`
- `warnings`

关键约束：

- `modeling_plan.plan_only = true`
- `modeling_plan.side_effects_executed = false`
- 仅当 `nx_expression_name` 不含中文、符合安全表达式命名、并存在于已读取 `drive_parameters` 中时，才进入 `modeling_plan.nx_parameter_updates`
- 中文参数名、中文显示名、模板字段名会进入 `blocked_parameters`，不会进入 NX 写入计划

## 业务状态机说明

1. `任务候选归一`
   - 外部 connector 原子调用结果或用户输入进入 `design_task_normalize`
   - 输出 `task_candidates`
   - 外部接口不可用按 `external_interface_unavailable` 分类

2. `任务选择保持`
   - 用户选择任务编号或候选序号后调用 `design_task_select`
   - 输出并持久化 `selected_task_context`
   - 后续多轮同一 `conversation_id` 可直接恢复

3. `模板/参数确认`
   - 模板仍通过 `teamcenter-flow` 查询 TC `智能体模板库`
   - 参数先调用 `design_input_classify` 归入五类

4. `参数分支判定`
   - 调用 `design_parameter_prepare`
   - 输出四类分支、缺失参数、追问和下一步动作
   - 任何分支默认 `nx_write_gate.allowed_now=false`

5. `NX 写入前计划`
   - 读取真实 NX 驱动参数和参数映射后调用 `design_modeling_plan_build`
   - 只输出待确认计划
   - 用户确认前不允许调用 `nx_update_param` 或 `nx_batch_update_params`

6. `后续副作用阶段`
   - NX 写入、模型保存、二维图、报告、DFMEA 和 TC 上传仍分别由对应技能和工具处理
   - TC 上传必须另行确认上传清单

## 与零部件需求文档的覆盖关系

需求文档中的流程要求已覆盖：

- “任务抓取展示”：`query_ipm_list`、`connect_qpp`、`query_ecr_list` 继续作为原子 connector，返回后由 `design_task_normalize` 统一成 `task_candidates`
- “用户选择任务编号”：`design_task_select` 生成并保持 `selected_task_context`
- “模板确认”：skill 更新要求先有任务上下文，再通过 `teamcenter-flow` 查询 TC `智能体模板库`
- “三种操作选择”：`design_parameter_prepare` 返回参数分支、缺失参数和下一步动作，支持直接计划、补充参数、查看模板参数
- “四类参数情形”：`design_parameter_prepare` 覆盖参数齐全、参数不全/无参数、仅边界参数、混合参数
- “边界参数换算前置”：`boundary_only` 和 `mixed_parameters` 分支输出 `needs_boundary_conversion`
- “NX 写入前确认”：`design_modeling_plan_build` 只生成计划，不写入 NX；中文参数名不能进入写入计划
- “建模后 TC/图纸/DFMEA/报告”：skill 更新保持后续阶段门禁，本任务未执行真实 NX 写入、TC 上传或 DFMEA 文件生成

问题跟踪表中的重点问题已覆盖：

- “未实现任务参数转化及引导式用户提供数据”：新增四类分支稳定输出
- “推送三种操作选项”：分支输出 `next_actions` 和 `question_prompts`
- “任务编号多轮保持”：`design_task_select` 按 `conversation_id` 保存上下文
- “修改参数有时候没转换用参数ID修改，工具调用用的是中文描述”：`design_modeling_plan_build` 阻止中文名进入 NX 写入计划

## namespace 修复说明

已确认并扩展 Tjuae inline plugin 本地工具 namespace 映射：

- `tool.nx -> namespace=tool.nx`
- `tool.local_file -> namespace=tool.local_file`
- `tool.dfmea -> namespace=tool.dfmea`
- `tool.design_flow -> namespace=tool.design_flow`

`ClientApp.invoke_tool` 支持：

- `nx` / `tool.nx`
- `local` / `local_file` / `tool.local_file`
- `dfmea` / `tool.dfmea`
- `design_flow` / `tool.design_flow`
- `connector.*` 转发 K8s connector

`dfmea_*` 不再经 `local` namespace 声明或调用，避免被本地 API 以 `TOOL_NAMESPACE_UNSUPPORTED` 拒绝。

## 测试命令和结果

执行目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx`

使用 Python：`C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`

已执行：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client/tests/test_design_flow_tools.py -q
```

结果：`4 passed`

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client/tests/test_tool_registry.py -q
```

结果：`23 passed`

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client/tests/test_tjuae_runtime_adapter.py -q
```

结果：`19 passed`

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client/tests/test_design_skill_contract.py -q
```

结果：`18 passed`

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client/tests/test_dfmea_tools.py -q
```

结果：`8 passed`

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client/tests/test_usage_issue_fixes.py -q
```

结果：`11 passed`

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client/tests -q
```

结果：`185 passed in 19.96s`

## K8s 说明

本次未修改 `mc-design-ai-service`。新增能力位于 `mc-design-nx` Python client 本地工具层和静态资产层，因此不需要手动更新 K8s 才能验证 `tool.design_flow` 本地工具链。

如果后续决定把 `tool.design_flow` 迁移或复制到 AI Service 侧聚合工具，则需要项目负责人手动更新 K8s 后才能做全通路测试。
