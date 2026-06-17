# Tjuae 测试后审查与能力沉淀策略

本文件记录 mc-design 监管侧固定策略。它不是运行时提示词，不直接进入 `agent_assets.mcdpkg`。

## 1. 基本原则

测试不是终点。每次完成一项测试后，应补做一次审查，判断测试暴露出的知识、规则、边界和可复用动作是否需要沉淀到项目能力中。

审查顺序固定为：

1. 判断是 tjuae 通用能力、mc-design 客户端能力、业务 skill 能力，还是外部系统/网络问题。
2. 判断测试结果是通过、失败、阻塞、偶发、环境不可用，还是需求口径变化。
3. 判断是否需要新增或更新 `examples`、`resources`、`scripts`、`templates`、`TOOL.md`、`SKILL.md` 或 Python 本地工具。
4. 判断是否需要新增回归测试，防止同类问题复发。
5. 记录无法由 tjuae 通用项目提供的能力，不要求 tjuae 做 mc-design 定制。

## 2. Tjuae 支持情况

调研依据：`F:\Documents\tjuae` 当前代码和文档。

可依赖的通用能力：

- 项目级 skill：tjuae 原生从工作目录下 `.tjuae/skills/<name>/SKILL.md` 发现 skill。
- Skill 目录变量：`SKILL.md` 可使用 `${CLAUDE_SKILL_DIR}` 指向 skill 所在目录。
- Skill frontmatter：支持 `description`、`when_to_use`、`allowed-tools`、`context`、`model`、`paths`、`hooks` 等。
- Python SDK：支持 session create/history/reuse/close、chat run/stream/respond、plugins install/reload/list、tools list/execute、providers/settings、readiness/diagnostics。
- 插件工具：支持通用 HTTP remote executor，错误会以 `tool_failed` 语义事件暴露。
- 事件流：支持 content/reasoning delta、tool started/completed/failed、question/permission/plan interaction、final completed、failed。

mc-design 当前集成方式：

- 源资产：`mc-design-nx/assets/source`
- 打包资产：`mc-design-nx/client/resources/agent_assets.mcdpkg`
- 运行投影：`mc-design-nx/client/data/asset_views/runtime-agentloop`
- tjuae skill 发现目录：`mc-design-nx/client/data/workspace/.tjuae/skills`
- mc-design 的 asset 打包白名单已包含 `resources`、`scripts`、`templates`、`examples`。

结论：复杂业务能力优先沉淀在 `assets/source/skills/<skill>/` 下，而不是要求 tjuae 提供 mc-design 专用接口。

## 3. 内容放置策略

放到 `SKILL.md`：

- 工作流顺序、前置条件、用户确认规则、禁止事项。
- 何时加载其他 skill、何时使用本地工具或 connector。
- 少量稳定的业务原则和流程约束。

放到 `resources/`：

- 可机读规则、schema、状态机、参数分支、固定枚举。
- 业务规则的结构化来源摘要。
- 不随单次会话变化的标准材料。

放到 `scripts/`：

- 可重复执行的计算、转换、校验、模板填充、报告生成。
- 需要精确输出 JSON、不能靠模型自由发挥的业务逻辑。
- 脚本应能由客户端内置 Python 运行，并优先使用标准库或已打包依赖。

放到 `examples/`：

- 测试通过的最小正例、缺参例、失败例、边界例。
- 回归复现 payload 和期望输出。
- 能被脚本或测试直接读取的 JSON 样例。

放到 `templates/`：

- DOCX/XLSX 等稳定模板。
- 模板应有配套 schema、检查脚本或测试。

做成 Python 本地工具：

- 需要被 tjuae tool registry 直接调用。
- 需要访问本地文件、DFMEA 模板、设计流程状态或客户端安全边界。
- 需要稳定输入输出 schema，并要出现在 `tool_execution_map.json`。

做成 NX plugin 工具：

- 只限 NX 会话内能力，例如打开部件、查询视图、切换视图、截图、查询/修改表达式。
- 文件桥、通用脚本执行、通用上下文管理不得放入 NX plugin。
- 自动出图和 Sheet 级图纸工具禁用；图纸只允许通过 `nx_open_tcpart` 打开已绑定图纸。

## 4. 测试后审查清单

每次测试完成后建议审查：

- 这次测试验证的是 tjuae 支持、mc-design adapter、客户端工具、skill 规则，还是外部系统可用性？
- 是否走了合适入口，例如本地全链路优先走 `POST /api/runtime/test/call-agent`，需要补充输入时走 `POST /api/runtime/test/respond-agent`。
- `call_agent` 是否模拟真实用户自然输入？不要为了让测试通过，在入口或测试 payload 中额外注入隐藏的 `allowed_tools`、`forbidden_tools` 或“必须调用某工具”的特制约束；如果确需做定向工具诊断，应单独标记为工具诊断，不能记为真实用户闭环通过。
- 测试结论是否经过完整 JSONL 日志审计？会话 summary 只能快速判断工具事件，不能替代 JSONL 对工具输出、`conversation_id`、建模计划、阻断项和副作用门禁的深度检查。
- 测试中使用的输入是否应沉淀成 `examples/*.json`？
- 测试中验证的业务规则是否应沉淀成 `resources/*.json`？
- 测试中重复的人工作业是否应沉淀成 `scripts/*.py`？
- 测试中出现的禁止事项或前置条件是否应写入 `SKILL.md` 或 `TOOL.md`？
- 是否需要新增测试验证 asset 包投影后，`.tjuae/skills` 中仍能读取资源和执行脚本？
- 是否误把 Excel、脚本、规则文件中的参数名当成设计参数唯一真相源？设计参数 ID/名称唯一真相源仍是 MySQL 参数词典。
- 是否误把外部网络问题归为 mc-design 缺陷？QPP 外部接口不通不计入缺陷队列，除非本地错误处理有问题。

## 5. 沉淀验收标准

新增或修改 business skill 能力时，至少满足：

- asset 打包测试能证明新增 `resources/scripts/examples/templates` 被打入 `agent_assets.mcdpkg`。
- 本地 `call_agent` 测试能证明投影并同步到 `.tjuae/skills` 后可读取资源、执行脚本。
- 脚本输出必须是结构化 JSON，包含 `ok/code/message` 或明确的业务结果字段。
- 业务脚本不得依赖开发机绝对路径。
- 业务规则不得要求 tjuae 修改 mc-design 专用能力；只能使用 tjuae 已有通用 session/chat/tool/plugin/skill 能力。
- 重要测试必须留下执行回执或审计回执，并指定产物路径。
- 零部件设计闭环测试必须能用 `part-design/scripts/validate_design_flow_turn.py` 对 JSONL 日志审计；五个 `design_flow` 状态工具完成只是必要条件，`conversation_id` 不一致、工具失败、建模计划缺失或出现未确认副作用时，不能封闭。

## 6. 后续派发任务要求

派发给其他智能体的任务必须包含：

- 任务编号。
- 是否可并行；若有顺序阻塞，必须明确写“不得并行”。
- 工作目录。
- 参考文件和预期修改位置。
- 审计回执或执行回执输出路径。
- 测试命令和结果要求。
- 禁止事项，尤其是 tjuae 不做 mc-design 定制、NX 自动出图禁用、设计参数字典以 MySQL 为唯一真相源。
