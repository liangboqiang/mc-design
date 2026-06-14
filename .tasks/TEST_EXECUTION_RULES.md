# MC Design Test Execution Rules

更新时间：2026-06-14

本文件是后续派发测试、预回归、E2E smoke、K8s connector 检查、NX 前置检查任务时必须提供给执行智能体的公共规则。执行智能体不得用自己的理解覆盖本文件中的边界。

## 适用范围

后续任务提示词只要涉及以下任一内容，都必须引用本文件：

1. 客户端打包、卸载、安装、启动、健康检查。
2. 本地 `agent-turn`、运行时、tjuae 运行链路测试。
3. K8s readiness、connector catalog、IPM/QPP/ECMS/MySQL/TC connector 测试。
4. NX plugin、NX 工具、TC/NX 模型或图纸打开测试。
5. `零件设计智能体试用问题跟踪表.xlsx` 的预回归或正式回归。
6. Skill、tool、asset、manifest、规则包、报告模板等静态审计。

## 测试身份和登录信息

统一测试身份：

```text
user_id = "88000044"
user_name = "宋明芮"
```

Teamcenter 密码管理规则：

1. Teamcenter 密码只能写入本机用户配置，不得写入项目仓库、任务提示词、回执、日志摘要或截图说明。
2. 回执中如需证明密码已配置，只能写 `tc_key_configured=true` 或脱敏值。
3. 不允许在回执中打印 `tc_key`、`user_pass`、完整 API key、cookie、token 或任何明文凭据。

本机客户端配置位置：

```text
C:\Users\ASUS\AppData\Local\McDesign\configure\mc-design-client.config
```

执行智能体如需检查登录状态，只能检查配置是否存在、`user_id`/`user_name` 是否正确、`tc_key_configured=true` 是否成立，以及客户端 `/health` 是否显示 bridge connected。不得输出密码明文。

## 客户端运行规则

本地客户端默认健康检查地址：

```text
GET http://127.0.0.1:8765/health
GET http://127.0.0.1:8765/api/status
```

规则：

1. 通路测试前必须检查客户端是否运行。
2. 如果任务允许启动客户端，发现未运行时应先启动客户端再测试。
3. 如果任务明确禁止启动/重启客户端，发现未运行只能记录 `CLIENT_NOT_RUNNING`，不能擅自启动。
4. 如果另一个 E2E/安装任务正在使用客户端或安装目录，不得抢占、重启、卸载或覆盖，只能记录冲突或等待回执。
5. 如果客户端更新参与本轮测试，必须先完成打包、卸载旧版本、安装新版本、启动客户端和健康检查，不能只跑源码测试。
6. 打包、卸载、安装、启动任一失败，应先归类为客户端交付链路阻塞，不能跳过后直接测 K8s、NX 或业务工具。

## E2E 和安装包规则

安装包级测试必须记录：

1. 构建产物路径、bundle version、是否使用 `--skip-msbuild`。
2. 卸载旧客户端结果。
3. 安装新客户端结果。
4. 客户端启动方式、进程、端口、`/health`、`/api/status`。
5. 日志位置。
6. K8s smoke 和本地 `agent-turn` 结果。
7. 失败分类和停止点。

当前状态：

1. `PKG-001` 已通过安装包加固，但只代表安装包加固通过。
2. `E2E-SMOKE-001` 正式回执为环境阻塞；后续人工恢复验证只算监管补充，不能改判原任务通过。
3. `E2E-SMOKE-002` 正式回执为不通过：客户端卸载链路失败。`PKG-001` 安装包卸载阶段通过 `package-helper-fallback` 处理当前安装目录，但将 `C:\Users\ASUS\AppData\Local\McDesign` 判为 `foreign-dir` 后拒绝清理，退出码 9；未进入安装、启动、K8s smoke 或本地 `agent-turn`。

在 `E2E-SMOKE-002` 未通过前，不得把 tjuae 替换、客户端交付链路或问题表全量回归记为最终通过。

## 本地 agent-turn 规则

本地测试入口：

```text
POST http://127.0.0.1:8765/api/runtime/test/agent-turn
```

规则：

1. `test_agent_turn` 属于本地 `mc-design-client`，不属于 K8s。
2. K8s 不应暴露 `/api/mc-design/test/agent-turn`；该旧路径返回 404 是正确结果。
3. 本地 MCP Stream Tool 不能在本地直接访问和调用，不作为本地全通路测试入口。
4. 极简健康检查中出现环境类工具调用，只能证明本地入口和工具回调可用，不代表业务问题表回归通过。

## K8s connector 规则

K8s 基础检查优先级：

1. readiness。
2. connector catalog。
3. `mysql_query select 1` smoke。
4. IPM/QPP/ECMS 最小无副作用预检查。
5. 同一只读查询连续 5 次一致性检查。

人工前置：

1. `mc-design-ai-service` 有更新时，必须由项目负责人手动更新/重启 K8s 后才能做全通路测试。
2. 如果 K8s 连接失败且判断是网络未启动，记录 `VPN_REQUIRED` 或 `K8S_NETWORK_BLOCKED`，提醒项目负责人手动开启 VPN。
3. 不允许把网络/VPN 未就绪直接判成代码失败。

当前已知事实：

1. `K8S-SMOKE-001` 已通过 readiness、connector catalog、`mysql_query select 1`。
2. `K8S-CONNECTOR-PRE-001` 显示 `query_ipm_list` 默认参数、`query_ipm_list` 分页、`query_ecr_list` 分页均可成功。
3. `connect_qpp` 在 `K8S-CONNECTOR-PRE-001` 中出现上游 QPP 超时，且项目负责人确认当前 QPP 连接确实不通。后续涉及 QPP 的测试应直接归类为 `EXTERNAL_INTERFACE_UNAVAILABLE` 或 `QPP_EXTERNAL_UNAVAILABLE`，不是 mc-design 代码失败。
4. connector schema 中仍存在 Teamcenter `BEYA_TC_BASE_URL` 等旧命名问题，应作为 `RT-NAME-001` 类治理问题跟踪，不影响当前只读 smoke 的基础判定。

## NX 和图纸规则

强制规则：

1. NX plugin 中自动出图插件必须禁用。
2. 不允许使用或恢复 `nx-auto-drawing`、`nx_run_auto_drawing`、`nx_updatedrawings`、sheet 级自动图纸操作工具。
3. NX 图纸操作只允许通过 `nx_open_tcpart` 打开 NX 图纸。
4. NX 图纸与 NX 数模绑定后的自动更新，即视为项目所需的自动出图。

NX 前置检查：

1. 检查 NX 是否启动。
2. 检查 NX plugin 是否在 `127.0.0.1:8088` 监听。
3. 检查运行工具列表或 manifest 中是否包含 `nx_open_tcpart`。
4. 检查禁用工具是否不存在。
5. 只读预检查不得打开、修改、保存模型，不得调用有副作用的工具。

当前已知事实：

1. `NX-PRECHECK-001` 显示 NX 进程已启动，但客户端未运行，NX plugin 端口 8088 未监听。
2. 上述状态应记录为 `CLIENT_NOT_RUNNING` 和 `NX_PLUGIN_NOT_CONNECTED`，不判定代码失败。
3. 如 `nx_open_tcpart` 因测试环境网络无法打开 TC/NX 模型，应记录 `TC_NX_NETWORK_BLOCKED` 或 `NEED_MANUAL_MODEL_OPEN`，由项目负责人手动打开目标模型后继续。

## 问题表回归规则

问题表来源：

```text
references/开发资料/零件设计智能体试用问题跟踪表.xlsx
.tasks/receipts/S0-6/ACCEPTANCE_MATRIX.csv
.tasks/receipts/REG-001-PREP/AUDIT_RECEIPT.md
.tasks/receipts/REG-EVIDENCE-001/REGRESSION_EVIDENCE_CARDS.md
.tasks/receipts/REG-EVIDENCE-001/REGRESSION_EVIDENCE_CARDS.csv
```

规则：

1. `REG-001-PREP` 和 `REG-EVIDENCE-001` 只代表准备完成，不代表测试通过。
2. 已解决、已完成、已优化项仍必须在当前运行时和当前全通路条件下复测，不能按原表状态直接关闭。
3. 在 `E2E-SMOKE-002` 未通过前，可以做探索型/预回归；不能做最终验收型全通路回归。
4. 预回归结论只能写发现问题、证据、阻塞、可复现性和建议，不能写“全部通过”。
5. 正式回归必须逐条记录输入、输出、工具调用、截图/日志、失败分类、人工介入项和是否满足通过标准。

## 静态审计规则

静态审计任务必须检查：

1. skill/tool/asset 是否存在冲突描述。
2. 是否仍存在用户可见 Beya 旧表述。
3. 是否引用不存在的工具、文件、资源或 agent。
4. 是否存在 tool schema 与 skill 调用说明不一致。
5. 是否仍存在零件规则硬编码、报告模板硬编码、fixture 与 part-rules 重叠等问题。
6. 是否违反 tjuae 外部通用项目边界。

当前已知审计问题：

1. `SKILL-CONSIST-001` 发现 1 个 P0、4 个 P1、2 个 P2。
2. P0 是零件规则仍硬编码在 skill/runtime 中，后续建议任务编号 `SK-003`。
3. P1 包括 Teamcenter/Beya 命名不一致、报告模板硬编码连杆、capabilities 不统一、fixture 与 part-rules 重叠。
4. 这些问题应进入治理台账，但不应和正在进行的 E2E smoke 并发整改。

## 回执和证据规则

所有任务必须指定回执目录：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\<TASK_ID>\
```

执行类任务必须输出：

```text
EXECUTION_RECEIPT.md
```

审计类任务必须输出：

```text
AUDIT_RECEIPT.md
```

回执必须包含：

1. 任务边界。
2. 输入依据。
3. 执行步骤和命令。
4. 结果摘要。
5. 证据文件路径。
6. 失败分类。
7. 是否有人工前置条件。
8. 是否输出或涉及敏感信息，且必须说明未输出密码明文。

## 失败分类标准

推荐统一分类：

```text
CLIENT_NOT_RUNNING
CLIENT_INSTALL_FAILED
CLIENT_UNINSTALL_FAILED
CLIENT_HEALTH_FAILED
K8S_NOT_UPDATED
K8S_NETWORK_BLOCKED
VPN_REQUIRED
CONNECTOR_SCHEMA_MISMATCH
EXTERNAL_INTERFACE_UNAVAILABLE
QPP_EXTERNAL_UNAVAILABLE
MYSQL_QUERY_FAILED
NX_NOT_RUNNING
NX_PLUGIN_NOT_CONNECTED
TC_NX_NETWORK_BLOCKED
NEED_MANUAL_MODEL_OPEN
SIDE_EFFECT_NOT_ALLOWED
BUSINESS_ASSERTION_FAILED
TEST_PRECONDITION_NOT_MET
```

原则：

1. 环境前置未满足时，不判定代码失败。
2. 预回归不做最终通过结论。
3. 安装/启动链路未闭环时，不做全通路终验。
4. 外部系统超时、VPN 未开、NX 未启动、模型需手动打开都必须单独归类。

## 并发派发规则

1. 可以并发派发彼此不依赖的静态审计、证据整理、K8s 只读预检查、NX 只读预检查。
2. 不得并发派发顺序阻塞任务。
3. 不得在 E2E 安装/卸载任务进行中并发执行会启动、停止、卸载、安装或重启客户端的任务。
4. 后续任务如果依赖 `E2E-SMOKE-002` 结果，必须等正式回执返回后再派发。
