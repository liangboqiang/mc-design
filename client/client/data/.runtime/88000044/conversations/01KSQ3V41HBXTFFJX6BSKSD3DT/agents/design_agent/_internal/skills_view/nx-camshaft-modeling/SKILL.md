---
name: nx-camshaft-modeling
description: 凸轮轴 NX 建模技能
capabilities:
  - tool.nx.health
  - tool.nx.query
  - tool.nx.parameter
  - tool.nx.modeling
  - tool.nx.visual
  - tool.workspace.read
---

# 凸轮轴 NX 建模技能

## 适用场景

用于新建或更新凸轮轴数模，包括新建零件、轴体、型线导入、凸轮、凸轮阵列、端部凸台、过渡区、安装面、细节收口和视图截图。

## 推荐流程

1. 确认 NX 连接和当前零件；没有目标零件时，询问保存位置和零件名后使用 `nx_create_new_part`。
2. 型线：确认型线文件路径，优先调用 `nx_import_or_update_cam_profile_curve`；旧流程可用 `nx_import_cam_profile`。
3. 轴体：确认轴径、轴长，优先调用 `nx_build_or_update_camshaft_shaft`；旧流程可用 `nx_build_camshaft`。
4. 凸轮：确认凸轮厚度，优先调用 `nx_build_or_update_cam_lobe_from_profile`；旧流程可用 `nx_build_cam_lobe`。
5. 端部凸台：确认凸台长度和直径，调用 `nx_build_or_update_end_boss`；旧流程可用 `nx_build_cam_boss` + `nx_mount_boss_to_shaft`。
6. 阵列：确认缸数、缸心距，优先调用 `nx_build_or_update_cam_lobe_array`；旧流程可用 `nx_build_cam_lobe_array` + `nx_mount_cam_lobes_to_shaft`。
7. 需要过渡区、安装面或细节收口时，调用 `nx_build_or_update_camshaft_transition_zone`、`nx_build_or_update_camshaft_mount_face`、`nx_build_or_update_camshaft_detail_finish`。
8. 建模工具成功返回后再调用视图或截图工具，并向用户总结已生成对象和仍缺失的输入；若任何 NX 工具失败或没有返回成功结果，只能说明阻断原因。

## 一键工具边界

`nx_build_camshaft_one_click` 只用于用户明确要求快速生成、输入已经完整或回归测试场景。交互式设计优先分步执行，避免把缺失参数藏在默认值里。

## 禁止事项

- 禁止跳过必要尺寸确认。
- 禁止把默认路径、默认型线或默认尺寸当成用户确认值。
- 禁止调用当前 NXServer 未暴露的开槽、snapshot、任意 build_feature/create_prt/modify_parameter 等工具。
- 禁止在 NX 失败、未连接或没有成功工具结果时继续执行后续依赖步骤或声称已完成建模。
