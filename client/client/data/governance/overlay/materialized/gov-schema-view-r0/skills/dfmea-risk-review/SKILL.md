---
name: dfmea-risk-review
description: DFMEA 风险复核技能
capabilities:
  - tool.workspace.read
  - tool.mysql.query
---

# DFMEA 风险复核技能

## 适用场景

用于对设计变更、参数调整、材料/结构方案或报告内容进行失效模式和风险复核。

## 工作方法

1. 先读取用户需求、设计对象、已修改参数和证据文件。
2. 如 DFMEA 或规则表存放在数据库中，使用 `mysql_query` 查询；如在工作区中，使用 `glob` / `grep` / `read_file` 定位。
3. 按失效模式、原因、后果、预防控制、探测控制和建议措施整理风险。
4. 对缺证据或低置信度风险标记为“需人工复核”，不要做确定性结论。

## 输出要求

每条风险包含：对象、触发条件、潜在后果、依据、建议动作和是否阻断继续执行。
