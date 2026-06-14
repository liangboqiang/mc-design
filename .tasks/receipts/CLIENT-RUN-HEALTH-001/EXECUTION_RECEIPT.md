# CLIENT-RUN-HEALTH-001 执行回执

执行时间：2026-06-14

## 目标

修复并验证本地安装态客户端启动健康问题，确保测试前运行 `McDesignClient.exe` 时能自动拉起 Python 客户端，并能访问本地健康接口与会话日志接口。

## 根因

本机安装态只看到 `McDesignClient.exe` 进程，没有 `python.exe` 客户端进程，`127.0.0.1:8765/health` 不通。

排查结论：

- `McDesignClient.exe` 普通启动只打开控制面板，不自动启动 Python runtime。
- 只有 `--start-minimized` 或用户点击“启动客户端”才会启动 runtime。
- 本地安装配置缺少 TC key，launcher 启动校验会阻断 runtime。

这与“测试前必须检查客户端是否运行，未运行则启动”的规则冲突。

## 已完成修改

改动文件：

- `mc-design-nx/client-launcher/McDesign.ClientLauncher/MainForm.cs`
- `mc-design-nx/client/tests/test_windows_installer_build.py`

修改内容：

- `McDesignClient.exe` 普通打开后自动尝试启动 Python runtime。
- 如果 runtime 已运行，不重复启动。
- 如果配置不完整，仍在 UI 中提示配置错误，保留“启动客户端”按钮用于手动重试。
- 增加静态测试约束，防止 launcher 回退为只开 UI 不启动 runtime。

## 构建与安装验证

Launcher 构建：

```powershell
mc-design-nx\client-launcher\build-launcher.bat Release
```

结果：

```text
Client launcher built successfully.
```

安装包构建：

```powershell
(echo F:\Documents\tjuae\dist\tjuae-sdk) | package\windows\build-installer.bat --skip-msbuild
```

结果：

```text
Build succeeded.
Installer: package/windows/output/installers/McDesignClientSetup-dev-75f8142.zip
archive_self_check.ok=true
```

安装：

```powershell
install.bat C:\Users\ASUS\AppData\Local\McDesign D:\Siemens\NX 11.0
```

结果：

```text
Install succeeded.
```

## 本机配置

本机安装配置已更新为：

- `user_id=88000044`
- `user_name=宋明芮`
- `tc_key_configured=true`

未在回执或日志中记录 TC key 明文。

## 运行验证

启动：

```powershell
C:\Users\ASUS\AppData\Local\McDesign\McDesignClient.exe
```

结果：

```text
/health ready after 14 seconds
ok=true
bundle_version=dev-75f8142
tc_key_configured=true
conversation_logs.dir=C:\Users\ASUS\AppData\Local\McDesign\client\logs\conversations
```

## agent-turn 与日志验证

测试会话：

```text
conversation_id=client-run-health-001-20260614-160822
```

结果：

```text
POST /api/runtime/test/agent-turn ok=true status=success
GET /api/runtime/conversation-log?conversation_id=client-run-health-001-20260614-160822 ok=true
summary_exists=true
last_status=success
bundle_version=dev-75f8142
tjuae_sdk.effective_version=0.1.0
```

## 测试命令

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest mc-design-nx/client/tests/test_windows_installer_build.py -q
```

结果：

```text
26 passed
```

相关打包测试在上一轮 `PACK-USABILITY-001` 中已验证：

```text
33 passed
```

## 新发现问题

记录为后续加固项：`TJUAE-SERVER-PORT-ISOLATION-001`

现象：

- 本机 `127.0.0.1:3456` 被 `F:\Documents\tjuae` 的开发 server 占用。
- 安装态 `/health` 显示：
  - `tjuae_server.healthy=true`
  - `tjuae_server.managed=false`
  - `tjuae_server.base_url=http://127.0.0.1:3456`
- 这说明本机测试当前连接的是外部 unmanaged tjuae server，而不是安装包内置 `client\tjuae-server\server\win-x64\tjuae-server.exe`。

影响：

- 不影响本次 launcher 自动启动与会话日志验证。
- 但会影响“客户安装包是否能独立启动内置 tjuae-server”的验收准确性。

建议后续修复：

- 客户端启动时应优先使用安装包内置 managed server。
- 如果默认端口被非托管 server 占用，应选择下一个可用端口启动内置 server，或在 `/health` 中明确标记 `EXTERNAL_TJUAE_SERVER_IN_USE`。

