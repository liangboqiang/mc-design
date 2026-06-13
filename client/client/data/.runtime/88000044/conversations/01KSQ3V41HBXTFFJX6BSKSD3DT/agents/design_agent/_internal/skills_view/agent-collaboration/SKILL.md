---
name: agent-collaboration
description: Beya Agent 协作技能
capabilities:
  - tool.collaboration.board
  - tool.collaboration.mailbox
  - tool.collaboration.publish_log
  - tool.collaboration.agents
---

# agent-collaboration

## 适用场景

用于需要多个 Agent 通过 Board、Mailbox 和 PublishLog 协作推进的任务。

## 工作方法

1. 用 Board 表达任务、状态、阻塞和结果；不要把复杂工作只放在单个 Agent 的临时清单里。
2. 用 `spawn_agent` 补充新的 Agent 能力；新 Agent 自己观察 Board / Mailbox / PublishLog 并运行同一个 Loop。
3. 用 `publish` 将公共发现、阶段结论和可复用文件摘要写入 PublishLog。
4. 用 `mailbox_send` 只发送必要的定向通知；能通过 Board / PublishLog 表达的协作信息优先不要走点对点消息。
5. 需要留痕时使用 `publish` 写入 PublishLog；需要回看时使用 `read_publish_log`。
6. 涉及 NX 修改、报告导出、Teamcenter 上传/复制、数据库写入等副作用动作时，仍需用户确认。

## 边界

- 不让 Agent 直接调用另一个 Agent 或另一个 Loop。
- 不把协作日志当成知识真相或长期资产真相。
- 不向用户索要 `user_id`、`conversation_id`、服务器地址、token 等运行时字段。
