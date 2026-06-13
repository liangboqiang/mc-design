---
name: skill-governance
description: Skill 资产治理 Skill
capabilities:
  - tool.governance.asset
  - tool.governance.write
  - tool.governance.policy
  - tool.governance.test
---

# skill-governance

@id: [[skill.skill_governance]]
@type: skill
@scope: platform
@status: active
@version: 0.5.0

@uses.tool:
- [[tool.governance]]

@governed.by: [[agent.governance_agent]]

## 目标

用于治理当前 Agent 可用的 Skill，包括新增 Skill、修改 Skill、整理边界、补充推荐工具、修复冲突，以及处理 Skill 的用户级或资产级启停。默认修改写入 hot overlay，用户输入 `/confirm` 后下一轮生效。

## 规则

1. 用户级启停使用 `gov_policy_get` 和 `gov_policy_set`，只影响当前用户，立即长期生效。
2. 资产级启停必须修改 Skill 的 `@status` 或 Agent 引用，并走 stage、diff、validate、提示 `/confirm` 的流程。
3. Skill 正文修改必须基于证据：用户明确要求、工具结果、会话运行时记录或现有资产冲突。
4. 不把一次性偏好、未验证推测、失败工具结果写成长效 Skill 规则。
5. 修改前必须读取目标 Agent、相关 Skill、当前 runtime 证据和可用工具边界。
6. 禁止直接改打包投影 `asset_views`、公共源码、安装目录或绕过治理工具写文件。

## 输出

回复应包含：治理目标、现状摘要、用户级/资产级影响、候选修改、关键 diff、验证结果、风险、回退方式，以及是否等待用户输入 `/confirm`。
