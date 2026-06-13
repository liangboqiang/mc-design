---
name: design-report
description: 固定模板设计报告技能
capabilities:
  - tool.design_report.slot
  - tool.design_report.image
  - tool.design_report.generate
  - tool.workspace.read
  - tool.workspace.write
  - tool.workspace.export
  - tool.nx.visual
  - tool.mysql.query
  - tool.teamcenter.query
  - tool.teamcenter.file
  - tool.external
---

# 固定模板设计报告技能

## 适用场景

用于工程交付型设计报告。设计报告必须走固定 DOCX 槽位模板路线：创建报告状态、读取模板槽位、按槽位填充内容、检查缺失、用户确认后导出 DOCX。

## 报告路线

1. 需要模板时，用 `mysql_query` 查询 `doc_template_table` 或根据用户给定路径确定模板。
2. 调用 `design_report_create`，读取返回的 `report_id` 与槽位列表。
3. 按槽位收集证据：NX 参数/截图、TC 文件/属性、QPP/ECR/IPM 信息、用户输入和工作区资料。
4. 调用 `design_report_update` 按 `slot_id` 分批填充槽位。
5. 调用 `design_report_detail` 检查缺失槽位。
6. 需要三维截图时，先用 `nx-visual` 或 `design_report_capture_image` 生成图片，再填入 image 槽位。
7. 用户确认后调用 `design_report_export` 导出 DOCX。
8. 用户需要下载时，使用 `export_file` 将 private/ 中的报告副本导出为下载链接和 curl 命令。

## 约束

- 不改变固定模板结构，不做报告风格偏好设计。
- 不猜测模板槽位；必须以设计报告工具返回的 slots 为准。
- 不伪造数据；没有工具证据或用户输入时，槽位应标记缺失或待确认。
- 导出、截图、写入远端路径属于副作用动作，需要用户明确确认。
- `design_report_export` 成功返回前，不得说 DOCX 已导出；`export_file` 成功返回前，不得说用户可下载。
