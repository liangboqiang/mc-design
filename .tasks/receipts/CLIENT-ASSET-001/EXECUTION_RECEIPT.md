# CLIENT-ASSET-001 执行回执

更新时间：2026-06-14

## 任务边界

本次只做 mc-design-client 资产链路只读自检、文档固化、测试补强和必要诊断代码。未处理 beya -> tjuae 运行时替换，未处理客户端安装包卸载失败，未删除、迁移或清理 `cc_haha`、旧 `.beya`、旧 `asset_views`、`package/windows/output`，未修改外部 tjuae 项目，未启动客户端、K8s、NX 或 Teamcenter。

## 输入依据

- `.tasks/TEST_EXECUTION_RULES.md`
- `.tasks/receipts/CLIENT-ARCH-001/AUDIT_RECEIPT.md`
- `.tasks/receipts/CLIENT-ARCH-001/CLIENT_ARCHITECTURE_MAP.md`
- `.tasks/receipts/CLIENT-ARCH-001/CLIENT_CLEANUP_CANDIDATES.csv`
- `.tasks/receipts/CLIENT-ARCH-001/CLIENT_RESTRUCTURE_PROPOSAL.md`
- `mc-design-nx/package/windows/build/scripts/export_assets.py`
- `mc-design-nx/package/windows/build/scripts/payload_builder.py`
- `mc-design-nx/client/src/mc_design_client/assets/store.py`
- `mc-design-nx/client/src/mc_design_client/runtime/environment.py`
- 目标测试文件：`test_asset_store.py`、`test_agent_loop_assets.py`、`test_tjuae_runtime_adapter.py`

## 改动文件清单

- `mc-design-nx/client/src/mc_design_client/assets/diagnostics.py`：新增只读资产链路诊断函数 `inspect_asset_chain(...)`。
- `mc-design-nx/client/src/mc_design_client/assets/__init__.py`：导出 `inspect_asset_chain`，便于测试和 CLI 使用。
- `mc-design-nx/client/src/mc_design_client/cli.py`：`doctor` 增加 `checks.asset_chain`；补齐 `python -m mc_design_client.cli ...` 直接执行入口。
- `mc-design-nx/client/README_TJUAE_RUNTIME.md`：新增 Asset Chain 文档，固化 asset、asset_view、`.tjuae/skills`、tjuae SDK/server 和 `cc_haha` 边界。
- `mc-design-nx/client/tests/test_asset_store.py`：新增只读诊断一致性和 legacy 只报告不删除测试。
- `mc-design-nx/client/tests/test_agent_loop_assets.py`：增强运行资产包来源、当前 asset view、tjuae 可见路径和 legacy report_only 断言。
- `mc-design-nx/client/tests/test_tjuae_runtime_adapter.py`：增强 workspace `.tjuae/skills` managed manifest 同步断言。

## 资产链路说明

当前固化链路为：

```text
mc-design-nx/assets/source
  -> mc-design-nx/client/resources/agent_assets.mcdpkg
  -> mc-design-nx/client/data/asset_views/runtime-agentloop
  -> mc-design-nx/client/data/workspace/.tjuae/skills
```

结论：

- `asset` 是源资产或打包资产内容，包括 agent runtime、skills、tools、static 协议文件、脚本、模板和示例。
- `asset_view` 是从 `agent_assets.mcdpkg` 解包出来的运行时投影/cache，不是源。
- `agent_assets.mcdpkg` 是当前运行资产包来源，由 `AssetStore` 读取，由 `AssetStore.project_to(...)` 投影到 `runtime-agentloop`。
- `RuntimeEnvironment._sync_project_skills()` 把 `runtime-agentloop/skills` 下的项目 skills 同步到 `workspace/.tjuae/skills`，并写 `.mc-design-managed` 与 `.mc-design-managed.json`。
- `tjuae-sdk` 不直接读取 `agent_assets.mcdpkg` 或 `asset_views`；mc-design adapter 通过 tjuae SDK 调用 session/plugin/tool/chat API。
- tjuae server 实际通过 `work_dir/cwd = client/data/workspace` 发现 `workspace/.tjuae/skills`。
- `cc_haha_agent_runtime_migration_pack` 是外部 cc-haha/Claude Code 风格迁移参考残留，不是当前 client runtime、测试或 Windows payload 依赖。它不应留在活跃客户端结构中，否则会继续误导运行时边界判断；本任务只报告，不删除。

## 诊断入口和示例输出

入口：

```powershell
$env:PYTHONPATH = 'E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\client\src'
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m mc_design_client.cli --root mc-design-nx\client doctor
```

`doctor` 现在输出 `checks.asset_chain`。该块为只读，不调用 `AssetStore.project_to(...)`，不删除、不迁移 legacy 目录。

本次诊断摘要：

```json
{
  "ok": true,
  "bundle_version": "test-local-dev",
  "sha256": "20f55c4146ac2ac7bb04eeeacd5739a4432dfe328d8a30a4084908cefef01859",
  "source": "E:\\A0_Projects\\A1_Dynamics_Design_LM\\mc-design\\mc-design-nx\\assets\\source",
  "package": "E:\\A0_Projects\\A1_Dynamics_Design_LM\\mc-design\\mc-design-nx\\client\\resources\\agent_assets.mcdpkg",
  "asset_view_root": "E:\\A0_Projects\\A1_Dynamics_Design_LM\\mc-design\\mc-design-nx\\client\\data\\asset_views\\runtime-agentloop",
  "workspace_skills": "E:\\A0_Projects\\A1_Dynamics_Design_LM\\mc-design\\mc-design-nx\\client\\data\\workspace\\.tjuae\\skills",
  "consistency": {
    "source_package_skills_match": true,
    "package_projection_skills_match": true,
    "projection_workspace_managed_skills_match": true,
    "package_workspace_managed_skills_match": true,
    "all_skills_match": true
  }
}
```

说明：`doctor` 同时报告 `local_api` 和 `nx_plugin` 连接拒绝，因为本任务明确不启动客户端和 NX。这不影响 `asset_chain.ok=true` 的静态资产链路判定。

## Legacy 候选目录清单

本任务只报告，不删除：

| 名称 | 路径 | 类型 | 状态 |
|---|---|---|---|
| `runtime-live` | `mc-design-nx/client/data/asset_views/runtime-live` | legacy asset view | exists, report_only |
| `test-local-dev` | `mc-design-nx/client/data/asset_views/test-local-dev` | legacy asset view | exists, report_only |
| `.beya` | `mc-design-nx/client/data/workspace/.beya` | legacy Beya workspace | exists, report_only |
| `cc_haha_agent_runtime_migration_pack` | `mc-design-nx/client/cc_haha_agent_runtime_migration_pack` | external runtime migration reference | exists, report_only |
| `governance` | `mc-design-nx/client/data/governance` | legacy governance overlay or pending data | exists, report_only |

旧 `runtime-live` 和 `test-local-dev` 未被当成当前运行入口；当前入口只认 `client/data/asset_views/runtime-agentloop`。

## 新增/更新测试清单

- `test_asset_store.py::test_asset_chain_diagnostics_reports_consistency_and_legacy_without_deleting`
- `test_agent_loop_assets.py::test_packaged_agent_assets_control_identity_and_indexed_assets`
- `test_agent_loop_assets.py::test_registry_runtime_projection_is_the_only_runtime_asset_view`
- `test_tjuae_runtime_adapter.py::test_tjuae_adapter_syncs_workspace_skills_and_plugin_tools_only_from_static_assets`

覆盖点：

- `agent_assets.mcdpkg` 是运行资产包来源。
- `AssetStore.project_to(...)` 稳定投影到当前 `runtime-agentloop`。
- `RuntimeEnvironment._sync_project_skills()` 把项目 skills 同步到 `workspace/.tjuae/skills`。
- 旧 `runtime-live` / `test-local-dev` 不被当作当前运行入口。
- 诊断逻辑只报告 legacy 候选，不删除 sentinel 文件。

## 测试命令和结果

执行命令：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx\client\tests\test_asset_store.py mc-design-nx\client\tests\test_agent_loop_assets.py mc-design-nx\client\tests\test_tjuae_runtime_adapter.py -q
```

结果：

```text
29 passed in 1.17s
```

另执行 `doctor` 入口验证，退出码 0，`checks.asset_chain.ok=true`。未启动客户端、K8s、NX 或 Teamcenter。

## 未处理事项及原因

- 未删除 `runtime-live`、`test-local-dev`、`.beya`、`cc_haha`、`governance` 或 `package/windows/output`：本任务边界要求只报告不删除。
- 未处理 beya -> tjuae 运行时替换：明确排除在本任务之外。
- 未处理客户端安装包卸载失败：明确排除在本任务之外，仍归属 E2E/安装链路任务。
- 未修改外部 tjuae 项目：本任务仅在 mc-design-client 内补诊断和文档。
- 未做真实客户端、K8s、NX、Teamcenter E2E：本任务不要求启动这些系统。

## 敏感信息

本次未输出 `tc_key`、API key、cookie、token 或任何明文凭据。`doctor` 输出中仅包含本地路径、bundle version、sha256、静态链路一致性和连接状态。
