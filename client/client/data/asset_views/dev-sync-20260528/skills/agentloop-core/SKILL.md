---
name: agentloop_core
description: Beya 用户侧基础运行技能
capabilities:
  - local.workspace.read
  - local.workspace.write
  - local.workspace.exec
  - local.tool.registry
---

# Beya 用户侧基础运行技能
@id: [[skill.agentloop_core]]
@type: skill
@scope: local
@status: active
@version: 0.3.0

Beya 的主运行链路是 MCP -> AI Service Runtime Bridge -> customer-side Python
client -> AgentLoop。AI 服务只负责 MCP 入口、LLM proxy、平台工具代理和资产版本元
数据；AgentLoop、SessionState、workspace、profile、AssetStore 和本地/NX 工具注册
都在用户侧 Python client 中运行。

## Principles

1. 多步骤工作优先维护显式任务状态，记录目标、进展、阻塞和结果。
2. 工具调用必须走 Python client 的统一 ToolRegistry，由 registry 按
   `source=local|nx|platform` 路由。
3. NX 工具由本地 NX 插件提供 loopback API。Agent 只处理标准化工具结果，不关心端口、
   NX 启动顺序或重连细节。
4. 本地资产通过 `client/resources/agent_assets.mcdpkg` 和 AssetStore 读取；云端资产
   接口只返回版本、授权、hash 和更新元数据。
5. 文件、workspace、profile、日志和诊断能力在用户侧执行；LLM 和平台连接器通过唯一
   AI 服务 WebSocket 请求云端代理。
6. 修改前先精确读取，副作用动作仍遵守用户确认和业务边界。

## Boundaries

基础运行技能只描述用户侧运行规则，不硬编码 NX、TC、MySQL、报告等业务流程。领域能力
仍通过对应 Skill 激活，并通过同构工具注册表调用。
