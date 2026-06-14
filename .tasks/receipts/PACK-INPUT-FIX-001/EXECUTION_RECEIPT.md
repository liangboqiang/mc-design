# PACK-INPUT-FIX-001 执行回执

执行时间：2026-06-14

## 问题

测试人员执行 Windows 客户端打包时失败：

```text
FileNotFoundError: tjuae-server package must contain tjuae-server.exe: ...\mc-design-nx\client\tjuae-server
```

## 根因

Python SDK 已经内置到 `mc-design-nx/client/vendor/tjuae-sdk-python`，但本地 tjuae server 发布包没有纳入仓库默认路径。

打包脚本未显式传入 `--tjuae-server-package` 或 `--tjuae-sdk-dist` 时，会默认查找：

```text
mc-design-nx/client/tjuae-server
```

该路径缺失，因此直接抛出 Python traceback。

## 已完成修复

改动文件：

- `mc-design-nx/package/windows/build/scripts/payload_builder.py`
- `mc-design-nx/package/windows/build/scripts/build_installer.py`
- `mc-design-nx/package/windows/build-installer.bat`
- `mc-design-nx/package/windows/README.md`
- `mc-design-nx/client/tests/test_windows_payload_builder.py`

修复内容：

- 增加 tjuae server 默认查找路径：
  - `client/tjuae-server`
  - `client/vendor/tjuae-server`
  - `client/vendor/tjuae-sdk`
- 缺少 server 包时，不再只给无行动价值的 traceback，错误信息明确提示：
  - `--tjuae-server-package <path>`
  - `--tjuae-sdk-dist <path>`
  - `TJUAE_SERVER_PACKAGE`
  - `TJUAE_SDK_DIST`
- `build-installer.bat --dry-run` 不再打印旧的 installer archive marker。
- 外部 `--tjuae-sdk-dist` 没有 `VENDORED_SDK.json` 时，自动生成最小 `client/resources/tjuae-sdk-vendor.json`，用于后续日志版本追溯。
- installer archive 自检新增关键运行时依赖：
  - `payload/client/resources/tjuae-sdk-vendor.json`
  - `payload/client/tjuae-server/server/win-x64/tjuae-server.exe`

## 验证结果

测试命令：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest mc-design-nx/client/tests/test_windows_payload_builder.py -q
```

结果：

```text
7 passed
```

缺少 server 包时的 dry-run：

```powershell
mc-design-nx\package\windows\build-installer.bat --dry-run
```

结果：

- 失败是预期结果。
- `output/logs/build-installer.last.log` 输出 JSON，明确提示传入 `--tjuae-server-package` 或 `--tjuae-sdk-dist`。
- 不再只暴露原始 Python traceback。

显式使用 tjuae dist 的 dry-run：

```powershell
mc-design-nx\package\windows\build-installer.bat --dry-run --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk
```

结果：

```text
Dry run succeeded.
```

真实打包：

```powershell
mc-design-nx\package\windows\build-installer.bat --bundle-version PACK-INPUT-FIX-003 --skip-msbuild --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk
```

结果：

```text
Build succeeded.
Installer: mc-design-nx\package\windows\output\installers\McDesignClientSetup-PACK-INPUT-FIX-003.zip
archive_self_check.ok=true
```

## 给测试人员的当前可用命令

如果测试机器有 tjuae dist：

```powershell
mc-design-nx\package\windows\build-installer.bat --bundle-version <版本号> --tjuae-sdk-dist <tjuae>\dist\tjuae-sdk
```

如果 Python SDK 使用仓库内置 wheel，只外部提供 server 包：

```powershell
mc-design-nx\package\windows\build-installer.bat --bundle-version <版本号> --tjuae-server-package <tjuae>\dist\tjuae-sdk
```

当前本机可用路径：

```powershell
F:\Documents\tjuae\dist\tjuae-sdk
```

## 未纳入本次提交的事项

`tjuae-server.exe` 约 118MB，不应直接作为普通 Git 对象提交。若要实现所有测试人员无需传参的开箱即用打包，需要单独决定 server 发布包分发策略：

- Git LFS 跟踪 `mc-design-nx/client/vendor/tjuae-server/**`
- 或内部制品库下载/同步
- 或由 tjuae 项目发布固定 dist 包，mc-design 打包时显式引用

## 当前本机运行态提示

前序安装验证过程中，安装脚本为了替换 NX plugin 文件停止过 `ugraf.exe`。当前本机 `127.0.0.1:8765/health` 未连通，只看到 `McDesignClient.exe` 进程，未看到 Python runtime、tjuae-server 或 NX 进程。

这与 PACK-INPUT-FIX-001 的打包问题独立。后续做本机 E2E 前，需要重新启动客户端，并由项目负责人手动重新打开 NX。

