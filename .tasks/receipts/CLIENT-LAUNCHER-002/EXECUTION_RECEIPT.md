# CLIENT-LAUNCHER-002 Execution Receipt

更新时间：2026-06-14 14:35 Asia/Shanghai

## 任务边界

- 已读取并遵守 `.tasks/TEST_EXECUTION_RULES.md`。
- 本次只处理客户端交付链路：`mc-design-nx/client-launcher/`、`mc-design-nx/package/windows/`、`mc-design-nx/client/src/mc_design_client/config` 及启动相关客户端代码、installer/launcher tests。
- 未处理 QPP 连通性；QPP 不通不作为本任务失败。
- 未修改 runtime adapter、NX plugin、参数规则。

## 变更摘要

- `McDesignClient.exe` 启动器增加启动前配置校验：
  - `user_id=88000044`
  - `user_name=宋明芮`
  - `tc_key_configured=true`
  - 缺失 TC key 时返回 `TC_KEY_NOT_CONFIGURED`，不输出明文 key。
- 正式启动链路增加：
  - `launcher-start.log`
  - Python stdout/stderr 重定向
  - `/api/status` 端口等待
  - 子进程提前退出、超时和友好失败原因输出。
- Python 客户端增加安全配置摘要：
  - `/health`、`/api/status` 输出 `tc_key_configured` 布尔值。
  - CLI `start` 在 TC key 缺失时输出结构化 `code=TC_KEY_NOT_CONFIGURED`。
- 安装/卸载脚本加固：
  - 卸载时保留运行中的根 `uninstall.bat`，避免 `The batch file cannot be found`。
  - 卸载成功后保留本机 `configure/mc-design-client.config`、`client/data`、`client/logs`，便于重装复用本机配置。
  - 正常安装/卸载只停止 MC Design 客户端相关进程，不直接结束正在运行的 NX。
- 安装包 smoke 增加 `--start-client`：
  - 构建/卸载/安装/启动前置配置检查。
  - 等待 `/health` 和 `/api/status`。
  - TC key 缺失时停止启动和 TC/NX 相关 smoke，返回 `TC_KEY_NOT_CONFIGURED`。

## 构建产物

- Launcher exe:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\client-launcher\dist\McDesignClient.exe`
- Installer zip:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-CLIENT-LAUNCHER-002.zip`
  - size: `93484504`
  - bundle_version: `CLIENT-LAUNCHER-002`
  - `--skip-msbuild=true`
  - `release_eligible=true`
  - `python_runtime_bundled=true`

## 安装包级 Smoke

测试目录：

- Package extract:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\CLIENT-LAUNCHER-002\package-extract\McDesignClientSetup-CLIENT-LAUNCHER-002`
- Isolated install dir:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\CLIENT-LAUNCHER-002\smoke-install\McDesign`
- Fake NX dir for installer registration only:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\CLIENT-LAUNCHER-002\fake-nx\NX11`

卸载结果：

- Command:
  - `uninstall.bat "<isolated install dir>"`
- Result:
  - `exit_code=0`
  - path: `package-helper-fallback`
  - install directory state: `empty`
  - preserved user config/data/logs: `true`
- Log:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\CLIENT-LAUNCHER-002\uninstall-smoke.log`

安装结果：

- Command:
  - `install.bat "<isolated install dir>" "<fake NX dir>"`
- Result:
  - `exit_code=0`
  - `McDesignClient.exe` installed: `true`
  - `install-state.json` written: `true`
  - user config preserved: `true`
- Log:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\CLIENT-LAUNCHER-002\install-smoke.log`

启动方式：

- Installed smoke command:
  - `smoke-test.bat --start-client --release`
- Result:
  - `exit_code=1`
  - `failures=["TC_KEY_NOT_CONFIGURED"]`
  - `started={}`
  - `/health={}`
  - `/api/status={}`
  - TC/NX smoke skipped because `TC_KEY_NOT_CONFIGURED`
- Log:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\CLIENT-LAUNCHER-002\startup-smoke.log`

Python start config-check:

- Command:
  - `client\python\python.exe client\app\mc_design_client.pyz --root client start`
- Result:
  - `exit_code=2`
  - `code=TC_KEY_NOT_CONFIGURED`
- Log:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\CLIENT-LAUNCHER-002\pyz-start-config-check.log`

Package static smoke:

- Command:
  - `smoke-test.bat --release`
- Result:
  - `exit_code=0`
  - `ok=true`
  - `failures=[]`
- Log:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\CLIENT-LAUNCHER-002\package-static-smoke.log`

## 进程和端口

- 本次 `--start-client` smoke 未启动新 launcher/python 进程，因为启动前配置检查返回 `TC_KEY_NOT_CONFIGURED`。
- 当前 `127.0.0.1:8765` 已有既有监听进程：
  - `pid=54676`
  - `process=python`
  - `path=C:\Users\ASUS\AppData\Local\McDesign\client\python\python.exe`
- 该既有进程的 `/health` 和 `/api/status` 返回 `ok=true`，但不是本次隔离安装包启动结果，不作为本任务启动通过依据。

## 配置检查结果

默认本机配置：

- Config path:
  - `C:\Users\ASUS\AppData\Local\McDesign\configure\mc-design-client.config`
- `exists=true`
- `user_id=88000044`
- `user_name=宋明芮`
- `tc_key_configured=false`

隔离安装配置：

- Config path:
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\CLIENT-LAUNCHER-002\smoke-install\McDesign\configure\mc-design-client.config`
- `exists=true`
- `user_id=88000044`
- `user_name=宋明芮`
- `tc_key_configured=false`

结论：

- 当前机器未发现可复用的非空 TC key 本机配置。
- 按公共规则，TC/NX 相关启动 smoke 已在 `TC_KEY_NOT_CONFIGURED` 停止，未继续伪通过。

## 测试命令和结果

- `C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest mc-design-nx\client\tests\test_client_static.py mc-design-nx\client\tests\test_windows_installer_build.py -q`
  - Result: `66 passed in 10.61s`
- `cmd /c mc-design-nx\client-launcher\build-launcher.bat Release`
  - Result: `exit_code=0`
- `cmd /c mc-design-nx\package\windows\build-installer.bat --bundle-version CLIENT-LAUNCHER-002 --skip-msbuild --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk`
  - Result: `exit_code=0`
- `uninstall.bat "<isolated install dir>"`
  - Result: `exit_code=0`
- `install.bat "<isolated install dir>" "<fake NX dir>"`
  - Result: `exit_code=0`
- `smoke-test.bat --release`
  - Result: `exit_code=0`
- `smoke-test.bat --start-client --release`
  - Result: `exit_code=1`, expected stop: `TC_KEY_NOT_CONFIGURED`
- `client\python\python.exe client\app\mc_design_client.pyz --root client start`
  - Result: `exit_code=2`, expected stop: `TC_KEY_NOT_CONFIGURED`

## 失败分类

- `TEST_PRECONDITION_NOT_MET`
- Specific code: `TC_KEY_NOT_CONFIGURED`

## 敏感信息声明

- 未在代码、日志摘要、回执中输出 Teamcenter 密码明文。
- 本回执只记录 `tc_key_configured=true/false`。
- 已扫描本次 `.log` 证据文件，未发现非空 Teamcenter key 配置值。
  形式的明文配置输出。
