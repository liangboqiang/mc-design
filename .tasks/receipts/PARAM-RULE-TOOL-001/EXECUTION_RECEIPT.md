# PARAM-RULE-TOOL-001 执行回执

## 任务定位

把已存在的零部件参数规则资源接入客户端本地工具 `design_parameter_prepare`，使连杆、活塞销、止推片的四分支判断和参数计算不再只依赖 skill 文本说明或 LLM 推断。

## 覆盖问题

- P0 行 2-5：参数齐全、参数不全/无参数、仅边界参数、混合参数四分支返回结构化结果。
- P0 行 6：缺参时返回三种操作选项：直接按现有参数生成受限建模计划、补充参数后建模、查看模板全部设计参数。
- P0 行 10：输出候选 NX 参数 ID/表达式候选，但仍禁止把中文参数名直接进入 NX 写入计划。
- SKILL-CONSIST-001-P0-001：阶段缓解。规则仍在 skill 资产包中，但客户端工具面已经读取机器化 `part_rules.json` 和 `part_rule_calculator.py`，不再只靠硬编码说明。

## 改动文件

- `mc-design-nx/client/src/mc_design_client/tools/design_flow_provider.py`
- `mc-design-nx/client/tests/test_design_flow_tools.py`
- `mc-design-nx/client/tests/test_asset_store.py`

## 关键实现

- `design_parameter_prepare` 识别 `conrod/连杆`、`piston_pin/活塞销`、`thrust_washer/止推片` 后，优先加载 `logic-expression-design/scripts/part_rule_calculator.py`。
- 资产定位兼容两种运行形态：
  - 开发仓库：`mc-design-nx/assets/source/skills/logic-expression-design`
  - 已安装客户端：`client/resources/agent_assets.mcdpkg` 投影到 `client/data/asset_views/runtime-agentloop`
- 返回结构新增：
  - `input_branch`
  - `calculated_parameters`
  - `calculated_formula_output_map`
  - `missing_questions`
  - `operation_options`
  - `template_design_parameters`
  - `formula_output_slots`
  - `design_parameter_dictionary`
  - `modeling_preconditions`
  - `cannot_model_reasons`
  - `rule_trace`
- 2026-06-14 追加收紧：设计参数标准 ID、标准中文名、编码和参数词典映射的唯一真相源是 MySQL 参数词典 `nx_param_dic_cn_v2`。规则包、Excel、公式脚本输出、历史测试用例和 NX 候选只允许作为公式槽位/计算依据，不允许作为标准参数 ID/名称来源。
- 未识别零件或规则资源不可用时，保留原通用分支逻辑作为兜底。

## 验证结果

命令：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest mc-design-nx/client/tests/test_design_flow_tools.py mc-design-nx/client/tests/test_asset_store.py mc-design-nx/assets/source/skills/logic-expression-design/tests/test_part_rule_calculator.py
```

结果：`21 passed`

命令：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest mc-design-nx/client/tests/test_tool_registry.py mc-design-nx/client/tests/test_agent_loop_assets.py mc-design-nx/client/tests/test_design_skill_contract.py
```

结果：`51 passed`

## 当前边界

- 这次没有调用真实 NX，不验证 NX 写参数。
- `nx_write_gate.allowed_now=false`，仍要求先通过 `mysql_query` 查询 MySQL 参数词典取得标准设计参数 ID/名称，再读取真实 NX 驱动参数并确认映射。
- 后续需要用本地 `test_agent_turn` 或客户端界面重跑 P0 参数四分支业务用例，确认 agent 会主动调用 `design_parameter_prepare` 并展示工具返回结果。
