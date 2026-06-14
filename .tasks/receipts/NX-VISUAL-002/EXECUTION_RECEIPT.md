# NX-VISUAL-002 执行回执

执行时间：2026-06-14 14:22:17 +08:00

## 任务边界

- 已先阅读 `.tasks/TEST_EXECUTION_RULES.md`。
- 本次只处理 NX 视图/截图相关源码、skill、manifest 和测试。
- 未启用、恢复或调用 `nx-auto-drawing`、`nx_run_auto_drawing`、`nx_updatedrawings` 或 Sheet 级自动图纸工具。
- 未打开、修改或保存 NX 模型；实机阶段只做当前会话健康和只读视图信息预检。

## 改动文件清单

本次直接改动/生成：

- `mc-design-nx/nx-plugin/src/McDesign.NXTools/ViewTools.cs`
- `mc-design-nx/nx-plugin/src/McDesign.NXTools/FileTools.cs`
- `mc-design-nx/assets/source/skills/nx-visual/SKILL.md`
- `mc-design-nx/assets/source/skills/design-report/SKILL.md`
- `mc-design-nx/assets/source/skills/design-report/examples/report_payload.complete.json`
- `mc-design-nx/client/tests/test_tool_registry.py`
- `mc-design-nx/client/resources/nx_tools_manifest.json`（资源目录当前未被 git 跟踪；已重新生成，SHA256=`2FAC6C5E7B2B56320672825BCCE54350DD40238EA393E0CCABB6FD7A5BA5EEE5`）

说明：

- `mc-design-nx/nx-plugin/src/McDesign.NXSDK/NXResult.cs` 已有 `code/retryable/details` 支持，本次未继续修改。
- 工作树中存在大量本任务外既有未提交变更；本次未回滚、未整理这些无关变更。

## 视图确认逻辑

`nx_switch_view` 现在按以下顺序执行：

1. 校验 `view_name` 非空，否则返回 `NX_VIEW_NAME_REQUIRED`。
2. 读取当前 WorkPart 的现有 `ModelingViews`，先匹配已存在视图。
3. 匹配顺序为：原文完全相等、大小写不敏感相等、规范化名称相等。规范化会去除非字母数字字符并转小写。
4. 未命中返回 `NX_VIEW_NOT_FOUND`；规范化命中多个返回 `NX_VIEW_NAME_AMBIGUOUS`。
5. 只使用匹配到的真实视图名调用 `WorkView.Orient(...)`。
6. 切换后读取 `part.ModelingViews.WorkView.Name`，规范化后必须等于匹配视图名；否则返回 `NX_VIEW_SWITCH_NOT_CONFIRMED`，并在 details 中返回 requested/matched/previous/confirmed/available/normalized 信息。

`nx_get_all_view_names` 现在返回结构化数据：

- `current_view_name`
- `current_normalized_view_name`
- `available_view_names`
- `all_view_names`（兼容字段）
- `normalized_matching_info.views`
- `normalized_matching_info.ambiguous_normalized_view_names`

## 截图结果和失败错误码

`nx_create_image` 成功时返回：

- `path`
- `file_path`
- `resolvedPath`
- `resolved_path`
- `size_bytes`
- `sha256`
- `view_name`
- `work_part_name`
- `work_part_path`
- `format`
- `pre_capture.filePath/resolvedPath/view_name/work_part_name/work_part_path`

截图失败返回结构化 `code/details`，details 至少包含：

- `filePath`
- `resolvedPath`
- `view_name`
- `work_part_name`
- `work_part_path`
- `exception_type`
- `exception_message`

新增/使用的截图失败错误码：

- `NX_IMAGE_PATH_REQUIRED`
- `NX_FILE_PATH_DENIED`
- `NX_FILE_PATH_INVALID`
- `NX_IMAGE_FORMAT_REQUIRED`
- `NX_IMAGE_FORMAT_UNSUPPORTED`
- `NX_IMAGE_FILE_NOT_CREATED`
- `NX_IMAGE_FILE_EMPTY`
- `NX_IMAGE_CAPTURE_FAILED`

## Skill/Manifest 更新

- `nx-visual` 截图流程改为：`nx_get_all_view_names` -> `nx_switch_view` -> 必要时 `nx_fit_view` -> `nx_create_image`。
- `design-report` 截图规则同步为逐张执行上述顺序，并要求检查 `confirmed_view_name`、记录 `path/size_bytes/sha256/view_name/work_part_name`。
- `design-report/examples/report_payload.complete.json` 的多视角图片 source 已补充 `nx_get_all_view_names`。
- 已重新生成 `client/resources/nx_tools_manifest.json`，工具数 `21`；检查确认禁用自动出图/Sheet 级工具未出现在 manifest 中。

## 测试命令和结果

1. 规则读取

```powershell
Get-Content -LiteralPath .tasks/TEST_EXECUTION_RULES.md
```

结果：已读取。

2. manifest 生成

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' package/windows/build/scripts/generate_nx_manifest.py --source-root nx-plugin/src/McDesign.NXTools --output client/resources/nx_tools_manifest.json
```

结果：

```json
{"ok": true, "tool_count": 21, "output": "client/resources/nx_tools_manifest.json"}
```

3. Python 静态/单元测试

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client/tests/test_tool_registry.py assets/source/skills/design-report/tests/test_design_report.py
```

结果：`38 passed in 2.73s`。

4. C# 构建

```powershell
& 'C:\Program Files\dotnet\dotnet.exe' build nx-plugin/McDesign.NXPlugin.sln -p:Configuration=Debug -p:Platform=x64
```

结果：构建成功，`0` error，`93` warning。warning 为本机 NX 附加程序集引用缺失类警告（例如 `CaeDseWorkflowOpen`、`CLDCommonOpen` 等），未阻塞编译。

5. NX 实机只读预检

```powershell
Get-Process -Name ugraf -ErrorAction SilentlyContinue
Invoke-WebRequest -Uri 'http://127.0.0.1:8088/health' -UseBasicParsing -TimeoutSec 3
Invoke-WebRequest -Uri 'http://127.0.0.1:8088/tools/GetAllViewNames' -Method Post -Body '{}' -ContentType 'application/json' -UseBasicParsing -TimeoutSec 10
Invoke-WebRequest -Uri 'http://127.0.0.1:8088/tools/GetWorkPartInfo' -Method Post -Body '{}' -ContentType 'application/json' -UseBasicParsing -TimeoutSec 10
```

结果：

- NX 进程存在：`ugraf.exe`。
- `UGII_BASE_DIR=D:\Siemens\NX 11.0`。
- NX plugin health：HTTP 200，`{"ok":true,"data":"heartbeat","message":"执行成功"}`。
- 当前运行中插件 `GetAllViewNames` 返回旧数组结构：`["Top","Front","Right","Back","Bottom","Left","Isometric","Trimetric"]`。
- 当前 WorkPart 可读：`K08_1004201_21_conrod_body`。

## 实机验证是否完成

- 已完成 NX/NX plugin 环境只读补验。
- 未完成“改后插件实机截图验证”。原因：当前运行中 NXServer `/tools` 仍暴露旧 `SwitchView`/`CreateImage` 描述，`GetAllViewNames` 也返回旧数组结构，说明运行中 NX 会话未加载本次构建产物。没有 HTTP reload 路由；本次未重启 NX、未替换正在运行的插件 DLL，避免扩大操作范围。

## 失败分类和人工前置

- 代码静态/单元/构建验证：通过。
- 改后实机验证状态：`TEST_PRECONDITION_NOT_MET`，需要人工部署或重启 NX plugin 使本次构建产物进入当前 NX 会话后，再执行视图切换和截图实机验证。
- 人工前置：部署/加载改后 NX plugin DLL。

## 敏感信息

- 未输出 Teamcenter 密码、API key、cookie、token 或其他明文凭据。
- 未读取或记录 `tc_key`/`user_pass`。
