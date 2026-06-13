---
name: task-decomposition
description: Beya 持久任务拆解技能
capabilities:
  - tool.collaboration.subagent
  - tool.collaboration.subagent
---

# task-decomposition

## 适用场景

用于复杂设计任务、代码改造任务、工具排查任务和多阶段验证任务，需要把目标拆成可跟踪、可回看、可验收的子任务。

## 工作方法

1. 先把用户目标拆成少量有明确验收标准的任务项。
2. 使用 `board_create` / `board_update` / `board_list` 维护任务状态；短期执行步骤仍可使用 `todo`。
3. 对需要独立探索、资料梳理或低风险并行分析的部分，可使用 `run_subagent` 启动 subagent，并要求其只返回摘要、证据和风险。
4. 主 Agent 必须对 subagent 输出做复核，不直接把子结果当成最终结论。
5. 涉及外部系统写入、NX 修改、报告导出或数据库写入时，任务项中必须标明确认条件和回退策略。

## 边界

- 任务拆解是运行治理能力，不是提示词迁移。
- subagent 是上下文隔离的辅助探索能力，不改变主 Agent 的业务身份。
- 不向用户索要运行时字段；运行时身份和连接由 Beya 注入。
