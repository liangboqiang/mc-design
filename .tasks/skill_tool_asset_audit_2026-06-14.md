# Skill/Tool/Asset Audit Issues - 2026-06-14

## 审计结论

本次审计对象为 `mc-design-nx/assets/source/agents`、`mc-design-nx/assets/source/skills`、`mc-design-nx/assets/source/tools`、运行资产包 `mc-design-nx/client/resources/agent_assets.mcdpkg`、NX manifest、以及 `mc-design-ai-service` connector/runtime 相关说明和测试。

当前未发现会直接导致运行资产缺文件、禁用工具误暴露或 K8s connector 不可用的问题：

- Source 与运行资产包一致：13 个 skill、3 个 tool 全部进入 `agent_assets.mcdpkg`。
- 运行资产包未包含 `nx-auto-drawing`、`nx_run_auto_drawing`、`nx_open_tc_drawing`、`tool.mysql`、`tool.external`、`tool.teamcenter`、用户可见 Beya 文案。
- NX manifest 当前 20 个工具，保留 `nx_open_tcpart`，自动出图/Sheet 级图纸工具未暴露。
- `mc-design-nx` 关键静态/资产测试：53 passed。
- `mc-design-ai-service` runtime/connector 测试：63 passed, 1 warning。

但存在以下架构整洁度、扩展性和一致性问题，需进入监管台账。

## 问题记录

| 编号 | 问题 | 类型 | 优先级 | 状态 | 证据 | 建议任务 |
|---|---|---|---|---|---|---|
| AUDIT-ST-001 | 零件规则仍硬编码在 skill/runtime 中，新增零件或规则变更仍需要改正文。 | 已有问题 + 新证据 | P0 | 已记录，待 SK-003 | `runtime.md`、`part-design/SKILL.md`、`logic-expression-design/SKILL.md` 仍要求连杆继续加载 `conrod-design`；`conrod-design/SKILL.md` 仍含完整参数表、公式和 Python 脚本。 | `SK-003` |
| AUDIT-ST-002 | Runtime/Tjuae 中性命名未完全收口，AI Service 内部仍有 Beya 兼容命名。 | 新发现 | P1 | 已记录，待整改 | `beya_mcp`、`beya.toml`、`BEYA_LLM_*`、`BeyaApiKeyMiddleware` 仍作为兼容面存在；当前用户可见资产已去 Beya 化，但内部命名不优雅。 | `RT-NAME-001` |
| AUDIT-ST-003 | Teamcenter connector schema 暴露 `BEYA_TC_BASE_URL` 作为显式输入字段，与 tjuae 中性接口不一致。 | 新发现 | P1 | 已记录，待整改 | `mc-design-ai-service/tools/business/teamcenter/teamcenter.py` 的 `tc_call` 入参和描述包含 `BEYA_TC_BASE_URL`。 | `RT-NAME-001` |
| AUDIT-ST-004 | Agent 索引与实际 runtime skill 列表不完全一致，文档索引可能误导后续智能体。 | 新发现 | P2 | 已记录，待整改 | `agents/INDEX.md` 的主要 skill 少列 `nx-parameter`、`nx-visual`、`design-verification`、`dfmea-risk-review`，但 `runtime.md` 和资产包包含这些 skill。 | `ASSET-GOV-001` |
| AUDIT-ST-005 | 报告模板仍硬编码为连杆模板，报告能力对活塞销、止推片等零件泛化不足。 | 已有问题 + 新证据 | P1 | 已记录，待方案 | `design-report/SKILL.md` 只允许 `<asset_root>/skills/design-report/templates/conrod_design_report_template.docx`；`SK-002-REVIEW` 已指出报告模板硬编码未纳入规则包 schema。 | `REPORT-TEMPLATE-001` |
| AUDIT-ST-006 | Skill capabilities 声明没有统一机器校验；静态工具、动态 connector、能力组混写，后续容易出现引用失真。 | 新发现 | P1 | 已记录，待整改 | capabilities 中同时存在 `mysql_query`、`tc_call`、`tool.nx.query`、`dfmea_template_*` 等不同层级；当前依靠测试和人工约束，没有统一解析规则。 | `ASSET-GOV-001` |
| AUDIT-ST-007 | `logic-expression-design/resources/minimal_test_cases.json` 仍承担三零件 fixture 职责，和后续 part-rules 方向重叠。 | 已有问题 + 新证据 | P1 | 已记录，待 SK-003/后续 | 当前最小用例包含连杆、活塞销、止推片；`SK-002-REVIEW` 要求后续由 `part-rules/resources/test_cases/` 接管。 | `SK-003` 后续 |
| AUDIT-ST-008 | NX manifest 中 `nx_test` 作为连接检查工具名称不够语义化，可能被误解为测试/开发工具。 | 新发现 | P2 | 已记录，待评估 | `nx_tools_manifest.json` 暴露 `nx_test`；`nx-operation/SKILL.md` 说明当前连接检查工具是 `nx_test`。 | `NX-TOOL-NAMING-001` |
| AUDIT-ST-009 | 资产导出仍保留 `beya.md` fallback，符合兼容策略但长期看会增加运行资产解释成本。 | 新发现 | P2 | 已记录，暂不整改 | `export_assets.py` 中 `AGENT_ASSET_FILENAMES = ("runtime.md", "beya.md")`；当前包优先 runtime.md，未把 Beya 文案打入运行包。 | 后续兼容清理 |
| AUDIT-ST-010 | 仓库根目录仍存在安装后的 `client/` payload，与 `mc-design-nx/client` 源码目录重复，且包含旧 beya 运行数据/依赖痕迹。 | 新发现 | P1 | 已由 `CLIENT-ACTIVE-ROOT-001` 有条件关闭 | 根 `client/` 非敏感 payload 已归档移除，活跃根目录仅剩含本机 `tc_key` 的 `client/configure/mc-design-client.config`，需项目负责人确认后续保留、迁移或删除。 | 无新任务；人工确认配置处理策略 |
| AUDIT-ST-011 | `assets/source/tools/*/TOOL.md` 只是工具说明资产，实际执行在 Python provider；缺少 TOOL.md -> provider spec -> HTTP executor 的机器校验映射。 | 新发现 | P1 | 已由 `CLIENT-ACTIVE-ROOT-001` 关闭 | `mc-design-nx/client/resources/tool_execution_map.json` 已建立 TOOL.md -> provider -> registry -> HTTP executor -> Tjuae namespace 映射，测试 48 passed。 | 无新任务 |
| AUDIT-ST-012 | 需求文档要求的任务抓取、模板确认、参数分类、参数换算、建模计划目前主要靠 skill 编排，缺少一个可调用、可测试的业务适配工具层。 | 新发现 | P0 | 已由 `BIZ-ADAPTER-001` 阶段关闭 | 新增 `tool.design_flow`，覆盖 `design_task_normalize`、`design_task_select`、`design_input_classify`、`design_parameter_prepare`、`design_modeling_plan_build`；复跑相关测试 83 passed。后续转入真实 agent-turn 回归验证。 | 无新任务；回归验证 |
| AUDIT-ST-013 | 本地工具进入 tjuae inline plugin 时 namespace 映射过粗，`tool.dfmea` 可能被声明成 `local`，导致 tjuae 调用回本地 API 后被 `ClientApp.invoke_tool` 拒绝。 | 新发现 | P0 | 已由 `BIZ-ADAPTER-001` 阶段关闭 | `tool.local_file`、`tool.dfmea`、`tool.nx`、`tool.design_flow` executor namespace 已映射到对应工具组，并有 `test_tjuae_runtime_adapter.py`/`test_tool_registry.py` 覆盖。 | 无新任务；回归验证 |
| AUDIT-ST-014 | 外部任务查询工具仍是原子 connector，缺少“跨 IPM/ECMS/QPP 聚合、任务编号选择、多轮任务上下文保持”的本地业务适配输出。 | 新发现 | P0 | 已由 `BIZ-ADAPTER-001` 阶段关闭 | 本地侧已输出 `task_candidates`、`selected_task_context`、`external_interface_issues`，QPP 不通时归类为外部接口不可用。真实 IPM/QPP/ECMS 业务链路仍需后续 agent-turn 回归。 | 无新任务；回归验证 |
| AUDIT-ST-015 | NX plugin 自动出图源码仍在 `AutoDrawingTools.cs` 中保留 `[Tool]` 方法，当前靠 ToolManager/manifest/client registry 多层禁用兜底；长期应降低编译暴露面。 | 新发现 | P1 | 已由 `NX-TOOL-HARDEN-001` 阶段关闭 | `ToolManager` 禁用表、manifest 生成、客户端 registry 和 `tool.nx` 说明均继续过滤自动出图/Sheet 级工具；直接调用禁用工具返回 `NX_DRAWING_TOOL_DISABLED`。未跑 NX 实机编译。 | 无新任务；实机补验 |
| AUDIT-ST-016 | NX plugin 与本地 API 对请求体大小、坏 JSON、并发和错误码保护不足，容易把协议错误表现为非结构化异常。 | 新发现 | P1 | 已由 `NX-TOOL-HARDEN-001` 阶段关闭 | NX plugin 和本地 API 已补 1 MiB body、坏 JSON、非 object、非法 Content-Length、并发 busy 等结构化错误码；Python 静态编译与相关测试通过。 | 无新任务；实机补验 |
| AUDIT-ST-017 | K8s connector 直连可用，但本地 agent-turn 工具面没有暴露 IPM 查询/任务选择能力，导致用户任务选择链路无法闭环。 | REG-P0-FULL-001 新发现 | P0 | 已记录，待整改 | `REG-P0-FULL-001` 回执显示 `query_ipm_list` 直连 K8s 可用且一致性通过，但本地 agent-turn 两轮均提示“未找到 IPM 任务相关的查询工具或接口定义”，业务结果为 `context_task_selection_not_confirmed`。 | 待新编号 |
| AUDIT-ST-018 | 参数四分支虽然能通过 agent-turn transport 返回，但业务断言不通过，说明 skill/tool 流程仍未稳定绑定参考逻辑和真实 NX 参数 ID。 | REG-P0-FULL-001 新发现 | P0 | 已记录，待整改 | `REG-P0-FULL-001` 回执显示连杆参数齐全、活塞销缺参、止推片边界、连杆混合四类分支均为 `BUSINESS_ASSERTION_FAILED`；未调用 NX 参数读取工具确认真实表达式 ID。 | 待新编号 |
| AUDIT-ST-019 | MCP/local `files` 入参在 schema 和 TurnCommand 中存在，但进入 tjuae SDK 前被丢弃，导致附件/文件上下文实际不可见。 | 本轮审计新发现 | P0 | 已由 `RUNTIME-CONTEXT-001` 阶段关闭 | `_compose_sdk_input()` 已注入 files 安全摘要、runtime prompt、prompt metadata、tool directory 和 connector visibility；客户端测试 197 passed。 | 真实 agent-turn 回归 |
| AUDIT-ST-020 | runtime 基础提示、工具目录和动态 connector 目录未稳定注入 agent-turn 模型输入，真实链路可能只看到裸 query。 | 本轮审计新发现 | P0 | 已由 `RUNTIME-CONTEXT-001` 阶段关闭 | `query_ipm_list/query_ecr_list/connect_qpp/mysql_query/tc_call` 可见性进入 SDK input；未改 AI Service，`K8S_UPDATE_REQUIRED=false`。 | 真实 agent-turn 回归 |
| AUDIT-ST-021 | NX 视图切换和截图工具存在结果确认不严与错误不可诊断问题。 | REG-P0-FULL-001 + 本轮审计 | P0 | 源码阶段已由 `NX-VISUAL-002` 关闭，待实机验证 | `nx_switch_view` 增加已存在视图匹配与确认；`nx_create_image` 增加 path/size/sha256 和结构化错误。当前运行中 NX plugin 仍加载旧程序集。 | 加载新 NX plugin 后实机补验 |
| AUDIT-ST-022 | 客户端正式启动/安装卸载链路仍不稳，fresh install 后 `tc_key_configured=false` 会阻塞 TC/NX 全链路。 | E2E/REG 新发现 | P0 | 已由 `CLIENT-LAUNCHER-002` 阶段关闭，待本机配置前置 | Launcher 增加日志、端口等待、配置检查；安装/卸载隔离 smoke 通过；启动 smoke 按 `TC_KEY_NOT_CONFIGURED` 停止。 | 配置 `tc_key_configured=true` 后复测 |
| AUDIT-ST-023 | NX 参数工具缺少“中文/别名 -> 真实表达式 ID”的可审计解析面，部分失败路径还会退化为空引用异常。 | 本轮审计新发现 | P0 | 源码阶段已由 `NX-PARAM-002` 关闭，待实机验证 | 新增/加固参数解析与安全写入；修复 `HighLightDim` 空引用路径；C# build 通过。当前运行中 NX plugin 仍加载旧程序集。 | 加载新 NX plugin 后实机补验 |

## 已验证通过项

1. `NX-DRAW-001` 已解决自动出图插件暴露问题，当前只保留 `nx_open_tcpart` 作为 NX 图纸入口。
2. `RT-003` 已将 `test_agent_turn` 移至本地客户端，K8s 不再提供 `/api/mc-design/test/agent-turn`。
3. `K8S-SMOKE-001` 已通过，K8s readiness、connector catalog、`mysql_query select 1` 均正常。
4. 静态工具组当前只有 `tool.nx`、`tool.local_file`、`tool.dfmea`，业务 connector 通过 K8s catalog 动态同步，方向符合 tjuae 使用规则。

## 后续建议

优先级建议：

1. `BIZ-ADAPTER-001` 和 `NX-TOOL-HARDEN-001` 已完成并阶段验收，不再重复派发。
2. 后续重点转为真实通路整改：launcher 正式入口启动、agent-turn 工具面同步 connector、参数四分支业务断言、NX 截图和 TC/NX 生命周期。
3. `SK-003`、`ASSET-GOV-001`、`RT-NAME-001`、`REPORT-TEMPLATE-001` 继续保留为后续候选，必须重新编号和指定回执目录后再派发。
