# NX-PARAM-002 EXECUTION RECEIPT

执行日期：2026-06-14

## 任务边界

- 已阅读 `.tasks/TEST_EXECUTION_RULES.md`。
- 本轮只处理 NX 参数工具、NX 参数 skill/tool 说明、NX manifest 生成和相关测试。
- 未修改 runtime adapter、参数规则脚本、launcher。
- 未启用、恢复或调用自动出图工具；`nx-auto-drawing`、`nx_run_auto_drawing`、`nx_updatedrawings` 仍仅作为禁用能力出现在说明中。

## 改动文件清单

- `mc-design-nx/nx-plugin/src/McDesign.NXTools/ExpressionTools.cs`
- `mc-design-nx/package/windows/build/scripts/generate_nx_manifest.py`
- `mc-design-nx/assets/source/skills/nx-parameter/SKILL.md`
- `mc-design-nx/assets/source/tools/tool.nx/TOOL.md`
- `mc-design-nx/client/tests/test_tool_registry.py`
- `mc-design-nx/client/resources/tool_execution_map.json`

生成/验证文件：

- `mc-design-nx/client/resources/nx_tools_manifest.json`：由 `generate_nx_manifest.py` 重新生成，当前 `.gitignore` 忽略。
- `mc-design-nx/client/resources/agent_assets.mcdpkg`：由 pytest session fixture / asset 打包测试重新生成，当前 `.gitignore` 忽略。

## 新/改工具 schema

### `nx_resolve_parameter`

- `danger_level`: `read`
- 输入字段：
  - `std_id?: string`
  - `display_name?: string`
  - `aliases?: string[]`
  - `expected_group?: string`
  - `unit?: string`
  - `allow_ambiguous?: boolean`
- 唯一解析成功时 `ok=true`，`data` 包含：
  - `resolved`
  - `matches`
  - `selected_expression`
  - `ambiguity_reason`
  - `available_groups`
- 无输入、未命中或多命中时 `ok=false`，上述字段进入 `details`，不得进入写入。

### `nx_update_param`

- 输入字段：
  - `std_id: string`
  - `value: string`
  - `resolved_expression_id?: string`
- `std_id` 直接写入时必须是安全真实 NX 表达式 ID；中文/别名/业务名必须先解析。

### `nx_batch_update_params`

- 输入字段：
  - `expressions: [{ std_id: string, value: string, resolved_expression_id?: string }]`
- `expressions[]` item schema 已包含 `required: ["std_id", "value"]`。

## 写入安全边界

- 直接 `std_id` 写入只接受 ASCII 标识符格式：`^[A-Za-z_][A-Za-z0-9_]*$`。
- `std_id` 含中文、非 ASCII、空格或非标识符字符时，直接写入返回 `NX_PARAMETER_NAME_REQUIRES_RESOLVE`。
- `resolved_expression_id` 必须精确命中当前 WorkPart 中真实表达式，且表达式可编辑。
- 未找到表达式、表达式不可编辑、值为空、值为 `NaN` / `Infinity` 均不写入。
- `BatchUpdateParams` 改为两阶段：先校验整批目标和值；任一项失败时返回 `NX_PARAMETER_BATCH_VALIDATION_FAILED`，整批不执行。
- `ResolveParameter` 未命中或多命中返回失败结构；歧义结果只能用于人工确认，不得写入。
- `HighLightDim` 未找到尺寸时立即返回 `NX_DIMENSION_NOT_FOUND`，不再继续访问空对象。

## 错误码说明

- `NX_PARAMETER_QUERY_REQUIRED`：解析工具缺少输入。
- `NX_PARAMETER_NO_MATCH`：解析无候选。
- `NX_PARAMETER_AMBIGUOUS`：解析命中多个候选。
- `NX_PARAMETER_RESOLVE_FAILED`：解析过程异常。
- `NX_PARAMETER_ID_REQUIRED`：写入目标表达式 ID 为空。
- `NX_PARAMETER_NAME_REQUIRES_RESOLVE`：直接写入参数名不是安全 NX 表达式 ID。
- `NX_PARAMETER_NOT_FOUND`：真实表达式 ID 不存在。
- `NX_PARAMETER_READONLY`：表达式不可编辑。
- `NX_PARAMETER_VALUE_REQUIRED`：写入值为空。
- `NX_PARAMETER_VALUE_INVALID`：写入值为 `NaN` / `Infinity` 等非法值。
- `NX_PARAMETER_BATCH_EMPTY`：批量更新列表为空。
- `NX_PARAMETER_BATCH_VALIDATION_FAILED`：批量预校验失败，未执行写入。
- `NX_PARAMETER_BATCH_UPDATE_FAILED`：批量执行阶段异常。
- `NX_PARAMETER_UPDATE_FAILED`：单项更新异常。
- `NX_DIMENSION_NOT_FOUND`：未找到待高亮尺寸。
- `NX_DIMENSION_HIGHLIGHT_FAILED`：高亮过程异常。

## 测试命令和结果

1. 生成 NX manifest

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' mc-design-nx/package/windows/build/scripts/generate_nx_manifest.py --source-root mc-design-nx/nx-plugin/src/McDesign.NXTools --output mc-design-nx/client/resources/nx_tools_manifest.json
```

结果：`ok=true`，`tool_count=21`。

2. NX 工具注册/参数安全静态测试

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx/client/tests/test_tool_registry.py -q
```

结果：`31 passed in 0.87s`。

3. 资产打包与 Windows payload 静态测试

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx/client/tests/test_asset_store.py mc-design-nx/client/tests/test_windows_payload_builder.py -q
```

结果：`14 passed in 1.36s`。

4. NX core C# 构建

```powershell
cmd /c mc-design-nx\nx-plugin\build-core.bat Release
```

结果：构建成功，输出 `NXSDK.dll`、`NXTools.dll`、`NXServer.dll`。MSBuild 报告若干 NX 可选 managed assembly 未解析 warning，例如 `CaeDseWorkflowOpen`、`CLDCommonOpen`、`DSEOpen`，未出现编译错误。

5. 空白/冲突标记检查

```powershell
git diff --check -- nx-plugin/src/McDesign.NXTools/ExpressionTools.cs package/windows/build/scripts/generate_nx_manifest.py assets/source/skills/nx-parameter/SKILL.md assets/source/tools/tool.nx/TOOL.md client/tests/test_tool_registry.py client/resources/tool_execution_map.json
```

结果：通过；仅有既有 LF/CRLF warning。

## NX 实机验证

- NX 进程检查：存在 `ugraf` 进程，PID `67296`，启动时间 `2026/6/14 13:18:09`。
- NX plugin 端口检查：`127.0.0.1:8088` 正在监听。
- `GET http://127.0.0.1:8088/health`：返回 `ok=true`，`data=heartbeat`。
- `GET http://127.0.0.1:8088/tools`：当前运行中的插件仍加载旧工具程序集，未暴露 `ResolveParameter`，`UpdateParam` / `BatchUpdateParams` 描述仍是旧版本。

结论：未完成新工具的 NX 实机验证。原因是当前 NX 会话未重载本轮新构建的 NXTools 程序集；本轮未重启 NX/plugin，未调用任何参数写入工具。分类：`TEST_PRECONDITION_NOT_MET`（运行中插件未加载新程序集）。

## 敏感信息

- 未读取、输出或写入 Teamcenter 密码、API key、cookie、token。
- 本回执不包含明文凭据。
