# PACK-USABILITY-001 执行回执

执行时间：2026-06-14

## 问题

打包入口虽然已能提示缺少 `tjuae-server.exe`，但对测试人员仍然不友好：

- 需要手工拼 `--tjuae-sdk-dist` 或 `--tjuae-server-package` 参数。
- 错误文案会让人误以为需要提供 SDK。
- 默认 `--bundle-version` 仍可能是人工输入版本，不便于和代码仓提交对应。

## 调整原则

- 普通人员只运行 `mc-design-nx\package\windows\build-installer.bat`。
- Tjuae Python SDK 固定使用 `mc-design-nx` 仓库内置 wheel。
- 如果仓库内没有 `tjuae-server.exe`，就在 cmd 窗口中提示输入 server 包或 dist 目录。
- 未传 `--bundle-version` 时，版本号默认使用当前 `mc-design-nx` Git 分支 + 短提交。

## 已完成修改

改动文件：

- `mc-design-nx/package/windows/build-installer.bat`
- `mc-design-nx/package/windows/build/scripts/build_installer.py`
- `mc-design-nx/package/windows/build/scripts/payload_builder.py`
- `mc-design-nx/package/windows/README.md`
- `mc-design-nx/client/tests/test_windows_payload_builder.py`
- `mc-design-nx/client/tests/test_windows_installer_build.py`

关键结果：

- `build-installer.bat` 缺少 server 包时会直接提示：

```text
Tjuae server package/dist dir:
```

- 用户输入示例：

```text
F:\Documents\tjuae\dist\tjuae-sdk
```

- 打包日志确认 SDK 来源为仓库内置 wheel：

```text
client/vendor/tjuae-sdk-python/wheelhouse/tjuae_sdk-0.1.0-py3-none-any.whl
```

- `--tjuae-sdk-dist` 保留为兼容参数，但不再覆盖内置 SDK，只作为 server 来源。
- 错误文案不再要求普通用户提供 SDK。
- 默认版本号示例：`dev-596a4a2`。

## 验证

测试命令：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest client/tests/test_windows_payload_builder.py client/tests/test_windows_installer_build.py -q
```

结果：

```text
33 passed
```

交互 dry-run：

```powershell
(echo F:\Documents\tjuae\dist\tjuae-sdk) | package\windows\build-installer.bat --dry-run
```

结果：

```text
Bundle version: dev-596a4a2
Dry run succeeded.
sdk_python_source = client/vendor/tjuae-sdk-python/wheelhouse/tjuae_sdk-0.1.0-py3-none-any.whl
server_executable = F:\Documents\tjuae\dist\tjuae-sdk\server\win-x64\tjuae-server.exe
```

真实打包：

```powershell
(echo F:\Documents\tjuae\dist\tjuae-sdk) | package\windows\build-installer.bat --skip-msbuild
```

结果：

```text
Build succeeded.
Installer: package/windows/output/installers/McDesignClientSetup-dev-596a4a2.zip
archive_self_check.ok=true
```

## 给测试人员的新用法

普通方式：

```powershell
mc-design-nx\package\windows\build-installer.bat
```

如果提示输入 Tjuae server 包目录，填：

```text
F:\Documents\tjuae\dist\tjuae-sdk
```

不需要提供 SDK 路径。

