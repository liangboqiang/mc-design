---
name: context-governance
description: 上下文和 Prompt 策略治理 Skill
capabilities:
  - tool.governance.asset
  - tool.governance.write
  - tool.governance.policy
---

# context-governance

@id: [[skill.context_governance]]
@type: skill
@scope: platform
@status: active
@version: 0.3.0

@uses.tool:
- [[tool.governance]]

@governed.by: [[agent.governance_agent]]

## 目标

用于治理 Agent 上下文策略、压缩策略、prompt policy、Skill 激活边界、auto gov 复盘策略和运行时可读视图。

## 规则

1. auto gov 的用户级开关、触发点和模式使用 `gov_policy_get`、`gov_policy_set` 管理，默认开启、会话结束触发、低风险自动启用。
2. 自然语言上下文策略写入 hot overlay 中的 context policy 资产，必须走 stage、diff、validate，并提示用户输入 `/confirm`。
3. 机器参数类上下文预算写入当前用户 profile，不写成长文本知识库。
4. 不得把完整会话、完整工具结果或大量运行时流水塞进 Prompt。
5. 上下文策略优先级低于当前用户指令、正式 Skill、Tool schema 和真实工具结果。
6. 修改前必须读取目标 Agent、相关 Skill、当前 runtime prompt/context 记录和 auto gov 审计结果。

## 输出

回复应说明策略要解决的问题、注入位置、预算影响、误导风险、热生效范围、验证方式和是否等待用户输入 `/confirm`。
