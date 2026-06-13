---
name: workspace-isolation
description: Beya 工作区与 worktree 隔离技能
capabilities:
  - tool.workspace.read
  - tool.workspace.write
  - tool.workspace.exec
  - tool.workspace
  - tool.collaboration.worktree
---

# workspace-isolation

## 适用场景

用于需要隔离修改、验证、回滚或并行实验的任务，例如代码/配置改造、工具修复、模板试改、可重复验证脚本执行。

## 工作方法

1. 先读取目标文件和相关说明，明确修改范围，避免全局扫改。
2. 小改动优先直接在当前 private workspace 中完成；需要隔离实验、并行分支或可回滚路径时再创建 worktree。
3. worktree 名称应短、可追踪，并与任务或变更点对应。
4. 在 worktree 内执行命令前，先确认命令作用域和副作用；高风险命令必须向用户说明。
5. 验证通过后说明保留、移除或合并建议；不要让临时 worktree 变成新的事实来源。

## 边界

- 文件读写仍然只使用 Beya 的 workspace 工具。
- worktree 是隔离执行手段，不是新的项目主干。
- 不引入额外目录约定或额外文件工具实现。
