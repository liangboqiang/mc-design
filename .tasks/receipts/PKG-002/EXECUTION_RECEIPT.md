# PKG-002 EXECUTION RECEIPT

## 1. 结论

通过。

本任务已继续加固 Windows 客户端安装/卸载链路中的安装目录识别、fallback 卸载、拒绝日志和退出码诊断，并已构建新的安装包：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-002.zip
```

未执行真实用户目录的全通路 smoke；已完成安装包构建自检和包内 `package-helper-fallback` 临时目录自检。

## 2. 任务边界

本轮仅处理 Windows 客户端安装/卸载链路加固。

未处理、未修改：

- CLIENT-ASSET-001 资产链路问题
- `cc_haha`、旧 `asset_views`、旧 `.beya` 或 package output 的清理
- `beya -> tjuae` 替换任务
- K8s、AI Service、NX plugin、业务 skill
- Teamcenter 密码或任何明文凭据

未跳过卸载失败继续测试 K8s 或业务链路。

## 3. 输入依据

- `.tasks\TEST_EXECUTION_RULES.md`
- `.tasks\receipts\E2E-SMOKE-002\EXECUTION_RECEIPT.md`
- `.tasks\receipts\E2E-SMOKE-002\uninstall-output.log`
- `.tasks\receipts\PKG-001\EXECUTION_RECEIPT.md`
- `mc-design-nx\package\windows\build\scripts\build_installer.py`
- `mc-design-nx\client\tests\test_windows_installer_build.py`

## 4. E2E-SMOKE-002 失败根因

E2E-SMOKE-002 中的真实安装目录只剩以下顶层项：

```text
C:\Users\ASUS\AppData\Local\McDesign
  client/
  configure/
  uninstall.bat
```

其中 `client/` 下只剩 `data/`、`logs/`，`configure/` 下保留 `mc-design-client.config`。PKG-001 的识别逻辑把 `configure\mc-design-client.config`、`client\data`、`client\logs` 视为受保护用户数据；剩余唯一未保护项是 `uninstall.bat`。旧逻辑没有把带有 `[mc-design]`、`MC_DESIGN_UNINSTALL_CHILD`、`install_helper.mcpy` 等文本标记的旧卸载脚本纳入 McDesign 证据，因此 `package-helper-fallback` 进入 helper 后将目录判为 `foreign-dir`，输出：

```text
Install directory state: foreign-dir
Refusing unsafe manual cleanup for a non-mc-design directory
```

结果是卸载退出码 9，目录仍存在，E2E 按规则停止。

## 5. 新安装目录分类规则

分类入口统一为 `analyze_install_dir(root)`，`preinstall` 和 `uninstall` 共用同一套判定。

- `empty`：目录不存在、为空，或只剩受保护的 `configure\mc-design-client.config`、`client\data\`、`client\logs\`。
- `current-layout`：存在 `installer\tools\install_helper.mcpy`。
- `legacy-layout`：存在旧根目录 `install_helper.py`。
- `broken-layout`：存在明确 McDesign 强证据但缺少 current/legacy helper，例如 `install-state.json`、`package-manifest.json`、`client\python\python.exe`、`client\resources\*.mcdpkg`、`nx-plugin\startup\NXServer.dll` 等。
- `package-helper-fallback-layout`：缺少目标目录内 helper/runtime，但同时存在 `client/`、`configure\mc-design-client.config`，且 `uninstall.bat` 文本包含 McDesign 卸载标记。该分类覆盖 E2E-SMOKE-002 的目录形态。
- `foreign-dir`：非空且没有足够 McDesign 证据的目录。

日志新增：

- `Install directory evidence: ...`
- `Install directory refusal reason: ...`
- 已保留 `Install directory state: ...`
- 已保留 `Uninstall path: new-layout-helper|legacy-root-helper|package-helper-fallback|unsafe-manual-cleanup-refused`

## 6. 卸载安全边界

仍拒绝删除无法证明属于 McDesign 的目录：

- 只有 `client/`、`configure/`、`uninstall.bat` 但卸载脚本没有 McDesign 文本标记的 lookalike 目录仍判为 `foreign-dir`。
- `foreign-dir` 在 `preinstall` 中返回 9，不覆盖。
- `foreign-dir` 在 `uninstall` 中返回 9，不清理。
- 拒绝日志会列出原因和前几个未保护项，例如 `no McDesign marker evidence found; non-protected entries: ...`。

保留既有用户数据保护：

- helper 清理阶段默认保留 `configure\mc-design-client.config`、`client\data\`、`client\logs\`。
- 正式 `uninstall.bat` 在 helper 成功后仍按既有完整卸载语义删除安装目录。

另修复一个包内自检暴露的问题：`remove_install_dir` 原兜底逻辑按“命令行包含目标目录”杀进程，可能杀掉正在运行的卸载 `cmd.exe` 自身，导致 helper 已成功但批处理退出码为 `-1`。现已改为只对可验证属于安装目录的客户端进程名执行清理，并初始化 `TARGET_REMOVED=0`。

## 7. 改动文件清单

本轮直接编辑：

- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\build\scripts\build_installer.py`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\client\tests\test_windows_installer_build.py`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\PKG-002\EXECUTION_RECEIPT.md`

本轮生成证据/产物：

- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-002.zip`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\logs\build-installer.last.log`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\PKG-002\package-helper-selfcheck-final.log`

说明：工作区进入任务前已存在大量与本任务无关的修改/删除；本轮未回退、未清理这些既有变更。

## 8. 新增/更新测试清单

已新增或加强覆盖：

- E2E-SMOKE-002 目录形态：`client/`、`configure\mc-design-client.config`、带 McDesign 标记的 `uninstall.bat` 被识别为 `package-helper-fallback-layout`，不再误判为 `foreign-dir`。
- lookalike foreign 目录：`client/`、`configure/`、普通 `uninstall.bat` 仍判为 `foreign-dir` 并拒绝清理。
- `broken-layout` 可通过 uninstall 清理已知残留，并保留配置。
- `configure\mc-design-client.config`、`client\data`、`client\logs` 在 helper 清理阶段保留。
- 当前布局卸载失败时返回 7，并输出目录类型、命中证据和失败原因。
- 批处理 `remove_install_dir` 不再使用宽泛的“任意命令行包含目标路径即杀进程”逻辑。

## 9. 测试命令和结果

指定测试：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest mc-design-nx\client\tests\test_windows_installer_build.py -q
```

结果：

```text
25 passed in 9.95s
```

语法检查：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m py_compile mc-design-nx\package\windows\build\scripts\build_installer.py
```

结果：通过。

## 10. 构建命令和结果

构建命令：

```powershell
cd E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx
$env:MC_DESIGN_NO_PAUSE='1'
cmd /c package\windows\build-installer.bat --bundle-version PKG-002 --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk
```

结果：

```text
[mc-design] Build succeeded.
[mc-design] Installer: "E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-002.zip"
```

未使用 `--skip-msbuild`。构建日志字段：

```text
archive_self_check_ok=True
msbuild_status=built
ui_build_status=built
launcher_build_status=built
python_runtime_prepare_ok=True
release_eligible=True
```

## 11. 安装包自检

zip 关键条目检查：

```text
zip_exists=True
missing=[]
entry_count=290
```

包内 fallback 临时自检：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\PKG-002\package-helper-selfcheck-final.log
```

关键输出：

```text
selfcheck_exit_code=0
Uninstall path: package-helper-fallback
Install directory state: package-helper-fallback-layout
Install directory evidence: text marker: uninstall.bat; package-helper fallback evidence: client/, configure/mc-design-client.config, mc-design uninstall.bat
Uninstall succeeded.
Install directory removed.
```

注意：首次包内自检在修复前触发了 helper 既有的强制 NX 停止逻辑，日志显示停止了当时的 `ugraf.exe pid=46060`；最终自检前确认没有 `ugraf.exe`，最终自检退出码为 0。

## 12. 新安装包路径

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-002.zip
```

## 13. 失败分类和敏感信息

PKG-002 本轮构建和自检通过，无新的代码失败分类。

E2E-SMOKE-002 历史失败分类仍为：

```text
CLIENT_UNINSTALL_FAILED
```

本轮未读取、未输出 Teamcenter `tc_key`、`user_pass`、API key、cookie、token 或任何明文凭据。临时自检配置仅写入无敏感值的 `user_id = "selfcheck"`。

## 14. 仍需 E2E-SMOKE-003 复测事项

建议使用 `McDesignClientSetup-PKG-002.zip` 启动 E2E-SMOKE-003，至少复测：

- 对真实 `C:\Users\ASUS\AppData\Local\McDesign` 现有残留执行卸载，确认不再误判为 `foreign-dir`。
- 确认卸载日志包含 `Uninstall path: package-helper-fallback`、目录类型、命中证据和最终退出码。
- 确认旧目录被完整移除或按安装/卸载既有规则处理。
- 安装 PKG-002 并检查关键文件。
- 启动客户端并检查 `GET http://127.0.0.1:8765/health`、`GET http://127.0.0.1:8765/api/status`。
- 仅在卸载、安装、启动、健康检查闭环后，再继续 K8s connector smoke 或本地 `agent-turn`。
