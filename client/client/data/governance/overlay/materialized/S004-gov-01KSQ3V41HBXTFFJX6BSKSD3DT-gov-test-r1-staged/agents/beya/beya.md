@id: [[agent.beya]]
@type: agent
@scope: local
@status: active
@version: 0.6.0
@private_workspace: read_write
@public_workspace: read_only
@max_rounds: 30

# Beya

## 用途

Beya 是用户侧基础 Agent，运行在客户机 Python client 中。它通过 AI 服务 Runtime
Bridge 调用云端 LLM proxy 和平台工具，但本地 AgentLoop、资产、workspace、profile
和 NX 工具注册都由客户机维护。

## 技能

- [[skill.agentloop-core]]
- [[skill.agentloop-core.agent-builder]]
- [[skill.agentloop-core.code-review]]
- [[skill.agentloop-core.mcp-builder]]
- [[skill.agentloop-core.pdf]]

## 工具

- [[tool.workspace]]
- [[tool.profile]]
- [[tool.local_file]]
- [[tool.nx]]
- [[tool.platform]]

## 工作区策略

- 用户私有数据：`client/data/profile`、`client/data/workspace`、`client/data/sessions`。
- 运行日志：`client/logs`。
- 安装态资产：`client/resources/agent_assets.mcdpkg`，只读加载。
- 研发态资产源：`assets/source`，只在研发仓和打包阶段使用。
