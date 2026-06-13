---
name: nx-auto-drawing
description: NX 图纸页查看与自动出图技能
capabilities:
  - tool.nx.health
  - tool.nx.query
  - tool.nx.drafting
  - tool.nx.visual
---

# nx-auto-drawing

## 适用场景

用于查看当前零件已有二维图纸页、打开图纸页、生成图纸截图；在用户明确要求且方案确认后，执行自动出图和 PMI 继承。

## 推荐流程

1. 调用 `nx_get_work_part_info` 确认当前零件。
2. 调用 `nx_get_drawing_sheet_name_list` 查看已有图纸页。
3. 用户只要求查看图纸时，调用 `nx_open_drawing_sheet` 打开指定图纸页，再按需截图。
4. 用户要求自动出图时，先调用 `nx_get_auto_drawing_tool_guide` 和 `nx_validate_auto_drawing_plan`。
5. 输出图纸方案：图纸尺寸、比例、视图、模板路径、PMI 继承规则、是否删除旧图纸。
6. 用户确认后才允许 `nx_run_auto_drawing(dry_run=false)` 或分步创建图纸页/视图。

## 禁止事项

- 禁止调用旧二维图纸更新工具：`nx_updatedrawings`、`nx_update_drawing*`、`nx_update_draw*`。这些入口在工具层也会被硬拦截。
- 禁止默认删除已有图纸页。
- 禁止把“查看图纸页”描述成“已完成自动出图”。
- 禁止在用户未确认方案时执行创建图纸、删除图纸或继承 PMI 的写入动作。
- 禁止凭空创建尺寸；本技能只继承模型已有 PMI 或自动出图规则。
