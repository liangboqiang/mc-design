# PKG-001 EXECUTION RECEIPT

## 1. 结论

通过。

本任务已加固 Windows 客户端安装包的安装、卸载、升级前清理、NX `custom_dirs.dat` 清理、进程处理和构建后 zip 自检。未执行 E2E 通路测试，符合本任务限制。

## 2. 失败根因复盘

E2E-SMOKE-001 失败原因是旧安装目录 `C:\Users\ASUS\AppData\Local\McDesign` 处于历史/残缺布局：存在 `client\python\python.exe`、根目录 `install_helper.py`、`uninstall.bat`、`install-state.json`，但不存在新布局 `installer\tools\install_helper.mcpy`，也缺少 `McDesignClient.exe` 和 `client\app\mc_design_client.pyz`。

旧 `uninstall.bat` 只按新布局查找 `installer\tools\install_helper.mcpy`，因此在卸载阶段直接失败，没有进入新安装、客户端启动、K8s smoke 或本地 agent-turn smoke。

本任务修复方式：新 `uninstall.bat` 增加 helper 选择优先级，先用新布局 helper，再用旧根目录 helper，最后可用当前安装包自带 Python 和 helper 对目标安装目录执行清理；如果三者都不可用，则输出 `unsafe-manual-cleanup-refused` 并拒绝不安全手工删除。

## 3. 改动文件清单

- `mc-design-nx/package/windows/build/scripts/build_installer.py`
- `mc-design-nx/package/windows/README.md`
- `mc-design-nx/client/tests/test_windows_installer_build.py`
- `.tasks/receipts/PKG-001/EXECUTION_RECEIPT.md`

## 4. 安装目录识别策略

- `empty`：目录不存在、为空，或只剩被保护的 `configure\mc-design-client.config`、`client\data\`、`client\logs\`。
- `current-layout`：存在 `installer\tools\install_helper.mcpy`。
- `legacy-layout`：存在旧根目录 `install_helper.py`。
- `broken-layout`：存在明确 mc-design 标记，但缺少当前/旧 helper，例如 `install-state.json`、`package-manifest.json`、`client\python\python.exe`、`client\resources\*.mcdpkg`、`nx-plugin\startup\NXServer.dll` 等。
- `foreign-dir`：非空且没有明确 mc-design 标记；preinstall/uninstall 均拒绝覆盖或清理。

## 5. 卸载 helper 选择策略

- `new-layout-helper`：使用目标安装目录的 `client\python\python.exe` 和 `installer\tools\install_helper.mcpy`。
- `legacy-root-helper`：使用目标安装目录的 `client\python\python.exe` 和旧根目录 `install_helper.py`。
- `package-helper-fallback`：使用当前解压安装包的 `payload\client\python\python.exe` 和 `installer\tools\install_helper.mcpy` 清理目标目录。
- `unsafe-manual-cleanup-refused`：上述路径都不可用时拒绝删除，避免误删 foreign 或无法判定归属的目录。

## 6. 保留/清理策略

保留：

- `configure\mc-design-client.config`
- `client\data\`
- `client\logs\`

清理：

- `client\app`
- `client\resources`
- `client\python`
- `client\tjuae-server`
- `nx-plugin`
- `installer`
- `McDesignClient.exe`
- `start-client.bat`
- `smoke-test.bat`
- `README_INSTALL.txt`
- `package-manifest.json`
- 旧根目录脚本 `install_helper.py`、`smoke_test.py`
- 旧布局残留 `code`、`runtime`、`startup`、`tools`、`sdk`、`application`、`plugin`
- 旧 `MCPClient.*`、`NXWebSocketClient.*` 文件

路径逃逸防护：所有相对清理路径都通过 `safe_child(root, rel)` 解析，目标必须等于 install dir 或位于 install dir 下；`..\outside` 这类路径会抛出 `Refusing path outside install dir`。

## 7. NX custom_dirs.dat 清理策略

卸载和升级前都会清理旧 mc-design block：

- 优先读取 `install-state.json` 中的 `nx_custom_dir.custom_dir_file`、`ugii_dir`、`nx_base_dir`。
- state 缺失或不完整时，继续检查 `UGII_BASE_DIR`、`UGII_ROOT_DIR`。
- 最后只检查保守的 NX11 默认位置，例如 `C:\Siemens\NX11`、`C:\Program Files\Siemens\NX11`、`C:\Program Files (x86)\Siemens\NX11`。
- 只在文件中存在 `# MC Design Client BEGIN` / `# MC Design Client END` marker 时写回；不会创建或删除陌生文件。
- 无法定位时仅输出 warning。

## 8. 进程处理策略

- 安装/卸载前调用 `stop_running_processes(root, include_nx=True, force=True)`。
- `McDesignClient.exe` 和 `tjuae-server.exe` 必须能关联到当前 install dir 才会停止。
- `python.exe` / `pythonw.exe` 必须同时关联当前 install dir 且命令行包含 `mc_design_client` / `mc-design-client` / `mcdesignclient` 才会停止。
- 仅从 PID 文件无法验证归属时不强杀，只输出 warning。
- NX `ugraf.exe` 仍沿用原策略：交互模式询问，force 模式停止。

## 9. 新增/更新测试清单

- 构建 zip 后 `archive_self_check` 必须通过。
- zip 内必须包含 `installer/tools/install_helper.mcpy` 和任务要求的关键 payload 文件。
- `uninstall.bat` 必须包含 `new-layout-helper`、`legacy-root-helper`、`package-helper-fallback`、`unsafe-manual-cleanup-refused`。
- 新布局 uninstall 清理 managed 文件并保留配置/data/logs。
- 旧布局只有根目录 `install_helper.py` 时 uninstall 可清理旧根目录脚本。
- broken-layout 缺 `McDesignClient.exe` / `mc_design_client.pyz` 时 preinstall 可安全清理。
- foreign-dir 被拒绝覆盖。
- `configure\mc-design-client.config`、`client\data`、`client\logs` 被保留。
- 旧根目录 `install_helper.py`、`smoke_test.py` 被清理。
- preinstall 幂等，二次运行只剩保留路径时识别为 `empty`。
- 路径逃逸被拒绝。
- 无 state 时可按 `UGII_BASE_DIR` 清理 NX `custom_dirs.dat` 旧 block。
- 进程处理不会误杀无关 python 进程。
- stale PID 文件不再直接强杀不可验证进程。

## 10. 测试命令和结果

命令：

```powershell
cd /d E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client\tests\test_windows_installer_build.py -q
```

结果：

```text
21 passed in 9.56s
```

附加语法检查：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m py_compile package\windows\build\scripts\build_installer.py
```

结果：通过。

## 11. 构建命令和结果

命令：

```powershell
cd /d E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx
set MC_DESIGN_NO_PAUSE=1
package\windows\build-installer.bat --bundle-version PKG-001 --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk
```

结果：

```text
[mc-design] Build succeeded.
[mc-design] Installer: "E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-001.zip"
```

未使用 `--skip-msbuild`。构建日志显示 `launcher_build.status=built`，`python_runtime_prepare.ok=true`，`archive_self_check.ok=true`。

## 12. 安装包路径和关键文件自检结果

安装包：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-001.zip
```

关键文件自检：通过。

```text
OK install.bat
OK uninstall.bat
OK smoke-test.bat
OK installer/tools/install_helper.mcpy
OK payload/McDesignClient.exe
OK payload/start-client.bat
OK payload/client/app/mc_design_client.pyz
OK payload/client/python/python.exe
OK payload/client/resources/agent_assets.mcdpkg
OK payload/client/resources/nx_tools_manifest.json
OK payload/client/resources/mc-design-package.mcdpkg
OK payload/configure/mc-design-client.config
OK payload/nx-plugin/startup/NXServer.dll
OK payload/nx-plugin/tools/NXTools.dll
OK payload/nx-plugin/sdk/NXSDK.dll
OK package-manifest.json
```

## 13. 未完成/阻塞项

- 未执行 E2E 通路测试，符合任务限制。
- 未手动删除 `C:\Users\ASUS\AppData\Local\McDesign` 等真实用户安装目录，符合任务限制。
- 未修改运行时 adapter、K8s、NX 参数工具、DFMEA、报告 skill。

## 14. 后续建议

可以使用新生成的 `McDesignClientSetup-PKG-001.zip` 进入 E2E-SMOKE-002 或等价的卸载/重装 smoke。建议先覆盖 E2E-SMOKE-001 的失败现场：旧目录仅有 `client\python\python.exe`、根目录 `install_helper.py`、`uninstall.bat`、`install-state.json`，确认卸载输出 `legacy-root-helper` 或在从新包发起时输出 `package-helper-fallback`。

如果 E2E-SMOKE-002 仍不能运行，原因应来自本任务范围外的真实环境前置条件，例如 NX 未启动、K8s 部署未更新、VPN/内网未连接、目标模型未在 NX 中打开等。
