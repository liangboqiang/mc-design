---
name: agent-builder
description: Agent Builder
capabilities:
  - tool.workspace.read
  - tool.workspace.write
  - tool.workspace.exec
---

# Agent Builder

用于构建任意领域的 AI Agent：客服、研究、运营、创意工作，或专门的业务流程。

## 核心哲学

> **模型本来就知道如何成为 Agent。你的工作是少挡路。**

Agent 不是复杂工程。它是一个邀请模型行动的简单循环：

```text
LOOP:
  模型看到：上下文 + 可用能力
  模型决定：行动或回复
  若行动：执行能力，加入结果，继续循环
  若回复：返回给用户
```

就是这样。魔力不在代码里，而在模型里。代码只需要提供清晰的边界和可用的工具。

## 架构准则

1. **循环要薄**：运行时只负责消息、工具、结果和终止条件。
2. **能力要原子化**：工具越小越稳定，职责越清晰越容易组合。
3. **上下文要按需进入**：用 Skill、文件读取和任务状态扩展上下文，不要一次性注入全部资料。
4. **状态要显式**：todo、任务、文件和运行日志都应成为可检查的外部状态。
5. **少写规则，多给工具**：让模型基于工具和观察选择下一步，而不是把所有分支写进 Python。
6. **先做单 Agent 闭环**：单 Agent 稳定后，再引入子 Agent、审批、团队通信和 worktree 隔离。

## 最小 Agent 循环

```python
history = []
while True:
    response = model(system=system_prompt, messages=history, tools=tools)
    history.append(response)

    if response.finish_reason != "tool_calls":
        return collect_text(response)

    tool_results = []
    for call in response.tool_calls:
        result = dispatch_tool(call.name, call.input)
        tool_results.append(result)
    history.append({"role": "user", "content": tool_results})
```

## 能力分层建议

### Level 0：一个 shell 工具

适合原型。一个 `bash` 足以完成读取、搜索、运行测试和简单写入。

### Level 1：四个基础工具

```text
bash
read_file
write_file
edit_file
```

覆盖大多数代码和文件任务。

### Level 2：增加任务跟踪

加入 `todo`，让多步骤任务显式化，减少模型遗忘和跳步。

### Level 3：增加 Skill

加入 `load_skill`，把领域知识按需加载，而不是全部塞进系统提示词。

### Level 4：增加子 Agent

加入 `Task` 或子 Agent 工具，用于隔离探索、规划、审查和并行子任务。

## 设计 Agent 时先回答的问题

- 这个 Agent 的主要任务是什么？
- 它必须读写哪些外部世界？
- 哪些能力应该做成工具？
- 哪些知识应该做成 Skill？
- 哪些状态必须持久化？
- 什么时候需要用户审批？
- 哪些操作危险，必须加权限或隔离？

## 推荐文件结构

```text
my-agent/
  agent.py              # 运行循环
  tools.py              # 工具定义和实现
  skills/               # 按需加载的能力说明
  workspace/            # Agent 可操作文件区
  data/<runtime-root>/<user>/conversations/<conversation>/agents/<agent>/  # 运行态、日志、任务状态
```

## 常见反模式

- 把业务分支写死到循环里。
- 让每个领域都拥有一套新 runtime。
- 在系统提示中塞入所有文档。
- 工具过大，一个工具承担多个职责。
- 工具 schema 不稳定或没有边界。
- 没有工作区隔离，工具可以随意读写系统文件。
- 没有任务状态，多步骤工作只靠模型记忆。

## 与 Beya 的对应关系

- `agentloop_core/` 是薄 Harness 和稳定 loop。
- `tools/base/` 是原生基础工具箱。
- `skills/agentloop_core/` 是冻结的原生 Skill 包。
- `agents/*/beya.md` 是 Agent 装配文件。
- `client/data/<runtime-root>/<user_id>/conversations/<conversation_id>/agents/<agent_id>` 是按会话和 Agent 分区的运行态。
- `workspaces/private/<user_id>` 是用户私有空间。
- `workspaces/public/<agent_id>` 是 Agent 公用空间。

## 参考材料

- `references/agent-philosophy.md`：Agent 设计哲学。
- `references/minimal-agent.py`：最小 Agent 示例。
- `references/subagent-pattern.py`：子 Agent 模式。
- `references/tool-templates.py`：工具模板。
- `scripts/init_agent.py`：新 Agent 脚手架生成脚本。
