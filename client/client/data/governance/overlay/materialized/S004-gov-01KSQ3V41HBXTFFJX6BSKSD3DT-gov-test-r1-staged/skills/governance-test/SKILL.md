---
name: governance-test
description: 治理修改验证和被治理 Agent 测试技能
capabilities:
  - tool.governance.test
  - tool.governance.asset
---

# governance-test

@id: [[skill.governance_test]]
@type: skill
@scope: platform
@status: active
@version: 0.2.0

@uses.tool:
- [[tool.governance]]

@governed.by: [[agent.governance_agent]]

## 目标

用于在治理过程中测试被治理 Agent 的表现，比较修改前后回答、工具可见 schema、工具调用参数、Skill 加载和风险。

## 规则

1. 能用 `gov_agent_test` 测试时，优先用同一用户问题测试目标 Agent。
2. staged overlay 可以用于 A/B 测试；未确认的 staged 修改不得进入普通 Agent。
3. 测试结果必须作为证据，而不是自动应用理由。
4. 测试失败、工具不可用、模型不可用或验证失败时，不得 apply。
5. schema 视图治理必须检查目标工具在测试中的可见参数和实际调用参数是否符合预期。

## 输出

输出测试问题、目标 Agent、可见资产或 schema 差异、结果摘要、工具调用差异、验证结论和下一步建议。
