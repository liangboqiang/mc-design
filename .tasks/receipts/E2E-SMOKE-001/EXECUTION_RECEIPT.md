# E2E-SMOKE-001 Execution Receipt

## 1. 结论

结论：环境阻塞。

阻塞分类：客户端卸载/重装链路阻塞。

本次 smoke 已完成环境基线记录、Windows 客户端安装包构建、安装包解压和旧客户端卸载尝试。旧客户端卸载失败后，按任务规则停止，未继续执行新客户端安装、客户端启动、K8s connector smoke 和本地 agent-turn smoke。

## 2. 改动说明

本任务不允许改代码；执行过程中未进行任何源码编辑、未执行 git reset/checkout 等回滚操作。

已发生的非源码操作：

- 生成/覆盖构建产物和日志：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\`
- 解压安装包到回执目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-001\installer\`
- 生成本回执：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-001\EXECUTION_RECEIPT.md`

git 基线：

- 时间：`2026-06-14T10:49:43.7194925+08:00`
- 机器名：`BRYAN-ROG`
- 当前 commit：`41841e94bbaad4b9fd4d1f0a927f82f9d63085b4`
- 工作区状态：记录时工作区非干净；后续摘要为 `29 modified / 889 deleted / 8 untracked / total 926`。这些包含执行前已存在的大量变更、本次构建产物和回执目录；本任务未手工修改代码。

## 3. 环境基线

旧客户端进程：

- `McDesignClient.exe`：未发现。
- `python.exe` 中运行 `mc_design_client`：未发现。
- `tjuae-server.exe`：未发现。

默认安装目录：

- 路径：`C:\Users\ASUS\AppData\Local\McDesign`
- 基线状态：存在。
- 顶层内容包括：`client\`、`configure\`、`nx-plugin\`、`install_helper.py`、`install-state.json`、`package-manifest.json`、`README_INSTALL.txt`、`smoke_test.py`、`smoke-test.bat`、`start-client.bat`、`uninstall.bat`。

## 4. 构建信息

构建工作目录：

`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx`

构建命令：

```powershell
$env:MC_DESIGN_NO_PAUSE='1'
package\windows\build-installer.bat --bundle-version E2E-SMOKE-001 --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk
```

构建结果：

- Exit code：`0`
- 结果：`Build succeeded`
- 是否使用 `--skip-msbuild`：否。

安装包路径：

`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-E2E-SMOKE-001.zip`

安装包信息：

- Size：`93405564` bytes
- LastWriteTime：`2026-06-14 10:50:13`

build log 路径：

`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\logs\build-installer.last.log`

build log 信息：

- Size：`7756` bytes
- LastWriteTime：`2026-06-14 10:50:13`

构建日志摘要：

- `ui_build.status`: `built`
- `launcher_build.status`: `built`
- `python_runtime_prepare.ok`: `true`
- `python_runtime_prepare.python_version`: `3.8.10`
- `archive`: `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-E2E-SMOKE-001.zip`

## 5. 卸载/安装结果

安装包解压目录：

`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-001\installer\McDesignClientSetup-E2E-SMOKE-001\`

安装包内脚本确认：

- `install.bat`：存在。
- `uninstall.bat`：存在。
- `smoke-test.bat`：存在。
- `payload\start-client.bat`：存在。

旧客户端卸载结果：失败。

卸载尝试 1：

```powershell
$env:MC_DESIGN_NO_PAUSE='1'
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-001\installer\McDesignClientSetup-E2E-SMOKE-001\uninstall.bat
```

- Exit code：`4`
- 输出摘要：`Uninstall dir` 被解析为解压包目录，随后报 `Missing bundled Python or uninstall helper.`

卸载尝试 2：

```powershell
$env:MC_DESIGN_UNINSTALL_NO_PAUSE='1'
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\E2E-SMOKE-001\installer\McDesignClientSetup-E2E-SMOKE-001\uninstall.bat C:\Users\ASUS\AppData\Local\McDesign
```

- Exit code：`4`
- 输出摘要：`Uninstall dir: C:\Users\ASUS\AppData\Local\McDesign`
- 失败原因：`Missing bundled Python or uninstall helper.`

卸载后现场检查：

- `C:\Users\ASUS\AppData\Local\McDesign`：仍存在。
- `C:\Users\ASUS\AppData\Local\McDesign\client\python\python.exe`：存在。
- `C:\Users\ASUS\AppData\Local\McDesign\installer\tools\install_helper.mcpy`：不存在。
- `C:\Users\ASUS\AppData\Local\McDesign\install_helper.py`：存在。
- `C:\Users\ASUS\AppData\Local\McDesign\uninstall.bat`：存在。
- `C:\Users\ASUS\AppData\Local\McDesign\client\app\mc_design_client.pyz`：不存在。
- `C:\Users\ASUS\AppData\Local\McDesign\McDesignClient.exe`：不存在。
- 卸载后进程残留：未发现 `McDesignClient.exe` / `mc_design_client` Python 进程 / `tjuae-server.exe`。

新客户端安装结果：未执行。

停止原因：旧客户端卸载失败。按任务规则“如果卸载失败，本任务停止，回执标记为客户端卸载/重装链路阻塞”，未运行 `install.bat`。

新安装目录关键文件清单：未检查；新客户端未安装。

## 6. 客户端运行结果

未执行。

原因：旧客户端卸载失败后任务停止，未进入新客户端安装和启动阶段。

- 启动方式：未执行。
- 端口：未检查。
- `/health` 响应：未执行。
- `/api/status` 响应：未执行。
- `tjuae_server` 状态：未检查。
- `bridge` 状态：未检查。
- tools count：未检查。
- assets 状态：未检查。
- 日志位置：未产生新客户端运行日志。

## 7. K8s Smoke 结果

未执行。

原因：旧客户端卸载失败后任务停止，未进入 K8s connector smoke 阶段。

- readiness：未执行。
- connectors/tools：未执行。
- mysql_query `select 1`：未执行。
- K8s 旧 `/api/mc-design/test/agent-turn` 404 验证：未执行。

说明：本次未访问 K8s，因此未判断 `K8s 未更新`、`VPN/网络未开启` 或外部接口可用性。

## 8. 本地 Agent-Turn Smoke 结果

未执行。

原因：旧客户端卸载失败后任务停止，未安装并启动新客户端，不能调用本地客户端入口。

计划请求体：

```json
{
  "query": "请做一次本地通路 smoke，只返回当前客户端、运行时和工具目录状态摘要，不要调用 NX 修改类工具。",
  "conversation_id": "e2e-smoke-001",
  "agent_id": "design_agent",
  "timeout": 300,
  "metadata": {
    "test_id": "E2E-SMOKE-001",
    "purpose": "local-client-agent-turn-smoke"
  }
}
```

实际结果：

- HTTP 状态：未执行。
- 返回摘要：未执行。
- frames/events/tool 摘要：未执行。
- 副作用工具检查：未触发工具。

## 9. 失败分类

- 代码缺陷：未判定。本次在卸载链路停止，没有进入运行态验证。
- 客户端打包失败：否。构建成功。
- 客户端卸载/重装失败：是。旧客户端卸载失败，阻塞重装。
- 客户端未启动或健康检查失败：未执行。
- K8s 未更新：未执行，未判定。
- VPN/网络未开启：未执行，未判定。
- NX 未启动：未执行，未判定。
- TC/NX 模型需手动打开：未执行，未判定。
- 外部接口不可用：未执行，未判定。

## 10. 后续建议

- 先确认当前旧安装目录是否为历史版本或残缺安装；它缺少新卸载脚本要求的 `installer\tools\install_helper.mcpy`，且缺少 `McDesignClient.exe` 和 `client\app\mc_design_client.pyz`。
- 项目负责人可选择手动清理或用旧安装目录内自带卸载逻辑处理 `C:\Users\ASUS\AppData\Local\McDesign` 后重跑本 smoke。
- 建议评估新安装包的 `uninstall.bat` 是否需要兼容旧版安装布局中的 `install_helper.py`，以避免客户端更新 smoke 在历史安装目录上被卸载链路阻塞。
