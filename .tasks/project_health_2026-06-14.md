# Project Health Check - 2026-06-14

## 结论

当前项目已从“多任务并行整改”进入“安装包级通路验证 + 业务回归准备”阶段。`S0-2`、`S0-3`、`TJ-001`、`NX-005`、`SK-001R`、`S0-4`、`S0-6`、`NX-DRAW-001`、`K8S-SMOKE-001`、`PKG-001`、`PKG-002`、`CLIENT-LEGACY-001`、`CLIENT-ACTIVE-ROOT-001`、`BIZ-ADAPTER-001`、`NX-TOOL-HARDEN-001` 已通过阶段验收；`REG-EVIDENCE-001`、`SKILL-CONSIST-001`、`K8S-CONNECTOR-PRE-001`、`NX-PRECHECK-001`、`CLIENT-ARCH-001`、`CLIENT-ASSET-001` 已完成预回归准备/静态审计/只读预检查；`E2E-SMOKE-003` 已完成但严格不通过，失败点从旧卸载链路转移到正式启动入口 `McDesignClient.exe`；`REG-P0-FULL-001` 已完成正式 P0 试跑但不通过，35 条覆盖中 11 通过、17 失败、7 阻塞；`RT-001`、`RT-002`、`RT-003` 只能判定为运行时替换阶段通过，不能判定为全通路终验；`SK-002-REVIEW` 有条件通过。

当前最大风险有六类：一是真实全通路尚未跑通；二是 `E2E-SMOKE-003` 证明正式 launcher 入口仍不能稳定拉起本地端口；三是重装后 Teamcenter `tc_key_configured=false`，需要在后续 TC/NX 测试前处理配置；四是本地 agent-turn 工具面未暴露 IPM 查询能力，K8s connector 可用但 agent 任务选择链路不闭环；五是参数四分支业务断言失败，仍未按参考逻辑稳定输出；六是 QPP 外部接口不通、NX 截图失败、NX/TC 生命周期前置不足等阻塞仍存在。NX 图纸能力口径已由 `NX-DRAW-001` 和 `NX-TOOL-HARDEN-001` 继续收口：NX plugin 中自动出图插件禁用；NX 图纸操作只允许通过 `nx_open_tcpart` 打开 NX 图纸，图纸与数模绑定后的自动更新即视为自动出图。

## 当前派发状态

截至本次整理：`BIZ-ADAPTER-001`、`NX-TOOL-HARDEN-001`、`E2E-SMOKE-003`、`REG-P0-FULL-001` 已收到回执并完成检查。当前无正在执行任务、无已派发待回执任务；后续如需继续，必须重新编号、指定回执目录并避免顺序阻塞任务并发。

`E2E-SMOKE-003` 当前结论：使用 `PKG-002` 安装包复测时，卸载旧客户端和新安装均通过；诊断入口 `start-client.bat` 可启动同一 Python runtime，local health/status、本地 `POST /api/runtime/test/agent-turn` 和 K8s readiness/catalog/mysql/IPM/ECR smoke 均有通过证据。但正式入口 `McDesignClient.exe` 超时内未拉起 8765 端口，严格判定为 `CLIENT_START_FAILED`。重装后安装目录配置显示 `tc_key_configured=false`，后续 TC/NX 测试前需处理本机配置。

## 后续测试派发公共规则

已新增公共规则文件：`.tasks/TEST_EXECUTION_RULES.md`。后续派发测试、预回归、E2E smoke、K8s connector 检查、NX 前置检查、问题表回归、Skill/Tool/Asset 审计任务时，必须把该文件作为参考资料提供给执行智能体。

## 客户端通路测试门禁

后续只要进入通路测试，且本轮包含 `mc-design-client` 更新，就必须把客户端打包、卸载、重装、启动作为测试前置和验收内容，而不是只跑源码或本地单元测试。

强制口径：

1. 客户端更新后，必须重新打包 Windows 客户端或安装包。
2. 测试前必须卸载旧客户端，再安装新客户端，验证卸载和重装流程可用。
3. 通路测试前必须检查客户端是否正在运行；未运行则启动客户端。
4. 回执必须记录客户端启动方式、进程/端口/健康检查结果、版本或构建产物路径、日志位置。
5. 如果打包、卸载、重装或启动失败，应先判定为客户端交付链路阻塞，不能跳过后直接测 K8s、NX 或业务工具。
6. 这条规则同时用于验证“客户端打包、卸载重装、运行”能力本身是否正常。

## 通路测试身份

后续测试默认使用项目负责人指定的测试身份：

1. `user_id = "88000044"`
2. `user_name = "宋明芮"`
3. Teamcenter 密码只允许写入本机用户配置 `configure\mc-design-client.config` 的 `tc_key`，不得写入项目仓库、任务提示词正文或回执明文。
4. 回执中如需证明密码已配置，只能写 `tc_key_configured=true` 或脱敏值，不得输出原文。
5. 当前本机安装目录 `C:\Users\ASUS\AppData\Local\McDesign\configure\mc-design-client.config` 已按该测试身份更新并重启客户端，`/health` 显示 bridge connected。

### E2E-SMOKE-001 失败记录

`E2E-SMOKE-001` 已执行失败，阻塞分类为“客户端卸载/重装链路阻塞”。构建成功，安装包 `McDesignClientSetup-E2E-SMOKE-001.zip` 生成成功；失败点在旧客户端卸载。当前旧安装目录 `C:\Users\ASUS\AppData\Local\McDesign` 是历史/残缺布局：存在 `client\python\python.exe` 和旧 `install_helper.py`，但缺少新卸载脚本要求的 `installer\tools\install_helper.mcpy`，也缺少 `McDesignClient.exe` 和 `client\app\mc_design_client.pyz`。因此新包 `uninstall.bat` 无法卸载旧布局，通路测试未进入新安装、客户端启动、K8s smoke 和本地 agent-turn smoke。

加固方向：新安装包必须能识别并处理旧版/残缺安装目录；安装/卸载脚本不能只支持最新布局。后续应先派发客户端打包、安装、卸载加固任务，再重跑通路 smoke。

### E2E-SMOKE-001 人工恢复后继续验证

项目负责人要求不等待 `PKG-001` 完成，先人工推进通路。执行结果：使用旧安装目录自带旧版 `uninstall.bat` 成功卸载历史/残缺安装目录；随后使用 `E2E-SMOKE-001` 安装包重新安装成功，关键文件均存在。安装后首次启动失败，原因是默认 `configure\mc-design-client.config` 中 `user_id = "local"` 被启动校验视为无效占位值；临时将安装目录配置改为 `user_id = "e2e_smoke_001"`、`user_name = "E2E Smoke"` 后客户端启动成功。

恢复后验证结果：`GET http://127.0.0.1:8765/health` 与 `/api/status` 成功；AI bridge connected；assets bundle version 为 `E2E-SMOKE-001`；工具数 29；NX plugin 未连接，按当前环境视为人工前置项。K8s readiness、connector catalog、`mysql_query select 1` 均通过；K8s 旧 `/api/mc-design/test/agent-turn` 返回 404，符合新规则。本地 `POST http://127.0.0.1:8765/api/runtime/test/agent-turn` 成功，返回 `status=success`，产生 447 个 frames、4 个 events，并完成本地链路检查工具调用，未调用 NX 修改类工具。

新增问题：安装包默认用户配置 `user_id = "local"` 会导致正式启动失败，但 `login/doctor` 不会提前暴露该阻塞。该问题应并入 `PKG-001` 或后续客户端安装配置加固：安装后必须提示/要求设置真实 user_id，或让安装/启动前诊断明确报告“占位用户 ID 无效”。

### 当前体检记录

本轮最新体检结果：`BIZ-ADAPTER-001` 与 `NX-TOOL-HARDEN-001` 已回执并复跑相关测试，`mc-design-nx` 目标测试 83 passed，NX/本地 API 相关 Python 静态编译检查通过。`E2E-SMOKE-003` 使用 `PKG-002` 安装包完成卸载、安装和诊断入口 smoke，但正式 `McDesignClient.exe` 启动失败，严格判定为 `CLIENT_START_FAILED`。

本地 `POST /api/runtime/test/agent-turn` 在 `E2E-SMOKE-003` 诊断入口启动后可返回 `status=success`，并调用 `local_file_exists` 完成轻量工具回调；K8s readiness、connector catalog、`mysql_query select 1`、IPM/ECR 基础只读检查通过。`REG-P0-FULL-001` 已补正式回执，但结论为不通过：35 条覆盖，11 通过、17 失败、7 阻塞；核心失败包括本地 agent-turn 找不到 IPM 查询工具、四类参数分支业务断言失败、截图失败、TC/NX 生命周期因 `tc_key_configured=false` 与未完成三维修改被阻塞。

## 本轮回执复验

| 任务 | 复验结论 | 证据 |
|---|---|---|
| SK-001R | 通过 | 审计回执覆盖 11 个文件/资料源、56 个硬编码点、P0/P1/P2 分级、保留/迁出/fixture 建议和连杆试点建议。 |
| S0-4 | 通过 | `mc-design-nx`: `python -m pytest client/tests/test_design_skill_contract.py -q`，结果 18 passed。 |
| S0-6 | 通过 | 生成 `ACCEPTANCE_MATRIX.csv` 和 `ACCEPTANCE_MATRIX.md`；纳入 59 条问题记录、35 条 P0、13 条 P1、11 条 P2。 |
| RT-002 | 阶段通过，未全通路终验 | `mc-design-ai-service`: `python -m pytest -q`，结果 72 passed, 3 warnings；`mc-design-nx`: `build_installer.py --dry-run --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk`，结果 ok=true。 |
| RT-003 | 阶段通过，K8s smoke 已通过 | 已复验回执；本地 `POST /api/runtime/test/agent-turn` 由 `mc-design-client` 提供，K8s `/api/mc-design/test/agent-turn` 已移除；复跑 `mc-design-nx` 相关测试 49 passed，`mc-design-ai-service` 相关测试 56 passed, 1 warning。 |
| NX-DRAW-001 | 通过 | 禁用并移除 `nx-auto-drawing` 运行资产和 manifest 暴露；图纸入口只保留 `nx_open_tcpart`；相关客户端测试 43 passed，资产循环测试 2 passed。 |
| SK-002-REVIEW | 有条件通过 | 规则包方案可作为连杆试点前置；不允许直接批量迁移活塞销/止推片，不允许改运行时/NX/K8s；已记录 schema 缺口。 |
| REG-001-PREP | 通过，准备完成 | 形成 59 条问题的分批回归准备、P0 checklist 和证据模板；不代表真实全通路已经测试通过。 |
| K8S-SMOKE-001 | 通过 | `/api/readiness`、connector catalog、`mysql_query select 1` 均通过；K8s 旧 `/api/mc-design/test/agent-turn` 返回 404，符合 RT-003 新规则。 |
| PKG-001 | 通过 | Windows 客户端安装包安装、卸载、升级前清理、旧/残缺布局识别、NX `custom_dirs.dat` 清理、进程处理和 zip 自检已加固；`test_windows_installer_build.py` 21 passed；产物为 `McDesignClientSetup-PKG-001.zip`。 |
| PKG-002 | 通过，允许进入 E2E 复测 | 针对 `E2E-SMOKE-002` 的 `package-helper-fallback` 误判继续加固；新增 `package-helper-fallback-layout` 分类、拒绝日志和进程清理收口；复跑 `test_windows_installer_build.py` 25 passed，`build_installer.py` 语法检查通过；产物为 `McDesignClientSetup-PKG-002.zip`。 |
| E2E-SMOKE-001 | 正式回执为环境阻塞；后续人工恢复仅作继续验证 | 原回执失败点是旧客户端卸载/重装链路阻塞；后续人工使用旧卸载脚本清理并安装 `E2E-SMOKE-001` 后，本地 health、K8s smoke 和本地 agent-turn 健康检查通过，但不改写原任务结论。 |
| E2E-SMOKE-002 | 不通过 | 使用 `PKG-001` 安装包复测时，卸载旧客户端失败；`package-helper-fallback` 将当前安装目录判为 `foreign-dir` 并拒绝清理，退出码 9；未进入安装、启动、K8s smoke 和本地 agent-turn。 |
| E2E-SMOKE-003 | 不通过，失败点转为正式启动入口 | 使用 `PKG-002` 安装包复测时，卸载、安装、诊断入口启动、本地 health/status、本地 agent-turn、K8s readiness/catalog/mysql/IPM/ECR 均有通过证据；但 `McDesignClient.exe` 未在超时内拉起 8765，严格判定 `CLIENT_START_FAILED`。 |
| BIZ-ADAPTER-001 | 通过，业务适配层阶段完成 | 新增 `tool.design_flow`，覆盖任务候选归一、任务选择保持、参数分类、四类参数分支和 NX 写入前计划；复跑 `mc-design-nx` 相关测试 83 passed。未修改 AI Service，不需要 K8s 更新。 |
| NX-TOOL-HARDEN-001 | 通过，静态/单测阶段完成 | NX plugin 和本地 API 补齐自动出图禁用、manifest 过滤、坏 JSON/大 body/并发/错误码边界；复跑 Python 静态编译检查通过，相关测试已包含在 83 passed。未执行 NX 实机编译/会话测试。 |
| REG-P0-FULL-001 | 不通过，正式 P0 试跑完成 | 覆盖 35 行问题表记录；11 通过、17 失败、7 阻塞。本地 agent-turn 未暴露 IPM 查询工具；参数四分支均为业务断言失败；报告/DFMEA 部分通过；截图失败；TC/NX 生命周期因前置不足阻塞。 |
| REG-EVIDENCE-001 | 通过，证据准备完成 | 35 条 P0 均形成回归证据卡片；输出 `REGRESSION_EVIDENCE_CARDS.md` 和 `.csv`；不代表真实业务回归通过。 |
| SKILL-CONSIST-001 | 通过，发现新增治理问题 | 静态审计未发现禁用自动出图工具误暴露；发现 1 个 P0、4 个 P1、2 个 P2，最高风险仍是零件规则硬编码。 |
| K8S-CONNECTOR-PRE-001 | 完成，存在外部接口阻塞 | readiness、catalog、mysql smoke、IPM/ECR 预检查通过；`connect_qpp` 上游超时；项目负责人确认 QPP 当前确实不通，归类为外部接口不可用。 |
| NX-PRECHECK-001 | 完成，存在环境前置阻塞 | 客户端未运行、NX 已启动但 NX plugin 8088 未监听；禁用工具未暴露，`nx_open_tcpart` 在 manifest 中存在。 |
| CLIENT-ARCH-001 | 通过，架构边界审计完成 | 已厘清 `assets/source`、`agent_assets.mcdpkg`、`asset_views/runtime-agentloop`、`workspace/.tjuae/skills` 的生成/运行边界；`tjuae-sdk` 不直接读取 `.mcdpkg` 或 `asset_views`；`cc_haha_agent_runtime_migration_pack` 判定为迁移参考残留。 |
| CLIENT-ASSET-001 | 通过，资产链路自检和文档固化完成 | 新增 `inspect_asset_chain(...)` 和 `doctor.checks.asset_chain`；确认当前链路 `assets/source -> agent_assets.mcdpkg -> asset_views/runtime-agentloop -> workspace/.tjuae/skills` 一致；legacy 候选只报告不删除；复跑测试 29 passed。 |
| CLIENT-LEGACY-001 | 通过，legacy 归档清理完成 | 旧 `runtime-live`、`test-local-dev`、`.beya`、`governance` 已归档到 `.tasks/archives/CLIENT-LEGACY-001/` 后从活跃目录移除；`cc_haha` 已迁移到 `references/legacy-runtime/cc-haha/`；复跑测试 30 passed，实时 doctor `asset_chain.ok=true`。 |
| CLIENT-ACTIVE-ROOT-001 | 有条件通过，根安装 payload 收口完成 | 根 `client/` 安装 payload 已归档到 `.tasks/archives/CLIENT-ACTIVE-ROOT-001/client/`；根 `client/` 仅剩 `client/configure/mc-design-client.config`，因 `tc_key_configured=true` 不复制、不删除；新增 `tool_execution_map.json` 和工具映射测试；复跑 48 passed。保留项：`.install-backup`、`.tmp-runtime-check` 删除记录不在回执范围内，提交前需单独确认。 |
| ASSET-001R | 历史问题已由 NX-DRAW-001 覆盖关闭 | 原回执暴露的 `nx-auto-drawing` 旧口径已在 `NX-DRAW-001` 中清理；保留 `runtime.md` 优先和 `beya.md` fallback 的归属记录。 |
| S0-5 | 阶段通过，待全通路回归 | 报告预览、保存、本地下载、旧说明书来源和截图证据链已实现；旧自动出图口径已并入 `NX-DRAW-001` 清理。 |
| DFMEA-001 | 工具侧通过，待全通路回归 | `tool.dfmea` 注册、模板 inspect/fill/validate、AP/RPN 测试通过；旧图纸引用已随 `NX-DRAW-001` 收口，真实 TC/NX 上传仍待联调。 |

补充事实：全通路测试包含人工环境前置条件。`mc-design-ai-service` 更新后需要项目负责人手动更新 K8s；本地不能直接访问和调用 MCP Stream Tool；`test_agent_turn` 已落在本地 `mc-design-client` 的 `POST /api/runtime/test/agent-turn`；K8s 网络/VPN、NX 启动、TC/NX 模型打开都可能需要项目负责人手动处理。

## 新监管规则

### 1. 每个派发任务必须指定回执路径

以后任务提示词必须包含固定回执目录：

```text
回执目录：
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\<TASK_ID>\
```

执行类任务必须输出：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\<TASK_ID>\EXECUTION_RECEIPT.md
```

审计/检查类任务必须输出：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\<TASK_ID>\AUDIT_RECEIPT.md
```

如果任务产出方案、schema、测试日志或中间数据，必须放在同一目录下，或在回执中写清绝对路径。

### 2. 顺序阻塞任务只派当前一个

以后如果任务存在依赖关系，只派发当前可执行任务。后续任务最多写入监管计划，不作为可执行提示词发出。

禁止一次性同时派发类似：

- `SK-001 审计` 和依赖其结果的 `SK-002 schema 方案`
- `SK-002 方案` 和依赖其通过的 `SK-003 迁移`
- `ASSET-001 修复打包` 和依赖其通过的 `NX-005 补验`

## 任务状态台账

| 任务 | 当前状态 | 验收/检查结果 | 已知产物 | 下一步 |
|---|---|---|---|---|
| S0-2 参数转换与 skill 加固 | 通过 | 原验收通过；后续受全通路和零件规则包迁移验证约束 | `parameter_schema.json`、`input_branch_state_machine.json`、`minimal_test_cases.json` | 冻结后续动作，待新方案重新派发 |
| S0-3 外部任务工具契约稳定化 | 通过 | 当前体检 `tests/test_usage_issue_fixes.py` 为 7 passed | `external.py`、`TOOL.md`、`test_usage_issue_fixes.py` | 冻结后续动作，待新方案重新派发 |
| TJ-001 tjuae 通用能力整改 | 通过 | 已验收 `check:sdk`、WebSocket 事件测试、delivery build | `F:\Documents\tjuae\dist\tjuae-sdk` | 保留为外部能力基础，不再派后续任务 |
| NX-005 本地文件工具迁移 | 通过 | 当前体检 `client/tests/test_tool_registry.py` 为 12 passed | `local_file_provider.py`、`tool.local_file/TOOL.md`、NX manifest 过滤 | 冻结后续动作，待新方案重新派发 |
| ASSET-001R runtime.md 资产打包归属补审 | 已由 NX-DRAW-001 覆盖关闭 | 回执归属清楚；`runtime.md` 优先和 `beya.md` fallback 可接受；旧图纸口径已由 `NX-DRAW-001` 清理 | `AUDIT_RECEIPT.md`、`export_assets.py`、`test_asset_store.py` | 不再单独派发 |
| SK-001R 零部件 Skill 硬编码审计补交 | 通过 | 审计台账覆盖 56 个硬编码点、P0/P1/P2 分级、保留/迁出/fixture 建议 | `AUDIT_RECEIPT.md` | 冻结后续动作，待新方案重新评审 |
| SK-002 规则包 schema 与加载方案 | 有条件通过 | `SK-002-REVIEW` 判定连杆规则包试点具备条件；仍存在 NX mapping、公式证据、fixture schema、默认值/样例边界等缺口 | `.tasks/SK-002_part_rules_schema_design.md`、`.tasks/receipts/SK-002-REVIEW/AUDIT_RECEIPT.md` | 原 `SK-003` 候选撤回，待新方案重新编号 |
| RT-001 mc-design 一次性替换 | 阶段通过，未终验 | `mc-design-nx` 活动源码已无有效 beya 运行时命中；tjuae adapter/server/打包测试通过；但无旧规则回执，且未跑全通路 | `tjuae_runtime_adapter.py`、`tjuae_server.py`、`runtime.md`、`tjuae-client-core.zh.md`、Windows payload 改动 | 冻结全通路动作，待新方案重新派发 |
| RT-002 运行时替换收口 | 阶段通过，未终验 | AI Service 全量 72 passed；真实 tjuae dist dry-run ok=true；兼容保留 `beya_mcp`/`beya.toml`/`BEYA_*` | `EXECUTION_RECEIPT.md`、`test_runtime_replacement_policy.py`、README/打包脚本更新 | 已由 RT-003 修正 test_agent_turn 入口方向 |
| RT-003 本地 test_agent_turn 与 K8s connector/MySQL 修整 | 阶段通过，K8s smoke 已通过 | `mc-design-nx`: 49 passed；`mc-design-ai-service`: 56 passed, 1 warning。K8s 侧 test_agent_turn 已移除，本地 client 提供 `/api/runtime/test/agent-turn`；MySQL 缺配置、依赖缺失、连接失败、SQL 失败已拆分错误码 | `.tasks/receipts/RT-003/EXECUTION_RECEIPT.md`、`server.py`、`app.py`、`runtime_bridge.py`、`integrations/mysql/client.py`、`test_mysql_connector_errors.py` | 独立本地 `agent-turn` smoke 候选撤回；`E2E-SMOKE-002` 内仍需验证本地入口 |
| K8S-SMOKE-001 K8s 部署后 smoke test | 通过 | readiness、connector catalog、`mysql_query select 1` 均通过；旧 K8s test-agent-turn 返回 404 为正确结果 | `.tasks/receipts/K8S-SMOKE-001/EXECUTION_RECEIPT.md` | 不阻塞下一步测试 |
| PKG-001 客户端安装包加固 | 阶段通过，但真实 E2E 复测未通过 | 安装/卸载/升级前清理、旧/残缺布局识别、foreign-dir 拒绝、NX `custom_dirs.dat` 清理、进程处理、zip self-check 已加固；测试 21 passed | `.tasks/receipts/PKG-001/EXECUTION_RECEIPT.md`、`McDesignClientSetup-PKG-001.zip` | `E2E-SMOKE-002` 证明卸载链路仍需继续加固 |
| PKG-002 客户端卸载/安装链路继续加固 | 通过，已完成 E2E 复测 | 覆盖 `client/ + configure/mc-design-client.config + 带 McDesign 标记 uninstall.bat` 的 `package-helper-fallback-layout`，不再误判为 `foreign-dir`；`E2E-SMOKE-003` 已证明卸载/安装通过 | `.tasks/receipts/PKG-002/EXECUTION_RECEIPT.md`、`McDesignClientSetup-PKG-002.zip`、`package-helper-selfcheck-final.log` | 后续阻塞转为 `McDesignClient.exe` 正式启动失败 |
| E2E-SMOKE-001 安装包级 smoke | 环境阻塞；人工恢复后基础链路可跑 | 正式回执失败于旧客户端卸载/重装；人工恢复后本地 health、K8s smoke、本地 agent-turn 健康检查通过 | `.tasks/receipts/E2E-SMOKE-001/EXECUTION_RECEIPT.md`、监管人工恢复记录 | 不改判原任务；失败原因已由 `PKG-001` 加固处理，待 `E2E-SMOKE-002` 复测 |
| E2E-SMOKE-002 安装包级 smoke 复测 | 不通过 | 使用 `PKG-001` 安装包复测时，卸载旧客户端失败；`package-helper-fallback` 将当前安装目录判为 `foreign-dir` 并拒绝清理，退出码 9；未进入安装/启动/K8s/agent-turn | `.tasks/receipts/E2E-SMOKE-002/EXECUTION_RECEIPT.md`、`uninstall-output.log` | 需要继续加固安装目录识别和卸载策略 |
| E2E-SMOKE-003 安装包级 smoke 复测 | 不通过 | `PKG-002` 卸载/安装通过；`start-client.bat` 诊断入口可启动并完成本地/K8s smoke；正式入口 `McDesignClient.exe` 未拉起 8765 | `.tasks/receipts/E2E-SMOKE-003/EXECUTION_RECEIPT.md`、`client-start-result.json`、`local-health-status.json`、`local-agent-turn-response-retry.json`、`k8s-smoke-result.json` | 下一步应单独排查 launcher 启动、等待、错误提示和日志落盘；同时处理重装后 `tc_key_configured=false` |
| BIZ-ADAPTER-001 业务适配工具层 | 通过 | `tool.design_flow` 已接入本地 Python 工具、Tjuae inline plugin、静态工具资产和相关 skill；复跑 83 passed | `.tasks/receipts/BIZ-ADAPTER-001/EXECUTION_RECEIPT.md`、`design_flow_provider.py`、`tool.design_flow/TOOL.md`、`tool_execution_map.json` | 后续业务回归应优先验证 agent 是否实际调用这些工具，而不是只看工具存在 |
| NX-TOOL-HARDEN-001 NX/工具 API 加固 | 通过，待实机补验 | 自动出图工具禁用口径继续加固；NX plugin、本地 API、manifest、工具注册和说明均补齐协议边界；静态编译检查通过 | `.tasks/receipts/NX-TOOL-HARDEN-001/EXECUTION_RECEIPT.md`、`HttpServer.cs`、`ToolManager.cs`、`server.py`、`generate_nx_manifest.py` | 后续有 NX 环境时补跑真实 NX plugin 编译/会话 smoke |
| REG-P0-FULL-001 P0 证据试跑 | 不通过 | 35 条覆盖中 11 通过、17 失败、7 阻塞；本地 agent-turn IPM 工具面缺失、参数四分支业务断言失败、截图失败、TC/NX 生命周期阻塞 | `.tasks/receipts/REG-P0-FULL-001/EXECUTION_RECEIPT.md`、`P0_REGRESSION_MATRIX.csv`、`matrix_status_summary.json` | 针对本地 agent-turn 工具同步和参数四分支业务断言失败重新派发整改；报告/DFMEA 已通过部分保留证据 |
| REG-EVIDENCE-001 问题表回归证据整理 | 通过，准备完成 | 59 条矩阵记录中 35 条 P0 均形成证据卡片；未执行真实业务回归 | `.tasks/receipts/REG-EVIDENCE-001/EXECUTION_RECEIPT.md`、`REGRESSION_EVIDENCE_CARDS.md`、`REGRESSION_EVIDENCE_CARDS.csv` | 后续正式回归必须引用这些卡片 |
| SKILL-CONSIST-001 Skill/Tool/Asset 一致性审计 | 通过，发现治理问题 | 无 P0 运行资产缺失；无自动出图禁用工具误暴露；发现 1 个 P0、4 个 P1、2 个 P2 | `.tasks/receipts/SKILL-CONSIST-001/AUDIT_RECEIPT.md`、`ISSUE_LIST.csv` | `SK-003`、`RT-NAME-001`、`REPORT-TEMPLATE-001` 等候选继续冻结，待 E2E 后重排 |
| K8S-CONNECTOR-PRE-001 K8s connector 预回归 | 完成，存在外部接口阻塞 | readiness/catalog/mysql/IPM/ECR 基础项通过；QPP 上游超时；项目负责人确认 QPP 当前确实不通 | `.tasks/receipts/K8S-CONNECTOR-PRE-001/EXECUTION_RECEIPT.md`、`CONNECTOR_PRECHECK_RESULTS.json` | QPP 归类为外部接口不可用，不判定 mc-design 代码失败 |
| NX-PRECHECK-001 NX 前置预检查 | 完成，存在环境前置阻塞 | 客户端未运行；NX 已启动但 NX plugin 8088 未监听；禁用工具未暴露；`nx_open_tcpart` manifest 存在 | `.tasks/receipts/NX-PRECHECK-001/EXECUTION_RECEIPT.md`、`NX_PRECHECK_RESULTS.json` | 后续需人工启动/释放客户端并加载 NX plugin 后再测实机 |
| CLIENT-ARCH-001 mc-design-client 架构边界审计 | 通过 | 明确资产链路为 `assets/source -> agent_assets.mcdpkg -> asset_views/runtime-agentloop -> workspace/.tjuae/skills`；确认 `asset_views` 是投影缓存，不是 tjuae-sdk 直接读取对象；`cc_haha` 为外部运行时迁移参考残留 | `.tasks/receipts/CLIENT-ARCH-001/AUDIT_RECEIPT.md`、`CLIENT_ARCHITECTURE_MAP.md`、`CLIENT_CLEANUP_CANDIDATES.csv`、`CLIENT_RESTRUCTURE_PROPOSAL.md` | 已由 `CLIENT-ASSET-001` 承接完成链路自检 |
| CLIENT-ASSET-001 客户端资产链路自检与文档固化 | 通过 | 新增只读资产链路诊断；`doctor` 输出 `asset_chain.ok=true`；source/package/projection/workspace managed skills 全一致；legacy 候选均为 `report_only` | `.tasks/receipts/CLIENT-ASSET-001/EXECUTION_RECEIPT.md`、`diagnostics.py`、`README_TJUAE_RUNTIME.md`、相关测试 | 可以派发 `CLIENT-LEGACY-001` 做归档式清理，不直接硬删 |
| CLIENT-LEGACY-001 客户端 legacy 归档清理 | 通过 | 活跃 client 目录中的 `runtime-live`、`test-local-dev`、`.beya`、`governance` 已归档后移除；`cc_haha_agent_runtime_migration_pack` 已移动到 `references/legacy-runtime/cc-haha/`；legacy candidate action 变为 `absent` | `.tasks/receipts/CLIENT-LEGACY-001/EXECUTION_RECEIPT.md`、`LEGACY_MANIFEST_BEFORE.json`、`LEGACY_MANIFEST_AFTER.json`、`DOCTOR_RESULT.json`、`.tasks/archives/CLIENT-LEGACY-001/` | 暂不继续派发目录治理任务，先等 `E2E-SMOKE-003` 回执 |
| CLIENT-ACTIVE-ROOT-001 根安装 payload 收口与工具执行映射 | 有条件通过 | 根 `client/` 537 个文件中 536 个非敏感 payload 文件已归档并从活跃根目录移除；只剩 `client/configure/mc-design-client.config` 需项目负责人确认处理；`tool.local_file`、`tool.dfmea`、`tool.nx` 的 TOOL.md -> provider -> registry -> HTTP executor -> tjuae namespace 映射已机器化 | `.tasks/receipts/CLIENT-ACTIVE-ROOT-001/EXECUTION_RECEIPT.md`、`ROOT_CLIENT_MANIFEST_BEFORE.json`、`ROOT_CLIENT_MANIFEST_AFTER.json`、`.tasks/archives/CLIENT-ACTIVE-ROOT-001/client/`、`mc-design-nx/client/resources/tool_execution_map.json` | `AUDIT-ST-010/011` 关闭；提交前单独确认 `.install-backup` 和 `.tmp-runtime-check` 删除记录 |
| NX-DRAW-001 NX 图纸规则收口 | 通过 | `nx-auto-drawing` 已禁用/移出运行资产；只保留 `nx_open_tcpart` 图纸打开口径；相关测试通过 | `.tasks/receipts/NX-DRAW-001/EXECUTION_RECEIPT.md` | 冻结后续动作，待新方案重新派发 |
| REG-001-PREP 问题表全量回归准备 | 通过，准备完成 | 59 条问题已分批并形成 P0 checklist、证据模板和阻塞分类；未执行真实全通路 | `.tasks/receipts/REG-001-PREP/AUDIT_RECEIPT.md` | 原 `REG-001` 执行候选撤回，待新方案重新编号 |
| S0-4 TC/NX 模型生命周期规则加固 | 通过 | skill 契约测试 18 passed；真实 NX/TC 副作用动作未执行 | `EXECUTION_RECEIPT.md`、skill/TOOL/test 更新 | 冻结后续动作，待新方案重新派发 |
| S0-6 问题表验收矩阵 | 通过 | 生成验收矩阵；原 Excel 未修改 | `ACCEPTANCE_MATRIX.csv`、`ACCEPTANCE_MATRIX.md`、`EXECUTION_RECEIPT.md` | 用作后续验收主台账 |
| S0-5 设计报告/截图/说明书链路加固 | 阶段通过，待全通路 | 报告流程实现和自测通过；旧自动出图口径已由 `NX-DRAW-001` 清理 | `EXECUTION_RECEIPT.md`、design-report 相关改动 | 原回归候选撤回，待新方案重新编号 |
| DFMEA-001 DFMEA/FMEA 模板工具与 Skill 补全 | 工具侧通过，待全通路 | `tool.dfmea` 本地工具组已注册；DFMEA 测试 21 passed，客户端相关测试 46 passed；原始模板未修改 | `dfmea_provider.py`、`tool.dfmea/TOOL.md`、DFMEA 模板副本、`EXECUTION_RECEIPT.md` | 原回归候选撤回，待新方案重新编号 |
| NX-001 至 NX-004 | 未收到完成报告 | 未验收 | 无 | 暂不判定 |

## 全通路测试人工前置条件

以下条件必须写入后续全通路测试任务提示词和回执模板：

1. `mc-design-ai-service` 有更新时，测试前需要项目负责人手动更新 K8s。否则测试可能命中旧版本服务，不能直接判定代码失败。RT-002 和 RT-003 均已更新 AI Service，进入下一轮真实 connector smoke test 前必须执行此人工步骤。
2. MCP Stream Tool 不能在本地直接访问和调用，因此不作为本地全通路测试入口。
3. `test_agent_turn` 已按 RT-003 调整到本地 `mc-design-client`，入口为 `POST /api/runtime/test/agent-turn`；K8s 不再提供 `/api/mc-design/test/agent-turn`，该接口返回 404 是正确结果。
4. 如果本轮包含 `mc-design-client` 更新，必须先完成客户端打包、卸载旧版本、安装新版本、启动客户端并检查运行状态；未运行则启动。
5. K8s 连接失败时，如果判断是网络未启动，需要项目负责人手动开启 VPN。
6. NX 未启动时，需要项目负责人手动开启 NX。
7. 当前测试环境下 `nx_open_tcpart` 因网络原因不可用，需要项目负责人手动打开目标模型，再继续后续链路测试。

回执中必须区分失败原因：代码缺陷、客户端打包失败、客户端卸载/重装失败、客户端未启动或健康检查失败、K8s 未更新、VPN 未开启、NX 未启动、TC/NX 模型需手动打开、外部接口不可用。

## 当前体检命令

本段只保留当前仍有效的体检证据。旧记录中 `client\tests\test_design_skill_contract.py client\tests\test_asset_store.py client\tests\test_windows_payload_builder.py` 的 `28 passed, 2 failed` 是 `NX-DRAW-001` 前的历史失败，失败原因是旧规则仍要求 `nx-auto-drawing` 存在；该口径已被 `NX-DRAW-001` 覆盖关闭，不能再作为当前阻塞。

当前有效证据：

| 范围 | 命令/来源 | 结果 | 当前解释 |
|---|---|---|---|
| `mc-design-ai-service` 全量阶段测试 | `python -m pytest -q` | 72 passed, 3 warnings | `RT-002` 阶段证据；不代表全通路终验。 |
| `RT-003` 本地 agent-turn/K8s connector/MySQL 修整 | 回执复验 | `mc-design-nx` 49 passed；`mc-design-ai-service` 56 passed, 1 warning | K8s 旧 test-agent-turn 返回 404 是正确行为。 |
| `NX-DRAW-001` 图纸规则收口 | 回执复验 | 43 passed + 2 passed | 自动出图插件已禁用，运行资产不应再包含 `nx-auto-drawing`。 |
| `K8S-SMOKE-001` K8s smoke | 回执复验 | readiness、connector catalog、`mysql_query select 1` 均通过 | K8s 基础 connector 可用。 |
| `PKG-001` 客户端安装包加固 | 回执复验 | `test_windows_installer_build.py` 21 passed；zip self-check 通过 | E2E 复测仍失败，需继续加固卸载链路。 |
| `PKG-002` 客户端卸载/安装链路继续加固 | 回执复验并本地复跑 | `test_windows_installer_build.py` 25 passed；`build_installer.py` 语法检查通过；fallback 自检退出码 0；`E2E-SMOKE-003` 卸载/安装通过 | 安装包清理链路阶段通过；真实通路阻塞转为正式 launcher 启动失败。 |
| 本机人工恢复后的健康检查 | 监管记录 | local `/health` OK，bridge connected，`tc_key_configured=true`；K8s smoke OK；本地 agent-turn 健康检查成功 | 只证明手工恢复后基础链路可跑，不等同于问题表回归通过。 |
| `REG-EVIDENCE-001` 回归证据整理 | 回执复验 | 35 条 P0 证据卡片，无法整理项 0 | 准备完成，不等同于真实回归通过。 |
| `SKILL-CONSIST-001` 静态审计 | 回执复验 | 1 个 P0、4 个 P1、2 个 P2 | 新问题已纳入治理视野，暂不与 E2E 并发整改。 |
| `K8S-CONNECTOR-PRE-001` K8s connector 预回归 | 回执复验 | readiness/catalog/mysql/IPM/ECR 通过；QPP 超时 | QPP 已确认当前不通，归类为外部接口不可用。 |
| `NX-PRECHECK-001` NX 前置检查 | 回执复验 | 客户端未运行；NX 已启动但 plugin 未监听；禁用工具未暴露 | 环境前置阻塞，不判定代码失败。 |
| `E2E-SMOKE-002` 安装包级 smoke 复测 | 回执复验 | 不通过；卸载旧客户端失败，退出码 9；未进入安装/启动/K8s/agent-turn | 客户端卸载链路阻塞，需继续加固。 |
| `E2E-SMOKE-003` 安装包级 smoke 复测 | 回执复验 | 不通过；卸载/安装通过，诊断入口 smoke 通过，正式 `McDesignClient.exe` 启动失败；`tc_key_configured=false` | 失败点已从卸载链路转为 launcher 正式入口；不能跳过该失败直接做正式全链路验收。 |
| `BIZ-ADAPTER-001` 业务适配工具层 | 回执复验并本地复跑 | 83 passed；`tool.design_flow` 覆盖任务归一、选择保持、参数分类、四分支和建模计划 | 阶段通过；后续需要在真实 agent-turn 回归中验证工具调用路径。 |
| `NX-TOOL-HARDEN-001` NX/本地 API 加固 | 回执复验并本地复跑 | Python 静态编译通过；相关测试纳入 83 passed；未跑 NX 实机编译/会话 | 阶段通过；真实 NX 会话仍需环境具备后补验。 |
| `REG-P0-FULL-001` P0 证据试跑 | 回执复验 | 35 覆盖；11 通过、17 失败、7 阻塞；IPM 任务选择上下文未确认，参数四分支业务断言失败 | 不通过，不计入问题表完成。 |
| `RUNTIME-CONTEXT-001` runtime 上下文/files/connector 可见性 | 回执复验 | `mc-design-nx/client/tests` 197 passed；未改 AI Service | 阶段通过；修复 files 入参丢失和 runtime prompt/connector 目录未进入 SDK input。 |
| `PARAM-RULES-002` 参数四分支规则脚本化 | 回执复验 | skill 脚本测试 5 passed；JSON/py_compile 通过 | 阶段通过；连杆中心距以 Excel/minimal case 的 212mm 为准，REG 中 206.1/210 变体需业务确认。 |
| `NX-PARAM-002` NX 参数工具解析与安全写入 | 回执复验 | manifest tool_count=21；`test_tool_registry.py` 31 passed；资产/Windows payload 14 passed；C# build 成功 | 源码/静态/构建通过；当前运行中 NX plugin 未加载新 DLL，实机新工具验证未完成。 |
| `NX-VISUAL-002` NX 视图/截图工具加固 | 回执复验 | `test_tool_registry.py` + design-report 测试 38 passed；C# build 成功；NX 只读预检通过 | 源码/静态/构建通过；当前运行中 NX plugin 仍是旧程序集，改后截图实机验证未完成。 |
| `CLIENT-LAUNCHER-002` 正式启动/安装卸载/TC key 配置链路加固 | 回执复验 | launcher build 成功；installer build 成功；静态 smoke 通过；安装/卸载隔离 smoke 通过；start smoke 按 `TC_KEY_NOT_CONFIGURED` 停止 | 交付链路加固阶段通过；本机/隔离配置 `tc_key_configured=false` 是 TC/NX 测试前置阻塞，不输出密码明文。 |
| `LOG-001` 会话级日志插队实现 | 本轮自处理 | `mc-design-nx/client/tests` 199 passed | 已在客户端 runtime 旁路写入每 conversation_id 一份 JSONL 日志和 summary；`test_agent_turn` 返回日志路径，API 可查询日志状态。 |
| `CLIENT-ARCH-001` 客户端架构审计 | 回执复验 | asset/source、资产包、asset_views、`.tjuae/skills` 边界已厘清；`cc_haha` 为残留参考包 | 已由 `CLIENT-ASSET-001` 补齐只读链路自检。 |
| `CLIENT-ASSET-001` 客户端资产链路自检 | 回执复验并本地复跑 | 29 passed；`doctor.checks.asset_chain.ok=true`；legacy 候选 `runtime-live/test-local-dev/.beya/cc_haha/governance` 均为 `report_only` | 可进入归档式 legacy 清理，但仍不得硬删未归档内容。 |
| `CLIENT-LEGACY-001` 客户端 legacy 归档清理 | 回执复验并本地复跑 | 30 passed；实时 `doctor.checks.asset_chain.ok=true`；活跃 legacy 路径不存在，归档/参考路径存在 | 通过；后续目录治理任务具备排期条件，但先不与 `E2E-SMOKE-003` 叠加。 |
| `CLIENT-ACTIVE-ROOT-001` 根安装 payload 收口与工具执行映射 | 回执复验并本地复跑 | 48 passed；根 `client/` 仅剩 `client/configure/mc-design-client.config`；归档目录 536 files / 272255160 bytes；`tool_execution_map.json` 存在且 namespace 为 `tool.local_file`、`tool.dfmea`、`tool.nx` | 有条件通过；敏感配置保留需人工确认，`.install-backup`/`.tmp-runtime-check` 删除记录不归入本任务成果。 |

## 工作树健康

### 顶层

顶层显示：

```text
 M mc-design-ai-service
 M mc-design-nx
?? .tasks/
?? references/
```

说明：监管资料和开发资料已纳入，但 `.tasks/`、`references/` 尚未正式归档或提交。`CLIENT-ACTIVE-ROOT-001` 后，顶层 `client/` 大量安装 payload 删除记录是任务范围内结果；但 `.install-backup/` 与 `.tmp-runtime-check/` 也显示删除记录，且不在该任务回执和 manifest 中，提交前必须单独确认其来源和是否保留。

### mc-design-ai-service

当前改动集中在外部工具契约：

```text
tests/test_usage_issue_fixes.py
tools/business/external/TOOL.md
tools/business/external/external.py
```

风险较低，测试通过。

### mc-design-nx

当前改动面很大，至少混有以下任务：

1. `S0-2` 参数 schema / skill 加固。
2. `NX-005` 本地文件工具迁移。
3. `ASSET-001` runtime.md 资产打包修复。
4. `RT-001` beya -> tjuae 运行时替换相关改动。
5. `SK-002` 规则包方案产物。

风险：

1. 多任务改动混在同一工作树，后续验收必须按任务回执拆分归属。
2. `RT-001` 改动很大，包括删除 beya server、删除 beya adapter、增加 tjuae adapter、调整 Windows payload/build 逻辑；当前不能仅凭测试通过判定替换完成。
3. `ASSET-001R` 的旧图纸口径已由 `NX-DRAW-001` 覆盖清理；当前剩余风险转为真实 NX/TC 环境下的链路验证。

## 当前阻塞与决策

1. `E2E-SMOKE-003` 不通过，当前首要阻塞分类为 `CLIENT_START_FAILED`：`McDesignClient.exe` 未在超时内拉起 8765，且没有形成足够 launcher 日志。诊断入口可启动，说明 Python runtime/资产/K8s 基础链路不是本轮主阻塞。
2. `E2E-SMOKE-003` 重装后 `tc_key_configured=false`，后续涉及 TC/NX 的正式测试前必须处理本机安装目录配置；密码不得写入提示词或回执明文。
3. `BIZ-ADAPTER-001` 和 `NX-TOOL-HARDEN-001` 已阶段通过，`AUDIT-ST-012` 至 `AUDIT-ST-016` 可标为阶段关闭；但真实 agent-turn 是否稳定调用 `tool.design_flow`、真实 NX plugin 实机表现仍需回归验证。
4. `REG-P0-FULL-001` 正式回执结论为不通过：35 条覆盖中 11 通过、17 失败、7 阻塞；核心失败是本地 agent-turn 工具面缺失和参数四分支业务断言失败，不计入问题表完成率。
5. 在 launcher 阻塞和测试配置处理前，不把 tjuae 替换记为全通路终验，也不把问题表 P0 真实回归记为完成。
6. `RT-001`/`RT-002`/`RT-003` 均只能记为阶段通过；`K8S-SMOKE-001`、`E2E-SMOKE-003` 的 K8s 部分只证明 readiness、catalog、MySQL、IPM/ECR 基础只读链路可用。
7. `REG-001-PREP` 和 `REG-EVIDENCE-001` 是问题表回归准备，不是回归执行；零件设计智能体试用问题跟踪表中的条目尚未完成全量真实通路测试。
8. QPP 当前已由项目负责人确认不通；`connect_qpp` 相关失败归类为外部接口不可用，不判定 mc-design 代码失败。
9. `NX-PRECHECK-001` 中 NX plugin 8088 未监听，属于环境前置阻塞；后续 NX 实机测试需要人工启动/释放客户端并加载 NX plugin。
10. 根 `client/configure/mc-design-client.config` 因含本机 `tc_key` 仍保留，后续删除或迁移需项目负责人确认；`.install-backup` 与 `.tmp-runtime-check` 删除记录仍需提交前单独确认。
11. NX/TC 真实环境仍是全通路人工前置项：VPN、NX 启动、目标模型手动打开、`nx_open_tcpart` 网络限制都需要在回归任务里显式区分。
12. 已完成任务必须有固定回执目录，否则不进入“完成”状态；当前不做物理删除清理，避免误删其他智能体生成或用户改动。
13. `RUNTIME-CONTEXT-001` 已关闭 files 丢失和工具目录不可见的代码问题，后续必须用真实 `test_agent_turn` 验证 IPM 任务选择闭环。
14. `NX-PARAM-002`、`NX-VISUAL-002` 只缺改后 NX plugin 实机加载验证；当前不是源码测试失败，而是运行中 NX 会话仍加载旧程序集。
15. `CLIENT-LAUNCHER-002` 已把启动失败变成可诊断的前置失败；后续 TC/NX smoke 必须先确保本机安装配置 `tc_key_configured=true`，但不得在日志/回执中输出明文。
16. 会话日志能力已加入客户端：每个 `conversation_id` 对应 `client/logs/conversations/<conversation_id>.jsonl` 和 summary，后续测试问题应带 conversation_id 与日志文件一起回传。

## 运行过程无效内容清理

本次整理只做监管口径清理，不删除源码、回执或参考资料。

1. “无已派发待回执任务/全部冻结”的旧记录已被后续 `E2E-SMOKE-002`、`E2E-SMOKE-003`、`BIZ-ADAPTER-001`、`NX-TOOL-HARDEN-001` 等回执覆盖；现状态为这些任务已验收或失败归类完成，当前无待回执任务。
2. 旧的 `nx-auto-drawing` 测试失败记录已被 `NX-DRAW-001` 覆盖；现规则是自动出图插件禁用，只允许 `nx_open_tcpart` 打开图纸。
3. `E2E-SMOKE-001` 正式结论仍为环境阻塞；后续人工恢复验证只能证明基础链路可继续跑，不能把原任务改判为通过。
4. 本地 `agent-turn` 健康检查中出现 `Bash` 工具调用只证明本地测试入口和工具回调可用，不计入零件设计问题表业务回归通过。
5. `REG-P0-FULL-001` 已补回执，但结论是不通过；不能因为报告/DFMEA 局部通过就把 P0 全量回归算完成。
6. 所有“可派发/候选任务”均不构成执行授权；后续必须重新编号、指定回执目录、避免顺序阻塞任务并发。

## Skill/Tool/Asset 审计问题索引

审计台账：`.tasks/skill_tool_asset_audit_2026-06-14.md`。

本次审计未发现运行资产缺文件、禁用工具误暴露或 K8s connector 不可用的问题；但新增/确认治理问题，编号为 `AUDIT-ST-001` 至 `AUDIT-ST-018`。其中当前优先级最高的是：

1. `AUDIT-ST-001`：零件规则仍硬编码在 skill/runtime 中，原 `SK-003` 候选已撤回，后续等待新方案重新编号。
2. `AUDIT-ST-002` / `AUDIT-ST-003`：Beya 兼容命名和 `BEYA_TC_BASE_URL` 暴露问题，原 `RT-NAME-001` 候选已撤回，后续等待新方案重新编号。
3. `AUDIT-ST-005` / `AUDIT-ST-006`：报告模板硬编码和 capabilities 缺少机器校验，原 `REPORT-TEMPLATE-001` / `ASSET-GOV-001` 候选已撤回，后续等待新方案重新编号。
4. `AUDIT-ST-010`：已由 `CLIENT-ACTIVE-ROOT-001` 有条件关闭；根安装 payload 已归档移除，只剩含本机 `tc_key` 的配置文件需项目负责人确认迁移/删除。
5. `AUDIT-ST-011`：已由 `CLIENT-ACTIVE-ROOT-001` 关闭；`tool_execution_map.json` 已建立 TOOL.md -> provider spec -> registry -> HTTP executor -> tjuae namespace 映射，并通过测试。
6. `AUDIT-ST-012`：已由 `BIZ-ADAPTER-001` 阶段关闭；新增 `tool.design_flow` 业务适配工具层，后续转入真实 agent-turn 回归验证。
7. `AUDIT-ST-013`：已由 `BIZ-ADAPTER-001` 阶段关闭；`tool.local_file`、`tool.dfmea`、`tool.nx`、`tool.design_flow` namespace 映射已测试覆盖。
8. `AUDIT-ST-014`：已由 `BIZ-ADAPTER-001` 阶段关闭；本地侧已有 `task_candidates`、`selected_task_context` 和外部接口不可用分类，QPP 不通仍按外部阻塞处理。
9. `AUDIT-ST-015` / `AUDIT-ST-016`：已由 `NX-TOOL-HARDEN-001` 阶段关闭；后续补真实 NX plugin 编译/会话 smoke。
10. `AUDIT-ST-017`：`REG-P0-FULL-001` 新发现本地 agent-turn 未暴露 IPM 查询/任务选择工具面，K8s connector 直连可用但 agent 任务选择不闭环。
11. `AUDIT-ST-018`：`REG-P0-FULL-001` 新发现参数四分支 transport 成功但业务断言失败，参考逻辑和真实 NX 参数 ID 仍未稳定绑定。
12. `AUDIT-ST-019` / `AUDIT-ST-020`：已由 `RUNTIME-CONTEXT-001` 阶段关闭；files、runtime prompt、工具目录和动态 connector 可见性进入 SDK input。
13. `AUDIT-ST-021`：已由 `NX-VISUAL-002` 源码阶段关闭；等待改后 NX plugin 实机加载验证。
14. `AUDIT-ST-022`：已由 `CLIENT-LAUNCHER-002` 阶段关闭；启动链路现在能明确输出 `TC_KEY_NOT_CONFIGURED`，等待本机配置前置。
15. `AUDIT-ST-023`：已由 `NX-PARAM-002` 源码阶段关闭；等待改后 NX plugin 实机加载验证和真实参数映射确认。
