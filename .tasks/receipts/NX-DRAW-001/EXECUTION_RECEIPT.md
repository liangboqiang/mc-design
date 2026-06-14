# NX-DRAW-001 Execution Receipt

日期：2026-06-14

## 结论

已按最新 NX 图纸规则收口：

- `nx-auto-drawing` 不再进入 source skill、skill index、agent runtime、asset bundle 或 Windows payload。
- NX 自动出图和 Sheet 级图纸工具不再进入 NX manifest、client registry 或 agent 可发现清单。
- 当前唯一允许的 NX 图纸入口是 `nx_open_tcpart`：只在三维模型修改、参数校验和保存/更新完成后，打开用户确认的已绑定 NX 图纸 ItemRevision。
- 图纸与数模绑定后的自动更新即为项目所需图纸结果，mc-design 不再执行自动出图插件。

## 改动文件清单

- `mc-design-nx/assets/source/agents/design_agent/runtime.md`
- `mc-design-nx/assets/source/skills/INDEX.md`
- `mc-design-nx/assets/source/skills/nx-operation/SKILL.md`
- `mc-design-nx/assets/source/skills/design-report/SKILL.md`
- `mc-design-nx/assets/source/skills/dfmea-risk-review/SKILL.md`
- `mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md`
- `mc-design-nx/assets/source/skills/part-design/SKILL.md`
- `mc-design-nx/assets/source/skills/nx-parameter/SKILL.md`
- `mc-design-nx/assets/source/skills/nx-auto-drawing/SKILL.md`：已删除。
- `mc-design-nx/assets/source/tools/tool.nx/TOOL.md`
- `mc-design-nx/client/src/mc_design_client/tools/registry.py`
- `mc-design-nx/client/src/mc_design_client/tools/nx_provider.py`
- `mc-design-nx/client/tests/test_design_skill_contract.py`
- `mc-design-nx/client/tests/test_asset_store.py`
- `mc-design-nx/client/tests/test_windows_payload_builder.py`
- `mc-design-nx/client/tests/test_tool_registry.py`
- `mc-design-nx/client/tests/test_agent_loop_assets.py`
- `mc-design-nx/client/resources/agent_assets.mcdpkg`：已重新导出运行资产包。
- `mc-design-nx/client/resources/nx_tools_manifest.json`：已重新生成 NX 工具 manifest。
- `mc-design-nx/nx-plugin/src/McDesign.NXPlugin/ToolManager.cs`
- `mc-design-nx/nx-plugin/src/McDesign.NXTools/FileTools.cs`
- `mc-design-nx/nx-plugin/src/McDesign.NXTools/McDesign.NXTools.csproj`
- `mc-design-nx/package/windows/build/scripts/export_assets.py`
- `mc-design-nx/package/windows/build/scripts/generate_nx_manifest.py`
- `client/client/resources/agent_assets.mcdpkg`：已同步安装态运行资产包。
- `client/client/resources/nx_tools_manifest.json`：已同步安装态 NX manifest。
- `.tasks/receipts/S0-5/EXECUTION_RECEIPT.md`
- `.tasks/receipts/DFMEA-001/EXECUTION_RECEIPT.md`
- `.tasks/receipts/NX-DRAW-001/EXECUTION_RECEIPT.md`

未修改 `mc-design-ai-service`，未处理 K8s、test_agent_turn 或 beya/tjuae 替换。

## 删除/禁用的自动出图入口

- 删除 source skill：`mc-design-nx/assets/source/skills/nx-auto-drawing/SKILL.md`。
- 资产导出禁用 skill：`nx-auto-drawing` 加入 `export_assets.py` 的 `DISABLED_SKILLS`。
- NX manifest 生成禁用：
  - `nx_run_auto_drawing`
  - `nx_get_auto_drawing_tool_guide`
  - `nx_validate_auto_drawing_plan`
  - `nx_create_auto_drawing_sheet`
  - `nx_create_auto_drawing_views`
  - `nx_apply_pmi_inheritance_to_drawing_views`
  - `nx_delete_drawing_sheets`
  - `nx_enter_drafting_environment`
  - `nx_open_tc_drawing`
  - `nx_open_drawing_sheet`
  - `nx_get_drawing_sheet_name_list`
  - `nx_updatedrawings`
- Client registry 禁用同一批工具；直接调用返回 `NX_DRAWING_TOOL_DISABLED`，不会透传到 NX connector。
- NX plugin 扫描器 `ToolManager` 增加禁用清单；即使旧 DLL 中仍有相关 `[Tool]`，扫描注册和直接执行都会被拒绝。
- `McDesign.NXTools.csproj` 移除 `AutoDrawingTools.cs` 编译项，后续重新构建 NXTools.dll 时不会编入自动出图工具集。
- `FileTools.cs` 移除 `OpenTcDrawing`、`GetDrawingSheetNameList`、`OpenDrawingSheet`、`Updatedrawings` 的 `[Tool]` 公开属性。

## 当前唯一允许的 NX 图纸操作

唯一允许入口：`nx_open_tcpart`。

使用条件：

- 已完成三维模型修改。
- 已完成参数校验。
- 已完成保存/更新，或已明确需要用户/项目负责人在 NX/TC 中手动完成。
- 用户已确认要打开的已绑定 NX 图纸 ItemRevision。

禁止事项：

- 不通过 specification/drawing 数据集路径拼接打开图纸。
- 不调用自动出图插件。
- 不调用 Sheet 级图纸页列表、打开、创建、删除、更新或 PMI 继承工具。
- 未完成三维模型修改前不得打开图纸。

## nx-auto-drawing 存在性

`mc-design-nx/assets/source/skills/nx-auto-drawing/SKILL.md` 已删除，目录也已移除；它不再进入：

- `assets/source/skills/INDEX.md`
- `assets/source/agents/design_agent/runtime.md`
- `client/resources/agent_assets.mcdpkg`
- `client/client/resources/agent_assets.mcdpkg`
- Windows payload 临时构建结果
- agent 可加载清单

`nx-plugin/src/McDesign.NXTools/AutoDrawingTools.cs` 源文件仍作为历史源码保留，但：

- 不再由 `McDesign.NXTools.csproj` 编译。
- `generate_nx_manifest.py` 会过滤其 `[Tool]` 入口。
- `ToolManager` 会拒绝注册和执行相关名称。
- Client registry 会拒绝注册和透传相关名称。

因此 agent 不能发现或调用该能力。

## 验证结果

Manifest：

- `mc-design-nx/client/resources/nx_tools_manifest.json` 工具数：20。
- `client/client/resources/nx_tools_manifest.json` 工具数：20。
- 两处 manifest 均包含 `nx_open_tcpart`。
- 两处 manifest 均不包含：
  - `nx_run_auto_drawing`
  - `nx_get_auto_drawing_tool_guide`
  - `nx_validate_auto_drawing_plan`
  - `nx_open_tc_drawing`
  - `nx_open_drawing_sheet`
  - `nx_get_drawing_sheet_name_list`

Registry：

- `ClientToolCatalog.manifest()` 不注册禁用工具。
- 对 `Updatedrawings`、`nx_updatedrawings`、`RunAutoDrawing`、`nx_run_auto_drawing`、`OpenTcDrawing`、`nx_open_tc_drawing` 的 `call_nx()` 均返回 `NX_DRAWING_TOOL_DISABLED`。

Asset bundle：

- `mc-design-nx/client/resources/agent_assets.mcdpkg` 解包后 `skill_count=13`。
- `client/client/resources/agent_assets.mcdpkg` 解包后 `skill_count=13`。
- 两处资产包均不含 `nx-auto-drawing`。
- 两处 agent runtime 均不含 `skill.nx-auto-drawing`。

Windows payload：

- `test_windows_payload_builder.py` 覆盖临时 Windows payload 构建。
- 临时 payload 中 `agent_assets.mcdpkg` 不含 `nx-auto-drawing`。
- 临时 payload 中 NX manifest 不含禁用图纸/自动出图工具。
- 临时 payload 中保留 `nx_open_tcpart`。

搜索检查：

- `mc-design-nx/client/resources` 中未命中禁用工具名或 `nx-auto-drawing`。
- `client/client/resources` 中未命中禁用工具名或 `nx-auto-drawing`。
- source skill、agent runtime、tool 文档中没有把禁用入口写成可用能力；保留命中只存在于禁用清单、负向测试断言和历史源码。

## 测试命令和完整结果

指定测试命令：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client\tests\test_design_skill_contract.py client\tests\test_asset_store.py client\tests\test_windows_payload_builder.py client\tests\test_tool_registry.py -q
```

结果：

```text
...........................................                              [100%]
43 passed in 3.00s
```

额外回归：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client\tests\test_agent_loop_assets.py -q
```

结果：

```text
..                                                                       [100%]
2 passed in 0.20s
```

Diff 检查：

```powershell
git diff --check -- <NX-DRAW-001 touched tracked files>
git diff --check -- client/client/resources/agent_assets.mcdpkg client/client/resources/nx_tools_manifest.json
```

结果：通过。仅有 Git 提示部分文本文件未来可能按仓库设置进行 LF/CRLF 转换。

## 未处理项和原因

- 未处理 `test_agent_turn`：任务明确限制不处理。
- 未处理 K8s：任务明确限制不处理。
- 未处理 beya/tjuae 替换：任务明确限制不处理。
- 未修改 AI service：任务明确限制不改 AI service。
- 未新增任何自动出图能力。
- 未重新编译 NX plugin DLL：本轮完成源码、manifest、registry、asset bundle、Windows payload 和安装态资源收口；当前 agent 已无法发现或调用禁用入口。发布新 NXTools/NXServer DLL 时仍需在具备 NX11/MSBuild 的环境执行正式构建。
