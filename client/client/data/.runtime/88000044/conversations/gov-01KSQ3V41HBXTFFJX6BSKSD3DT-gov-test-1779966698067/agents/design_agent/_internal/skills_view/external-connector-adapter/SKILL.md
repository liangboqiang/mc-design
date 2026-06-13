---
name: external-connector-adapter
description: 外部系统适配器技能
capabilities:
  - tool.external
  - tool.workspace.read
---

# external-connector-adapter

## 适用场景

用于查询 QPP、ECR、IPM 等外部业务系统。外部系统 URL 从 `beya.toml` 的 `[external.*]` 配置读取，Agent 只传业务查询参数。

用户说“查询任务”“查设计任务”“看看我的任务”时，必须把 IPM、QPP、ECR 都理解为设计任务来源；根据用户给出的条件选择一个或多个现有工具调用，不新增统一工具名。

## 工具边界

- `connect_qpp`：查询 QPP 任务。`worker` 不传时使用运行时 `user_name`。
- `query_ecr_list`：查询 ECR 信息，按编号、主题、状态、申请人、责任人、日期等过滤。
- `query_ipm_list`：查询 IPM 任务。`principle` 不传时使用运行时 `user_id`；`principleName` 不传时使用运行时 `user_name`；`confirmStatusList` 不传时默认查询 `未提交`、`不通过`、`已确认`。

## 规则

- 不向用户索要 `user_id`、`user_name`、`conversation_id`、host、port、token 或 base_url。
- 用户只需要提供业务条件，例如项目名、ECR 编号、日期范围、责任人姓名或任务名称。
- 如果用户只说“查询任务”且没有限定渠道，优先同时覆盖 IPM、QPP、ECR；如工具结果失败或为空，应分别说明每个渠道的结果。
- 查询失败时直接说明接口失败、网络失败或返回结构异常，不把空结果描述为已找到任务。
