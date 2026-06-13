---
name: workspace-cli
description: 本地 workspace CLI 与时间查询技能
capabilities:
  - tool.workspace.read
  - tool.workspace.exec
---

# workspace-cli

## 适用场景

用于需要读取客户机本地时间、确认本地时区、运行轻量命令或在 private workspace 中验证文件/脚本结果的任务。

## 工作方法

1. 用户询问当前时间、日期、时区或“现在几点”时，优先调用 `local_time`，不要猜测云端或 K8S 时间。
2. 需要执行命令时使用 `bash`，命令工作目录固定为 private workspace。
3. 命令只用于本地检查、轻量脚本、文件验证和可重复诊断；不要通过它访问 workspace 之外的任意路径。
4. 命令输出是工具结果，不是长期事实源；需要后续引用时，应把结论写入回答或可审计文件。

## 边界

- 不用 K8S、AI service 容器或远端服务器时间回答本地时间问题。
- 不执行破坏性命令、系统关机、权限提升或跨目录批量删除。
- 文件读写仍优先使用 `read_file`、`write_file`、`edit_file`。
