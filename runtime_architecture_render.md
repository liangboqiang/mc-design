# Runtime 架构与测试数据渲染

数据来源：

- `client/client/data/.runtime/88000044/conversations/codex-skill-fix-check-20260529-normal/agents/design_agent/events.jsonl`
- `client/client/data/.runtime/88000044/conversations/codex-skill-fix-check-20260529-normal/agents/design_agent/artifacts/turn-76d4a839b52f4d96b49a0a3285f0be5a/L001-request.json`
- `client/client/data/.runtime/88000044/conversations/codex-skill-fix-check-20260529-normal/agents/design_agent/artifacts/turn-76d4a839b52f4d96b49a0a3285f0be5a/L002-request.json`
- `client/client/data/.runtime/88000044/conversations/codex-skill-fix-check-20260529-normal/agents/design_agent/artifacts/turn-76d4a839b52f4d96b49a0a3285f0be5a/L003-request.json`

## 架构图

```mermaid
flowchart LR
  User["用户 / NX / Web UI"] --> API["Client API<br/>/api/chat/turns"]
  Cloud["AI Service MCP<br/>agent stream tools"] --> Bridge["ClientBridge<br/>WebSocket"]
  API --> App["ClientApp"]
  Bridge --> App
  App --> Host["RuntimeHost"]

  Host --> Control["Control Router<br/>/gov /confirm"]
  Host --> GovRoute["Governance Router<br/>active /gov routes to governance_agent"]
  Host --> Journal["Journal<br/>user/conversation/agent isolated"]

  Host --> Runner["Runner<br/>round loop / effects / confirm"]
  Runner --> Registry["Registry<br/>agents / skills / tools / policies"]
  Runner --> Projector["Projector<br/>PromptFrame builder"]
  Runner --> LLM["LLM request<br/>llm.chat"]
  Runner --> ToolExec["Tool Dispatch"]

  Registry --> Assets["AssetStore<br/>agent_assets.mcdpkg + overlays"]
  Registry --> LocalTools["Local/NX/Workspace tools"]
  Registry --> PlatformSpecs["Platform tools list<br/>via ClientBridge"]

  Projector --> Prompt["PromptFrame<br/>system + messages + tools + budget"]
  ToolExec --> LocalTools
  ToolExec --> PlatformCall["platform.tool.call"]
  PlatformCall --> Bridge
  Bridge --> RuntimeBridge["AI Service RuntimeBridge"]
  RuntimeBridge --> PlatformTools["MySQL / External / Teamcenter"]
  Runner --> Journal
```

## 运行时序图

```mermaid
sequenceDiagram
  participant U as User/API
  participant H as RuntimeHost
  participant R as Runner
  participant P as Projector
  participant G as Registry
  participant L as LLM
  participant T as Tool Dispatch
  participant B as ClientBridge
  participant S as AI Service Tools
  participant J as Journal

  U->>H: TurnCommand(agent_id=design_agent, query)
  H->>H: _control_command, _route_governance_command
  H->>J: open conversation/agent journal
  H->>R: run(command)
  R->>J: turn.started, message.user

  R->>P: prompt(round=1, loaded_skills=[])
  P->>G: visible_tools(design_agent, [])
  G-->>P: [load_skill]
  P-->>R: PromptFrame(tools=1, available_skills)
  R->>L: llm.chat L001
  L-->>R: tool_call load_skill(external-connector-adapter)
  R->>T: dispatch(load_skill)
  T->>G: validate skill visibility + load SKILL.md
  G-->>T: skill content
  T-->>R: tool.completed
  R->>J: tool.completed(load_skill)

  R->>P: prompt(round=2, loaded_skills=[external-connector-adapter])
  P->>G: skill_tool_refs -> tool.external
  G-->>P: load_skill + workspace read + external tools
  R->>L: llm.chat L002
  L-->>R: tool_call query_ipm_list({})
  R->>T: dispatch(query_ipm_list)
  T->>B: platform.tool.call
  B->>S: ExternalTools.query_ipm_list
  S-->>B: IPM result(total=21)
  B-->>T: ok result
  T-->>R: tool.completed(query_ipm_list)
  R->>J: tool.completed(query_ipm_list)

  R->>P: prompt(round=3, tool result in messages)
  R->>L: llm.chat L003
  L-->>R: final answer
  R->>J: turn.completed(success)
  H-->>U: streamed final content
```

## 本轮事件 Trace

| seq | event | round | 关键数据 |
|---:|---|---:|---|
| 1 | `turn.started` | - | mode=`normal` |
| 2 | `message.user` | - | 本地测试注入的中文在 artifact 中有编码损伤，业务链路不受影响 |
| 3 | `context.built` | 1 | `tool_count=1`, `context_chars=4805`, visible tool: `load_skill` |
| 4 | `llm.completed` | 1 | tool call: `load_skill` |
| 5 | `tool.requested` | 1 | `load_skill({"name":"external-connector-adapter"})` |
| 6 | `tool.completed` | 1 | loaded skill ok, capabilities: `tool.external`, `tool.workspace.read` |
| 7 | `context.built` | 2 | `tool_count=7`, loaded skill: `external-connector-adapter` |
| 8 | `llm.completed` | 2 | tool call: `query_ipm_list` |
| 9 | `tool.requested` | 2 | `query_ipm_list({})` |
| 10 | `tool.completed` | 2 | IPM returned `total=21` |
| 11 | `context.built` | 3 | query result appears as `role=tool` message |
| 12 | `llm.completed` | 3 | final answer, no tool calls |
| 13 | `turn.completed` | 3 | status=`success` |

## PromptFrame 示例

### L001-request: 初始轮

```text
tools:
- load_skill

loaded_skills: []

budget:
active_revision: 3
char_budget: 8000
context_chars: 4805
message_count: 2
round: 1
tool_count: 1

runtime_context excerpt:
available_skills:
- design-data-query tools=tool.mysql.query
- teamcenter-flow tools=tool.teamcenter.file,tool.teamcenter.query,tool.teamcenter.write,tool.workspace.read,tool.workspace.write
- external-connector-adapter tools=tool.external,tool.workspace.read

Load the matching skill from available_skills before using its tools;
do not ask the user for a skill name when the list already contains a matching domain skill.
```

这一轮只能调用 `load_skill`。这是预期行为：runtime 先让模型从 `available_skills` 选择领域 Skill。

### L002-request: 加载 external-connector-adapter 后

```text
tools:
- load_skill
- local_file_read
- local_workspace_status
- profile_get
- connect_qpp
- query_ecr_list
- query_ipm_list

loaded_skills:
- external-connector-adapter

messages:
[0] runtime_context
[1] user query
[2] assistant tool_call(load_skill)
[3] tool result(load_skill): SKILL.md content with tool.external capability
```

这一轮 `query_ipm_list` 已经可见，模型实际选择了它。

### L003-request: IPM 工具返回后

```text
tools:
- load_skill
- local_file_read
- local_workspace_status
- profile_get
- connect_qpp
- query_ecr_list
- query_ipm_list

loaded_skills:
- external-connector-adapter

messages:
[0] runtime_context
[1] user query
[2] assistant tool_call(load_skill)
[3] tool result(load_skill)
[4] assistant tool_call(query_ipm_list)
[5] tool result(query_ipm_list): ok=true, total=21
```

这一轮模型不再调用工具，直接基于 `query_ipm_list` 的工具结果生成最终回复。

## 检查点

1. `tool_count` 从 1 增加到 7，说明 Skill-gated tool activation 生效。
2. `query_ipm_list` 在加载 `external-connector-adapter` 前不可见，加载后可见，符合安全模型。
3. 本次没有 `effect.pending`，说明 IPM 查询没有走高风险确认；之前看到的 `/confirm` 是 `/gov` 治理模式文本，不是工具执行确认。
4. 如果 `/gov` active，普通业务请求会被路由到 `governance_agent`，业务 Skill 会不可见。这是定位工具“确认后也执行不了”的关键原因。
5. 当前 profile 里 `context.budget=1200`，但 Projector 有最低 `char_budget=8000` 保护，所以实际 prompt budget 是 8000；这里需要团队确认这是不是期望策略。
