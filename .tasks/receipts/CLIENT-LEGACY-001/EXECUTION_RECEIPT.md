# CLIENT-LEGACY-001 执行回执

更新时间：2026-06-14

## 任务边界

本次只处理 mc-design-client legacy 运行残留的归档、迁移、诊断说明和测试补强。未处理客户端安装包卸载失败，未修改 PKG/E2E 逻辑，未处理 CLIENT-DATA-001 或 CLIENT-TJUAE-001 的 data root/managed skills 分离，未做 beya -> tjuae 运行时替换，未修改外部 tjuae 项目，未启动客户端、K8s、NX 或 Teamcenter，未清理 `package/windows/output`。

所有从活跃 `mc-design-nx/client` 目录移除的 legacy 数据均已先生成 before manifest；旧运行数据目录已复制归档并校验后再移除，`cc_haha` 已移动到 `references/legacy-runtime/cc-haha/` 保留证据。

## 输入依据

- `.tasks/TEST_EXECUTION_RULES.md`
- `.tasks/receipts/CLIENT-ARCH-001/AUDIT_RECEIPT.md`
- `.tasks/receipts/CLIENT-ARCH-001/CLIENT_CLEANUP_CANDIDATES.csv`
- `.tasks/receipts/CLIENT-ASSET-001/EXECUTION_RECEIPT.md`
- `mc-design-nx/client/README_TJUAE_RUNTIME.md`
- `mc-design-nx/client/src/mc_design_client/assets/diagnostics.py`
- `mc-design-nx/client/src/mc_design_client/cleanup.py`

## 改动文件清单

- `mc-design-nx/client/README_TJUAE_RUNTIME.md`：明确当前运行只认 `runtime-agentloop`，tjuae server 只通过 `workspace/.tjuae/skills` 发现项目 skills，归档后的 legacy 目录不应作为运行入口。
- `mc-design-nx/client/src/mc_design_client/assets/diagnostics.py`：legacy candidate 缺失时返回稳定 `action=absent`，存在时仍为 `report_only`。
- `mc-design-nx/client/tests/test_asset_store.py`：补充 legacy 存在/缺失两类诊断测试。
- `mc-design-nx/client/tests/test_agent_loop_assets.py`：补充当前资产链路一致性、`runtime-agentloop` 唯一运行入口、活跃 client 目录无 `cc_haha` 断言。
- `references/legacy-runtime/cc-haha/README.md`：说明 `cc_haha_agent_runtime_migration_pack` 仅为外部运行时迁移参考，不是 mc-design-client runtime 依赖。
- `references/legacy-runtime/cc-haha/cc_haha_agent_runtime_migration_pack/`：从活跃 client 目录迁移的 cc-haha 参考包。
- `.tasks/archives/CLIENT-LEGACY-001/`：旧运行数据目录归档证据。
- `.tasks/receipts/CLIENT-LEGACY-001/LEGACY_MANIFEST_BEFORE.json`
- `.tasks/receipts/CLIENT-LEGACY-001/LEGACY_MANIFEST_AFTER.json`
- `.tasks/receipts/CLIENT-LEGACY-001/DOCTOR_RESULT.json`
- `.tasks/receipts/CLIENT-LEGACY-001/EXECUTION_RECEIPT.md`

## legacy 归档前盘点

| 路径 | 是否存在 | 文件数 | 总大小 bytes | git tracked | 归档策略 | 是否允许从活跃 client 目录移除 |
| --- | --- | ---: | ---: | --- | --- | --- |
| `mc-design-nx/client/data/asset_views/runtime-live` | true | 133 | 252506 | false | archive_copy_to_tasks_then_remove_active | true |
| `mc-design-nx/client/data/asset_views/test-local-dev` | true | 80 | 155741 | false | archive_copy_to_tasks_then_remove_active | true |
| `mc-design-nx/client/data/workspace/.beya` | true | 35 | 261712 | false | archive_copy_to_tasks_then_remove_active | true |
| `mc-design-nx/client/cc_haha_agent_runtime_migration_pack` | true | 1 | 1078 | false | move_to_references_legacy_runtime | true |
| `mc-design-nx/client/data/governance` | true | 0 | 0 | false | archive_copy_to_tasks_then_remove_active | true |

判定：所有候选体量均小于 100 MB，文件名级敏感标记扫描未触发需人工确认；`governance` 是空目录。未读取或输出文件内容中的凭据值。

## 归档/移动清单

| 原活跃路径 | 动作 | 目标路径 | 文件数 | bytes | 活跃路径已移除 | 证据保留 |
| --- | --- | --- | ---: | ---: | --- | --- |
| `mc-design-nx/client/data/asset_views/runtime-live` | archived_then_removed | `.tasks/archives/CLIENT-LEGACY-001/mc-design-nx/client/data/asset_views/runtime-live` | 133 | 252506 | true | true |
| `mc-design-nx/client/data/asset_views/test-local-dev` | archived_then_removed | `.tasks/archives/CLIENT-LEGACY-001/mc-design-nx/client/data/asset_views/test-local-dev` | 80 | 155741 | true | true |
| `mc-design-nx/client/data/workspace/.beya` | archived_then_removed | `.tasks/archives/CLIENT-LEGACY-001/mc-design-nx/client/data/workspace/.beya` | 35 | 261712 | true | true |
| `mc-design-nx/client/data/governance` | archived_then_removed | `.tasks/archives/CLIENT-LEGACY-001/mc-design-nx/client/data/governance` | 0 | 0 | true | true |
| `mc-design-nx/client/cc_haha_agent_runtime_migration_pack` | moved_to_references_legacy_runtime | `references/legacy-runtime/cc-haha/cc_haha_agent_runtime_migration_pack` | 1 | 1078 | true | true |

## 未移动项目及原因

无。所有 CLIENT-LEGACY-001 范围内候选均已归档或迁移；未发现过大目录或疑似用户数据目录需要人工确认。

不在本任务范围内且未处理：`package/windows/output`、客户端安装包卸载失败、data root/managed skills 分离、beya -> tjuae 运行时替换、外部 tjuae 项目。

## 当前资产链路 doctor 结果

执行命令：

```powershell
$env:PYTHONPATH = 'E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\client\src'
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m mc_design_client.cli --root mc-design-nx\client doctor
```

结果摘要：

```text
checks.asset_chain.ok=true
checks.asset_chain.projection.asset_view_root=E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\client\data\asset_views\runtime-agentloop
checks.asset_chain.workspace_skills.exists=true
checks.asset_chain.consistency.all_skills_match=true
checks.asset_chain.consistency.package_projection_skills_match=true
checks.asset_chain.consistency.projection_workspace_managed_skills_match=true
legacy_candidates actions=runtime-live:absent; test-local-dev:absent; .beya:absent; cc_haha_agent_runtime_migration_pack:absent; governance:absent
```

完整证据：`.tasks/receipts/CLIENT-LEGACY-001/DOCTOR_RESULT.json`。

说明：doctor 同时会报告 local API / NX plugin 连接状态；本任务明确禁止启动客户端和 NX，因此仅以 `checks.asset_chain` 作为本任务验证项。

## 新增/更新测试清单

- `test_asset_store.py::test_asset_chain_diagnostics_reports_consistency_and_legacy_without_deleting`：存在的 legacy 候选保持 `report_only`，缺失的 `governance` 为 `absent`，且不删除 sentinel。
- `test_asset_store.py::test_asset_chain_diagnostics_keeps_ok_when_legacy_candidates_are_absent`：所有 legacy 候选缺失时 `inspect_asset_chain(...)["ok"]` 仍为 true，候选 action 为 `absent`。
- `test_agent_loop_assets.py::test_registry_runtime_projection_is_the_only_runtime_asset_view`：当前运行只认 `runtime-agentloop`，`cc_haha` 不在活跃 client 目录，资产链路 source/package/projection/workspace managed skills 一致。

## 测试命令和结果

执行命令：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx\client\tests\test_asset_store.py mc-design-nx\client\tests\test_agent_loop_assets.py mc-design-nx\client\tests\test_tjuae_runtime_adapter.py -q
```

结果：

```text
30 passed in 1.26s
```

## 证据文件

- `.tasks/receipts/CLIENT-LEGACY-001/LEGACY_MANIFEST_BEFORE.json`
- `.tasks/receipts/CLIENT-LEGACY-001/LEGACY_MANIFEST_AFTER.json`
- `.tasks/receipts/CLIENT-LEGACY-001/DOCTOR_RESULT.json`
- `.tasks/archives/CLIENT-LEGACY-001/`
- `references/legacy-runtime/cc-haha/README.md`

## 失败分类

无执行失败。未触发 `CLIENT_NOT_RUNNING`、`CLIENT_INSTALL_FAILED`、`CLIENT_UNINSTALL_FAILED`、`K8S_NETWORK_BLOCKED`、`NX_PLUGIN_NOT_CONNECTED` 等失败分类；本任务未启动相关服务。

## 人工前置条件

无。没有需要人工确认后才能移动的本任务候选。

## 风险与后续建议

- 当前工作区在本任务开始前已有大量未提交/未跟踪改动，本次未回滚、未覆盖这些无关改动。
- `.tasks/archives/CLIENT-LEGACY-001/` 和 `references/legacy-runtime/cc-haha/` 当前作为归档证据保留；后续如需压缩、长期存放或清理，应另开归档保留策略任务。
- `package/windows/output` 仍未处理，保留策略应由 `CLIENT-PKG-OUTPUT-001` 或同类任务单独执行。
- data root 与 managed skills 分离仍属于 CLIENT-DATA-001 / CLIENT-TJUAE-001 边界，未在本任务处理。

## 敏感信息

本次未输出 Teamcenter 密码、`tc_key`、API key、cookie、token 或任何明文凭据。manifest 仅包含路径、文件数、大小、hash 和结构性状态。
