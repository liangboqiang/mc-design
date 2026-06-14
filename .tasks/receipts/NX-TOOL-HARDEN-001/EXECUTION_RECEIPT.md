# NX-TOOL-HARDEN-001 Execution Receipt

日期：2026-06-14

## 改动文件清单

- `mc-design-nx/nx-plugin/src/McDesign.NXSDK/NXResult.cs`
- `mc-design-nx/nx-plugin/src/McDesign.NXPlugin/ToolManager.cs`
- `mc-design-nx/nx-plugin/src/McDesign.NXPlugin/HttpServer.cs`
- `mc-design-nx/nx-plugin/src/McDesign.NXTools/FileTools.cs`
- `mc-design-nx/client/src/mc_design_client/api/server.py`
- `mc-design-nx/client/src/mc_design_client/tools/registry.py`
- `mc-design-nx/package/windows/build/scripts/generate_nx_manifest.py`
- `mc-design-nx/client/resources/nx_tools_manifest.json`
- `mc-design-nx/assets/source/tools/tool.nx/TOOL.md`
- `mc-design-nx/client/tests/test_tool_registry.py`
- `mc-design-nx/client/tests/test_usage_issue_fixes.py`
- `.tasks/receipts/NX-TOOL-HARDEN-001/EXECUTION_RECEIPT.md`

## NX Plugin 暴露面加固

- `ToolManager` 工具程序集加载从目录泛扫收敛为显式 allowlist，目前只加载 `NXTools.dll`。
- 未知 DLL、基础 DLL、临时 DLL 不再因为落在 `tools` 目录而被 `Assembly.LoadFrom` 加载。
- `NXResult` 增加结构化错误字段：`code`、`retryable`、`details`，保持既有 `ok`、`data`、`message` 兼容。
- 工具名为空、工具不存在、调用失败、参数缺失、参数转换失败、坏 JSON、参数名歧义均返回结构化错误码。
- 参数名大小写兼容和去 `_`/`-` 归一化仍保留，但归一化后匹配多个输入键时返回 `NX_PARAMETER_NAME_AMBIGUOUS`，不再选择第一个匹配项。

## 自动出图禁用验证

- `AutoDrawingTools.cs` 保留在源码树中，但 `McDesign.NXTools.csproj` 未编译该文件。
- `ToolManager` 禁用表覆盖以下工具及变体：`nx-auto-drawing`、`nx_run_auto_drawing`、`nx_updatedrawings`、`nx_update_drawings`、`nx_open_tc_drawing`、`nx_open_drawing_sheet`、自动创建/删除/打开 Sheet、自动创建工程图视图、PMI 继承到工程图视图等工具。
- `ToolCatalog` 和 `NxToolProvider` 保持禁用工具不过 manifest、不过 connector。
- 直接调用禁用工具名时返回 `NX_DRAWING_TOOL_DISABLED`，并声明唯一允许的 NX 图纸入口为 `nx_open_tcpart`。
- `generate_nx_manifest.py` 同步过滤禁用图纸工具和旧 `nx_fs_*` 文件桥工具，防止重新生成 manifest 时恢复暴露面。

## 请求体、坏 JSON、并发和错误码加固

- NX plugin `HttpServer`：
  - 请求头上限：64 KiB。
  - 请求体上限：1 MiB。
  - 非法或重复 `Content-Length` 返回 `400 / NX_INVALID_CONTENT_LENGTH`。
  - 超大请求体返回 `413 / NX_REQUEST_BODY_TOO_LARGE`。
  - 工具调用坏 JSON 返回 `400 / NX_BAD_JSON`。
  - 工具调用 JSON 非 object 返回 `400 / NX_JSON_OBJECT_REQUIRED`。
  - `GET /tools/{name}` 等非 POST 工具调用返回 `405 / NX_METHOD_NOT_ALLOWED`。
  - 并发处理使用 `SemaphoreSlim`，上限 8，超过等待窗口返回 `503 / NX_SERVER_BUSY`。
- 本地客户端 API：
  - `/api/runtime/tools/execute` 使用 1 MiB body 上限。
  - 坏 JSON 返回 `400 / LOCAL_API_BAD_JSON`。
  - 超大 body 返回 `413 / LOCAL_API_REQUEST_TOO_LARGE`。
  - 非 object JSON 返回 `400 / LOCAL_API_JSON_OBJECT_REQUIRED`。
  - `/api/runtime/test/agent-turn` 入口仍调用 `ClientApp.test_agent_turn`，路由行为保持。

## NX 文件/图片工具检查

- `CreateNewPart`：
  - `folder_path` 必须为绝对本地或 UNC 路径。
  - 拒绝相对路径、TC `@DB` 路径和 URI。
  - `part_name` 必须是文件名，不能包含目录片段或非法文件名字符。
  - 解析后的输出路径必须仍位于 `folder_path` 内。
- `CreateImage`：
  - `filePath` 必须为绝对本地或 UNC 路径。
  - 拒绝相对路径、TC `@DB` 路径和 URI。
  - 只允许 `.png`、`.jpg`、`.jpeg`、`.tif`、`.tiff`、`.bmp`、`.gif`。
  - 工具说明明确调用方需确认覆盖风险。
- `GetWorkPartInfo`：
  - 新增正确字段 `part_name`。
  - 保留旧字段 `part_nane` 作为兼容输出。

## tool.nx 更新

- 明确 NX plugin 只负责 NX 会话能力，不承载业务流程编排、Teamcenter 查询编排、文件桥接或自动出图流程。
- 明确 TC 主模型和已绑定 NX 图纸 ItemRevision 都只通过 `nx_open_tcpart` 打开。
- 明确 `nx-auto-drawing`、`nx_run_auto_drawing`、`nx_updatedrawings`、`nx_open_tc_drawing`、`nx_open_drawing_sheet` 和 Sheet 级图纸工具不可用。

## 新增/更新测试

- `test_nx_auto_drawing_source_is_outside_build_and_manifest`
- `test_nx_plugin_tool_manager_protocol_hardening_is_declared`
- `test_nx_plugin_http_server_protocol_limits_are_declared`
- `test_nx_file_tools_declare_write_boundaries_and_part_name_compatibility`
- `test_client_api_tool_execute_rejects_bad_json_and_large_body_without_crashing`
- 更新禁用工具验证，覆盖 `NX_DRAWING_TOOL_DISABLED`。

## 测试命令和结果

命令：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m py_compile client\src\mc_design_client\api\server.py client\src\mc_design_client\tools\registry.py package\windows\build\scripts\generate_nx_manifest.py client\tests\test_usage_issue_fixes.py client\tests\test_tool_registry.py
```

结果：通过。

命令：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client\tests\test_tool_registry.py::test_nx_auto_drawing_source_is_outside_build_and_manifest client\tests\test_tool_registry.py::test_nx_plugin_tool_manager_protocol_hardening_is_declared client\tests\test_tool_registry.py::test_nx_plugin_http_server_protocol_limits_are_declared client\tests\test_tool_registry.py::test_nx_file_tools_declare_write_boundaries_and_part_name_compatibility client\tests\test_tool_registry.py::test_disabled_nx_capability_tools_are_not_registered_or_passthrough client\tests\test_tool_registry.py::test_tc_drawing_manifest_contract client\tests\test_usage_issue_fixes.py::test_client_api_tool_execute_rejects_bad_json_and_large_body_without_crashing -q
```

结果：`7 passed in 0.73s`。

命令：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client\tests\test_usage_issue_fixes.py -q
```

结果：`11 passed in 1.33s`。

命令：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client\tests\test_tool_registry.py client\tests\test_usage_issue_fixes.py -q
```

结果：`34 passed in 1.82s`。

未运行 NX 实机编译或 NX 会话调用测试。原因：当前执行环境未确认可用的 NX/UGII/MSBuild 会话环境，本任务验证采用 Python 单测和 C# 源码静态协议边界检查。
