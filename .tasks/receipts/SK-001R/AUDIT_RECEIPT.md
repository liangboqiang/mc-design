# SK-001R 零部件 Skill 硬编码审计回执

审计日期：2026-06-14

审计边界：本次只审计指定 `SKILL.md` 与参考 Excel 中的硬编码点，未修改代码、未修改 skill、未执行 SK-002/SK-003 迁移、未做 beya/tjuae 替换。

## 1. 审计文件清单

| 序号 | 文件 | 审计状态 | 备注 |
|---:|---|---|---|
| 1 | `mc-design-nx/assets/source/skills/part-design/SKILL.md` | 已审计 | 总控流程、技能路由、TC/NX 门禁、工具名 |
| 2 | `mc-design-nx/assets/source/skills/logic-expression-design/SKILL.md` | 已审计 | 四类输入分支、计算脚本协议、确认表、NX 门禁 |
| 3 | `mc-design-nx/assets/source/skills/conrod-design/SKILL.md` | 已审计 | 连杆参数、公式、示例值、追问表、脚本、NX 顺序 |
| 4 | `mc-design-nx/assets/source/skills/parameter-mapping/SKILL.md` | 已审计 | 参数分类、数据库表名、编码规则、示例零件术语 |
| 5 | `mc-design-nx/assets/source/skills/nx-parameter/SKILL.md` | 已审计 | NX 参数读取/写入顺序、工具名、表达式门禁 |
| 6 | `mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md` | 已审计 | TC 默认模板库、查询/打开/写入顺序、图纸筛选词 |
| 7 | `mc-design-nx/assets/source/skills/design-report/SKILL.md` | 已审计 | conrod 报告模板、槽位、payload 示例、截图顺序 |
| 8 | `references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表(1).xlsx` | 已审计 | 连杆公式族、示例输入、完整/缺参任务描述 |
| 9 | `references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表（活塞销）3.0.xlsx` | 已审计 | 活塞销公式族、经验参数、示例输入 |
| 10 | `references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表（止推片）3.0.xlsx` | 已审计 | 止推片公式族、经验参数、示例输入 |
| 11 | `references/开发资料/零件设计智能体试用问题跟踪表.xlsx` | 已审计 | 四类输入分支、TC/NX/报告问题、历史缺陷线索 |

参考但未替代审计：`.tasks/SK-002_part_rules_schema_design.md`。该文档只用于核对“skill 保留/规则包迁移”的边界，不作为本回执的硬编码台账来源。

## 2. 风险分级定义

| 等级 | 判定标准 |
|---|---|
| P0 | 可能直接导致错误公式、错误 NX 写入、错误模型/报告、或新增零件无法走通主流程。 |
| P1 | 会造成新增零件/规则变更时高维护成本、模板/工具路由不稳定、或需要多处同步更新。 |
| P2 | 主要是示例、命名、重复说明或测试资料位置问题；短期不直接破坏执行，但会误导维护。 |

## 3. 硬编码点清单

| ID | 文件/位置 | 硬编码点 | 类型 | 风险 | 处理建议 | 理由 |
|---|---|---|---|---|---|---|
| HC-001 | `part-design/SKILL.md:16,21,31,43` | 总控流程中特指“连杆/曲轴”，并规定连杆继续加载 `conrod-design` | 零部件知识规则 | P1 | 迁出到零部件规则包 | 新增活塞销、止推片、曲轴等零件时，主控 skill 会继续偏向连杆；零件识别应来自规则索引。 |
| HC-002 | `part-design/SKILL.md:20,32,51` | TC `智能体模板库` 作为默认数模模板来源 | 通用流程规则 | P1 | 保留在 skill | 这是当前平台级模板来源规则，不属于单个零件；但后续若多环境模板库名称不同，应抽成平台配置。 |
| HC-003 | `part-design/SKILL.md:29-38` | 逻辑表达式、TC 模板检索、MySQL、NX、报告、TC 文件流转的固定顺序 | 通用流程规则 | P1 | 保留在 skill | 这是副作用门禁和跨工具编排，问题跟踪表中有“找错模型”“先下载再打开”等历史缺陷支撑，应保留为总控约束。 |
| HC-004 | `part-design/SKILL.md:31` | “缺参追问、输入完整后生成 Python 脚本、输出计算结果确认表” | 通用流程规则 | P2 | 保留在 skill | 属于通用执行协议；具体缺参项和输出行不应在总控 skill 中继续扩展。 |
| HC-005 | `part-design/SKILL.md:40-46` | Tjuae 能力映射中的技能名、外部系统名、脚本路径 | 通用流程规则 | P2 | 删除或合并 | 内容与各子 skill 重复，后续可收敛为能力索引说明；不应承载零件规则。 |
| HC-006 | `part-design/SKILL.md:50-56` | 禁止创成式建模、绕过 TC、本地猜 NX 路径、中文名写 NX 等 | 通用流程规则 | P0 | 保留在 skill | 这些是全局安全门禁，直接防止错误模型和错误参数写入。 |
| HC-007 | `logic-expression-design/SKILL.md:11-12` | 适用场景举例写死连杆、曲轴，并要求连杆加载 `conrod-design` | 零部件知识规则 | P1 | 迁出到零部件规则包 | 通用逻辑表达式 skill 不应知道具体零件技能；应由规则包索引匹配。 |
| HC-008 | `logic-expression-design/SKILL.md:16-26` | `design_parameter`、`boundary_parameter`、`template_parameter`、`drive_parameter`、`associated_parameter` 五类参数 schema | 通用流程规则 | P0 | 保留在 skill | 这是所有零件共享的安全分类，尤其防止中文设计参数直接写 NX。 |
| HC-009 | `logic-expression-design/SKILL.md:30-37` | 四类输入分支：参数齐全、不全/无参数、仅边界、混合参数 | 通用流程规则 | P0 | 保留在 skill | 问题跟踪表第 1-4 条明确要求该状态机；具体零件的 required 参数由规则包提供。 |
| HC-010 | `logic-expression-design/SKILL.md:44-49,75-99` | `.generated/calculators/<conversation_id>/`、`input.json`、`calculate.py`、`output.json` 和 JSON 输出字段 | 通用流程规则 | P1 | 保留在 skill | 这是计算执行器协议，不随零件变化；公式内容不应写在这里。 |
| HC-011 | `logic-expression-design/SKILL.md:54-61` | `minimal_test_cases.json` 中写入连杆、活塞销、止推片最小用例 | 零部件知识规则 | P1 | 迁出到测试 fixture | 这些是回归用例，不应继续堆在通用 skill 资源下。 |
| HC-012 | `logic-expression-design/SKILL.md:82` | 单位默认按 `mm` 处理 | 零部件知识规则 | P1 | 迁出到零部件规则包 | 多数当前零件用 mm，但止推片斜接口斜度是 `30°/deg`；默认单位应由规则包声明，skill 只保留“单位不明需确认”。 |
| HC-013 | `logic-expression-design/SKILL.md:101-109` | 计算结果确认表通用列和固定追问话术 | 通用流程规则 | P2 | 保留在 skill | 表结构可保留；具体输出参数行、经验参数行应由规则包提供。 |
| HC-014 | `logic-expression-design/SKILL.md:111-122` | NX 建模前置条件和允许工具名白名单 | 通用流程规则 | P0 | 保留在 skill | 这是跨零件写入防线，不属于零件知识。 |
| HC-015 | `conrod-design/SKILL.md:2-16` | 专门的 `conrod-design` 技能名、描述、来源 Excel | 零部件知识规则 | P1 | 迁出到零部件规则包 | 当前连杆规则已经完整硬编码，后续应收敛为薄调度或由规则包索引识别。 |
| HC-016 | `conrod-design/SKILL.md:22-25` | 连杆输入/输出参数类别：4 个设计参数、NX drive 参数映射要求 | 零部件知识规则 | P0 | 迁出到零部件规则包 | 具体“必须映射哪些输出参数”随零件变化；只保留通用映射门禁在 skill。 |
| HC-017 | `conrod-design/SKILL.md:31-48` | 11 个连杆必需输入、含义、单位、示例值 | 零部件知识规则 | P0 | 迁出到零部件规则包 | 新增或调整连杆边界时，这里最容易漏改；示例值应作为测试 fixture。 |
| HC-018 | `conrod-design/SKILL.md:40,173` | “曲柄半径通常为行程一半，但不得默认换算” | 零部件知识规则 | P0 | 迁出到零部件规则包 | 这是连杆关联参数/派生候选规则；通用 skill 只需保留“关联参数不得静默默认”。 |
| HC-019 | `conrod-design/SKILL.md:52-57` | 连杆中心距、大头直径、小头直径、厚度四条公式 | 零部件知识规则 | P0 | 迁出到零部件规则包 | 公式变更会直接影响模型参数。连杆厚度还存在 Excel 公式显示文本与实际单元格公式/当前脚本的证据差异，迁移前需业务确认。 |
| HC-020 | `conrod-design/SKILL.md:61-68` | 从自然语言抽取“上面 11 个必需输入”和连杆缺参追问表 | 零部件知识规则 | P0 | 迁出到零部件规则包 | 缺参清单必须由规则包 required 参数生成，否则新增零件无法复用。 |
| HC-021 | `conrod-design/SKILL.md:72-78` | 连杆计算脚本生成路径重复声明 | 通用流程规则 | P2 | 删除或合并 | 该协议已在 `logic-expression-design` 中定义，连杆 skill 中重复容易漂移。 |
| HC-022 | `conrod-design/SKILL.md:80-145` | 完整 Python 计算脚本硬编码 REQUIRED、公式、单位、trace | 零部件知识规则 | P0 | 迁出到零部件规则包 | 这是最重的硬编码点；应由规则包公式生成脚本，而不是在 skill 正文维护 Python。 |
| HC-023 | `conrod-design/SKILL.md:151-156` | 结果确认表中固定 4 行连杆输出参数和公式依据 | 零部件知识规则 | P0 | 迁出到零部件规则包 | 输出表行随零件和公式变化，应由规则包 `output_parameters/formulas` 渲染。 |
| HC-024 | `conrod-design/SKILL.md:160-169` | NX 参数化建模流程固定顺序，且第 4 步写死四个连杆输出参数 | 混合 | P0 | 保留在 skill + 迁出到规则包 | NX 连接、读 WorkPart、读 drive 参数、确认后写入是通用门禁；四个连杆参数列表应迁出。 |
| HC-025 | `conrod-design/SKILL.md:173-177` | 禁止事项中混合连杆专属和通用 NX 禁止项 | 混合 | P1 | 删除或合并 | 通用禁止项合并到 `logic-expression-design/nx-parameter`；曲柄半径规则进连杆规则包。 |
| HC-026 | `parameter-mapping/SKILL.md:18-22` | 参数分类示例硬编码连杆中心距、活塞销外径、止推片厚度、机体止推档内径、壁厚、斜接口斜度 | 零部件知识规则 | P1 | 迁出到零部件规则包 | 示例会把通用映射技能偏向三类样件；这些应成为规则包参数样例或测试 fixture。 |
| HC-027 | `parameter-mapping/SKILL.md:28,32,47,64` | 多处重复 TC `智能体模板库` 作为数模模板主路径 | 通用流程规则 | P1 | 删除或合并 | 该规则应由 `teamcenter-flow` 统一维护，避免总控/映射/TC 三处漂移。 |
| HC-028 | `parameter-mapping/SKILL.md:46-49` | SQL 表名 `nx_param_dic_cn_v2`、`part_template_table`、`doc_template_table`、`parameter_code_types` | 通用数据规则 | P1 | 删除或合并 | 这是数据查询路线，不是零件规则；应收敛到数据库查询技能或数据 schema 文档，避免表名变更影响映射 skill。 |
| HC-029 | `parameter-mapping/SKILL.md:48` | 新编码格式 `<part_code>_<section_code><semantic_code>` | 通用数据规则 | P1 | 保留在 skill | 若这是全局参数编码规范可保留；若存在零件差异，则后续应抽到编码规则配置。 |
| HC-030 | `parameter-mapping/SKILL.md:67-76` | NX 写入门禁：真实表达式必须来自 NX 返回 | 通用流程规则 | P0 | 保留在 skill | 问题跟踪表第 10 条明确出现“工具调用用中文描述”的缺陷，应保留强约束。 |
| HC-031 | `nx-parameter/SKILL.md:19-22` | `nx_create_param`、`nx_update_param`、`nx_batch_update_params` 语义边界 | 通用流程规则 | P0 | 保留在 skill | 直接防止把表达式创建误报为模型更新。 |
| HC-032 | `nx-parameter/SKILL.md:26-32` | NX 参数修改固定流程：读当前零件、读驱动参数、映射、确认、写入、复读 | 通用流程规则 | P0 | 保留在 skill | 全局可复用，且与问题跟踪表中的中文参数写入缺陷直接相关。 |
| HC-033 | `nx-parameter/SKILL.md:36-40` | 禁止中文名写 expression、未确认写模型、忽略失败明细 | 通用流程规则 | P0 | 保留在 skill | 全局安全防线。 |
| HC-034 | `teamcenter-flow/SKILL.md:15,26-27` | 默认查询 `智能体模板库`，`folder_name` 使用 `*关键词*` | 通用流程规则 | P1 | 保留在 skill | 当前模板来源规则应保留在 TC 流程层；若模板库名称环境化，后续转平台配置，不进零件规则包。 |
| HC-035 | `teamcenter-flow/SKILL.md:19-22` | `TJUAE_TC_BASE_URL`、`user_id`、`owner_id`、`user_pass` 入参规则 | 通用流程规则 | P1 | 保留在 skill | 这是 TC 连接/权限契约，不是零件知识。 |
| HC-036 | `teamcenter-flow/SKILL.md:29-31` | TC 查询后进入 NX 打开；图纸候选筛选 `specification/drawing/dwg/二维/图纸`；`@DB@...@specification@...` 路径示例 | 通用流程规则 | P1 | 保留在 skill | 问题跟踪表有“找错模型、未完成三维修改前打开二维图纸”；顺序要保留。筛选词若后续扩展可转 TC 适配器配置。 |
| HC-037 | `teamcenter-flow/SKILL.md:36-38` | TC 写入必须确认目标 item、版本、文件名、覆盖策略、用户/所有者一致 | 通用流程规则 | P0 | 保留在 skill | 上传/复制是副作用动作，必须保留强门禁。 |
| HC-038 | `design-report/SKILL.md:10-19` | 报告模板固定为 `conrod_design_report_template.docx`，槽位快照固定 `conrod_design_report_slots.json` | 零部件知识规则 | P0 | 迁出到零部件规则包 | 非连杆报告会错误套用连杆模板；模板名和槽位快照应由零件/报告模板元数据决定。 |
| HC-039 | `design-report/SKILL.md:21` | 槽位策略来自 DOCX `[[type:...]]` 的 name/section/prompt/schema/format | 通用流程规则 | P1 | 保留在 skill | 槽位驱动是报告生成通用机制，具体槽位名不应写死在正文逻辑外。 |
| HC-040 | `design-report/SKILL.md:35-42` | `design_report.py inspect-template/prepare/validate/generate` 命令 | 通用流程规则 | P1 | 保留在 skill | 报告生成执行器协议，不随零件变化。 |
| HC-041 | `design-report/SKILL.md:46-57` | 工具对照表固定 TC/NX/MySQL/External 工具名 | 通用流程规则 | P1 | 保留在 skill | 工具证据链通用；但工具名变更需集中维护，避免多个 skill 重复。 |
| HC-042 | `design-report/SKILL.md:80-107` | payload 示例写死“连杆体”、“K17N_1005001”、“三维主视图”、“左视图” | 零部件知识规则 | P2 | 迁出到测试 fixture | 示例值和视图选择会误导非连杆报告；可保留为报告测试样例。 |
| HC-043 | `design-report/SKILL.md:109` | `当前日期`、`当前时间` 自动填充 | 通用流程规则 | P2 | 保留在 skill | 通用报告槽位能力。 |
| HC-044 | `design-report/SKILL.md:113-117` | NX 截图顺序：先读视图名，切换一次截图一次，禁止连续切换后连续截图 | 通用流程规则 | P0 | 保留在 skill | 问题跟踪表第 14 条出现“全是正视图截图”，该顺序是必要防线。 |
| HC-045 | 连杆 Excel `(1).xlsx` | K08 连杆完整/缺参任务描述、11 个输入、4 个输出、示例值和公式 | 零部件知识规则 | P0 | 迁出到零部件规则包 + 测试 fixture | 公式/参数进入规则包；完整/缺参自然语言样例保留为 fixture。 |
| HC-046 | 连杆 Excel `(1).xlsx` | 连杆厚度单元格公式 `=(缸径*曲柄半径*2)^0.5*(1/6)` 与文本表达式 `((缸径*曲柄半径/2)^0.5)*(1/6)` 不一致 | 零部件知识规则 | P0 | 迁出到零部件规则包 | 迁移前必须保留 source_note 并由业务确认采用哪个公式；当前 skill 与单元格计算值一致，不与文本一致。 |
| HC-047 | 活塞销 Excel `（活塞销）3.0.xlsx` | 活塞销输入：挡圈轴向间距、连杆小头内径、连杆衬套厚度 | 零部件知识规则 | P0 | 迁出到零部件规则包 | 当前 skill 未内置活塞销完整规则，新零件扩展会缺公式依据。 |
| HC-048 | 活塞销 Excel `（活塞销）3.0.xlsx` | 经验参数：活塞挡圈与销装配间隙 0.1、活塞销壁厚 12.5，需设计人员确认 | 零部件知识规则 | P0 | 迁出到零部件规则包 | 经验默认值不能静默参与最终建模，规则包需声明确认时机。 |
| HC-049 | 活塞销 Excel `（活塞销）3.0.xlsx` | 公式：长度、外径、内径三条公式；示例任务写 90.0mm，表格值为 90.2 | 零部件知识规则 | P1 | 迁出到零部件规则包 + 测试 fixture | 公式进入规则包；样例值差异保留为 fixture/evidence note。 |
| HC-050 | 止推片 Excel `（止推片）3.0.xlsx` | 止推片 6 个边界输入、7 个输出参数和公式 | 零部件知识规则 | P0 | 迁出到零部件规则包 | 规则复杂度高，当前 skill 无对应零件规则，新增时会失效。 |
| HC-051 | 止推片 Excel `（止推片）3.0.xlsx` | 经验参数：径向间隙 3、轴向间隙 0.05、卡扣边距 70、斜接口水平交点边距 56.5、斜接口斜度 30° | 零部件知识规则 | P0 | 迁出到零部件规则包 | 多个经验参数直接影响公式，且含角度单位；必须声明确认策略和单位。 |
| HC-052 | 止推片 Excel `（止推片）3.0.xlsx` | 公式文本中“止推片厚度（轴向）= / （...”存在格式噪声 | 零部件知识规则 | P1 | 迁出到测试 fixture | 迁移时需要按单元格公式核对，不能盲信展示文本。 |
| HC-053 | 问题跟踪表 `测试计划` | 测试计划固定列出连杆、气门杆、曲轴、凸轮轴、报告、二维图、指标转换参数 | 测试资料 | P2 | 迁出到测试 fixture | 这是测试覆盖计划，不应被 skill 当作零件能力列表。 |
| HC-054 | 问题跟踪表第 1-4 条 | 四类输入分支需求文本 | 通用流程规则 | P1 | 保留在 skill + 迁出到测试 fixture | 状态机保留在 skill；原始需求文本应作为验收 fixture。 |
| HC-055 | 问题跟踪表第 8-10 条 | 关联参数未同步、TC 打开顺序、中文参数写工具问题 | 通用流程规则 | P0 | 保留在 skill + 迁出到测试 fixture | 这些缺陷支撑当前 NX/TC 门禁；也应进入回归用例。 |
| HC-056 | 问题跟踪表第 14、26-27 条 | 报告截图错误、找错模型、先打开二维图纸 | 通用流程规则 | P0 | 保留在 skill + 迁出到测试 fixture | 支撑 `design-report` 截图顺序和 `teamcenter-flow` 三维/二维打开顺序。 |

## 4. P0/P1/P2 风险汇总

| 风险 | 数量 | 主要集中位置 |
|---|---:|---|
| P0 | 23 | `conrod-design` 的参数/公式/脚本/NX 映射、`design-report` 的 conrod 模板、Excel 公式族、NX/TC/报告副作用门禁 |
| P1 | 25 | 总控和逻辑 skill 的零件路由、测试用例位置、默认单位、TC 模板库、SQL 表名、图纸筛选词 |
| P2 | 8 | 示例值、重复说明、payload 样例、测试计划类资料 |

P0 不是说现有功能必然错误，而是这些点一旦新增零件或修改规则，最可能直接产生错误计算、错误写入或错误报告。

## 5. 保留在 skill 的内容

以下内容属于通用流程规则，应保留在对应 skill 中：

| 内容 | 保留位置 | 原因 |
|---|---|---|
| 五类统一参数分层 | `logic-expression-design`、`parameter-mapping` | 防止边界参数、设计参数、中文名直接写 NX。 |
| 四类输入分支状态机 | `logic-expression-design` | 这是跨零件的交互流程，问题跟踪表已有明确需求。 |
| 计算脚本执行协议 | `logic-expression-design` | `.generated/calculators/<conversation_id>/input.json/calculate.py/output.json` 是执行器约定。 |
| 计算结果确认前不得建模 | `logic-expression-design`、`conrod-design` 的通用部分 | 防止未确认公式结果进入 NX。 |
| NX 当前 WorkPart 确认、读取真实驱动参数、映射确认后再写入 | `nx-parameter`、`logic-expression-design` | 这是所有零件共享的 P0 写入门禁。 |
| TC 查询候选不等于打开成功 | `teamcenter-flow`、`part-design` | 防止把 TC 命中误报为 NX 已打开或模型已改。 |
| TC 写入权限、覆盖策略、owner/user 确认 | `teamcenter-flow` | 文件上传/复制是副作用动作，必须保留。 |
| 报告槽位驱动、validate 后 generate | `design-report` | 通用报告生成机制。 |
| NX 截图顺序：读视图、切换一次、截图一次 | `design-report` | 直接对应历史截图错误。 |
| 工具失败/空结果不得描述为完成 | 各总控/子 skill | 通用完成态约束。 |

## 6. 应迁出到规则包的内容

以下内容属于零部件知识规则，不应继续写在 skill 正文：

| 内容 | 当前位置 | 建议归属 |
|---|---|---|
| 零件名、别名、适用场景，如连杆、活塞销、止推片、曲轴 | `part-design`、`logic-expression-design`、Excel | 规则包索引 |
| 连杆 11 个输入参数、4 个输出参数、单位、含义、示例 | `conrod-design`、连杆 Excel | `parts/conrod` 规则包；示例进 fixture |
| 连杆四条公式和依赖关系 | `conrod-design`、连杆 Excel | `parts/conrod` 规则包 |
| 连杆厚度公式证据差异说明 | 连杆 Excel、`conrod-design` | `parts/conrod` evidence/source_note |
| 连杆 REQUIRED 列表和 Python 公式实现 | `conrod-design` | 规则包公式 + 通用执行器生成脚本 |
| 连杆结果确认表固定四行 | `conrod-design` | 规则包 `output_parameters/formulas/confirmation_table` |
| 曲柄半径与行程一半的关系及禁止默认代入 | `conrod-design` | `parts/conrod` 关联/派生候选规则 |
| 活塞销输入、输出、三条公式 | 活塞销 Excel | `parts/piston_pin` 规则包 |
| 活塞销经验参数 0.1、12.5 及确认时机 | 活塞销 Excel | `parts/piston_pin` 规则包 |
| 止推片输入、输出、七条公式 | 止推片 Excel | `parts/thrust_washer` 规则包 |
| 止推片经验参数 3、0.05、70、56.5、30° | 止推片 Excel | `parts/thrust_washer` 规则包 |
| 具体缺参追问行、参数级示例填写值 | `conrod-design`、Excel | 规则包 + fixture |
| 必须映射到 NX 的具体输出参数列表 | `conrod-design` | 各零件规则包 |
| conrod 报告模板名和槽位快照名 | `design-report` | 零件/报告模板元数据；可由规则包引用 |

## 7. 应迁出到测试 fixture 的内容

| 内容 | 原因 |
|---|---|
| 连杆、活塞销、止推片的完整任务描述和缺参任务描述 | 用于回归自然语言抽取和缺参追问，不应作为运行规则正文。 |
| Excel 中的样例值，如 K08、350、0.7、90.2、123 等 | 样例值不是默认值；放在 skill 会误导真实设计。 |
| 问题跟踪表第 1-4 条四类输入分支原始需求 | 可作为流程验收用例。 |
| 问题跟踪表第 8-10、14、26-27 条 | 可作为防回归用例：关联参数、中文表达式、TC 打开顺序、截图顺序、二维/三维混淆。 |
| `design-report` payload 示例中的 `连杆体`、`K17N_1005001`、`front.png`、`左视图` | 适合报告生成 fixture，不适合成为通用报告规则。 |
| `parameter-mapping` 中连杆/活塞销/止推片参数示例 | 可作为映射样例或规则包示例，不应引导通用 skill。 |

## 8. 可删除或合并的内容

| 内容 | 建议 |
|---|---|
| `conrod-design` 中重复声明计算脚本路径和执行协议 | 合并到 `logic-expression-design`，连杆规则只声明公式和参数。 |
| `part-design`、`parameter-mapping`、`teamcenter-flow` 多处重复 TC `智能体模板库` 规则 | 合并到 `teamcenter-flow` 或平台配置说明，其他 skill 只引用。 |
| `parameter-mapping` 中 SQL 表名和 SQL 路线 | 合并到数据库查询技能或数据 schema 文档，避免映射 skill 同时承担 SQL 模板维护。 |
| `part-design` 中 Tjuae 能力映射的重复工具说明 | 合并到能力索引或各子 skill，避免总控 skill 变成工具名清单。 |
| `conrod-design` 禁止事项中的通用 NX 门禁 | 合并到 `logic-expression-design`/`nx-parameter`；连杆专属禁止项进规则包。 |

## 9. 新增零部件或规则变更时最容易失效的点

1. `conrod-design` 的 REQUIRED 列表、公式表、Python 脚本、结果确认表四处重复维护，同一公式变更需要同步多处。
2. `part-design` 和 `logic-expression-design` 仍把“连杆继续加载 `conrod-design`”写成主路径，活塞销/止推片即使有 Excel 公式也没有同等运行入口。
3. `design-report` 绑定 `conrod_design_report_template.docx`，非连杆报告会天然套错模板或槽位。
4. 单位默认按 `mm` 处理，但止推片斜接口斜度是 `30°/deg`，新增角度、质量、材料类参数时容易误解析。
5. 经验参数和关联参数确认策略不统一。活塞销、止推片 Excel 明确要求确认经验参数，当前通用流程只抽象到 `associated_parameter`，没有按零件声明确认时机。
6. 中文参数名到 NX expression 的映射仍依赖执行时纪律，历史问题已出现“工具调用用中文描述”；规则包需要提供参数 ID，NX 写入仍必须来自真实 drive 参数。
7. TC 模板库名称和图纸筛选词写在 skill 中，环境或 Teamcenter 数据结构变化时需要改 skill。
8. Excel 是事实来源之一，但公式展示文本、单元格公式和 skill 脚本存在差异时，缺少强制 evidence review 流程。

## 10. 建议试点迁移零件

首选试点：连杆。

原因：

1. 连杆硬编码最集中，覆盖输入参数、输出参数、公式、Python 脚本、追问表、确认表和 NX 映射列表，迁移收益最高。
2. 当前 `conrod-design/SKILL.md` 已有可运行规则，Excel 也有完整/缺参样例，便于做迁移前后数值回归。
3. 连杆公式数量适中，4 个输出、11 个输入，足以验证规则包 schema、公式执行、缺参追问、结果确认、NX 映射门禁。
4. 连杆厚度存在证据差异，适合作为规则包 evidence/source_note 和业务确认流程的试点。
5. 先迁连杆可以把最重的 skill 正文硬编码移出，同时不需要一次性处理活塞销/止推片更多经验参数策略。

第二候选：活塞销。它公式少，但包含 2 个经验参数确认，适合作为连杆之后验证 `associated_parameter.default_candidate` 和“结果确认时同时列经验参数”的场景。

不建议首个迁移止推片。止推片关联经验参数多、含角度单位、且公式文本存在噪声，适合作为第二阶段复杂规则验证。

## 11. 后续 SK-002/SK-003 前置建议

以下是前置条件建议，不是实施方案：

1. 先确认规则包的事实来源优先级：Excel 单元格公式、Excel 展示文本、现有 skill 脚本、业务确认之间发生冲突时，以哪一类为准。
2. 对连杆厚度公式做业务确认，并在规则包 evidence 中保留差异说明，避免迁移时静默改数。
3. 明确“样例值”和“默认值”的边界。Excel 中 K08、350、90.2、123 等应默认视为测试 fixture，不是运行默认值。
4. 明确经验参数确认时机。活塞销可在结果确认时确认；止推片多个经验参数更适合计算前确认。
5. 规则包只承载零件知识；NX/TC/MySQL/报告工具名、权限、执行顺序仍由 skill 或平台适配层维护。
6. SK-003 若以连杆为试点，应把 `conrod-design/SKILL.md` 中公式、参数表、Python 脚本、结果表迁出后做数值回归；但本 SK-001R 未执行该迁移。

## 12. 审计结论

当前 SK-001 未通过的根因成立：现有交付如果只描述规则包方案，会漏掉大量已经硬编码在 skill 正文、Excel 用例和报告模板路径中的具体点。本次 SK-001R 已逐文件补齐硬编码审计台账。

总体判断：

- 应保留在 skill 的，是跨零件通用流程、工具门禁、权限/确认规则、执行器协议和完成态约束。
- 应迁出到零部件规则包的，是零件名、别名、参数、公式、经验默认值、单位、缺参问题、结果表行、NX 输出参数映射要求和证据来源。
- 应迁出到测试 fixture 的，是 Excel 中自然语言样例、样例数值、问题跟踪表中的历史缺陷和报告 payload 示例。
- 当前最优试点是连杆，活塞销作为第二候选，止推片保留到复杂规则验证阶段。
