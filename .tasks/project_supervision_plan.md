# MC Design 项目监管计划

更新时间：2026-06-14

## 角色约定

本线程中，我的角色是项目经理/方案与计划负责人。职责是和项目负责人对齐总体方案、任务范围、优先级、计划、进度、验收标准和完成情况。

我们不在本线程直接做具体代码改进、功能开发或优化实现。具体工作拆成明确提示词，由项目负责人派发给其他智能体或执行团队完成。本线程负责监管、复盘、调整计划和验收口径。

职责边界修正：`tjuae` 能力查核、替换可行性判断、风险定级、整改验收口径由本线程负责，不下放给其他智能体。其他智能体只接收明确的整改、改造、测试、取证任务，不负责判断“是否应该替换”或“替换路线是否成立”。

外部项目边界修正：`tjuae` 是外部通用项目，不接受 `mc-design` 定制开发要求。我们只能要求 `tjuae` 修复其通用 bug，或把它已有的通用能力暴露到 Python SDK、server、CLI、文档和发布包中。所有 `mc-design` 专用适配、协议映射、资产投影、打包集成和验收用例由 `mc-design` 侧负责。

派发规则修正：以后所有任务提示词必须指定固定回执目录。执行类任务必须写入 `.tasks/receipts/<TASK_ID>/EXECUTION_RECEIPT.md`；审计类任务必须写入 `.tasks/receipts/<TASK_ID>/AUDIT_RECEIPT.md`。没有回执的任务不进入完成状态。

派发节奏修正：存在顺序阻塞关系的任务，只派发当前可执行的一个任务；后续任务只进入监管计划，不作为可执行提示词同时发出，避免误并发。

全通路测试环境修正：涉及 `mc-design-ai-service` 的更新，进入全通路测试前需要项目负责人手动更新 K8s；本地不能直接访问和调用 MCP Stream Tool，后续全通路测试入口放在本地 `mc-design-client` 的 `POST /api/runtime/test/agent-turn`；K8s 只保留 LLM/router/connector 能力。K8s 网络、VPN、NX 启动、`nx_open_tcpart` 测试环境限制均需要在测试前显式提醒项目负责人。

客户端测试门禁修正：只要本轮包含 `mc-design-client` 更新，通路测试前必须完成客户端打包、旧客户端卸载、新客户端安装、客户端启动和运行状态检查。未运行则先启动。该流程既是通路测试前置条件，也是验证客户端打包、卸载重装、运行功能是否正常的测试内容。回执必须记录安装包/构建产物路径、卸载重装结果、启动方式、进程/端口/健康检查结果和日志位置；任一环节失败，先判定为客户端交付链路阻塞，不能跳过后直接归因到 K8s、NX 或业务工具。

通路测试身份修正：后续测试默认使用 `user_id = "88000044"`、`user_name = "宋明芮"`。Teamcenter 密码只允许写入本机用户配置 `configure\mc-design-client.config` 的 `tc_key`，不得写入项目仓库、任务提示词正文或回执明文；回执只能记录 `tc_key_configured=true` 或脱敏值。

当前派发状态修正：截至本次整理，`BIZ-ADAPTER-001`、`NX-TOOL-HARDEN-001`、`E2E-SMOKE-003`、`REG-P0-FULL-001` 已回执并完成检查。`REG-P0-FULL-001` 结论为不通过，35 条覆盖中 11 通过、17 失败、7 阻塞。当前无正在执行任务、无已派发待回执任务；所有未开始、待派发、候选派发任务继续撤回冻结。后续如有需求，必须重新确认方案、重新编号、指定回执目录并给出可复制提示词；历史任务回执只保留为事实证据，不代表继续执行授权。

测试派发规则修正：后续所有测试、预回归、E2E smoke、K8s connector 检查、NX 前置检查、问题表回归、Skill/Tool/Asset 审计任务，都必须引用 `.tasks/TEST_EXECUTION_RULES.md`。该文件统一规定测试身份、登录/配置方式、密码脱敏、客户端启动规则、K8s/NX 人工前置、失败分类、回执要求和并发边界。

## 当前监管对象

1. `mc-design` 当前项目
   - 根目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design`
   - 关键子工程：
     - `mc-design-nx`：客户端、NX 插件、Windows 打包、智能体资产。
     - `mc-design-ai-service`：云端 AI Service、MCP Stream、Runtime Bridge、连接器和 LLM 代理。
   - 已纳入参考资料：
     - `references/开发资料/零件设计智能体试用问题跟踪表.xlsx`
     - `references/开发资料/零部件设计智能体需求及AI生成的解决方案.docx`
     - `references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表*.xlsx`

2. `tjuae` 外部依赖项目
   - 目录：`F:\Documents\tjuae`
   - 管辖方式：不纳入 `mc-design` 仓库直接管理，但作为替换 Beya 的外部受管依赖纳入监管。
   - 我们可以要求 `tjuae` 修复通用 bug、暴露已有通用能力到 Python SDK/server/CLI、提供通用发布说明，并跟踪其完成情况。
   - 不向 `tjuae` 提出 `mc-design` 专用接口、专用协议、专用打包结构或专用验收工程要求。

## 总体目标

目标一：将当前 `beya` 运行时一次性替换为 `tjuae`，不建设 `beya/tjuae` 双运行时，不保留 `beya` fallback。

目标二：解决 `零件设计智能体试用问题跟踪表.xlsx` 中全部问题。需要先按新运行时替换方案重新梳理问题，把 2026-06-18 之前要求完成的任务列为必须完成项。

## 当前架构判断

历史/替换前 `mc-design` 运行时链路是：

AI Web/MCP -> `mc-design-ai-service` -> WebSocket runtime bridge -> 本地 Python Client -> 本地 Beya Server / Beya SDK -> LLM 与工具编排 -> 本地 API 回调 -> NX 插件或云端连接器。

这条链路只作为替换范围基线保留，不再视为当前完成状态描述。替换 `beya` 不是简单改名，至少涉及：

1. 本地黑盒 `beya-server.exe` 替换为 `tjuae` 可嵌入运行时或本地服务。
2. Python 客户端内 `beya-sdk` 调用面替换为 `tjuae-sdk` 或兼容适配层。
3. Beya plugin 工具注册机制替换为 Tjuae plugin/tool/session 能力。
4. Beya 事件流 `LLM_PARTIAL / TOOL_INVOKED / TOOL_OBSERVATION / WORKFLOW_COMPLETED / APPROVAL_REQUESTED / QUESTION_REQUESTED` 映射为 `mc-design` RuntimeFrame/RuntimeEvent。
5. Windows 安装包中的 `client/beya-server/win-x64/beya-server.exe`、`beya-sdk` wheel、配置字段和日志路径替换。
6. AI Service 里所有 `beya_mcp` 命名、`beya.toml` 配置和测试命名需要迁移或兼容保留策略。

当前阶段性判断：

1. `RT-001`、`RT-002`、`RT-003` 已将运行时替换推进到阶段通过，但不是全通路终验。
2. `PKG-002` 已把旧的卸载误判问题推进到阶段通过；`E2E-SMOKE-003` 证明卸载/安装可以通过，但正式入口 `McDesignClient.exe` 仍不能稳定启动本地客户端。
3. `BIZ-ADAPTER-001` 已把任务候选归一、任务选择保持、参数分类、四类参数分支、NX 写入前计划落成本地业务适配工具层；后续重点是验证真实 agent-turn 是否实际调用这些工具。
4. `NX-TOOL-HARDEN-001` 已补齐 NX plugin/本地 API 协议边界和自动出图禁用防线；后续仍需 NX 实机编译/会话补验。
5. `REG-P0-FULL-001` 已补正式回执但不通过：本地 agent-turn 未找到 IPM 查询工具，参数四分支业务断言失败，截图失败，TC/NX 生命周期因前置不足阻塞；不得作为问题表 P0 全量回归通过依据。
6. 在 launcher 启动、测试身份/TC key、NX 实机前置和正式回执机制闭环前，不把 tjuae 替换记为全通路完成，也不把问题表全量回归记为完成。

## 全通路测试人工前置条件

全通路测试不能只看本地单元测试，以下环境条件需要在每次测试前确认：

1. `mc-design-ai-service` 有更新时，必须先提醒项目负责人手动更新 K8s，否则全通路仍可能跑旧服务版本。
2. MCP Stream Tool 在本地环境不能直接访问和调用，不应把本地 MCP Stream Tool 调用作为全通路验收入口。
3. RT-003 已明确 `test_agent_turn` 放在本地 `mc-design-client`，入口为 `POST /api/runtime/test/agent-turn`；K8s AI Service 不提供 HTTP agent-turn 测试接口。
4. 如果本轮包含客户端更新，必须先完成客户端打包、卸载旧版本、安装新版本、启动客户端并检查运行状态；未运行则启动。
5. 测试身份使用 `user_id = "88000044"`、`user_name = "宋明芮"`；Teamcenter 密码使用本机配置，不得在回执中明文输出。
6. 如果 K8s 连接失败且判断为网络未启动，需要提醒项目负责人手动开启 VPN。
7. 如果 NX 未启动，需要提醒项目负责人手动开启 NX。
8. 当前测试环境下 `nx_open_tcpart` 因网络原因不可用，需要提醒项目负责人手动打开目标 TC/NX 模型，再继续后续参数、截图、报告或工具链测试。

后续任何“全通路测试”任务提示词必须包含上述人工前置条件和回执要求。若测试失败，回执必须区分代码缺陷、客户端打包失败、客户端卸载/重装失败、客户端未启动或健康检查失败、K8s 未更新、VPN 未开启、NX 未启动、TC/NX 模型需手动打开这几类原因。

## `tjuae` 初步调研结论

`tjuae` 是 Bun/TypeScript 本地 Agent 工作台，包含 CLI/TUI、本地 Server、Tauri/React Platform、Python SDK、IM adapters、contracts/codegen、质量门禁和 `runtime/mc-design` 目录。

对 `mc-design` 替换 Beya 有价值的能力：

1. Python SDK 已有 `TjuaeClient().chat.stream()`、`chat.respond()`、`sessions`、`providers`、`plugins`、`tools`、`workspace` 等接口形态。
2. 插件模型支持 `define_plugin`、`define_tool`、`RemoteToolExecutor`、`ConnectorToolExecutor`，可承载当前 NX/连接器工具回调。
3. Server 有 `/rpc`、`/sessions/{sessionId}/live`、`/sessions/{sessionId}/runtime` 等通信路径，适合作为本地运行时服务。
4. 已有 contracts/codegen，适合作为稳定协议来源。
5. 当前 `tjuae` 工作区有未提交改动，需要在监管台账中标记为外部依赖风险，不能直接假设其可发布。

`tjuae` 可请求配合的通用能力边界：

1. 若 `tjuae` 已具备 Windows 本地 server/runner 能力，要求提供通用启动、停止、健康检查和发布说明；`mc-design` 专用打包接入由 `mc-design` 侧完成。
2. 若 `tjuae` server 已具备相关能力但 Python SDK 未暴露，要求暴露到 Python SDK：
   - provider upsert/activate
   - settings/permission mode
   - session create/history/reuse
   - chat stream/respond
   - plugin install_or_update/reload/list
   - tools list/execute
   - readiness/status/diagnostics
3. 若 `tjuae` 已具备 remote tool executor/server tool 能力，要求稳定通用协议、错误码和日志，不要求内置 `mc-design` 回调地址。
4. 事件流要求保持通用表达能力：content、reasoning、tool started、tool completed、tool failed、permission/question/plan interaction、final/failed。
5. 若 `tjuae` 已具备 workspace/skills/tools/agents 加载能力，要求提供通用目录规范和 SDK/server 调用方式；`mc-design` 资产投影由 `mc-design` 侧完成。
6. `tjuae` 只需提供通用测试、示例和发布验证；NX 工具回调、连接器工具回调、下载/附件产物等 `mc-design` 验收工程由 `mc-design` 侧负责。

## 问题跟踪表初步盘点

主表 `零件设计智能体试用问题跟踪表` 共 54 行问题记录，存在重复编号和已解决项。按要求完成时间统计：

| 要求完成时间 | 行数 | 处理策略 |
|---|---:|---|
| 2026-06-14 | 10 | 必须完成，P0 |
| 2026-06-15 | 3 | 已解决项，必须回归确认 |
| 2026-06-16 | 6 | 必须完成，P0 |
| 2026-06-18 | 9 | 必须完成，P0 |
| 空白 | 7 | 需去重或补充计划 |
| 2026-06-20 | 3 | P1 |
| 2026-06-22 | 3 | P1 |
| 2026-06-24 | 1 | P1，外部接口依赖 |
| 2026-06-30 | 11 | P2/二期或专项 |
| `.` | 1 | 信息不规范，需补齐日期 |

问题状态统计：

| 状态 | 行数 | 处理策略 |
|---|---:|---|
| 空白 | 42 | 需纳入计划 |
| 已解决 | 7 | 回归验证 |
| 已完成 | 1 | 回归验证 |
| 已优化 | 2 | 回归验证 |
| 升版接口已提单 | 2 | 外部依赖跟踪 |

## 2026-06-18 前必须完成项

### P0-A 参数转换与引导式建模闭环，要求 2026-06-14

覆盖行：2-11。

问题范围：

1. 设计参数齐全时自动校验并可直接建模。
2. 设计参数不全/无参数时展示已有参数和缺失参数，支持补充或跳过。
3. 仅边界参数时可按逻辑表达式推导设计参数，不足时精准提示缺失边界参数。
4. 混合参数时优先边界参数换算，整合设计参数后二次校验。
5. 驱动参数表格导入/导出。
6. 推送三种操作选项：直接建模、补充参数、查看模板全部参数。
7. 支持人工指定模板并识别模板参数要求。
8. 驱动参数变化后关联参数同步更改。
9. 从 TC 打开模型时避免先下载试错，应优先走稳定打开工具。
10. 参数修改必须使用参数 ID，不能随机用中文描述调工具。

监管验收口径：

1. 输入完整参数、缺失参数、边界参数、混合参数四类测试用例均能稳定进入预期分支。
2. 每类分支必须有明确用户可见提示，不能靠模型自由发挥。
3. 任务参数转换结果必须形成结构化中间态，可审计、可复用。
4. 工具调用中必须使用参数 ID 和稳定模板 ID。
5. 回归连杆、活塞销、止推片逻辑表达式表。

### P0-B 设计报告、二维图、说明书链路，要求 2026-06-16

覆盖行：12-17。

问题范围：

1. 二维图更新功能集成到多智能体。
2. 设计说明书自动编制功能集成到多智能体。
3. K8S 生成说明书下载链接本地不可下载。
4. 设计说明书截图偶发错误，全是正视图。
5. 报告生成需从 TC 下载既有设计说明书并复制相关内容。
6. 报告预览、保存、上传 TC、链接下载、按用户修改要求更新。

监管验收口径：

1. 报告产物必须本地可下载，不依赖 K8S 内部路径。
2. 说明书生成前后必须有预览与确认。
3. 截图视角必须可验证，至少覆盖关键视图而不是重复正视图。
4. TC 旧说明书内容导入必须保留来源记录。
5. 二维图更新和报告链路不能破坏三维模型修改顺序。

### P0-C IPM/QPP/ECMS 查询稳定性与任务选择，要求 2026-06-18

覆盖行：18-24、29。

问题范围：

1. 查询 3 个月内到期 IPM 任务必须使用当前日期，不能固定到 2024-10-06。
2. 同一查询条件返回结果必须稳定。
3. IPM 状态入参必须稳定，不能随机传枚举值 1。
4. 查询中不能停留在“正在查询，请稍候”。
5. 必须返回查询到的全部信息。
6. 可从 IPM、ECMS、QPP 抓取展示任务，并让用户选择任务编号执行。
7. DFMEA 表自动编制集成到多智能体。

监管验收口径：

1. IPM/QPP/ECMS 查询工具必须封装成稳定工具，不依赖 prompt 触发词。
2. 查询入参、出参、排序、分页、状态值必须结构化固定。
3. 相同查询至少连续执行 5 次结果一致或差异可解释。
4. 结果必须全部返回并可滚动/分页展示，不能只返回摘要。
5. 用户选中任务编号后，后续多轮对话必须保持任务上下文。

### P0-D TC/NX 文件与模型生命周期，要求 2026-06-18

覆盖行：30、33。

问题范围：

1. 上传到 TC 不能只有图号，三维模型和二维图纸也必须上传。
2. 多智能体不能找错模型，不能在三维模型修改前自行打开二维图纸。

监管验收口径：

1. TC 上传物清单必须包含图号、三维模型、二维图纸和相关报告，或明确说明缺失原因。
2. 模型打开顺序必须受状态机约束：任务确认 -> 模板/模型确认 -> 三维修改 -> 更新/校验 -> 二维图/报告。
3. 找错模型必须有拦截，不能继续执行副作用工具。

### P0-E 已解决项回归确认，要求 2026-06-15

覆盖行：20、25、26，以及空白日期中的已解决/已优化/已完成项。

问题范围：

1. 查询到的信息不直接返回、一直拉扯。
2. 复杂问题达到最大轮次直接挂机。
3. TC/IPM/QPP 连接信息已解决项。
4. 必须说固定触发词才能查询 IPM 的问题。
5. 查询到任务后多轮对话丢失任务的问题。
6. 模板未存 TC 的已解决项。
7. IPM 状态查询新增需求已解决项。

监管验收口径：

1. 已解决项不直接关闭，必须在替换 `tjuae` 后做一次回归。
2. 回归用例需要记录输入、输出、工具调用、结果截图或日志。

## 2026-06-20 至 2026-06-24 近期项

1. 找错模型/未完成三维修改前打开二维图纸的 bug 复核。
2. 质量防再发报告融入设计指标参数转化。
3. 最大轮次挂机问题二次复核。
4. TC 账号、链接、登录信息自动获取。
5. 智能体稳定性和一次完成率提升。
6. IPM 全部任务信息滑动显示。
7. 从 TC 查询文件功能，依赖宋明芮接口。

## 2026-06-30 二期/专项项

1. 主页面显示驱动参数。
2. 模型视图参数高亮提醒。
3. 运行提速。
4. 修改驱动参数时保证非目标参数不被误改。
5. 圆角等建模失败时可柔性修正并高亮修改点。
6. 后台任务中断。
7. TC 升版逻辑。
8. 通过设计参数值查找模型。
9. 指定零件 ID 升级版本或另存能力。

## 关键监管策略

1. 先做问题重分类，不按原表编号直接派工，因为存在重复编号、已解决项和二期项。
2. 2026-06-18 前只追 P0 闭环，二期功能不得挤占必须项。
3. `tjuae` 替换是底座工程，不等于所有业务问题自动解决；业务问题仍按参数链路、IPM 链路、报告链路、TC/NX 链路分别验收。
4. 所有“模型随机性”问题必须产品化为确定性状态机、结构化工具、固定 schema、可回归测试。
5. 外部接口依赖必须有责任人和阻塞状态，不能混入普通开发项。
6. 能力查核、方案判断、替换风险由项目监管线程承担；派工提示词只给执行任务，不让执行智能体承担 PM 判断。
7. 对 `tjuae` 只能提出通用 bug 修复和已有能力 SDK/server 暴露请求；`mc-design` 定制适配不得下压给 `tjuae`。
8. 零部件知识不能长期硬编码在单个 `SKILL.md` 正文中。具体零部件的输入参数、公式、默认/关联参数、缺参追问、输出表和测试用例应逐步沉淀为可版本化规则包或资源文件，`SKILL.md` 只保留通用流程、门禁和调度规则。
9. 每个执行或审计任务必须提供固定回执路径和产物路径。回执统一放在 `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\<TASK_ID>\`。
10. 顺序依赖任务不得一次性并发派发。只有前置任务回执通过验收后，才派发下一任务。
11. NX 图纸能力口径：NX plugin 中自动出图插件必须明确禁用。NX 图纸操作只保留通过 `nx_open_tcpart` 打开 NX 图纸；图纸与数模绑定后随数模更新自动更新，这已经算作项目所需的“自动出图”。不得再把 `nx-auto-drawing` 或 `nx_run_auto_drawing` 作为可用自动出图能力派发或验收。

## DFMEA/FMEA 模板与工具路线

资料来源已纳入项目参考目录：

- `references/开发资料/DFMEA模板/14N连杆部件边界图、P图和DFMEA.xls`
- `references/开发资料/DFMEA模板/K09LN-1004201-01A-DFMEA01.xls`
- `references/开发资料/DFMEA模板/K11-1004201-21-DFMEA01.xls`

同时已用 Excel COM 预转换出运行时优先使用的 `.xlsx` 副本：

- `references/开发资料/DFMEA模板/14N连杆部件边界图、P图和DFMEA.xlsx`
- `references/开发资料/DFMEA模板/K09LN-1004201-01A-DFMEA01.xlsx`
- `references/开发资料/DFMEA模板/K11-1004201-21-DFMEA01.xlsx`

模板结构判断：

1. 完整模板包含 `DFMEA`、`DFMEA-0530`、`P图`、`P图-0530`、`边界图`、`AP`、`严重度S`、`频度O`、`探测度D`、`更改控制页` 等 sheet，可作为 DFMEA/P 图/边界图一体化模板。
2. 两个轻量模板主要包含 `DFMEA`、`AP`、`更改控制页`，适合作为快速 DFMEA 表生成模板。
3. 运行时生成建议优先使用 `.xlsx` 副本，保留 `.xls` 原件用于来源追溯。

技术路线决策：

1. 不放入 NX plugin。DFMEA/FMEA 表生成、模板复制、字段替换、AP 计算和产物导出都不是 NX 会话能力，不应增加 NX plugin 负担。
2. 不要求 `tjuae` 定制。`tjuae` 只负责通用会话、工具调用和事件流；DFMEA 是 `mc-design` 业务能力。
3. 做 Python 客户端本地工具组 `tool.dfmea`。工具不依赖 NX 连接，通过客户端 tool registry 暴露。
4. 运行时优先使用 `.xlsx` 模板，建议自研轻量模板填充工具，基于 `openpyxl` 或标准 OpenXML 方式复制模板并写入指定单元格/表格行。
5. 不建议引入重型 Office 插件或把 Excel COM 作为强运行时依赖。Excel COM 可作为开发期 `.xls -> .xlsx` 转换手段；正式工具应能在无 Excel GUI 的客户端 Python 环境中处理 `.xlsx`。
6. Skill 负责 DFMEA 业务流程、缺项追问、风险确认、人工复核门禁和 TC 上传前确认；工具只负责模板发现、模板检查、字段填充、AP/RPN 计算、文件输出和元数据返回。

### DFMEA-001 DFMEA/FMEA 模板工具与 Skill 补全

范围：`dfmea-risk-review` skill、`design-report`/`teamcenter-flow` 的 DFMEA 边界说明、`mc-design-nx/assets/source/tools/tool.dfmea`、Python 客户端本地工具注册、相关测试。

目标：把当前“DFMEA 风险复核”补全为“DFMEA 表生成/更新/复核/上传前确认”闭环。新增 `tool.dfmea` 本地工具组，支持模板清单、模板结构检查、字段/表格填充、AP/RPN 计算、输出文件元数据返回，不依赖 NX。

价值：解决问题表中 DFMEA 表自动编制能力缺口，同时避免把 Excel 模板替换逻辑硬塞进 skill 正文或 NX plugin。

## 新增架构风险：零部件 Skill 硬编码

当前 `logic-expression-design` 已经具备通用流程框架，但 `conrod-design` 仍把连杆的 11 个必需输入、公式、结果确认表和 Python 计算示例写在 skill 正文中；活塞销、止推片目前也主要沉淀为最小测试用例，没有形成统一可复用的零部件规则包。

风险判断：

1. 新增零部件时容易复制一个新的专用 skill，导致规则、公式、追问表和测试用例分散。
2. 业务规则或公式变更时需要改 prompt 文本，难以版本化、差异审查和自动测试。
3. skill 正文过长会让智能体把零件知识、流程门禁和工具调用规则混在一起，增加误调用 NX、跳过确认或使用过期规则的概率。
4. 当前结构对连杆首例可用，但不适合作为多零件族规模化扩展方式。

治理方向：

1. 建立零部件规则包 schema：零部件 ID、适用场景、输入参数、输出参数、公式、关联/默认参数、单位、缺参追问、约束、证据来源、测试用例。
2. 将 `SKILL.md` 从“写死零件规则”调整为“读取规则包并执行通用流程”的调度说明。
3. 先做审计和规则包方案，再选择连杆作为试点迁移；活塞销、止推片跟随同一 schema 补齐。
4. 规则包必须可测试：完整输入、缺参输入、混合输入、公式变更、单位解析、经验默认值确认、NX 写入前映射门禁。

## `tjuae` 门禁前可先行派工任务

状态说明：本节保留为历史任务拆分和问题线索。由于项目方案可能发生较大变化，以下未执行任务均已撤回冻结，不再作为当前可派发任务。

这些任务不依赖 `tjuae` 最终 SDK/server 基线，不触碰 `beya -> tjuae` adapter、运行时启动、Windows runtime payload 和最终配置切换。

### S0-1 业务资产运行时中性化

范围：`mc-design-nx/assets/source/skills`、`mc-design-nx/assets/source/tools`、`mc-design-ai-service/tools/business/*/TOOL.md`。

目标：把业务 skill/tool 文档中的 `Beya Server/SDK/plugin` 实现名改为“运行时/Runtime/connector catalog/工具注册表”等中性表述，保留当前文件名和测试兼容，不做运行时代码替换。

价值：后续 `tjuae` 替换时，业务资产不会继续把 Beya 当作业务概念。

### S0-2 参数转换 schema 与测试用例固化

范围：`parameter-mapping`、`logic-expression-design`、`conrod-design`、活塞销/止推片/连杆逻辑表达式表、问题表行 2-11。

目标：先固化设计参数、边界参数、模板参数、驱动参数、关联参数 schema，以及四类输入分支的验收用例。不依赖运行时，只沉淀 skill、fixtures、测试和提示约束。

价值：P0-A 的核心随机性问题可提前收敛为确定性状态机和可回归用例。

### S0-3 IPM/QPP/ECMS 工具契约稳定化

范围：`mc-design-ai-service/tools/business/external`、`external-connector-adapter` skill、相关测试。

目标：稳定 query_ipm_list/connect_qpp/query_ecr_list 的入参、默认值、日期窗口、状态枚举、分页、排序和全量返回策略，补齐“查询 3 个月内到期任务”“相同查询 5 次一致”“用户选择任务编号”相关测试。

价值：P0-C 多数问题属于工具契约和展示流程，不必等运行时替换。

### S0-4 TC/NX 模型生命周期规则加固

范围：`part-design`、`teamcenter-flow`、`nx-operation`、`nx-parameter`、NX tool manifest 相关测试。

目标：加固任务确认 -> 模板/模型确认 -> 三维修改 -> 更新/校验 -> 二维图/报告的状态机；明确主模型和二维图打开边界；明确 TC 上传物清单包含三维模型、二维图纸、报告和缺失原因。

价值：P0-D 的“找错模型、过早打开二维图、上传不完整”可以先从 skill/tool 契约层阻断。

### S0-5 设计报告/截图/说明书链路加固

范围：`design-report` skill、`design_report.py`、报告模板资源和测试。

目标：补齐本地可下载路径、报告预览/确认、截图视角顺序验证、从 TC 旧说明书复制内容的来源记录、生成后上传 TC 前的确认规则。

价值：P0-B 的报告链路可先形成确定性脚本和测试，不依赖运行时替换。

### S0-6 问题表验收矩阵

范围：`references/开发资料/零件设计智能体试用问题跟踪表.xlsx` 和 `.tasks`。

目标：把 Excel 问题转成可派工、可验收、可回归的矩阵：原表行号、问题摘要、模块、优先级、截止日期、验收用例、依赖、证据要求、状态。

价值：后续每个执行智能体交付时按统一证据口径验收，避免只口头说“已优化”。

### SK-001 零部件 Skill 硬编码审计

范围：`mc-design-nx/assets/source/skills`、`references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表*.xlsx`、`references/开发资料/零件设计智能体试用问题跟踪表.xlsx`。

目标：审计所有零部件相关 skill 中硬编码的零件名、参数名、公式、追问表、输出表、工具名、模板名和默认值，区分“通用流程规则”和“零部件知识规则”。

价值：先看清硬编码面和迁移优先级，避免后续零件扩展继续复制专用 skill。

### SK-002 零部件规则包 schema 与加载方案

范围：`logic-expression-design`、`parameter-mapping`、`conrod-design`、最小测试用例资源。

目标：设计零部件规则包 schema、资源目录结构、版本字段、公式表达方式、缺参追问结构、测试用例格式和 skill 加载/引用方式。不直接大规模改造现有 skill。

价值：把零部件知识从 prompt 正文迁出到可版本化、可测试、可替换的资源层。

### SK-003 连杆规则包试点迁移

范围：`conrod-design` 及其关联资源和测试。

目标：在 SK-001/SK-002 方案通过后，将连杆的 11 个输入、4 个输出公式、确认表、计算脚本模板和测试用例迁移到规则包；`conrod-design` 只保留调度、门禁、NX 写入前置条件和异常处理。

价值：用连杆验证规则包方案，再推广到活塞销、止推片和后续零件。

当前状态：候选任务已撤回冻结，待新方案重新确认后再决定是否重新编号派发。

## 初始派工提示词模板

### 提示词 1：派给 `tjuae` 外部通用能力整改执行智能体

```text
你是 tjuae 外部通用能力整改执行智能体。

工作目录：
F:\Documents\tjuae

背景：
mc-design 已决定一次性将本地运行时从 beya 替换为 tjuae。能力查核和替换路线由 mc-design 项目监管方负责，你不需要判断是否应该替换，也不需要设计 mc-design 迁移方案。

重要边界：
1. tjuae 是外部通用项目，不做 mc-design 专用定制。
2. 你只能修复 tjuae 通用 bug，或将 tjuae 已有通用能力暴露到 Python SDK、server、CLI、文档和发布包中。
3. 如果某项能力在 tjuae 中不存在，不要新建 mc-design 专用能力；请标记为“当前 tjuae 通用能力不存在/不适合由 tjuae 提供”，由 mc-design 侧自行适配或由 PM 裁决。
4. 不允许写入 mc-design 专用路径、专用回调地址、专用协议名称或专用验收工程。

整改任务：
1. 若 tjuae 已有 Windows 本地 server/runner，提供通用启动、停止、健康检查和日志定位方式。
2. 若 tjuae server 已有能力但 Python SDK 未暴露，请暴露或稳定以下通用 SDK 调用面：
   - sessions create/history/reuse/close
   - chat stream/respond
   - plugins install_or_update/reload/list
   - tools list/execute
   - provider/settings 配置
   - readiness/status/diagnostics
3. 若 tjuae 已有 remote tool/server tool 能力，稳定其通用工具执行协议、错误码、超时、日志和返回结构。
4. 稳定事件流格式，至少覆盖：
   - content delta
   - reasoning delta
   - tool started
   - tool completed
   - tool failed
   - permission/question interaction
   - final completed
   - failed
5. 提供通用 Python SDK/server 示例：
   - 创建会话
   - 发送普通对话
   - 触发通用工具调用
   - 回传工具结果
   - 流式返回最终答案
6. 提供通用打包说明、启动命令、健康检查命令、日志位置。

输出格式：
- 改动文件清单
- 新增/修改接口说明
- 启动与健康检查方式
- 通用 SDK/server 示例
- 测试命令和结果
- 无法按通用项目边界提供的能力清单及原因
```

### 提示词 2：派给 `mc-design` 运行时替换执行智能体

```text
你是 mc-design 运行时替换执行智能体。

工作目录：
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design

外部依赖目录：
F:\Documents\tjuae

原则：
1. 一次性将 beya 替换为 tjuae。
2. 不建设 beya/tjuae 双运行时。
3. 不保留 beya fallback。
4. 不做业务功能优化。
5. 保持 mc-design 对上层 AI Service、NX 插件和工具调用契约尽量不变。

执行任务：
1. 全量搜索并替换运行时层面的 beya 依赖，包括 Python 依赖、import、server manager、adapter、runtime metadata、配置、打包脚本、部署文档。
2. 新增 tjuae 对应组件：
   - TjuaeServerManager
   - TjuaeRuntimeAdapter
   - tjuae session/chat/tool/event 映射
   - tjuae 健康检查
   - tjuae 配置读取
   - tjuae 打包路径
   以上组件必须基于 tjuae 对外提供的通用 Python SDK/server/CLI 能力实现，不得要求 tjuae 做 mc-design 专用接口。
3. 删除或弃用以下 beya 运行时链路：
   - beya_server.py 或其中 beya-server.exe 管理逻辑
   - runtime/beya_server_adapter.py
   - pyproject 中 beya-sdk 依赖
   - Windows payload 中 beya-server.exe 和 beya SDK 复制逻辑
4. 更新配置命名，不再使用 beya 作为运行时配置入口。
5. 更新最小测试，覆盖：
   - tjuae 启动
   - 健康检查
   - 创建会话
   - 普通对话流式返回
   - 工具调用与结果回传
6. 执行 `rg -i "beya"`，说明剩余命中是否为历史迁移说明；运行时代码不得保留有效 beya 依赖。

输出格式：
- 改动文件清单
- 替换后的启动链路说明
- 测试命令和结果
- `rg -i "beya"` 残留说明
- 阻塞项和需要 PM 裁决的问题
```

### 提示词 3：派给问题跟踪表重排智能体

```text
你负责重排 references/开发资料/零件设计智能体试用问题跟踪表.xlsx 中的问题。不要修改原始 Excel。

目标：
1. 读取所有工作表，重点读取“零件设计智能体试用问题跟踪表”。
2. 处理重复编号、已解决项、空白计划项和 2026-06-18 前必须项。
3. 按模块重排：参数转换、IPM/QPP/ECMS、报告/二维图/DFMEA、TC/NX 文件生命周期、部署问题、二期能力。
4. 每条问题给出：原表行号、原序号、问题摘要、目标完成日期、建议优先级、是否必须 18 号前完成、验收标准、依赖项。

输出格式：
- 总览统计
- 2026-06-18 前必须项清单
- 后续项清单
- 已解决待回归清单
- 外部依赖/阻塞清单
```

### 提示词 4：派给参数转换方案智能体

```text
你负责制定“任务参数转化及引导式用户提供数据”的产品与技术方案。不要直接实现。

参考资料：
- references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表(1).xlsx
- references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表（活塞销）3.0.xlsx
- references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表（止推片）3.0.xlsx
- references/开发资料/零件设计智能体试用问题跟踪表.xlsx 行 2-11

目标：
1. 定义设计参数、边界参数、模板参数、驱动参数、关联参数的结构化 schema。
2. 设计四类输入情形的状态机：参数齐全、不全/无参数、仅边界参数、混合参数。
3. 设计用户交互选项：直接建模、补充参数、查看模板全部参数。
4. 设计导入/导出驱动参数表格能力。
5. 给出验收用例和失败分支提示词。

输出格式：
- 参数 schema
- 状态机
- 工具/接口需求
- 测试用例
- 对实现智能体的开发提示词
```

### 提示词 5：派给 IPM/QPP/ECMS 稳定化方案智能体

```text
你负责制定 IPM/QPP/ECMS 查询稳定化方案。不要直接实现。

参考：
- references/开发资料/零件设计智能体试用问题跟踪表.xlsx 中 IPM/QPP/ECMS 相关问题
- mc-design-ai-service/tools/business/external/external.py
- mc-design-ai-service/beya_mcp/runtime_bridge.py

目标：
1. 梳理当前外部任务查询工具的入参/出参/状态枚举/分页/排序。
2. 设计稳定工具 schema，杜绝依赖“通过调用IPM接口查询”等提示词触发。
3. 设计“全部任务信息返回 + 用户选择任务编号 + 多轮上下文保持”的链路。
4. 给出相同查询 5 次结果一致性的验收方案。

输出格式：
- 当前风险
- 稳定 schema
- 状态枚举和默认值
- 展示与选择流程
- 回归测试用例
```

### 提示词 6：派给报告/二维图/DFMEA 方案智能体

```text
你负责制定设计说明书、二维图更新、DFMEA 集成方案。不要直接实现。

参考：
- references/开发资料/零件设计智能体试用问题跟踪表.xlsx 行 12-17、29
- references/开发资料/零部件设计智能体需求及AI生成的解决方案.docx
- mc-design-nx/assets/source/skills/design-report
- mc-design-nx/nx-plugin/src/McDesign.NXTools/AutoDrawingTools.cs

目标：
1. 设计报告生成、预览、保存、上传 TC、链接下载流程。
2. 解决 K8S 链接本地不可下载的交付策略。
3. 设计截图视角稳定策略。
4. 设计从 TC 下载旧说明书并复制内容的来源追踪。
5. 设计二维图更新和 DFMEA 集成到多智能体的验收标准。

输出格式：
- 用户流程
- 工具/接口需求
- 文件产物与下载策略
- TC 上传策略
- 测试与验收清单
```

## 完成验收记录

### 2026-06-14：S0-2 参数转换与 skill 加固

验收结论：阶段通过，可进入后续 P0-A 联调/实机验证。

已完成：

1. 新增统一参数 schema：`mc-design-nx/assets/source/skills/parameter-mapping/resources/parameter_schema.json`。
2. 新增四类输入分支状态机：`mc-design-nx/assets/source/skills/logic-expression-design/resources/input_branch_state_machine.json`。
3. 新增连杆、活塞销、止推片最小测试用例：`mc-design-nx/assets/source/skills/logic-expression-design/resources/minimal_test_cases.json`。
4. 更新 `logic-expression-design`、`parameter-mapping`、`conrod-design`、`nx-parameter`、`part-design` 和 skill 索引，明确中文参数名不得直接作为 NX 表达式名写入。
5. 更新资产打包和 skill 契约测试，确保新增资源进入 asset package。

验收证据：

- `mc-design-nx`: `python -m pytest client/tests/test_design_skill_contract.py client/tests/test_asset_store.py -q`
- 结果：17 passed。

剩余风险：

1. 活塞销、止推片当前沉淀为最小用例与期望值，尚未形成独立可执行计算脚本。
2. “不得随机调用 NX 参数写工具”目前主要由 skill/测试约束保证，运行时工具层强约束仍需依赖后续 NX 参数工具加固任务。

### 2026-06-14：S0-3 外部任务工具契约稳定化

验收结论：阶段通过，可进入后续 P0-C 联调/真实接口验证。

已完成：

1. `query_ipm_list` 固定默认状态为 `未提交`、`不通过`、`已确认`，并在 schema 中声明允许枚举。
2. `query_ipm_list` 明确 `page=1`、`pageSize=10` 默认值和分页边界。
3. `connect_qpp`、`query_ecr_list`、`query_ipm_list` 日期字段补充 `YYYY-MM-DD` 和“相对日期按当前日期计算”的契约说明。
4. `external-connector-adapter` skill 补齐 3 个月动态日期、全部任务分页、连续 5 次一致性、稳定任务编号、多轮上下文保持规则。
5. 新增 schema/状态枚举/分页/随机状态拒绝/5 次稳定查询/skill 文本约束测试。

验收证据：

- `mc-design-ai-service`: `python -m pytest tests/test_usage_issue_fixes.py -q`
- 结果：7 passed。

剩余风险：

1. “当前日期加 3 个自然月”目前是 tool schema 与 skill 层约束，工具函数本身不自动计算日期窗口。
2. “全部任务信息返回 + 用户选择任务编号 + 多轮上下文保持”目前是 skill 层约束，尚未有跨轮运行时状态测试。

### 2026-06-14：TJ-001 tjuae 外部通用能力整改

验收结论：阶段通过，可派发 mc-design 侧一次性替换集成任务。

已完成：

1. tjuae 通用 server 文档补齐启动、停止、健康检查、日志和诊断目录说明，不引入 mc-design 专用路径或专用协议。
2. Python SDK 补齐通用调用面：session create/history/reuse/close、chat stream/respond、plugins install_or_update/reload/list、tools list/execute、provider settings、readiness/status/diagnostics。
3. server WebSocket 事件补齐 `session.tool.started`，Python SDK `RunEvent.category` 形成稳定事件分类。
4. 通用事件流覆盖 content delta、reasoning delta、tool started、tool completed、tool failed、permission/question/plan interaction、final completed、failed。
5. 通用远程工具协议通过 server contract 测试覆盖，包含 HTTP executor payload、错误归一化、tool_call_id、session_id 和 metadata。
6. 交付包生成通用 Python 示例：普通对话、流式对话、插件安装、远程工具 server、工具 roundtrip。

验收证据：

- `tjuae`: `bun run check:sdk`
- 结果：server SDK contract 8 passed；Python SDK unittest 12 passed；Python SDK build passed。
- `tjuae`: `bun test src/server/__tests__/ws-memory-events.test.ts`
- 结果：16 passed。
- `tjuae`: `bun run delivery:build`
- 结果：生成 `F:\Documents\tjuae\dist\tjuae-sdk`，包含 server、healthcheck、contracts、Python wheel 和 examples。

剩余风险：

1. 交付包构建存在两个非阻断 bundler warning：`getCachedMCConfig` 与 `DISCOVER_SKILLS_TOOL_NAME` 导入目标不存在。当前不阻断 SDK/server 验收，但应由 tjuae 后续作为通用工程质量问题清理。
2. 停止方式目前是关闭前台进程或由进程管理器发送 SIGINT/SIGTERM；mc-design 侧替换时应自行管理 tjuae 子进程生命周期，不要求 tjuae 提供项目专用 stop API。
3. mc-design 侧只能使用 tjuae 已暴露的通用 SDK/server 能力；若替换过程中发现缺失能力，应按“tjuae 通用能力补齐/bug 修复”单独反馈，不允许在 tjuae 增加 mc-design 专用接口。

### 2026-06-14：NX-005 本地文件工具迁移

验收结论：通过。此前阻塞的 `runtime.md` 资产打包问题已在当前工作树中解除，正式测试已补跑通过。

已完成：

1. `NxFileBridgeTools.cs` 已从 NX plugin 删除，`McDesign.NXTools.csproj` 不再编译该文件。
2. `generate_nx_manifest.py` 增加过滤，原始 `fs_*` 和生成后的 `nx_fs_*` 都不会进入 NX manifest。
3. `client/resources/nx_tools_manifest.json` 与临时重新生成的 manifest 均未发现 `nx_fs_read_bytes`、`nx_fs_write_bytes`、`nx_fs_copy`、`nx_fs_exists`。
4. 新增 Python 客户端本地工具提供者 `local_file_provider.py`，注册：
   - `local_file_exists`
   - `local_file_read_bytes`
   - `local_file_write_bytes`
   - `local_file_copy`
5. 4 个工具均标记为 `source=python-client`、`tool_group=tool.local_file`、`requires_connection=false`。
6. 安全边界包括允许根目录、禁止 `..` 逃逸、默认不覆盖、读取/写入大小上限、返回 `size_bytes`/`sha256`/`path`、大文件不返回 base64。
7. `tool.nx` 说明已明确 NX plugin 不再承担文件桥能力，新增 `tool.local_file` 工具说明。

验收证据：

- `mc-design-nx`: 临时运行 `generate_nx_manifest.py` 到 temp manifest。
- 结果：tool_count=31，未发现 legacy `nx_fs_*` 或 `fs_*` 文件桥工具。
- `mc-design-nx`: 检查 `client/resources/nx_tools_manifest.json`。
- 结果：未发现 legacy `nx_fs_*` 或 `fs_*` 文件桥工具。
- `mc-design-nx`: 直接执行最小 Python 校验脚本。
- 结果：本地文件工具注册、无需 NX 连接、读写、越界路径拒绝、大文件拒绝、默认不覆盖均通过。
- `mc-design-nx`: 直接执行安全边界抽查。
- 结果：`C:\Windows\win.ini`、`C:\Users\ASUS\Documents\secret.txt`、`F:\not-under-workspace\x.txt` 均被 `LOCAL_FILE_PATH_DENIED` 拒绝。
- `mc-design-nx`: `python -m pytest client/tests/test_tool_registry.py -q`
- 结果：12 passed。

已解除阻塞：

1. `export_assets.py` 当前已支持优先打包 `agents/*/runtime.md`，并兼容回退 `beya.md`。
2. `client/tests/test_asset_store.py` 已覆盖 `runtime.md` 打包和 `runtime.md` 优先、`beya.md` 回退逻辑。
3. 该修复未见独立 ASSET-001 回执，暂记为当前工作树中已解除的阻塞，需要后续在 RT-001 或单独回执中归属。

剩余风险：

1. 当前工作树混有运行时替换相关改动，后续验收需注意按任务隔离变更范围，避免把 NX-005 与 RT-001 的问题混在一起。
2. ASSET-001 阻塞虽已解除，但缺少正式回执，后续需要执行方补充归属说明。

### 2026-06-14：SK-001 零部件 Skill 硬编码审计

验收结论：未通过，需退回补交审计结果。

检查结果：

1. 未找到明确命名为 `SK-001` 的审计交付文件。
2. 当前新增/可见交付物为 `.tasks/SK-002_part_rules_schema_design.md`，内容是零部件规则包 schema 与加载方案草案，更接近 SK-002，而不是 SK-001 审计。
3. 该方案文件包含规则包目录、schema、conrod/piston_pin/thrust_washer 示例轮廓、加载流程、测试策略和 SK-003 草案，对后续有参考价值。
4. 但缺少 SK-001 明确要求的逐文件审计清单、硬编码点清单、P0/P1/P2 风险分级、每个硬编码点的“保留/迁出”判定和迁移优先级。
5. 未看到对 `part-design`、`logic-expression-design`、`conrod-design`、`parameter-mapping`、`nx-parameter`、`teamcenter-flow` 等文件逐项覆盖的审计证据。

退回补交要求：

1. 补交 `SK-001` 审计结果，不要求改代码。
2. 输出必须包含：审计文件清单、硬编码点清单、P0/P1/P2 风险分级、应保留在 skill 的内容、应迁出到规则包的内容、建议试点迁移零件和原因。
3. 允许引用 `.tasks/SK-002_part_rules_schema_design.md` 作为后续方案参考，但不能用它替代 SK-001 审计台账。
4. 当前不建议派发 SK-003，待 SK-001 补交且 SK-002 方案通过后再派发。

### 2026-06-14：RT-001 mc-design 一次性替换 beya -> tjuae

验收结论：按旧规则可判定为“阶段通过”，但不能判定为全通路最终通过。

检查结果：

1. `mc-design-nx` 活动源码路径中未再检出有效 `beya` 运行时关键词，原本的本地 `beya-server.exe`、`beya_server.py`、`runtime/beya_server_adapter.py`、`beya-sdk-python` 依赖和相关测试已被删除或替换。
2. 新增 `tjuae` 侧运行时组件，包括 `tjuae_server.py`、`runtime/tjuae_runtime_adapter.py`、`runtime.md`、`tjuae-client-core.zh.md`、`README_TJUAE_RUNTIME.md` 和对应测试。
3. `host.py` 已切换到 `McDesignTjuaeAdapter`，运行时状态暴露为 `runtime=tjuae-sdk-adapter`、`backend=tjuae_server_sdk`。
4. Windows 打包脚本已调整为接收 `tjuae` SDK Python 包和 `tjuae` server 包，不再以 beya server 作为本地运行时 payload。
5. `export_assets.py` 已支持 `runtime.md` 优先、`beya.md` 兼容回退，解决了原资产命名对 beya 的硬绑定。
6. 由于该任务按旧规则完成，没有固定回执；本次验收基于代码检查和测试结果倒推。后续同类任务必须提供回执。

验收证据：

- `mc-design-nx`: `python -m pytest client/tests/test_tjuae_runtime_adapter.py client/tests/test_local_tjuae_server.py client/tests/test_client_static.py client/tests/test_windows_payload_builder.py client/tests/test_windows_installer_build.py -q`
- 结果：79 passed。
- `mc-design-nx`: `python -m pytest client/tests/test_tool_registry.py client/tests/test_asset_store.py client/tests/test_design_skill_contract.py -q`
- 结果：31 passed。
- `mc-design-ai-service`: `python -m pytest tests/test_runtime_bridge_architecture.py tests/test_bridge_contract.py tests/test_usage_issue_fixes.py -q`
- 结果：55 passed，1 个 StarletteDeprecationWarning。
- `mc-design-nx` 活动源码扫描：`rg -n "beya|Beya|beya_mcp|beya\.toml|beya-server|beya_sdk|BeyaApiKey" mc-design-nx\assets\source mc-design-nx\client\src mc-design-nx\client\tests mc-design-nx\configure mc-design-nx\package\windows mc-design-nx\client-launcher`
- 结果：无命中。

剩余风险：

1. `mc-design-ai-service` 仍保留 `beya_mcp` 包名、`beya.toml` 配置名、`BeyaApiKeyMiddleware` 和多处 Beya 文档描述。当前测试仍基于这些旧命名通过，说明云端桥接层没有完成命名中性化或迁移策略落地。
2. `mc-design-ai-service/tools/business/*/TOOL.md` 和部分 tool schema 描述仍写着 “Beya SDK/插件/工作区”等旧概念，后续需要单独清理为 Runtime/Tjuae/connector catalog 中性表述。
3. 当前本地测试使用模拟或单元场景，尚未使用真实 `F:\Documents\tjuae\dist\tjuae-sdk` 产物完成正式 Windows payload 构建验收。
4. 全通路测试尚未执行。若涉及 `mc-design-ai-service` 更新，测试前必须由项目负责人手动更新 K8s；本地不能直接调用 MCP Stream Tool，应从本地 `mc-design-client` 的 `POST /api/runtime/test/agent-turn` 进入；NX 和目标模型也需要人工前置处理。
5. 工作树混有 RT-001、NX-005、S0-2、ASSET-001 等多任务改动，后续合并前必须按任务拆分归属和证据。

后续处理：

1. RT-001 可以进入“全通路测试准备”阶段，不建议退回重做。
2. 新增一个独立后续任务：`RT-002`，负责 `mc-design-ai-service` 运行时命名中性化、connector 文档去旧化、`stream_agent_turn(...)` 测试入口和真实 tjuae 产物打包验收准备。
3. 在 RT-002 通过前，不把 RT-001 记为最终完成，只记为本地替换阶段通过。

### 2026-06-14：SK-001R 零部件 Skill 硬编码审计补交

验收结论：通过，可进入 SK-002 正式评审，但不直接派发 SK-003。

已完成：

1. 审计覆盖 `part-design`、`logic-expression-design`、`conrod-design`、`parameter-mapping`、`nx-parameter`、`teamcenter-flow`、`design-report` 和 4 份参考 Excel/问题表资料。
2. 形成 56 个硬编码点清单，包含 P0/P1/P2 风险分级。
3. 明确区分应保留在 skill 的通用流程、应迁出到零部件规则包的知识规则、应迁出到测试 fixture 的样例/缺陷资料。
4. 建议试点迁移零件为连杆，活塞销作为第二候选，止推片放到复杂规则验证阶段。

验收证据：

- 回执：`.tasks/receipts/SK-001R/AUDIT_RECEIPT.md`。

剩余风险：

1. SK-001R 只是审计，不含代码迁移。
2. SK-002 方案需要结合 SK-001R 审计结果重新评审；不能直接跳到 SK-003。

### 2026-06-14：S0-4 TC/NX 模型生命周期规则加固

验收结论：通过，可进入实机/联调回归。

已完成：

1. `part-design`、`teamcenter-flow`、`nx-operation`、`nx-parameter`、`tool.nx` 补充任务确认 -> 模板/模型确认 -> 三维模型打开/修改 -> 参数校验 -> 保存/更新 -> 二维图/报告状态机。
2. 明确未完成三维模型修改前，不允许自行打开二维图纸。
3. 明确 TC 上传物清单必须包含三维模型、二维图纸、报告；缺失项需说明原因并等待用户确认。
4. 新增生命周期、二维图门禁、上传物清单、模型确认门禁相关契约测试。

验收证据：

- 回执：`.tasks/receipts/S0-4/EXECUTION_RECEIPT.md`。
- `mc-design-nx`: `python -m pytest client/tests/test_design_skill_contract.py -q`
- 结果：18 passed。

剩余风险：

1. 未执行真实 `nx_open_tcpart`、二维图打开、自动出图、保存/更新和 TC 上传。
2. 实机验证需要项目负责人手动启动 NX；当前网络环境下 `nx_open_tcpart` 不可用时需要手动打开目标模型。

### 2026-06-14：S0-6 问题表验收矩阵

验收结论：通过，后续验收主台账以该矩阵为基础。

已完成：

1. 只读读取 `零件设计智能体试用问题跟踪表.xlsx`，未修改原始 Excel。
2. 纳入 59 条问题类记录，其中主表 54 条、部署问题 4 条、报告说明书填写疑问 1 条。
3. 标注 35 条 P0、13 条 P1、11 条 P2。
4. 输出 2026-06-18 前必须项、已解决待回归项、外部依赖/阻塞项、二期项。

验收证据：

- 回执：`.tasks/receipts/S0-6/EXECUTION_RECEIPT.md`。
- 矩阵：`.tasks/receipts/S0-6/ACCEPTANCE_MATRIX.csv`。
- 矩阵：`.tasks/receipts/S0-6/ACCEPTANCE_MATRIX.md`。

剩余风险：

1. 矩阵是验收台账，不代表问题已修复。
2. 已解决/已完成/已优化项仍需在当前运行时和全通路条件下回归。

### 2026-06-14：RT-002 运行时替换收口

验收结论：阶段通过，但仍不是全通路终验。

已完成：

1. AI Service connector 文档和工具描述去除用户可见 Beya 表述，改为 Runtime/connector catalog 等中性表述。
2. 明确兼容保留 `beya_mcp`、`beya.toml`、`BeyaApiKeyMiddleware`、`BEYA_*` 配置项，不做破坏性重命名。
3. 新增认证 HTTP test endpoint：`POST /api/mc-design/test/agent-turn`，作为后续基于 `stream_agent_turn(...)` 的全通路测试入口。
4. Windows 打包支持 `--tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk` 形式的真实 tjuae dist root。
5. 文档补充 K8s 手动更新、VPN、NX 启动、手动打开目标模型等全通路人工前置条件。

验收证据：

- 回执：`.tasks/receipts/RT-002/EXECUTION_RECEIPT.md`。
- `mc-design-ai-service`: `python -m pytest -q`
- 结果：72 passed，3 warnings。
- `mc-design-nx`: `python package/windows/build/scripts/build_installer.py --dry-run --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk`
- 结果：ok=true，wheel 和 server executable 均从真实 dist root 解析成功。

剩余风险：

1. K8s 未更新，必须由项目负责人在全通路测试前手动处理。
2. VPN/NX/目标模型打开等人工前置条件未执行。
3. `beya_mcp`、`beya.toml`、`BEYA_*` 仍作为兼容面保留，后续如要彻底重命名需单独计划。
4. 当前资产打包仍被 NX 图纸口径不一致阻塞，需修正旧测试/说明仍要求 `nx-auto-drawing` 存在的问题。
5. 项目负责人最新明确：`test_agent_turn` 应放在本地客户端，不应进入 K8s AI Service。RT-002 中新增的 K8s `/api/mc-design/test/agent-turn` 方向需要回退或移除，并改由本地 `mc-design-client` 提供测试入口。

### 2026-06-14：RT-003 本地 test_agent_turn 与 K8s connector/MySQL 修整

验收结论：阶段通过；后续 `K8S-SMOKE-001` 已验证 K8s readiness、connector catalog 和 MySQL smoke 可用，但仍不是全通路终验。

已完成：

1. 本地 `mc-design-client` 提供 `POST /api/runtime/test/agent-turn`，内部走 `ClientApp.test_agent_turn(...)` -> `RuntimeHost.run(...)`。
2. K8s AI Service 移除 `POST /api/mc-design/test/agent-turn`、`POST /mc-design/ai-server/api/mc-design/test/agent-turn` 和 discovery 中的 `test_agent_turn` 字段。
3. 本地 connector 转发到 K8s `/mc-design/ai-server/api/mc-design/connectors/execute` 的前缀推导已修正，避免重复拼接或漏拼。
4. MySQL connector 错误拆分为 `MYSQL_CONFIG_MISSING`、`MYSQL_DEPENDENCY_MISSING`、`MYSQL_CONNECT_FAILED`、`MYSQL_QUERY_FAILED` 等结构化错误；readiness 不泄露密码。

验收证据：

- 回执：`.tasks/receipts/RT-003/EXECUTION_RECEIPT.md`。
- `mc-design-nx`: `python -m pytest mc-design-nx/client/tests/test_usage_issue_fixes.py mc-design-nx/client/tests/test_client_static.py -q`
- 结果：49 passed。
- `mc-design-ai-service`: `python -m pytest mc-design-ai-service/tests/test_runtime_bridge_architecture.py mc-design-ai-service/tests/test_bridge_contract.py mc-design-ai-service/tests/test_mysql_connector_errors.py mc-design-ai-service/tests/test_runtime_replacement_policy.py -q`
- 结果：56 passed，1 warning。

后续状态：

1. 项目负责人已完成 K8s 部署，`K8S-SMOKE-001` 已通过。
2. K8s 返回 `/api/mc-design/test/agent-turn` 404 是符合新规则的正确行为，因为该测试入口已迁移到本地 `mc-design-client`。
3. 原独立本地 `POST /api/runtime/test/agent-turn` smoke 候选任务已撤回冻结；当前本地入口验证被纳入 `E2E-SMOKE-002`。

### 2026-06-14：K8S-SMOKE-001 K8s 部署后 smoke test

验收结论：通过。该任务只证明 K8s 部署后的基础服务和 connector 可用，不等同于本地 agent-turn 或完整多智能体链路通过。

已完成：

1. `/api/readiness` 返回 200，router/connectors/mysql 状态正常。
2. `/api/mc-design/connectors/tools` 返回 connector catalog，包含 `mysql_query`、`query_ipm_list`、`query_ecr_list`、`connect_qpp`、`tc_call`。
3. `/api/mc-design/connectors/execute` 执行 `mysql_query` 的 `select 1` 成功，返回 `query_result` 为 `[{"1":1}]`。
4. K8s 旧接口 `/api/mc-design/test/agent-turn` 返回 404，符合 `RT-003` 新规则。

验收证据：

- 回执：`.tasks/receipts/K8S-SMOKE-001/EXECUTION_RECEIPT.md`。

当前状态：

1. 不再要求用户重复重启 K8s。
2. 原独立本地 `agent-turn` smoke 和后续问题表全量回归候选任务已撤回冻结；当前本地入口验证被纳入 `E2E-SMOKE-002`。
3. 如重新启动测试工作，必须检查的是 `mc-design-client` 本地端口和 `POST /api/runtime/test/agent-turn`，不是 K8s 旧路径。

### 2026-06-14：NX-DRAW-001 NX 图纸规则收口

验收结论：通过。该任务关闭 `ASSET-001R`、`S0-5`、`DFMEA-001` 中由旧自动出图口径引起的阻塞。

已完成：

1. `nx-auto-drawing` 已从 source/runtime/windows payload 中移除或禁用。
2. NX manifest 和客户端 registry 不再暴露自动出图和 sheet 级图纸工具。
3. NX 图纸操作口径统一为只通过 `nx_open_tcpart` 打开已绑定图纸；图纸与数模绑定后的自动更新视为自动出图结果。
4. `design-report`、`nx-operation`、`dfmea-risk-review` 等 skill/资产文案已按新规则收口。

验收证据：

- 回执：`.tasks/receipts/NX-DRAW-001/EXECUTION_RECEIPT.md`。
- `mc-design-nx`: `python -m pytest client/tests/test_design_skill_contract.py client/tests/test_asset_store.py client/tests/test_windows_payload_builder.py client/tests/test_tool_registry.py -q`
- 结果：43 passed。
- `mc-design-nx`: `python -m pytest client/tests/test_agent_loop_assets.py -q`
- 结果：2 passed。

剩余风险：

1. 这不是 NX/TC 实机出图验收；真实图纸打开、模型绑定更新、截图和报告仍要进入全通路回归。

### 2026-06-14：E2E-SMOKE-001 安装包级通路 smoke

验收结论：正式回执为环境阻塞。后续人工恢复验证只能作为监管补充，不能改写原任务结论。

已完成：

1. 构建 `McDesignClientSetup-E2E-SMOKE-001.zip` 成功。
2. 旧客户端卸载失败，失败点是历史/残缺安装目录缺少新布局 `installer\tools\install_helper.mcpy`，新包卸载脚本无法识别旧根目录 `install_helper.py`。
3. 任务按规则停止，未进入正式新安装、客户端启动、K8s smoke 和本地 agent-turn smoke。

后续人工恢复记录：

1. 使用旧安装目录自带旧版 `uninstall.bat` 成功清理历史安装目录。
2. 安装 `E2E-SMOKE-001` 后，本地 `/health`、K8s smoke 和本地 `POST /api/runtime/test/agent-turn` 健康检查通过。
3. 本机配置已改为测试身份 `user_id = "88000044"`、`user_name = "宋明芮"`，回执和台账只记录 `tc_key_configured=true`，不记录密码明文。

验收证据：

- 回执：`.tasks/receipts/E2E-SMOKE-001/EXECUTION_RECEIPT.md`。
- 监管补充记录：`.tasks/project_health_2026-06-14.md`。

### 2026-06-14：PKG-001 客户端安装包加固

验收结论：通过。该任务处理 `E2E-SMOKE-001` 暴露的旧/残缺安装目录卸载阻塞，但不等同于 E2E 通路已通过。

已完成：

1. 加固 Windows 安装包安装、卸载、升级前清理和构建后 zip 自检。
2. 支持识别 current-layout、legacy-layout、broken-layout、foreign-dir 等安装目录状态。
3. 卸载 helper 支持 new-layout、legacy-root 和 package-helper fallback，无法安全判断时拒绝手工清理。
4. 加固 NX `custom_dirs.dat` 清理和进程处理策略。

验收证据：

- 回执：`.tasks/receipts/PKG-001/EXECUTION_RECEIPT.md`。
- `mc-design-nx`: `python -m pytest client\tests\test_windows_installer_build.py -q`
- 结果：21 passed。
- 构建产物：`mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-001.zip`。

当前状态：

1. `E2E-SMOKE-002` 已证明 `PKG-001` 安装包在真实卸载链路上仍不通过，需要继续加固安装目录识别和卸载策略。

### 2026-06-14：PKG-002 客户端卸载/安装链路继续加固

验收结论：通过，允许进入真实 E2E 复测。该任务不等同于全通路通过。

已完成：

1. 复盘 `E2E-SMOKE-002` 的失败根因：真实安装目录只剩 `client/`、`configure/`、`uninstall.bat`，其中 `uninstall.bat` 带有 McDesign 卸载标记，但 `PKG-001` 未把该标记作为 McDesign 证据，导致目录被误判为 `foreign-dir`。
2. 新增 `package-helper-fallback-layout` 分类，覆盖 `client/ + configure/mc-design-client.config + 带 McDesign 标记 uninstall.bat` 的残留形态。
3. 保留安全边界：普通 lookalike 目录仍判为 `foreign-dir` 并拒绝删除。
4. 加固日志输出，增加 `Install directory evidence` 和 `Install directory refusal reason`。
5. 修正 `remove_install_dir` 兜底进程清理过宽的问题，避免按“命令行包含目标目录”误杀卸载进程自身。

验收证据：

- 回执：`.tasks/receipts/PKG-002/EXECUTION_RECEIPT.md`。
- 安装包：`mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-002.zip`。
- 包内自检：`.tasks/receipts/PKG-002/package-helper-selfcheck-final.log`，`selfcheck_exit_code=0`，目录类型为 `package-helper-fallback-layout`。
- 复跑测试：`python -m pytest mc-design-nx\client\tests\test_windows_installer_build.py -q`，结果 25 passed。
- 语法检查：`python -m py_compile mc-design-nx\package\windows\build\scripts\build_installer.py`，通过。

当前状态：

1. `E2E-SMOKE-003` 已完成复测：卸载/安装通过，但正式 `McDesignClient.exe` 启动失败，严格不通过。
2. `CLIENT-LEGACY-001` 已完成；`CLIENT-DATA-001`、`CLIENT-TJUAE-001`、`CLIENT-PKG-OUTPUT-001` 仍作为候选保留，但当前先处理 launcher 启动阻塞，不继续叠加目录治理任务。

### 2026-06-14：E2E-SMOKE-002 安装包级通路复测

当前状态：已完成，不通过。

任务定位：

1. 使用 `McDesignClientSetup-PKG-001.zip` 复测客户端卸载、安装、启动、健康检查、K8s smoke 和本地 `POST /api/runtime/test/agent-turn`。
2. 回执目录应为 `.tasks/receipts/E2E-SMOKE-002/`。
3. 因卸载失败按规则停止，未进入安装、启动、本地 agent-turn 或 K8s smoke。

执行结果：

1. 正式回执结论：不通过，客户端卸载链路失败。
2. 初始检测到本地客户端进程，并已通过 `POST http://127.0.0.1:8765/api/runtime/shutdown` 正常关闭，关闭后无客户端相关残留进程。
3. `McDesignClientSetup-PKG-001.zip` 解压后关键文件齐全，包括 `install.bat`、`uninstall.bat`、`installer\tools\install_helper.mcpy`、`payload\McDesignClient.exe`、`payload\client\app\mc_design_client.pyz`、`payload\client\python\python.exe`。
4. 执行 `uninstall.bat C:\Users\ASUS\AppData\Local\McDesign` 退出码为 9。
5. 卸载日志显示 `Uninstall path: package-helper-fallback`、`Install directory state: foreign-dir`、`Refusing unsafe manual cleanup for a non-mc-design directory`。
6. 安装目录卸载后仍存在，剩余顶层项包括 `client/`、`configure/`、`uninstall.bat`。
7. 未执行安装、启动、`/health`、`/api/status`、K8s connector smoke、本地 `POST /api/runtime/test/agent-turn`。

验收证据：

- 回执：`.tasks/receipts/E2E-SMOKE-002/EXECUTION_RECEIPT.md`。
- 日志：`.tasks/receipts/E2E-SMOKE-002/uninstall-output.log`。

### 2026-06-14：CLIENT-ARCH-001 mc-design-client 架构边界审计

验收结论：通过。该任务只完成架构边界审计和清理建议，不代表已经执行目录迁移、删除 legacy 资产或修复安装包问题。

已完成：

1. 明确当前资产链路：`mc-design-nx/assets/source/` 是源；`mc-design-nx/client/resources/agent_assets.mcdpkg` 是打包快照；`mc-design-nx/client/data/asset_views/runtime-agentloop/` 是运行时投影缓存；`mc-design-nx/client/data/workspace/.tjuae/skills/` 是给 tjuae server 发现的 skills 工作区。
2. 明确 `tjuae-sdk` 不直接读取 `.mcdpkg` 或 `asset_views`；它通过 sessions、plugins、tools、chat 等 SDK/server API 工作，实际被 tjuae server 发现的是 `.tjuae/skills`。
3. 判定 `cc_haha_agent_runtime_migration_pack` 是外部 cc-haha/Claude Code 风格运行时迁移参考残留，当前源码、测试、打包任务没有实际依赖。
4. 识别 `mc-design-client` “怪”的主要原因：源码、生成资源、运行时 data、`.tjuae`、旧 `.beya`、旧 asset_views、cc_haha 迁移参考包和 Windows package output 混在同一树下，增加审计和误删风险。
5. 给出分阶段建议：先做资产链路自检与文档固化，再做 runtime data root 治理、`.tjuae` managed/user skill 分离、legacy 清理、package output 保留策略。

验收证据：

- 回执：`.tasks/receipts/CLIENT-ARCH-001/AUDIT_RECEIPT.md`。
- 架构图：`.tasks/receipts/CLIENT-ARCH-001/CLIENT_ARCHITECTURE_MAP.md`。
- 清理候选：`.tasks/receipts/CLIENT-ARCH-001/CLIENT_CLEANUP_CANDIDATES.csv`。
- 重构建议：`.tasks/receipts/CLIENT-ARCH-001/CLIENT_RESTRUCTURE_PROPOSAL.md`。

当前处理策略：

1. `CLIENT-ASSET-001` 已完成，只读资产链路自检和文档固化通过。
2. `CLIENT-LEGACY-001` 已完成，legacy 归档清理通过。
3. `CLIENT-DATA-001`、`CLIENT-TJUAE-001`、`CLIENT-PKG-OUTPUT-001` 作为候选保留，等 launcher 启动阻塞处理后再排。

### 2026-06-14：CLIENT-ASSET-001 客户端资产链路自检与文档固化

验收结论：通过。该任务完成资产链路只读自检、文档固化和测试补强，未删除或迁移任何 legacy 目录。

已完成：

1. 新增 `mc_design_client.assets.inspect_asset_chain(...)`，用于只读检查 source/package/projection/workspace skills 链路。
2. `mc_design_client.cli doctor` 新增 `checks.asset_chain`，可输出 asset chain、bundle version、sha256、一致性状态和 legacy 候选。
3. 文档 `mc-design-nx/client/README_TJUAE_RUNTIME.md` 补充 asset、asset_view、`.tjuae/skills`、tjuae SDK/server 和 `cc_haha` 边界。
4. 确认当前链路为 `assets/source -> client/resources/agent_assets.mcdpkg -> client/data/asset_views/runtime-agentloop -> client/data/workspace/.tjuae/skills`。
5. 确认 `tjuae-sdk` 不直接读取 `.mcdpkg` 或 `asset_views`；tjuae server 实际通过 workspace 下 `.tjuae/skills` 发现项目 skills。
6. legacy 候选 `runtime-live`、`test-local-dev`、`.beya`、`cc_haha_agent_runtime_migration_pack`、`governance` 均只报告为 `report_only`，未删除。

验收证据：

- 回执：`.tasks/receipts/CLIENT-ASSET-001/EXECUTION_RECEIPT.md`。
- 复跑测试：`python -m pytest mc-design-nx\client\tests\test_asset_store.py mc-design-nx\client\tests\test_agent_loop_assets.py mc-design-nx\client\tests\test_tjuae_runtime_adapter.py -q`，结果 29 passed。
- 诊断入口：`python -m mc_design_client.cli --root mc-design-nx\client doctor`，`checks.asset_chain.ok=true`。

当前处理策略：

1. `CLIENT-LEGACY-001` 已完成归档式清理。
2. 暂不派发 `CLIENT-DATA-001` 或 `CLIENT-TJUAE-001`，先处理 `E2E-SMOKE-003` 暴露的正式入口启动失败。

### 2026-06-14：CLIENT-LEGACY-001 客户端 legacy 归档清理

验收结论：通过。该任务按要求先 manifest、后归档/迁移、再从活跃目录移除，没有硬删未归档内容。

已完成：

1. 生成 `LEGACY_MANIFEST_BEFORE.json` 和 `LEGACY_MANIFEST_AFTER.json`。
2. 将 `runtime-live`、`test-local-dev`、`.beya`、`governance` 归档到 `.tasks/archives/CLIENT-LEGACY-001/` 后从活跃 `mc-design-nx/client` 目录移除。
3. 将 `cc_haha_agent_runtime_migration_pack` 移到 `references/legacy-runtime/cc-haha/cc_haha_agent_runtime_migration_pack`。
4. 新增 `references/legacy-runtime/cc-haha/README.md`，说明该目录只是外部运行时迁移参考，不是 mc-design-client runtime 依赖。
5. 更新诊断逻辑，使 legacy candidate 缺失时稳定返回 `action=absent`，而不是报错。
6. 当前实时 `doctor.checks.asset_chain.ok=true`，当前运行链路仍为 `runtime-agentloop -> workspace/.tjuae/skills`。

验收证据：

- 回执：`.tasks/receipts/CLIENT-LEGACY-001/EXECUTION_RECEIPT.md`。
- 归档前 manifest：`.tasks/receipts/CLIENT-LEGACY-001/LEGACY_MANIFEST_BEFORE.json`。
- 归档后 manifest：`.tasks/receipts/CLIENT-LEGACY-001/LEGACY_MANIFEST_AFTER.json`。
- doctor 证据：`.tasks/receipts/CLIENT-LEGACY-001/DOCTOR_RESULT.json`。
- 归档目录：`.tasks/archives/CLIENT-LEGACY-001/`。
- 参考归档：`references/legacy-runtime/cc-haha/`。
- 复跑测试：`python -m pytest mc-design-nx\client\tests\test_asset_store.py mc-design-nx\client\tests\test_agent_loop_assets.py mc-design-nx\client\tests\test_tjuae_runtime_adapter.py -q`，结果 30 passed。

当前状态：

1. 客户端活跃目录中的 legacy 运行残留已完成降噪。
2. `CLIENT-DATA-001`、`CLIENT-TJUAE-001`、`CLIENT-PKG-OUTPUT-001` 具备后续排期条件。
3. 当前不继续叠加派发目录治理任务，先处理 `E2E-SMOKE-003` 暴露的正式 launcher 启动阻塞。

### 2026-06-14：CLIENT-ACTIVE-ROOT-001 根安装 payload 收口与工具执行映射

验收结论：有条件通过。核心目标已完成，`AUDIT-ST-010` 和 `AUDIT-ST-011` 可关闭；保留项是根 `client/configure/mc-design-client.config` 含本机 `tc_key`，不能由执行智能体擅自复制、归档或删除，需要项目负责人确认迁移/删除策略。

已完成：

1. 判定仓库根 `client/` 为安装后的 Windows payload 与运行数据形态，不是源码入口；源码入口仍是 `mc-design-nx/client/`。
2. 归档根 `client/` 中 536 个非敏感 payload 文件到 `.tasks/archives/CLIENT-ACTIVE-ROOT-001/client/`，总大小 272255160 bytes。
3. 根 `client/` 当前仅剩 `client/configure/mc-design-client.config`，大小 249 bytes；回执记录 `tc_key_configured=true`，未输出明文密钥。
4. 根 `.gitignore` 新增 `/client/`，README 明确根 `client/` 不是源码、测试、资产或打包入口。
5. 新增 `mc-design-nx/client/resources/tool_execution_map.json`，明确 `tool.local_file`、`tool.dfmea`、`tool.nx` 的 TOOL.md、Python provider、`ClientToolCatalog`、本地 HTTP executor 和 Tjuae namespace 映射。
6. 修复本地工具投影到 Tjuae inline plugin 的 namespace：`tool.local_file`、`tool.dfmea`、`tool.nx` 不再统一落为 `local`。
7. `NxToolProvider` 显式标记 `tool_group="tool.nx"`，并继续过滤禁用自动出图/Sheet 级图纸工具。
8. 新增/增强 `test_tool_registry.py` 覆盖工具映射、TOOL.md 声明、HTTP namespace alias、Tjuae executor namespace、根 payload 非源码入口。

验收证据：

- 回执：`.tasks/receipts/CLIENT-ACTIVE-ROOT-001/EXECUTION_RECEIPT.md`。
- 归档前 manifest：`.tasks/receipts/CLIENT-ACTIVE-ROOT-001/ROOT_CLIENT_MANIFEST_BEFORE.json`，记录根 `client/` 537 files、旧运行痕迹 248、敏感指示项 2。
- 归档后 manifest：`.tasks/receipts/CLIENT-ACTIVE-ROOT-001/ROOT_CLIENT_MANIFEST_AFTER.json`，记录 active_file_count_after=1、archive_file_count=536、no_secret_values_in_manifest=true。
- 归档目录：`.tasks/archives/CLIENT-ACTIVE-ROOT-001/client/`。
- 工具映射：`mc-design-nx/client/resources/tool_execution_map.json`。
- 复跑测试：`python -m pytest mc-design-nx\client\tests\test_tool_registry.py mc-design-nx\client\tests\test_asset_store.py mc-design-nx\client\tests\test_agent_loop_assets.py mc-design-nx\client\tests\test_tjuae_runtime_adapter.py -q`，结果 48 passed。

保留风险：

1. 根 `client/configure/mc-design-client.config` 仍在，需项目负责人确认是否迁移到正式安装配置、保留或删除。
2. 顶层工作树还显示 `.install-backup/` 与 `.tmp-runtime-check/` 删除记录；该内容不在 `CLIENT-ACTIVE-ROOT-001` 回执和 manifest 范围内，提交前需单独确认，不纳入本任务通过结论。

### 2026-06-14：BIZ-ADAPTER-001 业务适配工具层

验收结论：通过，阶段关闭 `AUDIT-ST-012`、`AUDIT-ST-013`、`AUDIT-ST-014`。

已完成：

1. 新增 Python 客户端本地工具组 `tool.design_flow`。
2. 工具覆盖 `design_task_normalize`、`design_task_select`、`design_input_classify`、`design_parameter_prepare`、`design_modeling_plan_build`。
3. 将 IPM/ECMS/QPP 或用户输入统一成 `task_candidates`，用户选择后生成并保持 `selected_task_context`。
4. 将设计参数、边界参数、模板参数、驱动参数、关联参数落成结构化分类，并输出参数齐全、参数不全/无参数、仅边界参数、混合参数四类分支。
5. `design_modeling_plan_build` 只生成 NX 写入前计划，不直接调用 NX；中文参数名、模板字段名和不安全表达式名不能进入 NX 写入计划。
6. 修复 `tool.local_file`、`tool.dfmea`、`tool.nx`、`tool.design_flow` 进入 tjuae inline plugin 后的 executor namespace 映射。

验收证据：

- 回执：`.tasks/receipts/BIZ-ADAPTER-001/EXECUTION_RECEIPT.md`。
- 复跑测试：`python -m pytest client\tests\test_design_flow_tools.py client\tests\test_tool_registry.py client\tests\test_tjuae_runtime_adapter.py client\tests\test_design_skill_contract.py client\tests\test_dfmea_tools.py client\tests\test_usage_issue_fixes.py -q`，结果 83 passed。

剩余风险：

1. 本任务证明工具和 skill 契约存在并通过单测，不证明真实 agent-turn 一定会稳定调用 `tool.design_flow`。
2. QPP 当前外部不通仍按外部接口不可用处理，不是本任务要修复的 mc-design 代码问题。

### 2026-06-14：NX-TOOL-HARDEN-001 NX/工具 API 加固

验收结论：通过，阶段关闭 `AUDIT-ST-015`、`AUDIT-ST-016`。

已完成：

1. NX plugin 工具 DLL 加载收敛到 allowlist，当前只加载 `NXTools.dll`。
2. 自动出图和 Sheet 级图纸工具在 ToolManager、manifest、客户端 registry 和 `tool.nx` 说明中继续禁用；唯一允许的 NX 图纸入口仍是 `nx_open_tcpart`。
3. `NXResult` 增加 `code`、`retryable`、`details` 结构化错误字段。
4. NX plugin HTTP server 补齐 header/body 限制、坏 JSON、非 object JSON、非法 Content-Length、超大 body、非 POST、并发 busy 等错误码。
5. 本地客户端 `/api/runtime/tools/execute` 补齐坏 JSON、超大 body、非 object JSON 的 400/413 分类。
6. NX 文件/图片工具增加路径和扩展名边界；`GetWorkPartInfo` 新增 `part_name` 并保留兼容字段 `part_nane`。

验收证据：

- 回执：`.tasks/receipts/NX-TOOL-HARDEN-001/EXECUTION_RECEIPT.md`。
- Python 静态编译检查通过。
- 相关客户端测试已纳入本轮 83 passed。

剩余风险：

1. 未运行 NX 实机编译、NX plugin 加载或真实会话调用。
2. 后续进入 NX 实机测试时，需要项目负责人启动 NX 并确保 NX plugin 8088 可监听。

### 2026-06-14：E2E-SMOKE-003 安装包级 smoke 复测

验收结论：不通过。阻塞分类从 `CLIENT_UNINSTALL_FAILED` 转为 `CLIENT_START_FAILED`。

已完成并通过的部分：

1. 使用 `PKG-002` 安装包卸载旧客户端成功，不再出现 `foreign-dir` 误判。
2. 新安装成功，关键文件存在。
3. 诊断入口 `start-client.bat` 可启动同一套 Python runtime。
4. local `/health`、`/api/status`、本地 `POST /api/runtime/test/agent-turn` 重试通过。
5. K8s readiness、connector catalog、`mysql_query select 1`、IPM page1、ECR page 检查通过。
6. K8s 旧 `/api/mc-design/test/agent-turn` 返回 404，符合当前规则。

失败点：

1. 正式入口 `C:\Users\ASUS\AppData\Local\McDesign\McDesignClient.exe` 未在超时内拉起 8765。
2. 未生成足够 launcher 日志，定位信息不足。
3. 重装后 `tc_key_configured=false`，后续 TC/NX 测试前需要处理本机配置。

验收证据：

- 回执：`.tasks/receipts/E2E-SMOKE-003/EXECUTION_RECEIPT.md`。
- 关键证据：`client-start-result.json`、`local-health-status.json`、`local-agent-turn-response-retry.json`、`k8s-smoke-result.json`。

### 2026-06-14：REG-P0-FULL-001 P0 试跑

验收结论：不通过。

结果总览：

1. 覆盖 35 行问题表记录。
2. 通过 11 条、失败 17 条、阻塞 7 条。
3. K8s connector 只读链路可用，包含 readiness、catalog、MySQL、IPM 默认/分页/三个月到期/五次一致性、ECR 分页；QPP 仍为外部超时。
4. 本地 agent-turn 基础入口可用，但 IPM connector 未集成到本地 agent-turn 可用工具面；两轮任务选择未闭环。
5. 参数四分支均为 `BUSINESS_ASSERTION_FAILED`：transport 成功，但参考公式、缺参精准性、确定值输出和真实 NX 参数 ID 校验均未达标。
6. 报告 prepare/preview/save/read 通过；DFMEA 在补齐模板资产后第二版通过。
7. NX 截图导出失败；TC/NX 生命周期因 `tc_key_configured=false`、未打开 TC 绑定模型/图纸、未完成三维修改而阻塞。
8. 安装包门禁中卸载日志出现 helper 已输出成功但 bat 报 `The batch file cannot be found.`，回执保留 `CLIENT_UNINSTALL_FAILED` 分类；这与 `E2E-SMOKE-003` 的卸载通过结论需要后续合并排查。

验收证据：

- 回执：`.tasks/receipts/REG-P0-FULL-001/EXECUTION_RECEIPT.md`。
- 状态矩阵：`.tasks/receipts/REG-P0-FULL-001/P0_REGRESSION_MATRIX.csv`。
- 汇总：`.tasks/receipts/REG-P0-FULL-001/matrix_status_summary.json`。
- 关键摘要：`ipm_task_selection_context_summary.json`、`parameter_four_branch_summary.json`、`dfmea_v2_standard_keys_summary.json`、`nx_screenshot_captures.json`。

处理决定：

1. `REG-P0-FULL-001` 作为正式试跑记录入账，但不计入问题表完成。
2. 新增 `AUDIT-ST-017`：本地 agent-turn 工具面未暴露 IPM 查询/任务选择能力。
3. 新增 `AUDIT-ST-018`：参数四分支业务断言失败，参考逻辑和真实 NX 参数 ID 未稳定绑定。

### 2026-06-14：REG-EVIDENCE-001 问题表回归证据整理

验收结论：通过，证据准备完成；不代表真实业务回归通过。

已完成：

1. 基于 S0-6 矩阵和 `REG-001-PREP`，整理 35 条 P0 证据卡片。
2. 每条卡片包含问题编号/来源行、问题摘要、预期行为、测试入口、前置条件、人工介入项、通过标准、失败分类和证据清单。
3. 已区分可本地 agent-turn 测、可 K8s connector 测、需 NX 启动、需 TC/NX 手动打开模型、需外部接口。

验收证据：

- 回执：`.tasks/receipts/REG-EVIDENCE-001/EXECUTION_RECEIPT.md`。
- 产物：`.tasks/receipts/REG-EVIDENCE-001/REGRESSION_EVIDENCE_CARDS.md`。
- 产物：`.tasks/receipts/REG-EVIDENCE-001/REGRESSION_EVIDENCE_CARDS.csv`。

### 2026-06-14：SKILL-CONSIST-001 Skill/Tool/Asset 一致性审计

验收结论：通过，新增治理问题已入账。

已完成：

1. 未发现 P0 级运行资产缺失、禁用自动出图工具误暴露或静态 tool 资产缺包问题。
2. 运行资产包无用户可见 Beya 文案；NX manifest 不包含 `nx-auto-drawing`、`nx_run_auto_drawing` 等禁用工具。
3. 发现 1 个 P0、4 个 P1、2 个 P2。
4. 最高风险是零件规则仍硬编码在 skill 中，建议后续任务编号 `SK-003`。
5. P1 问题包括 Teamcenter/Beya 命名不一致、报告模板硬编码连杆、capabilities 不统一、fixture 与 part-rules 重叠。

验收证据：

- 回执：`.tasks/receipts/SKILL-CONSIST-001/AUDIT_RECEIPT.md`。
- 问题清单：`.tasks/receipts/SKILL-CONSIST-001/ISSUE_LIST.csv`。

### 2026-06-14：K8S-CONNECTOR-PRE-001 K8s connector 预回归

验收结论：完成，存在外部接口阻塞；不判定 mc-design 代码失败。

已完成：

1. K8s readiness 通过。
2. connector catalog 返回 12 个工具。
3. `mysql_query select 1` 成功。
4. `query_ipm_list` 默认参数、`query_ipm_list` 分页、`query_ecr_list` 分页均成功。
5. `mysql_query select 1` 连续 5 次一致。
6. `connect_qpp` 使用当天 `StartDate` 与默认 worker 时 QPP 上游超时；项目负责人确认 QPP 当前确实不通，归类为外部接口不可用。

验收证据：

- 回执：`.tasks/receipts/K8S-CONNECTOR-PRE-001/EXECUTION_RECEIPT.md`。
- 结构化结果：`.tasks/receipts/K8S-CONNECTOR-PRE-001/CONNECTOR_PRECHECK_RESULTS.json`。
- 一致性记录：`.tasks/receipts/K8S-CONNECTOR-PRE-001/MYSQL_SELECT_1_CONSISTENCY_5_RUNS.json`。

### 2026-06-14：NX-PRECHECK-001 NX 前置环境预检查

验收结论：完成，存在环境前置阻塞；不判定代码失败。

已完成：

1. 只执行只读环境检查，未修改模型，未保存模型，未打开二维图纸，未执行自动出图，未调用 `nx_open_tcpart`。
2. 客户端未运行，记录为 `CLIENT_NOT_RUNNING`。
3. NX `ugraf.exe` 已运行，但 `127.0.0.1:8088` 没有 NX plugin HTTP 服务监听，记录为 `NX_PLUGIN_NOT_CONNECTED`。
4. 打包 manifest 中 `nx_open_tcpart` 存在，禁用自动出图工具未暴露。

验收证据：

- 回执：`.tasks/receipts/NX-PRECHECK-001/EXECUTION_RECEIPT.md`。
- 结构化结果：`.tasks/receipts/NX-PRECHECK-001/NX_PRECHECK_RESULTS.json`。

### 2026-06-14：SK-002-REVIEW 规则包方案评审

验收结论：有条件通过。

结论：

1. 原结论允许将 `SK-003` 作为连杆规则包试点候选，但该候选已撤回冻结。
2. 不允许同时批量迁移活塞销、止推片。
3. 不允许修改运行时、NX plugin、K8s 或 tjuae。
4. 后续必须补齐机器可校验 NX mapping、公式证据、fixture schema、默认值/样例边界等缺口。

验收证据：

- 回执：`.tasks/receipts/SK-002-REVIEW/AUDIT_RECEIPT.md`。

### 2026-06-14：REG-001-PREP 问题表全量回归准备

验收结论：通过，准备完成；不代表真实问题已全部测试通过。

已完成：

1. 以 `零件设计智能体试用问题跟踪表.xlsx` 为主台账，整理 59 条问题记录。
2. 输出按参数、IPM/QPP/ECMS、TC/NX 生命周期、报告/二维图、DFMEA、运行时、部署等维度的回归批次。
3. 形成 P0 checklist、证据模板、阻塞分类和人工环境前置条件。

验收证据：

- 回执：`.tasks/receipts/REG-001-PREP/AUDIT_RECEIPT.md`。

当前状态：

1. 原 `REG-001` 真实回归候选已撤回冻结。
2. 如重新派发回归任务，必须区分代码缺陷、K8s 未更新、VPN 未开启、NX 未启动、TC/NX 模型需手动打开、外部接口不可用。

### 2026-06-14：ASSET-001R runtime.md 资产打包归属补审

历史结论：需按最新 NX 图纸规则返工。状态更新：已由 `NX-DRAW-001` 覆盖关闭，以下保留为问题来源记录。

检查结果：

1. 回执明确该修复归属为独立 ASSET-001，不归入 RT-001，这一点可接受。
2. 回执确认 `runtime.md` 优先、`beya.md` legacy fallback 的方向可接受。
3. 项目负责人最新明确：NX plugin 中自动出图插件必须禁用；NX 图纸操作只允许通过 `nx_open_tcpart` 打开 NX 图纸；NX 图纸与 NX 数模绑定后的自动更新已经算作自动出图。
4. 因此 `nx-auto-drawing` 不应再作为必须进入资产包的 skill；旧测试和说明中要求 `nx-auto-drawing` 存在的口径需要改掉。
5. 复验 `test_asset_store.py` 和 `test_windows_payload_builder.py` 失败，原因是旧测试仍要求资产包包含 `nx-auto-drawing`。

验收证据：

- 回执：`.tasks/receipts/ASSET-001R/AUDIT_RECEIPT.md`。
- `mc-design-nx`: `python -m pytest client/tests/test_design_skill_contract.py client/tests/test_asset_store.py client/tests/test_windows_payload_builder.py -q`
- 结果：28 passed，2 failed。

历史返工要求（已由 `NX-DRAW-001` 完成）：

1. `nx-auto-drawing` 应明确禁用，不进入资产包。
2. 保留 `runtime.md` 优先、`beya.md` fallback。
3. `nx_run_auto_drawing`、`nx_updatedrawings`、图纸 sheet 级自动操作等自动出图入口应从 manifest/skill/测试口径中移除或标记禁用。
4. NX 图纸流程只保留通过 `nx_open_tcpart` 打开已绑定图纸；绑定更新后的图纸即为自动出图结果。
5. 复跑 `client/tests/test_asset_store.py` 和 `client/tests/test_windows_payload_builder.py`，测试应验证 `nx-auto-drawing` 不存在。
6. 返工回执编号建议为 `NX-DRAW-001`。

### 2026-06-14：S0-5 设计报告/截图/说明书链路加固

历史结论：部分通过，需按最新 NX 图纸规则返工。状态更新：旧自动出图口径已由 `NX-DRAW-001` 清理，报告链路进入全通路回归。

已完成：

1. `design-report` 补齐 inspect-template、prepare、validate、preview/generate、save-final 流程。
2. 报告预览和正式保存分离，预览确认后才能保存正式 DOCX。
3. 生成前确认、上传前确认、本地下载路径、`report_output` 读取路径已补充。
4. 截图视角证据链增加 `requested_view_name`、`confirmed_view_name`、`capture_order`，重复视角和重复 capture order 会被校验拦截。
5. 从 TC 旧说明书复用内容时，要求填写 `source_record`，至少包含来源文件和定位信息。

验收证据：

- 回执：`.tasks/receipts/S0-5/EXECUTION_RECEIPT.md`。
- 回执内自测覆盖 design-report 脚本、skill contract、local file/report output、agent assets、payload builder。

历史不通过点（已由 `NX-DRAW-001` 处理）：

1. 回执和改动仍把 `nx-auto-drawing`、`nx_run_auto_drawing` 当作二维图更新/自动出图可用能力。
2. 这与项目负责人最新规则冲突：NX plugin 中自动出图插件必须禁用；NX 图纸操作只保留通过 `nx_open_tcpart` 打开 NX 图纸；图纸与数模绑定后自动更新即视为自动出图。
3. `design-report`、`nx-operation`、`dfmea-risk-review`、asset/runtime/test 中关于自动出图的旧口径应并入 `NX-DRAW-001` 清理。

后续处理状态：

1. 保留报告生成、预览、保存、本地下载、截图证据、旧说明书来源记录的成果。
2. 自动出图插件相关 skill/测试/资产要求已由 `NX-DRAW-001` 清理。
3. 原 `REG-001` 报告链路全通路回归候选已撤回冻结。

### 2026-06-14：DFMEA-001 DFMEA/FMEA 模板工具与 Skill 补全

历史结论：工具侧阶段通过，skill 中图纸旧口径需随 `NX-DRAW-001` 修正。状态更新：图纸旧口径已由 `NX-DRAW-001` 清理，DFMEA 工具链进入全通路回归。

已完成：

1. 新增 Python 客户端本地工具组 `tool.dfmea`，通过 `DfmeaToolProvider` 注册，不依赖 NX、Teamcenter、Excel COM 或外部服务。
2. 工具包括 `dfmea_template_list`、`dfmea_template_inspect`、`dfmea_fill_template`、`dfmea_calculate_risk`、`dfmea_validate_workbook`。
3. 支持列出 3 个 `.xlsx` 模板、检查 DFMEA/AP sheet、基于模板生成新 xlsx、默认不覆盖、越界路径拒绝、AP/RPN 计算。
4. `dfmea-risk-review` 补充 DFMEA/FMEA 表生成、更新、风险计算、缺项追问、预览确认、TC 上传前 gate 和低置信度人工复核要求。
5. `design-report` 和 `teamcenter-flow` 中增加 DFMEA 输出文件引用和上传边界。

验收证据：

- 回执：`.tasks/receipts/DFMEA-001/EXECUTION_RECEIPT.md`。
- `mc-design-nx`: `python -m pytest client/tests/test_dfmea_tools.py client/tests/test_tool_registry.py -q`
- 结果：21 passed。
- `mc-design-nx`: `python -m pytest client/tests/test_client_static.py client/tests/test_agent_loop_assets.py client/tests/test_windows_payload_builder.py -q`
- 结果：46 passed。

剩余风险与状态：

1. `dfmea-risk-review` 的旧图纸口径已由 `NX-DRAW-001` 清理，后续重点转为真实链路回归。
2. `.xls` 原件只作为参考，正式运行时只支持 `.xlsx`。
3. 未实现真实 Teamcenter 上传，符合任务边界；后续上传仍由 TC 工具处理并需要用户确认。

### 2026-06-14：Skill/Tool/Asset 结构审计问题记录

审计台账：`.tasks/skill_tool_asset_audit_2026-06-14.md`。

审计结论：当前未发现运行资产缺文件、禁用工具误暴露或 K8s connector 不可用的问题；source 与 `agent_assets.mcdpkg` 一致，运行包中没有 `nx-auto-drawing`、旧 `tool.mysql/tool.external/tool.teamcenter` 或用户可见 Beya 文案。`mc-design-nx` 关键静态/资产测试 53 passed，`mc-design-ai-service` runtime/connector 测试 63 passed, 1 warning。

新增/确认问题：

| 编号 | 摘要 | 优先级 | 处理建议 |
|---|---|---|---|
| AUDIT-ST-001 | 零件规则仍硬编码在 skill/runtime 中，新增零件或规则变更仍需要改正文。 | P0 | 原 `SK-003` 候选已撤回，待新方案重排。 |
| AUDIT-ST-002 | AI Service 内部仍有 Beya 兼容命名，Runtime/Tjuae 中性命名未完全收口。 | P1 | 原 `RT-NAME-001` 候选已撤回，待新方案重排。 |
| AUDIT-ST-003 | Teamcenter connector schema 暴露 `BEYA_TC_BASE_URL`。 | P1 | 原 `RT-NAME-001` 候选已撤回，待新方案重排。 |
| AUDIT-ST-004 | Agent 索引与实际 runtime skill 列表不完全一致。 | P2 | 原 `ASSET-GOV-001` 候选已撤回，待新方案重排。 |
| AUDIT-ST-005 | 报告模板仍硬编码为连杆模板，泛化不足。 | P1 | 原 `REPORT-TEMPLATE-001` 候选已撤回，待新方案重排。 |
| AUDIT-ST-006 | Skill capabilities 声明缺少统一机器校验。 | P1 | 原 `ASSET-GOV-001` 候选已撤回，待新方案重排。 |
| AUDIT-ST-007 | 三零件 fixture 仍在 `logic-expression-design/resources/minimal_test_cases.json`，与 part-rules 方向重叠。 | P1 | 原 `SK-003` 候选已撤回，待新方案重排。 |
| AUDIT-ST-008 | `nx_test` 作为连接检查工具名称不够语义化。 | P2 | 原 `NX-TOOL-NAMING-001` 候选已撤回，待新方案重排。 |
| AUDIT-ST-009 | `beya.md` fallback 仍保留，长期增加资产解释成本。 | P2 | 后续兼容清理，暂不阻塞。 |
| AUDIT-ST-010 | 仓库根目录仍存在安装后的 `client/` payload，与 `mc-design-nx/client` 源码目录重复，且包含旧 beya 运行数据/依赖痕迹。 | P1 | 已由 `CLIENT-ACTIVE-ROOT-001` 有条件关闭；根 payload 已归档移除，仅剩含本机 `tc_key` 的配置文件需项目负责人确认。 |
| AUDIT-ST-011 | `assets/source/tools/*/TOOL.md` 只是工具说明资产，实际执行在 Python provider；缺少 TOOL.md -> provider spec -> HTTP executor 的机器校验映射。 | P1 | 已由 `CLIENT-ACTIVE-ROOT-001` 关闭；`tool_execution_map.json` 和测试覆盖已补齐。 |
| AUDIT-ST-012 | 需求文档中的任务抓取、模板确认、参数分类/换算、建模计划仍主要靠 skill 编排，缺少可调用、可测试的业务适配工具层。 | P0 | 已由 `BIZ-ADAPTER-001` 阶段关闭；后续转入真实 agent-turn 回归验证。 |
| AUDIT-ST-013 | 本地工具进入 tjuae inline plugin 时 namespace 映射过粗，`tool.dfmea` 可能被声明成 `local` 后被本地 API 拒绝。 | P0 | 已由 `BIZ-ADAPTER-001` 阶段关闭；namespace 映射和测试已补齐。 |
| AUDIT-ST-014 | IPM/ECMS/QPP 仍是原子 connector，缺少跨系统任务候选聚合、任务编号选择和多轮上下文保持的统一业务输出。 | P0 | 已由 `BIZ-ADAPTER-001` 阶段关闭；QPP 当前外部不通仍单独归类。 |
| AUDIT-ST-015 | NX plugin 自动出图源码仍保留 `[Tool]` 方法，当前靠多层禁用兜底；长期应降低编译暴露面。 | P1 | 已由 `NX-TOOL-HARDEN-001` 阶段关闭；后续需 NX 实机补验。 |
| AUDIT-ST-016 | NX plugin 与本地 API 对请求体大小、坏 JSON、并发和错误码保护不足。 | P1 | 已由 `NX-TOOL-HARDEN-001` 阶段关闭；后续需 NX 实机补验。 |
| AUDIT-ST-017 | K8s connector 直连可用，但本地 agent-turn 工具面没有暴露 IPM 查询/任务选择能力。 | P0 | `REG-P0-FULL-001` 新发现，待新编号整改。 |
| AUDIT-ST-018 | 参数四分支 transport 成功但业务断言失败，参考逻辑和真实 NX 参数 ID 未稳定绑定。 | P0 | `REG-P0-FULL-001` 新发现，待新编号整改。 |
| AUDIT-ST-019 | MCP/local `files` 入参进入 `TurnCommand` 后，在 tjuae adapter 组装 SDK 输入时被丢弃。 | P0 | 已由 `RUNTIME-CONTEXT-001` 阶段关闭；客户端测试 197 passed，后续做真实 agent-turn 回归。 |
| AUDIT-ST-020 | runtime 基础提示、工具目录和动态 connector 目录未稳定注入 agent-turn 模型输入。 | P0 | 已由 `RUNTIME-CONTEXT-001` 阶段关闭；`query_ipm_list/query_ecr_list/connect_qpp/mysql_query/tc_call` 可见性进入 SDK input。 |
| AUDIT-ST-021 | NX 视图切换和截图工具存在确认不严、截图失败不可诊断问题。 | P0 | 已由 `NX-VISUAL-002` 源码阶段关闭；等待运行中 NX plugin 加载新 DLL 后做截图实机验证。 |
| AUDIT-ST-022 | 正式客户端启动/安装卸载链路仍不稳，fresh install 后 TC key 配置缺失会阻塞全链路。 | P0 | 已由 `CLIENT-LAUNCHER-002` 阶段关闭；当前剩 `TC_KEY_NOT_CONFIGURED` 本机配置前置。 |
| AUDIT-ST-023 | NX 参数工具缺少中文/别名到真实表达式 ID 的可审计解析面，且 `HighLightDim` 失败路径可能空引用。 | P0 | 已由 `NX-PARAM-002` 源码阶段关闭；等待运行中 NX plugin 加载新 DLL 后做参数工具实机验证。 |

### 2026-06-14：插队任务回执整理与 LOG-001 会话日志

本轮回执检查结论：

1. `RUNTIME-CONTEXT-001`：通过。修复 `files` 入参丢失、runtime prompt/tool directory/connector directory 未进入 SDK input 的问题；未改 AI Service，`K8S_UPDATE_REQUIRED=false`。
2. `PARAM-RULES-002`：通过。新增 `logic-expression-design/scripts/part_rule_calculator.py` 和 `part_rules.json`；脚本只依赖客户端 Python 标准库和 JSON；三零件四分支脚本测试通过。
3. `NX-PARAM-002`：源码阶段通过。新增/加固参数解析与安全写入，修复 `HighLightDim` 空引用路径；C# build 和静态测试通过；运行中 NX plugin 仍加载旧程序集，实机新工具未验证。
4. `NX-VISUAL-002`：源码阶段通过。视图切换增加确认，截图返回路径、大小、sha256 和结构化错误；C# build 和静态测试通过；运行中 NX plugin 仍加载旧程序集，改后截图未实机验证。
5. `CLIENT-LAUNCHER-002`：阶段通过。正式 launcher、安装、卸载、日志和启动前配置检查已加固；当前停止点是 `TC_KEY_NOT_CONFIGURED`，不输出密码明文。
6. `LOG-001`：本轮由监管方直接实现。客户端每个 `conversation_id` 写一份 JSONL 日志和 summary；本地 `test_agent_turn` 返回 `conversation_log` 路径；`GET /api/runtime/conversation-log?conversation_id=...` 可查询日志状态；`mc-design-nx/client/tests` 199 passed。

后续问题绑定规则：

1. 测试人员提交问题时必须提供 `conversation_id`、复现输入、期望/实际表现、`conversation_log.log_path` 或日志文件。
2. 日志中不得包含 Teamcenter 密码、API key、cookie、token 等明文敏感信息；当前日志模块已做字段级脱敏和长文本截断。
3. QPP 当前不通仍归类为外部接口不可用，不进入 mc-design 缺陷队列。

## 下次对齐建议

下次会议/对话先处理客户端正式启动入口和回归口径：

1. `E2E-SMOKE-003` 已证明 `PKG-002` 卸载/安装通过，但正式 `McDesignClient.exe` 启动失败；下一步优先修 launcher 启动、等待、异常提示和日志落盘。
2. `REG-P0-FULL-001` 已完成正式试跑但不通过；后续优先整改本地 agent-turn 工具面和参数四分支业务断言失败。
3. QPP 当前确认不通，后续 QPP 相关测试只记录为外部接口不可用，不判定 mc-design 代码失败。
4. `K8S-SMOKE-001` 已通过，K8s 旧 `/api/mc-design/test/agent-turn` 返回 404 是正确结果，不应再让 K8s 暴露该测试接口。
5. 后续所有测试类提示词都必须引用 `.tasks/TEST_EXECUTION_RULES.md`。
6. `CLIENT-ASSET-001`、`CLIENT-LEGACY-001`、`CLIENT-ACTIVE-ROOT-001` 已完成，客户端源码/资产/根安装 payload 的主要混淆已降噪。
7. 根 `client/configure/mc-design-client.config` 的保留、迁移或删除需要项目负责人确认；提交前还需单独确认 `.install-backup/` 与 `.tmp-runtime-check/` 删除记录。
8. `REG-P0-FULL-001` 已有正式回执，但结论是不通过；当前只能作为失败清单和后续整改输入。
9. `CLIENT-DATA-001`、`CLIENT-TJUAE-001`、`CLIENT-PKG-OUTPUT-001` 暂不并发派发，等 launcher 阻塞处理后再排。
10. 规则包方向、连杆试点、报告模板泛化、Beya 命名中性化等候选事项全部继续冻结；如要推进，必须重新编号并单独派发，不与 launcher 阻塞整改并发。
