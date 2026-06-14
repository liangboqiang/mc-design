# E2E-SMOKE-002 Execution Receipt

## 结论

不通过：客户端卸载链路失败。

按任务规则，`uninstall.bat` 卸载失败后停止本 smoke，未继续执行安装、启动、`/health`、`/api/status`、K8s connector smoke、`/api/runtime/test/agent-turn`。

## 基线

- 执行时间：2026-06-14T11:24:38+08:00 起；回执生成时间：2026-06-14T11:52:21.2287115+08:00
- 机器名：BRYAN-ROG
- 工作目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design`
- git commit：`41841e94bbaad4b9fd4d1f0a927f82f9d63085b4`
- git status 摘要：非干净工作区；`git status --short` 共 926 行，分组：` D=668,  M=25, ??=8, D =221, M =3, MM=1`
- 初始安装目录：`C:\Users\ASUS\AppData\Local\McDesign` 存在
- `UGII_BASE_DIR`：`D:\Siemens\NX 11.0`

## 初始进程与关闭

初始检测到客户端进程：

```text
ProcessId: 53344
Name: python.exe
CommandLine: "C:\Users\ASUS\AppData\Local\McDesign\client\python\python.exe" "C:\Users\ASUS\AppData\Local\McDesign\client\app\mc_design_client.pyz" --root "C:\Users\ASUS\AppData\Local\McDesign\client" start
```

已按要求调用：

```text
POST http://127.0.0.1:8765/api/runtime/shutdown
status: 200
body: {"ok": true}
```

关闭后确认无以下残留进程：`McDesignClient.exe`、运行 `mc_design_client` 的 `python.exe/pythonw.exe`、`tjuae-server.exe`。

## 安装包解压

- 安装包：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-001.zip`
- 解压目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-002\installer\`
- 实际包根：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-002\installer\McDesignClientSetup-PKG-001\`
- 说明：zip 解压后包含顶层目录 `McDesignClientSetup-PKG-001`，因此关键文件位于该实际包根下。

关键文件检查：

| 文件 | 结果 |
|---|---|
| `install.bat` | 存在 |
| `uninstall.bat` | 存在 |
| `smoke-test.bat` | 存在 |
| `installer\tools\install_helper.mcpy` | 存在 |
| `payload\McDesignClient.exe` | 存在 |
| `payload\client\app\mc_design_client.pyz` | 存在 |
| `payload\client\python\python.exe` | 存在 |

## 卸载旧客户端

执行命令：

```text
set MC_DESIGN_UNINSTALL_NO_PAUSE=1
uninstall.bat C:\Users\ASUS\AppData\Local\McDesign
```

执行目录：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-002\installer\McDesignClientSetup-PKG-001
```

结果：

- 退出码：9
- 卸载日志：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-002\uninstall-output.log`
- 安装目录卸载后仍存在：`C:\Users\ASUS\AppData\Local\McDesign`
- 剩余顶层项：`client/`、`configure/`、`uninstall.bat`
- 卸载后无客户端相关残留进程。

helper 选择策略输出记录：

| 策略 | 结果 |
|---|---|
| `new-layout-helper` | 未观察到 |
| `legacy-root-helper` | 未观察到 |
| `package-helper-fallback` | 已观察到：`[mc-design] Uninstall path: package-helper-fallback` |
| `unsafe-manual-cleanup-refused` | 未作为 `Uninstall path` 输出；helper 后续输出了拒绝清理信息 |

卸载输出关键尾部：

```text
[mc-design] Uninstall dir: C:\Users\ASUS\AppData\Local\McDesign
[mc-design] Package source: E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-002\installer\McDesignClientSetup-PKG-001
[mc-design] Uninstall path: package-helper-fallback
[mc-design] Install directory state: foreign-dir
[mc-design] Refusing unsafe manual cleanup for a non-mc-design directory: C:\Users\ASUS\AppData\Local\McDesign
[mc-design] Uninstall helper failed.
[mc-design] Uninstall failed. Exit code: 9.
```

阻断判断：卸载链路未能完成，且安装目录仍保留非允许清理后的完整客户端结构。按规则停止本任务，结论为“不通过：客户端卸载链路失败”。

## 未执行项

以下步骤因卸载失败按规则停止，未执行：

- 安装 PKG-001 客户端
- 安装后关键文件检查
- `configure\mc-design-client.config` 用户配置检查
- 启动客户端
- `GET http://127.0.0.1:8765/health`
- `GET http://127.0.0.1:8765/api/status`
- K8s connector smoke
- 本地 `POST http://127.0.0.1:8765/api/runtime/test/agent-turn`

未读取、未输出 Teamcenter `tc_key` 明文；未调用 NX 修改类工具、TC 写入工具、文件写入工具。
