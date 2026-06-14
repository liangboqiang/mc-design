# S0-5 EXECUTION RECEIPT

## 改动文件清单

- `mc-design-nx/assets/source/skills/design-report/SKILL.md`
- `mc-design-nx/assets/source/skills/design-report/scripts/design_report.py`
- `mc-design-nx/assets/source/skills/design-report/resources/report_payload.schema.json`
- `mc-design-nx/assets/source/skills/design-report/examples/report_payload.complete.json`
- `mc-design-nx/assets/source/skills/design-report/tests/test_design_report.py`
- `mc-design-nx/assets/source/skills/nx-auto-drawing/SKILL.md`（历史记录；NX-DRAW-001 已删除/禁用，不再作为可加载 skill）
- `mc-design-nx/assets/source/skills/nx-operation/SKILL.md`
- `mc-design-nx/assets/source/skills/dfmea-risk-review/SKILL.md`
- `mc-design-nx/assets/source/skills/INDEX.md`
- `mc-design-nx/assets/source/agents/design_agent/runtime.md`
- `mc-design-nx/assets/source/tools/tool.local_file/TOOL.md`
- `mc-design-nx/client/src/mc_design_client/tools/local_file_provider.py`
- `mc-design-nx/client/tests/test_tool_registry.py`
- `mc-design-nx/client/tests/test_design_skill_contract.py`
- `mc-design-nx/client/tests/test_agent_loop_assets.py`
- `mc-design-nx/client/tests/test_asset_store.py`
- `mc-design-nx/client/tests/test_windows_payload_builder.py`
- `mc-design-nx/package/windows/build/scripts/export_assets.py`
- `mc-design-nx/nx-plugin/src/McDesign.NXTools/FileTools.cs`
- `mc-design-nx/nx-plugin/src/McDesign.NXTools/ViewTools.cs`

未修改 IPM/QPP/ECMS 工具，未做 beya/tjuae 替换，未修改 TC/NX 生命周期主状态机。

## 报告/截图/说明书流程

1. `inspect-template` 读取 skill 内置 DOCX 模板和槽位。
2. `prepare` 创建 `design_reports/input`、`design_reports/images`、`design_reports/preview`、`design_reports/output`，并生成带 `confirmations` 的 payload skeleton。
3. `validate` 校验槽位、图片路径、截图视角证明、旧说明书来源记录。
4. 用户确认生成前摘要后，payload 写入 `confirmations.generation.confirmed=true` 和 `confirmation_source="user"`。
5. `preview` 或兼容别名 `generate` 只生成预览 DOCX，返回 `preview_path`、`preview_download`、`preview_token`，不写正式输出。
6. 用户打开预览并确认后，payload 写入 `confirmations.preview.confirmed=true`、`confirmation_source="user"`、`preview_token=<返回值>`。
7. `save-final` 校验 preview token 后复制预览为正式 DOCX。
8. Teamcenter 上传不由报告脚本执行；上传前必须再写入 `confirmations.tc_upload.confirmed=true`，否则 `tc_upload_allowed=false`。

## 本地下载路径策略

- 预览和正式输出都返回 `local_download` 或 `preview_download` 结构。
- `local_path` 是用户本机路径。
- `read_with_local_file` 使用 `local_file_read_bytes(root="runtime_workspace", path=<workspace_relative_path>)`。
- 正式输出位于 `design_reports/output` 时，还返回 `read_with_report_output_root`，可用 `local_file_read_bytes(root="report_output", path=<output_relative_path>)`。
- 明确禁止只向用户返回 K8s/容器内部路径。

## 截图视角验证策略

- 多视角图片槽位必须记录 `view_name` 和唯一 `capture_order`。
- 推荐记录 `view_proof.requested_view_name`、`view_proof.confirmed_view_name`、`view_proof.capture_order`。
- `validate` 会返回：
  - `SCREENSHOT_VIEW_PROOF_REQUIRED`
  - `SCREENSHOT_VIEW_NOT_DISTINCT`
  - `SCREENSHOT_CAPTURE_ORDER_DUPLICATE`
- `nx_switch_view` 成功结果现在返回 `requested_view_name` 和 `confirmed_view_name`。
- `nx_create_image` 成功结果现在返回 `view_name` 和 `work_part_name`，便于写入 payload 作为截图证据。

## TC 旧说明书来源记录方式

从 TC 下载旧说明书并复用内容时，槽位必须标记 `copied_from_previous_report=true` 或 `source_type="tc_previous_report"`，并填写：

```json
{
  "source_record": {
    "source_file": "旧说明书文件名.docx",
    "source_section": "来源章节或段落",
    "source_path": "Teamcenter:/item/rev/specification/旧说明书文件名.docx",
    "source_tool": "teamcenter download"
  }
}
```

至少需要 `source_file`，并在 `source_paragraph`、`source_section`、`source_path` 中提供一项定位信息；缺失时返回 `PREVIOUS_REPORT_SOURCE_RECORD_REQUIRED` 或 `PREVIOUS_REPORT_SOURCE_RECORD_INCOMPLETE`。

## 调用边界和前置条件

- NX-DRAW-001 修正后的图纸口径：二维图不再要求或调用自动出图插件；报告流程只能引用已通过 `nx_open_tcpart` 打开的已绑定 NX 图纸、截图和报告证据。图纸与数模绑定后的自动更新即视为项目所需图纸结果。自动出图插件、Sheet 级图纸工具和旧图纸更新工具均不得作为 S0-5 的可用能力或验收项。
- 说明书：归 `design-report`；前置条件是模板槽位、证据、截图视角证明、生成前确认和预览确认齐备。保存和上传分开确认。
- DFMEA：归 `dfmea-risk-review`；只输出风险复核，不打开/更新二维图，不保存说明书，不上传 Teamcenter。

## 新增/更新测试

- `design-report/tests/test_design_report.py`
  - 本地下载路径
  - 生成前确认
  - 预览确认后保存
  - 上传前确认 gate
  - 截图视角重复拒绝
  - TC 旧说明书来源记录
- `client/tests/test_design_skill_contract.py`
  - report 预览/保存/来源/视角合同
  - NX-DRAW-001 修正：不再要求自动出图 skill，改为验证 `nx_open_tcpart` 是唯一允许的 NX 图纸入口
  - DFMEA 边界
- `client/tests/test_tool_registry.py`
  - `report_output` 本地下载根
- `client/tests/test_agent_loop_assets.py`
  - NX-DRAW-001 修正：agent 不再加载 `nx-auto-drawing`
- `client/tests/test_asset_store.py`
  - NX-DRAW-001 修正：资产包/投影不包含 `nx-auto-drawing`
- `client/tests/test_windows_payload_builder.py`
  - NX-DRAW-001 修正：Windows payload 不包含 `nx-auto-drawing`

## 测试命令和结果

- `..\client\client\python\python.exe -m py_compile assets\source\skills\design-report\scripts\design_report.py`
  - 通过。
- `..\client\client\python\python.exe assets\source\skills\design-report\scripts\design_report.py inspect-template`
  - 通过，`slot_count=23`、`text_slot_count=18`、`image_slot_count=5`。
- 端到端 CLI 临时 workspace：`validate -> preview -> save-final`
  - 通过；预览存在、正式输出保存前不存在、未带 preview token 保存被拒绝、带 token 后保存成功、`tc_upload_allowed=false`。
- 负例 CLI：
  - 缺 `generation` 确认返回 `needs_generation_confirmation`。
  - 重复截图视图返回 `SCREENSHOT_VIEW_NOT_DISTINCT`。
  - 缺旧说明书 `source_record` 返回 `PREVIOUS_REPORT_SOURCE_RECORD_REQUIRED`。
- 自定义 runner 执行 `assets/source/skills/design-report/tests/test_design_report.py`
  - 12/12 通过。
- 自定义 runner 执行 `client/tests/test_design_skill_contract.py`
  - 18/18 通过。
- 自定义 runner 执行 `client/tests/test_tool_registry.py`
  - 12/12 通过。
- 自定义 runner 执行 `client/tests/test_agent_loop_assets.py`
  - 2/2 通过。
- fake pytest runner 执行 `client/tests/test_windows_payload_builder.py`
  - 5/5 通过。
- `client/tests/test_design_report_generation.py::test_design_report_assets_are_packaged_with_skill_resources`
  - 通过。
- `git diff --check`（S0-5 相关文件范围）
  - 通过；仅有 Git 提示未来可能 CRLF 转换。

## 无法实测项及原因

- 完整 `pytest`：当前可用嵌入式 Python 未安装 `pytest`，系统无 `python/py/uv/pip` 命令；已用自定义 runner 覆盖可直接执行的测试函数。
- `client/tests/test_asset_store.py` 全量：自定义 runner 中 6/7 通过，剩余 schema 测试因嵌入式环境缺少 YAML 解析依赖，fallback 解析器无法处理完整 YAML 缩进，属于测试环境限制。
- 真实 NX 截图：未发现 `ugraf/nx` 工作进程，仅有 Siemens 文档/Solr 服务；`127.0.0.1:8088` NX bridge 端口连接失败。无法实际执行 `nx_switch_view`/`nx_create_image`。需要用户启动 NX、打开目标模型并加载 NX bridge 后才能做真实截图实测。
