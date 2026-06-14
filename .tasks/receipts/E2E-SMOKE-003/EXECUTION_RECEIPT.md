# E2E-SMOKE-003 Execution Receipt

## 1. 最终结论

不通过：严格按安装包正式启动入口判定，`McDesignClient.exe` 首选启动后没有在超时内让 `127.0.0.1:8765` 进入监听/健康可用状态。

失败分类：

```text
CLIENT_START_FAILED
```

补充说明：为定位失败边界，本轮在记录首选入口失败后，使用安装目录中的诊断入口 `start-client.bat` 成功启动了同一套 Python 客户端运行时，并继续完成 `/health`、`/api/status`、本地 `agent-turn` 和 K8s 基础 smoke。补充结果显示运行时、资产包、本地工具回调、K8s readiness/catalog/mysql 链路均可用，但不能覆盖安装包正式入口 `McDesignClient.exe` 的启动失败判定。

非阻断分类：

```text
TC_KEY_NOT_CONFIGURED
NX_PLUGIN_NOT_CONNECTED
QPP_EXTERNAL_UNAVAILABLE
```

本轮未执行问题表正式回归，未调用 NX 修改类工具、TC 上传类工具、QPP 工具。未输出 Teamcenter 密码明文；回执中只记录 `tc_key_configured=false`。

## 2. 改动文件清单

代码改动：无。

本轮生成/更新的回执与证据文件：

- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\EXECUTION_RECEIPT.md`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\package-check.json`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\pre-shutdown-check.json`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\uninstall-result.json`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\uninstall-output.log`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\install-result.json`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\install-output.log`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\config-check.json`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\client-start-result.json`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\local-health-status.json`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\local-agent-turn-response.json`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\local-agent-turn-response-retry.json`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\k8s-smoke-result.json`

## 3. 输入与解压

安装包：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-PKG-002.zip
```

解压目录：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\installer-20260614-124915
```

实际包根：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\installer-20260614-124915\McDesignClientSetup-PKG-002
```

包内关键文件检查：全部存在。

| 文件 | 结果 |
|---|---|
| `install.bat` | 存在 |
| `uninstall.bat` | 存在 |
| `installer\tools\install_helper.mcpy` | 存在 |
| `payload\McDesignClient.exe` | 存在 |
| `payload\client\app\mc_design_client.pyz` | 存在 |
| `payload\client\python\python.exe` | 存在 |
| `payload\client\resources\agent_assets.mcdpkg` | 存在 |

## 4. 测试前客户端状态

记录文件：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\pre-shutdown-check.json
```

结果：

- 关闭前客户端相关进程：无。
- 关闭前 `8765/8088` 端口监听：无。
- `GET http://127.0.0.1:8765/health`：不可访问，连接被拒绝。
- `POST /api/runtime/shutdown`：未尝试，原因是客户端未运行。
- 关闭后客户端相关进程：无。
- 关闭后 `8765/8088` 端口监听：无。
- `ugraf.exe`：未运行；本轮未自动强杀 NX。

## 5. 卸载旧客户端

执行目录：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\installer-20260614-124915\McDesignClientSetup-PKG-002
```

命令：

```powershell
$env:MC_DESIGN_UNINSTALL_NO_PAUSE='1'
$env:MC_DESIGN_NO_PAUSE='1'
cmd.exe /c "E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\installer-20260614-124915\McDesignClientSetup-PKG-002\uninstall.bat" "C:\Users\ASUS\AppData\Local\McDesign"
```

结果：

- 退出码：`0`
- 完整卸载日志：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\uninstall-output.log`
- 卸载后安装目录存在：`false`
- 卸载后客户端相关残留进程：无。
- 未观察到 `foreign-dir` 误判。
- 已观察到 `package-helper-fallback-layout`、`Install directory evidence`、`Uninstall succeeded`。

关键日志：

```text
[mc-design] Uninstall path: package-helper-fallback
[mc-design] Install directory state: package-helper-fallback-layout
[mc-design] Install directory evidence: text marker: uninstall.bat; package-helper fallback evidence: client/, configure/mc-design-client.config, mc-design uninstall.bat
[mc-design] No running MC Design or NX processes found.
[mc-design] Removed NX registration, managed files, and shortcuts.
[mc-design] Uninstall succeeded.
[mc-design] Install directory removed.
```

## 6. 安装 PKG-002 客户端

执行目录：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\installer-20260614-124915\McDesignClientSetup-PKG-002
```

命令：

```powershell
$env:MC_DESIGN_NO_PAUSE='1'
cmd.exe /c "E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\installer-20260614-124915\McDesignClientSetup-PKG-002\install.bat" "C:\Users\ASUS\AppData\Local\McDesign" "D:\Siemens\NX 11.0"
```

结果：

- 退出码：`0`
- 完整安装日志：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\install-output.log`
- 安装日志显示 `Install directory state: empty`、`Install completed`、`Install succeeded`。

安装后关键文件检查：全部存在。

| 文件 | 结果 |
|---|---|
| `McDesignClient.exe` | 存在 |
| `start-client.bat` | 存在 |
| `client\app\mc_design_client.pyz` | 存在 |
| `client\python\python.exe` | 存在 |
| `client\resources\agent_assets.mcdpkg` | 存在 |
| `configure\mc-design-client.config` | 存在 |

## 7. 测试身份配置

配置文件：

```text
C:\Users\ASUS\AppData\Local\McDesign\configure\mc-design-client.config
```

结果：

```text
user_id=88000044
user_name=宋明芮
tc_key_configured=false
```

说明：`tc_key` 缺失，本轮未写入 Teamcenter 密码，按 `TC_KEY_NOT_CONFIGURED` 记录并继续非 TC/NX smoke。

## 8. 客户端启动

首选入口：

```text
C:\Users\ASUS\AppData\Local\McDesign\McDesignClient.exe
```

首选入口结果：

- `McDesignClient.exe` 进程曾启动，PID `56860`。
- 超时内未观察到 `127.0.0.1:8765` 监听或 `/health` 可用。
- 本轮停止了由本次首选启动产生的残留 `McDesignClient.exe` 进程。
- 未生成 `client\logs\launcher-start.log` 或 `client\data\client.pid`。
- 严格按安装包正式入口判定为 `CLIENT_START_FAILED`。

诊断后备入口：

```text
C:\Users\ASUS\AppData\Local\McDesign\start-client.bat
```

后备入口结果：

- `cmd.exe` PID：`61564`
- Python runtime PID：`63304`
- Python 命令行：`"C:\Users\ASUS\AppData\Local\McDesign\client\python\python.exe" "C:\Users\ASUS\AppData\Local\McDesign\client\app\mc_design_client.pyz" --root "C:\Users\ASUS\AppData\Local\McDesign\client" start`
- `127.0.0.1:8765`：已监听。
- 启动日志：
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\client-start-fallback-output.log`
  - `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\client-start-fallback-error.log`
  - `C:\Users\ASUS\AppData\Local\McDesign\client\logs\client.log`
  - `C:\Users\ASUS\AppData\Local\McDesign\client\logs\tjuae-server.log`

## 9. 本地 health/status

证据：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\local-health-status.json
```

`GET http://127.0.0.1:8765/health`：

- HTTP 状态码：`200`
- `ok=true`
- `service=mc-design-client`
- `user_id=88000044`
- `user_name=宋明芮`
- assets bundle version：`PKG-002`
- assets `tool_count=3`
- runtime tools `count=29`
- bridge `connected=true`
- runtime `ok=true`
- runtime backend：`tjuae_server_sdk`
- tjuae server：`available=true`、`healthy=true`、`ready=true`

`GET http://127.0.0.1:8765/api/status`：

- HTTP 状态码：`200`
- `ok=true`
- client `running=true`
- cloud `connected=true`
- NX plugin `connected=false`
- NX plugin last_error：`<urlopen error timed out>`
- runtime `bridge_connected=true`
- runtime tools `count=29`
- runtime `nx_count=0`

说明：本轮未启动 NX，`NX_PLUGIN_NOT_CONNECTED` 作为环境状态记录，不判定为代码失败。

## 10. 本地 agent-turn smoke

入口：

```text
POST http://127.0.0.1:8765/api/runtime/test/agent-turn
```

首次请求：

- 使用默认 external timeout，HTTP `200`，业务响应 `ok=false`。
- `client.log` 显示 `asyncio.exceptions.TimeoutError`。
- 失败响应保存于 `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\local-agent-turn-response.json`。

重试请求：

- 显式设置 `timeout=180`。
- 轻量提示词只允许本地只读 `local_file_exists`。
- 禁止调用 NX、Teamcenter、QPP、MySQL/IPM/ECR connector。

重试结果：

- HTTP 状态码：`200`
- `ok=true`
- `status=success`
- `entrypoint=local_runtime_host`
- frames 数量：`545`
- events 数量：`3`
- 调用工具：`local_file_exists`
- 禁止工具调用：无。
- 最终摘要：`agent_assets.mcdpkg` 存在，文件大小 `246034` 字节，SHA256 `018cd7951d442f0bc9cc0f95e54a6e14c83b57717c59143686b3c184422698fc`。
- 完整响应：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\local-agent-turn-response-retry.json`

## 11. K8s smoke

BASE：

```text
http://ai-powerequip.yuchaiqas.com/mc-design/ai-server
```

API key：`f61***d0e`

证据：

```text
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-003\k8s-smoke-result.json
```

结果：

| 检查 | HTTP | 判定 |
|---|---:|---|
| `GET /api/readiness` | 200 | 通过 |
| `GET /api/mc-design/connectors/tools` | 200 | 通过 |
| `POST /api/mc-design/connectors/execute` / `mysql_query select 1` | 200 | 通过，返回 `{"1": 1}` |
| `POST /api/mc-design/connectors/execute` / `query_ipm_list page=1 pageSize=1` | 200 | 通过，只读分页补充检查 |
| `POST /api/mc-design/connectors/execute` / `query_ecr_list skip=0 take=1` | 200 | 通过，只读分页补充检查 |
| `POST /api/mc-design/test/agent-turn` | 404 | 符合预期 |

connector catalog 观察到关键工具：

```text
mysql_query
query_ipm_list
query_ecr_list
connect_qpp
tc_call
```

QPP：本轮未执行 `connect_qpp`；按已知事实记录为 `QPP_EXTERNAL_UNAVAILABLE`，不影响本轮 K8s readiness/catalog/mysql 基础判定。

## 12. 敏感信息与人工前置

- Teamcenter 密码：未读取明文、未输出明文、未写入回执。
- `tc_key_configured=false`。
- K8s API key：仅使用请求头调用，回执只记录脱敏值 `f61***d0e`。
- NX：测试开始前未发现 `ugraf.exe`；本轮未自动强杀 NX。
- K8s 网络：可访问，未触发 `VPN_REQUIRED`。

## 13. 总结

卸载、安装、安装后文件检查、配置写入、诊断入口启动后的 `/health`、`/api/status`、本地 agent-turn、K8s readiness/catalog/mysql 均完成并通过。

但安装包正式启动入口 `McDesignClient.exe` 未能在本轮测试中拉起可用的本地客户端端口。按安装包级 smoke 的严格口径，本任务最终结论为不通过，失败分类为 `CLIENT_START_FAILED`。建议后续单独排查 launcher 的启动等待时间、异常提示路径和日志落盘行为；当前证据显示直接运行 `start-client.bat` 可启动同一 Python runtime。
