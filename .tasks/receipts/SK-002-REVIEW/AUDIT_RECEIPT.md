# SK-002-REVIEW 零部件规则包方案评审回执

评审日期：2026-06-14

评审对象：`.tasks/SK-002_part_rules_schema_design.md`

评审边界：本次只做方案评审和回执输出；未执行 SK-003，未迁移连杆规则包，未修改运行时、NX plugin、test_agent_turn/K8s、beya/tjuae，也未修改现有 skill 或 SK-002 方案正文。

## 1. 评审结论

结论：有条件通过。

是否允许进入 SK-003：允许，但只能作为“连杆规则包试点迁移”进入，且必须满足第 8 节前置条件。SK-003 不得扩大为活塞销、止推片批量迁移，不得改运行时和 NX plugin，不得把规则迁移与 TC/NX/报告链路改造混在一起。

总体判断：

1. SK-002 已经吸收 SK-001R 的主线结论：零件名、别名、参数、公式、经验默认值、单位、缺参问题、结果表行、NX 输出参数映射要求、证据来源和测试用例应迁入规则包或 fixture；skill 正文只保留通用流程、门禁和工具边界。
2. Schema 草案能覆盖连杆、活塞销、止推片的当前 Excel 公式族，并为后续新增零件提供基本扩展结构。
3. 但 schema 的若干门禁仍是文字约束或字符串数组，不够机器可验，尤其是 `parameter_id -> real NX expression` 映射门禁、公式版本/证据冲突策略、fixture schema、模板参数/驱动参数关系。
4. 因此不能判定为“通过”；可判定为“有条件通过”，允许 SK-003 在这些条件下做连杆试点，且试点包状态应保持 `draft` 或 `pilot`，不能标记为 `validated`。

未补充方案文件：本次没有修改 `.tasks/SK-002_part_rules_schema_design.md`，只新增本回执。

## 2. 参考资料核对摘要

已核对：

| 资料 | 关键结论 |
|---|---|
| `.tasks/SK-002_part_rules_schema_design.md` | 包含规则包目录、index、schema、公式语言、三零件示例轮廓、加载流程、测试策略、skill/规则包迁移边界和 SK-003 草案。 |
| `.tasks/receipts/SK-001R/AUDIT_RECEIPT.md` | 共有 HC-001 到 HC-056；与本 schema 直接相关的是零件路由、参数/公式/单位/缺参/NX 映射/test fixture；TC/NX/报告副作用门禁应保留在对应 skill 或后续元数据。 |
| `.tasks/receipts/S0-6/ACCEPTANCE_MATRIX.csv` | 确认四类输入分支、参数 ID/NX 写入门禁、关联参数、TC/NX 顺序等为验收依据；test_agent_turn/K8s 不纳入本任务。 |
| `logic-expression-design/SKILL.md` | 当前仍硬编码连杆/曲轴示例、最小测试用例位置、mm 默认单位、计算脚本协议、结果确认和 NX 门禁。SK-002 给出了迁出路径。 |
| `parameter-mapping/SKILL.md` | 当前已有统一参数类别和 NX 写入门禁；`parameter_schema.json` 中已有 `mapping.nx_expression_name`、`confirmed_by_user` 等字段，SK-002 schema 应显式复用。 |
| `conrod-design/SKILL.md` | 当前连杆参数、公式、计算脚本、确认表、NX 输出参数列表均硬编码，是 SK-003 首选试点对象。 |
| `part-design/SKILL.md` | 当前总控仍有“连杆继续加载 conrod-design”的路由硬编码；SK-002 index 设计可替代该路由，但 SK-003 需控制改动范围。 |
| 连杆 Excel | 11 个输入、4 个输出，单元格公式 `F10=(D8*B14*2)^0.5*(1/6)`，展示文本为 `((缸径*曲柄半径/2)^(0.5))*(1/6)`，期望值 20.3100960115899 与现有 skill `/3` 等价。 |
| 活塞销 Excel | 3 个边界输入、2 个经验参数、3 个输出；任务描述写 90.0mm，表格计算值使用 90.2mm；经验参数需给设计人员确认。 |
| 止推片 Excel | 6 个边界输入、5 个经验参数、7 个输出；经验参数含 `30°`，多个经验值要求计算前确认。 |
| 问题跟踪表 | 第 1-4 条支撑四类输入分支，第 8-10 条支撑关联参数和中文参数写工具门禁，第 14、26-27 条支撑报告/TC/NX 顺序门禁。 |

## 3. 覆盖 SK-001R 审计项的映射表

| SK-001R ID | SK-002 覆盖情况 | 归属判断 | 评审意见 |
|---|---|---|---|
| HC-001 | 部分覆盖 | 规则包 index + 总控路由 | `index.json` 覆盖零件识别，但 `part-design` 的连杆直连路由需在后续迁移中收敛。 |
| HC-002 | 已覆盖边界 | 保留在 skill | TC `智能体模板库` 是平台流程，不应进零件规则包。 |
| HC-003 | 已覆盖边界 | 保留在 skill | 跨工具顺序是副作用门禁，SK-002 明确不迁入规则包。 |
| HC-004 | 已覆盖 | 保留在 skill + 参数项进规则包 | 通用追问/计算/确认流程保留；具体缺参项和输出行迁入规则包。 |
| HC-005 | 部分覆盖 | 删除或合并 | Tjuae 能力映射不是本 schema 目标；后续应由能力索引收敛。 |
| HC-006 | 已覆盖边界 | 保留在 skill | 中文名禁写 NX、禁止跳过确认等全局门禁保留。 |
| HC-007 | 已覆盖 | 规则包 index | SK-002 用 `part-rules/index.json` 替代通用 skill 中的具体零件路由。 |
| HC-008 | 部分覆盖 | 保留在 skill + schema 复用 | SK-002 有五类参数枚举，但未显式 `$ref` 现有 `parameter_schema.json`。 |
| HC-009 | 已覆盖 | 保留在 skill + test fixture | SK-002 复用 `input_branch_state_machine.json` 并纳入测试策略。 |
| HC-010 | 已覆盖边界 | 保留在 skill | 计算脚本目录和 JSON 协议是执行器约定，公式内容迁出。 |
| HC-011 | 已覆盖 | 测试 fixture | SK-002 设计 `part-rules/resources/test_cases/` 接管通用最小用例。 |
| HC-012 | 已覆盖 | 规则包 | `units` 和单位解析测试覆盖 mm/毫米/deg；仍需补充单位未知阻断策略字段。 |
| HC-013 | 部分覆盖 | skill 模板 + 规则包行定义 | `confirmation_table` 已有，但 row policy、经验参数展示、冲突处理还不够机器可验。 |
| HC-014 | 已覆盖 | 保留在 skill | NX 前置条件和工具白名单保留为通用门禁。 |
| HC-015 | 已覆盖 | 规则包 | 连杆来源、别名、适用场景应进入 `conrod.json`。 |
| HC-016 | 已覆盖 | 规则包 + NX 门禁 | 具体连杆输出参数列表迁入规则包；真实 NX expression 仍必须运行时读取。 |
| HC-017 | 已覆盖 | 规则包 + fixture | 11 个输入迁入规则包，示例值进入 fixture。 |
| HC-018 | 已覆盖 | 规则包 | “曲柄半径 = 行程/2 不得默认代入”作为连杆关联/派生候选规则迁入。 |
| HC-019 | 已覆盖 | 规则包 | 四条公式迁入 `formulas`，厚度公式冲突保留 source note。 |
| HC-020 | 已覆盖 | 规则包 | required 参数和缺参追问由规则包生成。 |
| HC-021 | 已覆盖边界 | 删除或合并 | 计算脚本协议保留在 `logic-expression-design`，不在连杆 skill 重复。 |
| HC-022 | 已覆盖 | 规则包公式 + 通用执行器 | Python 公式脚本不应继续硬编码在 `SKILL.md`。 |
| HC-023 | 已覆盖 | 规则包 | 固定四行结果确认表由 `output_parameters/formulas/confirmation_table` 渲染。 |
| HC-024 | 部分覆盖 | skill 门禁 + 规则包输出列表 | NX 流程保留；四个连杆输出迁出。需补强机器可验映射 schema。 |
| HC-025 | 已覆盖 | 分拆处理 | 通用 NX 禁止项保留；连杆专属曲柄半径规则迁入规则包。 |
| HC-026 | 已覆盖 | 规则包或 fixture | `parameter-mapping` 中零件示例应从正文迁出。 |
| HC-027 | 已覆盖边界 | 删除或合并 | TC 模板库重复说明不进规则包；建议后续收敛到 TC 流程/平台配置。 |
| HC-028 | 已覆盖边界 | 删除或合并 | SQL 表名不是零件规则，不进本 schema。 |
| HC-029 | 已覆盖边界 | 保留在 skill 或配置 | 编码格式是通用数据规则，非零件规则。 |
| HC-030 | 部分覆盖 | 保留在 skill + 映射门禁 schema | SK-002 明确禁中文写 NX，但 `nx_mapping_requirements` 仍是字符串数组，应补结构化映射门禁。 |
| HC-031 | 已覆盖边界 | 保留在 nx skill | NX 工具语义边界不进规则包。 |
| HC-032 | 已覆盖边界 | 保留在 nx skill | 读 WorkPart、读 drive 参数、确认、写入、复读是通用门禁。 |
| HC-033 | 已覆盖边界 | 保留在 nx skill | 禁止中文名写 expression 属于全局安全防线。 |
| HC-034 | 已覆盖边界 | 保留在 TC skill | TC 查询规则不进零件规则包。 |
| HC-035 | 已覆盖边界 | 保留在 TC skill | TC 连接/权限契约不进规则包。 |
| HC-036 | 已覆盖边界 | 保留在 TC skill + fixture | 三维/二维打开顺序应作为流程 fixture，不是 part-rule schema。 |
| HC-037 | 已覆盖边界 | 保留在 TC skill | TC 写入确认门禁不进规则包。 |
| HC-038 | 未覆盖充分 | 后续报告模板元数据 | conrod 报告模板硬编码未被 SK-002 schema 正式吸收；不阻塞连杆规则包试点，但应列后续项。 |
| HC-039 | 已覆盖边界 | 保留在 report skill | 槽位驱动机制不进零件规则包。 |
| HC-040 | 已覆盖边界 | 保留在 report skill | 报告执行器协议不进规则包。 |
| HC-041 | 已覆盖边界 | 保留在 report skill | 工具证据链通用，不进规则包。 |
| HC-042 | 未覆盖充分 | 测试 fixture | 报告 payload 示例未纳入 SK-002 fixture 范围；建议后续报告 fixture 接管。 |
| HC-043 | 已覆盖边界 | 保留在 report skill | 当前日期/时间填充是通用能力。 |
| HC-044 | 已覆盖边界 | 保留在 report skill + fixture | 截图顺序门禁保留，原始缺陷进回归 fixture。 |
| HC-045 | 已覆盖 | 规则包 + fixture | 连杆 Excel 的参数、公式、样例均有迁移位置。 |
| HC-046 | 已覆盖 | 规则包 evidence | 连杆厚度公式证据差异已在 SK-002 source_note 中识别。 |
| HC-047 | 已覆盖 | 规则包 | 活塞销输入参数进入 `piston_pin.json` 轮廓。 |
| HC-048 | 已覆盖 | 规则包 | 活塞销经验参数和确认要求进入 associated parameters。 |
| HC-049 | 已覆盖 | 规则包 + fixture | 活塞销公式和 90.0/90.2 差异进入 evidence/fixture。 |
| HC-050 | 已覆盖 | 规则包 | 止推片 6 输入、7 输出和公式进入 `thrust_washer.json` 轮廓。 |
| HC-051 | 已覆盖 | 规则包 | 止推片经验参数、默认值、角度单位和确认时机进入 associated parameters。 |
| HC-052 | 已覆盖 | fixture + evidence | 止推片公式文本噪声应由单元格公式核对，并进入 fixture。 |
| HC-053 | 部分覆盖 | 测试 fixture | SK-002 覆盖三零件 fixture；更宽测试计划不属于本 schema。 |
| HC-054 | 已覆盖 | skill 状态机 + fixture | 四类输入分支已进入状态机和测试策略。 |
| HC-055 | 部分覆盖 | skill 门禁 + fixture | 关联参数和中文写 NX 已覆盖；TC 打开顺序为 SK-002 范围外但应保留回归。 |
| HC-056 | 部分覆盖 | report/TC skill + fixture | 报告截图和找错模型不属于 part-rule schema；不阻塞 SK-003，但需另行保留回归。 |

## 4. Schema 缺口清单

| ID | 缺口 | 严重度 | 是否阻塞 SK-003 | 处理要求 |
|---|---|---|---|---|
| GAP-001 | `parameter_spec` 未显式复用 `parameter-mapping/resources/parameter_schema.json` 的 `source/value/evidence/mapping/status` 结构。 | P1 | 不阻塞试点，但阻塞 validated | SK-003 至少要声明静态规则包参数如何转成统一参数记录。 |
| GAP-002 | `nx_mapping_requirements` 只是字符串数组，缺少结构化 `parameter_id -> drive_parameter.nx_expression_name` 映射计划 schema。 | P0 | 条件阻塞 NX 写入相关验收 | SK-003 测试必须用 mock NX drive 参数验证：表达式名只能来自 NX 读取结果。 |
| GAP-003 | `template_parameter`、`drive_parameter` 只在参数类别枚举中出现，没有 top-level 关系建模。 | P1 | 不阻塞边界公式试点 | 若 SK-003 覆盖“设计参数齐全”分支，需增加 template required 参数与 output parameter 的映射规则。 |
| GAP-004 | 公式版本主要隐含在 `formula_id`，缺少显式 `formula_version`、`effective_from`、`supersedes`、`review_status`。 | P1 | 不阻塞 draft | 连杆厚度这种证据冲突必须保持 `draft/pilot`，不能标 validated。 |
| GAP-005 | 缺少事实来源优先级和证据冲突状态。 | P0 | 条件阻塞 validated | Excel 单元格公式、展示文本、现有 skill 脚本冲突时，必须保留冲突并要求业务确认。 |
| GAP-006 | `default_candidate` 能表达默认候选，但无法完整区分样例值、经验参数、模板默认值和用户确认默认值。 | P1 | 不阻塞连杆，影响活塞销/止推片 | 建议增加 `value_origin` 或确认状态，避免把 Excel 样例当运行默认。 |
| GAP-007 | `supported_branches` 只声明支持哪些分支，没有分支级 required/optional/skip/merge/conflict policy。 | P1 | 不阻塞基础试点 | 混合参数分支验收时要补冲突合并规则。 |
| GAP-008 | `confirmation_table` 只定义列，不定义输出行、经验参数行、冲突行的生成规则和用户决策字段。 | P1 | 不阻塞基础试点 | 结果确认、经验参数确认和冲突确认应分别可断言。 |
| GAP-009 | `test_cases` 只是引用，没有 fixture schema。 | P1 | 条件阻塞 SK-003 验收 | SK-003 必须至少落地 conrod cases 的输入、期望输出、期望状态、负向断言和 mock NX 数据。 |
| GAP-010 | `mc_formula_v1` 对当前三零件足够，但不支持条件公式、查表、分段规则、约束求解、材料/枚举值。 | P2 | 不阻塞 SK-003 | 后续新增复杂零件时需升级公式语言版本。 |
| GAP-011 | `index.json` 没有别名冲突、优先级、禁用原因和候选追问策略字段。 | P2 | 不阻塞 SK-003 | 新增零件时应防止多个零件别名命中后直接计算。 |
| GAP-012 | `piston_pin.json`、`thrust_washer.json` 示例是轮廓，不满足完整 schema required 字段。 | P2 | 不阻塞连杆试点 | 文档应继续标注为非可运行示例，避免被当作 fixture。 |

## 5. 对三类零件和后续新增零件的支撑判断

| 零件 | 支撑判断 | 条件 |
|---|---|---|
| 连杆 | 可支撑 SK-003 试点。 | 需要保留厚度公式证据冲突，完整迁移 11 个输入、4 个输出、公式、单位、缺参追问、确认表、NX 输出映射要求和 fixture。 |
| 活塞销 | Schema 能表达。 | 必须强化经验参数确认，尤其 `0.1` 和 `12.5` 不能静默当最终输入；90.0/90.2 差异进入 evidence/fixture。 |
| 止推片 | Schema 基本能表达。 | 必须支持计算前确认多个经验参数，并规范 `30° -> deg`；公式文本噪声需按单元格公式核对。 |
| 后续新增零件 | 可作为 v1alpha1 基线。 | 若新增零件存在分段公式、查表、材料枚举、约束求解或复杂模板参数映射，需要升级 schema 和公式语言。 |

## 6. Skill 保留内容清单

以下内容应保留在 skill，不迁入零件规则包：

| 位置 | 应保留内容 |
|---|---|
| `part-design/SKILL.md` | 任务归口、模型生命周期状态机、TC 模板候选确认、三维/二维/报告顺序、全局禁止事项、工具成功证据优先。 |
| `logic-expression-design/SKILL.md` | 加载规则包、schema 校验、归一化参数、四类输入分支、缺参/确认/冲突通用流程、计算脚本执行协议、结果确认前禁止 NX 写入。 |
| `parameter-mapping/SKILL.md` | 中文语义到标准参数 ID/候选表达式的映射流程、数据库查询边界、NX 写入前真实 drive 参数映射门禁。 |
| `conrod-design/SKILL.md` | SK-003 后只保留薄调度或兼容入口：识别连杆任务后加载 `part-rules` 和通用流程；不得再保留完整参数表、公式脚本和固定结果表。 |
| `nx-parameter/SKILL.md` | `nx_update_param` / `nx_batch_update_params` 的副作用边界、读取 WorkPart、读取真实 drive 参数、映射确认、写入后复读。 |
| `teamcenter-flow/SKILL.md` | TC 模板查询、模型打开、文件生命周期和上传确认门禁。 |
| `design-report/SKILL.md` | 报告模板检查、槽位渲染、截图顺序、validate/generate 执行器协议；具体 conrod 模板名后续应迁入报告模板元数据。 |

## 7. 规则包迁移内容清单

以下内容应进入 `part-rules/resources/parts/*.json` 或规则包 index：

1. `part_id`、`part_name`、别名、适用场景、排除场景、启用状态和版本。
2. 输入参数、边界参数、发动机/装配参数、模板参数候选、输出设计参数、关联参数。
3. 参数 ID、中文名、别名、单位、值类型、required/optional、默认候选、经验参数确认策略。
4. 缺参追问的参数级问题、示例格式和单位提示。
5. 公式 ID、表达式、展示表达式、依赖、单位、容差、计算顺序、公式版本、证据引用。
6. 证据来源：Excel 文件、sheet/range、现有 skill、业务确认记录、source_note。
7. 结果确认表的输出行、经验参数行、冲突行和展示列配置。
8. 每个零件必须映射的输出参数列表，以及 NX 映射前置要求。
9. 零件专属注意事项，例如连杆曲柄半径不得默认由行程代入、连杆厚度公式证据冲突、活塞销经验间隙确认、止推片角度单位。

## 8. Fixture/Test 迁移内容清单

以下内容应进入 `part-rules/resources/test_cases/*.cases.json` 或后续 fixture：

1. 连杆完整输入、缺参输入、混合参数、单位解析、公式回归、禁止中文参数名写 NX 的用例。
2. 活塞销完整输入、缺参输入、经验参数确认、90.0/90.2 差异回归用例。
3. 止推片完整输入、缺参输入、多个经验参数计算前确认、`30°` 单位解析、公式文本噪声回归用例。
4. 问题跟踪表第 1-4 条四类输入分支原始需求，作为流程验收 fixture。
5. 问题跟踪表第 8-10 条关联参数同步和中文参数写工具问题，作为 NX 映射门禁负向用例。
6. 问题跟踪表第 14、26-27 条报告截图、找错模型、先打开二维图纸问题，保留到 report/TC/NX 回归 fixture。
7. `logic-expression-design/resources/minimal_test_cases.json` 中三零件最小用例应迁出或复制到新 fixture，通用 skill 资源中只保留过渡说明。
8. fixture 必须包含：输入文本、结构化输入、期望缺失项、期望输出、期望下一状态、经验参数确认要求、负向断言、mock NX drive 参数列表。

## 9. SK-003 前置条件

允许进入 SK-003 的前置条件如下：

1. SK-003 只做连杆规则包试点，不迁移活塞销和止推片。
2. SK-003 不修改运行时、NX plugin、test_agent_turn/K8s、beya/tjuae。
3. 新增或调整的资源应限定在 `part-rules` 规则包、连杆规则包、连杆 fixture，以及必要的 skill 薄调度说明。
4. `conrod.json` 必须使用稳定 `parameter_id`，公式依赖必须只引用 `parameter_id`，不得用中文名作为可执行变量。
5. 连杆厚度公式必须保留证据冲突说明；未获业务确认前，规则包状态只能是 `draft` 或 `pilot`。
6. `conrod.cases.json` 必须覆盖完整输入、缺参输入、混合参数、单位解析、公式回归和 NX 映射门禁负向用例。
7. NX 写入相关验收只能使用 mock drive 参数或读取结果做门禁断言，不得实际调用 NX 写工具。
8. `conrod-design/SKILL.md` 迁移后不得再保留完整 REQUIRED 列表、Python 公式脚本和固定四行确认表。
9. `logic-expression-design/SKILL.md` 如需更新，只能描述从 `part-rules/index.json` 加载、校验、计算和确认的通用流程，不得写入连杆公式。
10. 现有工作区已有大量与本任务无关的变更；SK-003 必须避免整理、回退或混入无关文件。

## 10. SK-003 验收标准

1. `part-rules/resources/schemas/part_rule_package.schema.json` 和 `index.json` 存在，conrod 包能通过 schema 校验。
2. `parts/conrod.json` 包含 11 个输入、4 个输出、单位、缺参追问、公式、证据来源、确认表配置、NX 映射要求和测试引用。
3. 完整输入 fixture 得到当前既有期望值：中心距 212、大头 88、小头 51、厚度 20.3100960115899。
4. 缺参 fixture 只输出缺失项，不生成 NX 写入计划。
5. 混合参数 fixture 对用户给定设计参数与计算值冲突输出冲突表，未确认前不合并。
6. 单位 fixture 支持 `mm`、`毫米`，并阻断未知单位。
7. NX 门禁 fixture 证明中文名、规则包输出名、模板字段名均不能直接作为 `expression_name`。
8. `conrod-design/SKILL.md` 不再包含完整公式实现和计算脚本大段代码。
9. 未确认计算结果或未确认映射时，不允许出现 NX 写工具调用方案。

## 11. 风险和建议

| 风险 | 影响 | 建议 |
|---|---|---|
| SK-002 文档末尾已有 SK-003 提示词草案 | 容易被误用为直接执行提示词 | 本评审不复写执行提示词；建议后续把执行提示词与设计方案分离。 |
| NX 映射门禁仍偏文字化 | 可能迁移后仍靠模型纪律防错 | 在 SK-003 fixture 中强制 mock NX drive 参数和负向断言。 |
| 公式证据冲突未业务确认 | 连杆厚度可能被静默固化为错误事实 | 规则包保留冲突，pilot 可回归现有值，validated 前必须业务确认。 |
| 样例值与默认值混淆 | 可能把 K08、350、90.2、123 当成默认设计值 | schema/fixture 明确 `sample_value` 与 `default_candidate` 的区别。 |
| 活塞销和止推片经验参数更多 | 连杆试点通过不代表复杂经验参数确认已成熟 | 连杆之后再用活塞销验证 `with_result_confirmation`，用止推片验证 `before_calculation` 和角度单位。 |
| 报告模板硬编码未纳入本 schema | 非连杆报告仍可能套错模板 | 另开报告模板元数据任务，不阻塞 SK-003 连杆规则包。 |
| 新增零件可能需要查表/分段公式 | `mc_formula_v1` 当前能力有限 | 保持 v1alpha1，后续按复杂零件升级公式语言。 |
| 现有工作区很脏 | 容易把无关运行时/NX/plugin变更混入迁移 | SK-003 必须只提交规则包和相关 skill/fixture 文件。 |

最终建议：允许 SK-003 进入连杆规则包试点迁移，但以“有条件通过”为准；SK-003 的主要目标应是把 SK-002 的 schema 从方案草案压实为可校验资源和可回归 fixture，而不是开始批量迁移多个零件或改动运行时链路。
