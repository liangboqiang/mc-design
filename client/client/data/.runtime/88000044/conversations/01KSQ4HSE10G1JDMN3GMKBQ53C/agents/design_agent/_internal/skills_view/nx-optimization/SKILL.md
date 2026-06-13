---
name: nx-optimization
description: NX 优化研究技能
capabilities:
  - tool.nx.health
  - tool.nx.query
  - tool.nx.parameter
  - tool.nx.modeling
  - tool.nx.visual
---

# NX 优化研究技能

## 适用场景

用于在当前 NX WorkPart 上做参数化优化研究，包括变量范围确认、目标与约束组织、dry-run 预检和正式优化执行。

## 核心边界

- 本技能服务“模板参数化模型”的优化：先读取真实驱动参数，再构建优化问题。除凸轮轴专用建模工具外，不做创成式建模。
- `nx_validate_optimization_study` 与 `dry_run=true` 只做预检，不代表优化完成。
- `nx_build_optimization_objective_expression` 只构建或写入目标表达式，不代表模型特征创建成功，也不代表优化已执行。
- 正式优化、批量参数更新和模型状态改变前必须先生成优化方案并交给用户确认。

## 推荐调用流程

1. 调用 `nx_get_work_part_info`，确认 NX 中已经打开正确 WorkPart。
2. 调用 `nx_get_drive_params_list` 或 `nx_get_all_params_list`，获取真实表达式列表。
3. 从用户需求和已读取资料中抽取候选变量、目标、约束、算法边界。
4. 输出优化方案：变量、范围、目标、约束、风险、需要用户确认的内容。
5. 用户确认前只允许预检；调用 `nx_validate_optimization_study` 或 `nx_run_optimization_study(dry_run=true)`。
6. 用户明确确认后，才允许调用 `nx_run_optimization_study(dry_run=false)` 或批量写入推荐参数。
7. 正式运行后必须汇总变量变化、目标变化、约束状态和失败信息；若工具返回失败或结果为空，不得声称优化完成。

## 小规模优化建议

首次演示或需求不完整时，优先构建不超过两个设计变量的小问题。典型输出应包含：

- 固定不改参数；
- 可优化参数；
- 风险参数；
- 变量范围；
- 约束阈值；
- 候选方案；
- 推荐方案和不推荐原因。

## 禁止事项

- 禁止猜表达式名、变量上下限、约束阈值。
- 禁止跨请求保存 OptimizationBuilder 或假设前一轮 Builder 仍有效。
- 禁止在用户未确认时执行 `dry_run=false` 的正式优化。
- 禁止把“创建 Objective_AI 表达式”描述为“模型已优化/模型已创建”。
