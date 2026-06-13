---
name: tool-governance
description: 工具说明、工具启停、schema 视图和 adapter 治理 Skill
capabilities:
  - tool.governance.asset
  - tool.governance.write
  - tool.governance.policy
---

# tool-governance

@id: [[skill.tool_governance]]
@type: skill
@scope: platform
@status: active
@version: 0.4.0

@uses.tool:
- [[tool.governance]]

@governed.by: [[agent.governance_agent]]

## 目标

用于治理工具说明、工具使用策略、失败 fallback、参数建议、可见性偏好、禁用边界、工具 schema 视图策略和本机 adapter。

## 规则

1. 用户级工具启停使用 `gov_policy_get` 和 `gov_policy_set`，支持按工具名、owner 或 group 启停。
2. 策略、列表、模型类治理自救工具不得禁用，避免用户无法恢复治理能力。
3. 工具 schema 视图策略使用 `gov_schema_policy_get/stage/diff/validate`，可以隐藏 Agent 可见参数、追加说明、调用前剔除隐藏参数。
4. 工具 adapter 使用 `gov_tool_adapter_stage`，只能实现 `adapt_schema`、`before_call`、`after_call`，用于参数映射、默认值补齐、结果格式规整。
5. schema 视图和 adapter 都不得修改云端 handler、真实平台 schema、NX 插件、安装脚本或 runtime 核心代码。
6. 隐藏不存在的参数只作为 warning；隐藏 required 参数且没有默认或注入策略时必须阻断。
7. 所有资产类变更必须展示 diff、validate 结果和风险，并提示用户输入 `/confirm` 后生效。

## 输出

回复应包含：当前工具状态、建议的用户级或 hot overlay 变更、schema/adapter 可见变化、影响范围、风险、验证方式、回退方式，以及是否等待 `/confirm`。
