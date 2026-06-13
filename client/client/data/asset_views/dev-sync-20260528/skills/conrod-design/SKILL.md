---
name: conrod-design
description: 连杆设计技能
capabilities:
  - tool.workspace.read
  - tool.mysql.query
  - tool.nx.health
  - tool.nx.query
  - tool.nx.parameter
  - tool.nx.visual
---

# 连杆设计技能

## 适用场景

用于连杆类零部件的模板定位、参数识别、方案确认、NX 参数调整和结果总结。

## 推荐流程

1. 用 `mysql_query` 查询连杆模板候选和参数词典候选。
2. 用户确认模板后，用 `nx_open_part` 打开模板或目标模型。
3. 用 `nx_get_drive_params_list` / `nx_get_all_params_list` 获取真实参数。
4. 对齐用户需求、标准参数候选和 NX 参数，形成参数修改表。
5. 用户确认后调用 `nx_update_param` 或 `nx_batch_update_params`。
6. 读取修改结果，必要时生成截图或转入设计报告。

## 禁止事项

禁止直接把“连杆大头/小头/杆身”等中文描述猜成 NX 表达式名；必须先查词典和当前模型参数。
