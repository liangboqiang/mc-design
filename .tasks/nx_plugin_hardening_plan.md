# NX Plugin 工具加固计划

更新时间：2026-06-14

## 监管口径

本计划只针对 `mc-design-nx/nx-plugin`、NX 工具 manifest、NX 相关 skills/tests 的加固与调整，不涉及 `beya -> tjuae` 运行时替换。

目标是把 NX 工具从“能被调用”加固到“可被智能体稳定、安全、可验收地调用”，重点降低参数误写、模型误打开、二维图误操作、截图视角错误和文件系统越界风险。

## 当前已确认工具面

客户端当前只通过 `mc-design-nx/client/resources/nx_tools_manifest.json` 暴露 `nx_*` 工具，manifest 来自 `mc-design-nx/package/windows/build/scripts/generate_nx_manifest.py` 扫描 C# `[Tool]` 属性。

当前 manifest 中与 P0 相关的工具组：

- 参数：`nx_get_all_params_list`、`nx_get_drive_params_list`、`nx_find_params`、`nx_create_param`、`nx_update_param`、`nx_batch_update_params`、`nx_high_light_dim`
- 文件/TC：`nx_open_part`、`nx_open_tcpart`、`nx_open_tc_drawing`、`nx_get_work_part_info`
- 图纸：`nx_get_drawing_sheet_name_list`、`nx_open_drawing_sheet`、`nx_create_auto_drawing_sheet`、`nx_create_auto_drawing_views`、`nx_apply_pmi_inheritance_to_drawing_views`、`nx_run_auto_drawing`、`nx_delete_drawing_sheets`
- 视图/截图：`nx_get_all_view_names`、`nx_switch_view`、`nx_set_view_style`、`nx_rotate_and_scale_view`、`nx_create_image`
- 文件桥：`nx_fs_read_bytes`、`nx_fs_write_bytes`、`nx_fs_copy`、`nx_fs_exists`

## P0 加固项

### NX-P0-1 参数写入工具安全加固

涉及文件：

- `mc-design-nx/nx-plugin/src/McDesign.NXTools/ExpressionTools.cs`
- `mc-design-nx/client/resources/nx_tools_manifest.json`
- `mc-design-nx/client/tests/test_tool_registry.py`
- `mc-design-nx/client/tests/test_design_skill_contract.py`

已发现问题：

1. `UpdateParam`、`BatchUpdateParams` 通过 `NormalizeNumberString` 处理 value；当前 `null` 或空字符串会被转成 `"0"`，存在缺失值被写成 0 的风险。
2. `BatchUpdateParams` 即使部分或全部失败也会执行 `NXContext.Update()` 并外层返回 success，容易被上层误认为全部成功。
3. `ToInfo` 直接读取 `exp.OwningPart.ExpressionGroups.GetGroupOfExpression(exp).Name`，未分组表达式可能导致读参数列表失败。
4. `HighLightDim` 找不到尺寸时没有 `return`，会继续访问空对象；入参名 `expName`、`isHighAssoOBjI` 不利于稳定 schema。

验收要求：

1. `nx_update_param` 和 `nx_batch_update_params` 必须拒绝空 value、`NaN`、`Infinity` 和明显非法数值。
2. 批量更新返回必须包含 `updated`、`failed`、`updated_count`、`failed_count`；存在失败项时不能只给“批量更新完成”的乐观结论。
3. 未分组表达式也能被 `nx_get_all_params_list` 正常返回，`group_name` 允许为空。
4. `nx_high_light_dim` 找不到尺寸时返回失败，不抛空引用；返回高亮对象数量和关联对象数量。
5. 更新 manifest 和静态测试，确保参数工具 schema 明确表达 `std_id/value`。

### NX-P0-2 WorkPart、打开模型和图纸工具返回结构加固

涉及文件：

- `mc-design-nx/nx-plugin/src/McDesign.NXTools/FileTools.cs`
- `mc-design-nx/assets/source/skills/nx-operation/SKILL.md`
- `mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md`
- `mc-design-nx/client/tests/test_tool_registry.py`
- `mc-design-nx/client/tests/test_design_skill_contract.py`

已发现问题：

1. `GetWorkPartInfo` 返回字段写成 `part_nane`，不是 `part_name`。
2. `GetDrawingSheetNameList` 直接返回 `List<string>`，没有统一 `NXResult`、没有 WorkPart 元信息、没有异常处理。
3. `OpenDrawingSheet` 缺少空参数校验和异常处理，返回信息过少。
4. `OpenPart` 描述为本地/明确 NX 文件路径，但实现未显式拒绝 `@DB`/TC path，也未校验本地文件存在和扩展名。
5. `OpenTCPart` 遇到已打开同名/同版本模型直接失败；更合理的是同一对象切换并返回，只有不同版本或冲突对象才失败。
6. `OpenTcDrawing` 只检查路径包含 `specification`，需要更严格确认这是 Teamcenter 图纸/数据集路径。

验收要求：

1. `nx_get_work_part_info` 返回 `part_name`、`part_path`、`has_write_access`、`is_teamcenter_part`、`application`；可临时保留 `part_nane` 作为兼容字段，但新字段必须正确。
2. `nx_get_drawing_sheet_name_list` 返回统一结构：`sheet_names`、`count`、`work_part`。
3. `nx_open_drawing_sheet` 返回打开的 `sheet_name`、`work_part`、`application=UG_APP_DRAFTING`。
4. `nx_open_part` 明确拒绝 TC `@DB` 路径和 specification/drawing 路径；本地文件不存在时失败。
5. `nx_open_tcpart` 对同一已打开模型应切换并返回成功；对不同版本冲突应返回明确错误。
6. `nx_open_tc_drawing` 必须要求来自 TC 查询的 `tc_db_path` 或完整 dataset 组合，并返回 dataset 路径、WorkPart、Drafting 状态。

### NX-P0-3 视图切换和截图链路加固

涉及文件：

- `mc-design-nx/nx-plugin/src/McDesign.NXTools/ViewTools.cs`
- `mc-design-nx/nx-plugin/src/McDesign.NXTools/FileTools.cs`
- `mc-design-nx/assets/source/skills/nx-visual/SKILL.md`
- `mc-design-nx/assets/source/skills/design-report/SKILL.md`

已发现问题：

1. `SwitchView` 未先校验视图名是否存在，也不返回实际切换后的视图。
2. `SetViewStyle` 未校验 enum 范围。
3. `RotateAndScaleView` 只校验 `scaleRatio > 0`，未校验 `NaN/Infinity` 和极端角度。
4. `CreateImage` 不创建目标目录，不校验导出后文件是否真实存在和大小，无法证明截图成功。
5. 设计报告多视角截图如果由多次 `switch` 和多次 `create_image` 分离执行，容易出现全部截图同一视角。

验收要求：

1. `nx_switch_view` 先通过当前模型视图集合校验，支持大小写匹配和标准视图别名，返回 `requested_view`、`actual_view`、`available_views`。
2. `nx_set_view_style` 拒绝未知样式，返回可选样式列表。
3. `nx_rotate_and_scale_view` 拒绝 `NaN/Infinity`、非正 scale、异常大 scale。
4. `nx_create_image` 创建父目录，导出后验证文件存在、大小大于 0，并返回 `file_path`、`format`、`size_bytes`、`active_view`。
5. 新增一个安全组合工具，建议名：`CaptureViewImage`，manifest 暴露为 `nx_capture_view_image`，入参 `view_name`、`filePath`、`fit_view`、`background`；内部完成“切换视图 -> fit -> 截图 -> 验证文件”，用于报告截图。

### NX-P0-4 自动出图与危险等级加固

涉及文件：

- `mc-design-nx/nx-plugin/src/McDesign.NXTools/AutoDrawingTools.cs`
- `mc-design-nx/package/windows/build/scripts/generate_nx_manifest.py`
- `mc-design-nx/client/resources/nx_tools_manifest.json`
- `mc-design-nx/client/tests/test_tool_registry.py`

已发现问题：

1. manifest 危险等级生成规则把工具名包含 `view` 的工具标为 `read`，导致 `nx_create_auto_drawing_views`、`nx_apply_pmi_inheritance_to_drawing_views` 被错误标成 `read`，但它们会修改工程图。
2. `ValidateAutoDrawingPlan` 预检不通过时外层仍返回 `ok=true`，上层可能误判。
3. `DeleteDrawingSheets(delete_all=true)` 是破坏性动作，当前只靠 skill 提醒，没有工具级二次保护。

验收要求：

1. manifest 危险等级改为显式规则或覆盖表，至少保证创建/打开/删除/写入/PMI 继承/图纸视图创建为 `write` 或更高风险。
2. `nx_validate_auto_drawing_plan` 在预检失败时外层返回失败，或返回结构必须有清晰 `valid=false` 且客户端/测试明确识别。
3. `nx_delete_drawing_sheets` 增加 dry_run 或确认参数；`delete_all=true` 必须有额外确认字段，否则失败。
4. 更新 manifest 生成测试，防止危险等级回退。

### NX-P0-5 文件桥工具边界加固

涉及文件：

- `mc-design-nx/nx-plugin/src/McDesign.NXTools/NxFileBridgeTools.cs`
- `mc-design-nx/package/windows/build/scripts/generate_nx_manifest.py`
- `mc-design-nx/client/resources/nx_tools_manifest.json`
- `mc-design-nx/assets/source/tools/tool.nx/TOOL.md`

已发现问题：

1. `nx_fs_read_bytes`、`nx_fs_write_bytes`、`nx_fs_copy` 可以读写任意本机路径。
2. 读取结果直接返回 base64，缺少文件大小限制，容易造成响应过大。
3. 写入/复制默认可覆盖，缺少目录白名单和扩展名限制。

验收要求：

1. 优先评估是否从公开 manifest 移除 `nx_fs_*`，作为内部桥接能力保留。
2. 如果必须公开，增加路径白名单、最大文件大小、允许扩展名、禁止系统目录、禁止相对路径逃逸。
3. `fs_write_bytes` 默认不覆盖，覆盖必须显式传参。
4. 返回结构包含 `size_bytes`、`sha256`、`path`，读取大文件时只返回元数据或失败，不直接返回超大 base64。

## P1 加固项

### NX-P1-1 HTTP 请求和 ToolManager 边界

涉及文件：

- `mc-design-nx/nx-plugin/src/McDesign.NXPlugin/HttpServer.cs`
- `mc-design-nx/nx-plugin/src/McDesign.NXPlugin/ToolManager.cs`

建议：

1. 增加 HTTP body 最大大小限制，当前只限制 header。
2. URL tool name 做 URL decode 和白名单校验。
3. 增加请求 trace_id，日志里记录 tool、耗时、ok、message。
4. 对参数反序列化错误返回结构化 code。
5. 评估失败时是否继续 HTTP 200，或客户端按 `ok=false` 做统一处理。

### NX-P1-2 旧 asset_views 清理确认

涉及目录：

- `mc-design-nx/client/data/asset_views`

已发现：

该目录中仍有旧 skill 文本引用 `nx_health_check`、`nx_open_tc_part`、`nx-camshaft-modeling`、`nx-optimization`、`nx-auto-drawing`。需要确认该目录是否参与当前运行时投影或安装包。如果参与，必须从 source assets 重新生成或清理。

验收要求：

1. 明确 `client/data/asset_views` 是否应纳入仓库和打包。
2. 如果不应纳入，更新 `.gitignore`/清理策略。
3. 如果需要作为测试 fixtures，必须与 `assets/source` 保持一致，不允许出现已禁用工具名。

## 可派发提示词

### 提示词 1：NX 参数工具加固

```text
你是 mc-design NX 参数工具加固执行智能体。

工作目录：
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design

范围：
- mc-design-nx/nx-plugin/src/McDesign.NXTools/ExpressionTools.cs
- mc-design-nx/client/resources/nx_tools_manifest.json
- mc-design-nx/client/tests/test_tool_registry.py
- mc-design-nx/client/tests/test_design_skill_contract.py

任务：
1. 加固 UpdateParam 和 BatchUpdateParams：拒绝空 value、NaN、Infinity 和明显非法数值，不能把空值转成 0。
2. BatchUpdateParams 返回 updated/failed/updated_count/failed_count；存在失败项时上层不能误判为全部成功。
3. 修复 ToInfo 对未分组表达式的空引用风险，group_name 可为空。
4. 修复 HighLightDim 找不到尺寸时未 return 的问题，补充异常处理和返回高亮对象数量。
5. 更新 manifest 和静态测试，确保参数工具 schema 清晰表达 std_id/value。

限制：
- 不做 beya/tjuae 替换。
- 不做业务参数转换方案。
- 不删除当前已注册的核心参数工具，除非测试说明替代工具已经覆盖。

输出：
- 改动文件清单
- 新旧返回结构对比
- 测试命令和结果
- 未能覆盖的 NX 实机验证项
```

### 提示词 2：NX 文件、TC 打开和图纸页工具加固

```text
你是 mc-design NX 文件/TC/图纸页工具加固执行智能体。

工作目录：
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design

范围：
- mc-design-nx/nx-plugin/src/McDesign.NXTools/FileTools.cs
- mc-design-nx/assets/source/skills/nx-operation/SKILL.md
- mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md
- mc-design-nx/client/tests/test_tool_registry.py
- mc-design-nx/client/tests/test_design_skill_contract.py

任务：
1. 修复 GetWorkPartInfo 的 part_nane 字段，新增正确 part_name 字段。
2. 将 GetDrawingSheetNameList 改为统一 NXResult 返回结构，包含 sheet_names/count/work_part。
3. 加固 OpenDrawingSheet：空参数校验、异常处理、返回 sheet/work_part/application。
4. 加固 OpenPart：拒绝 @DB/TC/specification 路径，校验本地文件存在和扩展名。
5. 优化 OpenTCPart：同一 TC 主模型已打开时切换并返回成功，不同版本冲突时明确失败。
6. 加固 OpenTcDrawing：严格要求 TC 图纸数据集路径或完整 dataset 组合，返回 Drafting 状态。
7. 更新对应 skill 和测试。

输出：
- 改动文件清单
- 每个工具的新返回结构
- 测试命令和结果
- 需要 NX/TC 实机验证的步骤
```

### 提示词 3：NX 视图与截图工具加固

```text
你是 mc-design NX 视图与截图工具加固执行智能体。

工作目录：
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design

范围：
- mc-design-nx/nx-plugin/src/McDesign.NXTools/ViewTools.cs
- mc-design-nx/nx-plugin/src/McDesign.NXTools/FileTools.cs
- mc-design-nx/assets/source/skills/nx-visual/SKILL.md
- mc-design-nx/assets/source/skills/design-report/SKILL.md
- mc-design-nx/client/resources/nx_tools_manifest.json
- mc-design-nx/client/tests/test_tool_registry.py

任务：
1. 加固 SwitchView：校验视图名，支持标准视图别名，返回 requested_view/actual_view/available_views。
2. 加固 SetViewStyle 和 RotateAndScaleView 的入参范围。
3. 加固 CreateImage：创建父目录，导出后验证文件存在和大小，返回 active_view、size_bytes。
4. 新增安全组合工具 CaptureViewImage，manifest 名建议为 nx_capture_view_image，内部执行切换视图、fit、截图、验证文件。
5. 更新 design-report 和 nx-visual skill，报告截图优先使用 nx_capture_view_image。
6. 更新 manifest 和测试。

输出：
- 改动文件清单
- 新工具 schema
- 报告截图调用顺序
- 测试命令和结果
- NX 实机截图验证步骤
```

### 提示词 4：NX 自动出图与 manifest 危险等级加固

```text
你是 mc-design NX 自动出图与 manifest 危险等级加固执行智能体。

工作目录：
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design

范围：
- mc-design-nx/nx-plugin/src/McDesign.NXTools/AutoDrawingTools.cs
- mc-design-nx/package/windows/build/scripts/generate_nx_manifest.py
- mc-design-nx/client/resources/nx_tools_manifest.json
- mc-design-nx/client/tests/test_tool_registry.py

任务：
1. 修复 manifest danger_level 生成规则，不允许因为工具名包含 view 就判定为 read。
2. 确保 nx_create_auto_drawing_views、nx_apply_pmi_inheritance_to_drawing_views 等会修改工程图的工具标为 write。
3. 调整 ValidateAutoDrawingPlan：预检失败不能让上层误认为成功。
4. 加固 DeleteDrawingSheets：delete_all=true 必须有 dry_run 或额外确认字段。
5. 重新生成 nx_tools_manifest.json 并补齐测试，防止危险等级回退。

输出：
- 改动文件清单
- danger_level 规则说明
- 关键工具危险等级对照表
- 测试命令和结果
```

### 提示词 5：NX 文件桥工具边界加固

```text
你是 mc-design NX 文件桥工具边界加固执行智能体。

工作目录：
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design

范围：
- mc-design-nx/nx-plugin/src/McDesign.NXTools/NxFileBridgeTools.cs
- mc-design-nx/package/windows/build/scripts/generate_nx_manifest.py
- mc-design-nx/client/resources/nx_tools_manifest.json
- mc-design-nx/assets/source/tools/tool.nx/TOOL.md

任务：
1. 评估 nx_fs_read_bytes、nx_fs_write_bytes、nx_fs_copy、nx_fs_exists 是否需要继续暴露给智能体。
2. 如果不需要公开，移出公开 manifest 或标记 internal，不影响内部桥接。
3. 如果必须公开，增加路径白名单、最大文件大小、允许扩展名、禁止系统目录、禁止相对路径逃逸。
4. fs_write_bytes 默认不覆盖，覆盖必须显式传参。
5. 大文件读取不得直接返回超大 base64，返回结构需包含 size_bytes 和 sha256。
6. 更新 tool.nx 说明和测试。

输出：
- 是否公开 nx_fs_* 的结论
- 改动文件清单
- 安全边界说明
- 测试命令和结果
```

### 提示词 6：NX asset_views 旧资产清理确认

```text
你是 mc-design NX 旧资产视图清理确认执行智能体。

工作目录：
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design

范围：
- mc-design-nx/client/data/asset_views
- mc-design-nx/client/src/mc_design_client/runtime/environment.py
- mc-design-nx/client/tests/test_agent_loop_assets.py
- mc-design-nx/client/tests/test_asset_store.py
- .gitignore

任务：
1. 确认 client/data/asset_views 是否是运行时生成物、测试 fixture、还是打包基线。
2. 搜索其中残留的旧工具名：nx_health_check、nx_open_tc_part、nx_update_drawing、nx-camshaft-modeling、nx-optimization、nx-auto-drawing。
3. 如果该目录不应纳入源码，更新清理/.gitignore/测试策略。
4. 如果必须保留，重新从 assets/source 生成一致内容，移除已禁用工具名和旧 skill。
5. 不修改运行时 adapter，不做 beya/tjuae 替换。

输出：
- asset_views 定位结论
- 残留旧工具/旧 skill 清单
- 改动文件清单
- 测试命令和结果
```
