---
name: asset-governance
description: 热治理资产审计 Skill
capabilities:
  - tool.governance.asset
  - tool.governance.test
---

# asset-governance

@id: [[skill.asset_governance]]
@type: skill
@scope: platform
@status: active
@version: 0.4.0

@uses.tool:
- [[tool.governance]]

## 目标

用于 `/gov` 治理模式下审计当前 Agent、Skill、Tool 策略、工具 schema 视图策略和 context policy。默认治理写入目标是用户端 hot overlay；打包资产和公共源码只作为基线、对比或可选导出对象。

## 工作区

- `assets`：当前有效资产基线，叠加 hot overlay 后用于目标 Agent 运行。
- `overlay`：用户端热治理覆盖层，用户输入 `/confirm` 后下一轮生效。
- `runtime`：被治理 Agent 的会话运行时目录，只读，用来取证和复盘。
- `scratch`：治理临时区，用于草稿、diff、检查输出。
- `asset_views/<bundle_version>`：打包投影，只读，禁止写入。

## 审计规则

1. 先用 `gov_governable_list`、治理资产列表和读取工具找到目标资产与相关引用。
2. 修改建议必须说明影响范围、风险等级、涉及的 Skill/Tool/Context。
3. 工具策略可以治理说明、使用建议、禁用偏好、fallback 和 schema 视图策略；不得修改 handler、云端服务或 NX 插件。
4. 任何写入都必须转入 `asset-write` 流程：stage -> diff -> validate -> 提示用户输入 `/confirm`。
5. 需要验证时调用 `gov_agent_test`，用临时会话测试被治理 Agent，不污染用户主会话。

## 输出要求

每次治理回复默认给用户：修改意图、影响范围、关键 diff 或草案摘要、风险和回退方式、已执行或建议执行的验证、是否正在等待用户输入 `/confirm`。
