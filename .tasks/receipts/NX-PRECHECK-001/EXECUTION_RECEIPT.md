# NX-PRECHECK-001 Execution Receipt

日期：2026-06-14

## 结论

预检查已完成，结论为 `COMPLETED_WITH_ENV_BLOCKERS`，不判定代码失败。

本任务只执行了只读环境检查、进程/端口检查、HTTP GET 健康检查、工具清单读取和回执写入。未修改模型，未保存模型，未打开二维图纸，未执行自动出图，未调用 `nx_open_tcpart`，未安装/卸载/启动/重启 mc-design 客户端。

当前阻塞：

- `CLIENT_NOT_RUNNING`：`http://127.0.0.1:8765/health` 和 `/api/status` 均被本机拒绝连接。
- `NX_PLUGIN_NOT_CONNECTED`：NX `ugraf.exe` 正在运行，但 `127.0.0.1:8088` 没有 NX plugin HTTP 服务监听。

## 客户端健康状态

- 安装态配置存在：`C:\Users\ASUS\AppData\Local\McDesign\configure\mc-design-client.config`。
- 配置端口：runtime `8765`，NX plugin `8088`。
- `McDesignClient` 进程：未运行。
- `127.0.0.1:8765`：无监听。
- `GET http://127.0.0.1:8765/health`：失败，错误为 `由于目标计算机积极拒绝，无法连接。 (127.0.0.1:8765)`。
- `GET http://127.0.0.1:8765/api/status`：失败，同上。
- 安装态客户端日志显示客户端曾在 2026-06-14 11:17:31 启动，11:18:05 bridge connected，11:30:08 停止。

`E2E-SMOKE-002` 回执目录存在且包含 installer 目录，但未发现 `EXECUTION_RECEIPT.md`；未发现活跃 smoke 进程。本任务按规则只记录状态，没有启动或重启客户端。

## NX 连接状态

- NX 进程：已启动。
- 进程：`ugraf.exe`
- PID：`46060`
- 路径：`D:\Siemens\NX 11.0\NXBIN\ugraf.exe`
- 启动时间：2026-06-14 11:34:23
- 命令行：`"D:\Siemens\NX 11.0\NXBIN\ugraf.exe" -nx`

因此未记录 `NX_NOT_RUNNING`。

NX plugin 状态：

- 预期端口：`8088`
- `GET http://127.0.0.1:8088/health`：失败，错误为 `由于目标计算机积极拒绝，无法连接。 (127.0.0.1:8088)`。
- `GET http://127.0.0.1:8088/tools`：失败，同上。
- 安装目录未发现当前 NX plugin 日志。
- 工作区 `client\nx-plugin\log\log.txt` 是 2026-06-06 旧日志，早于本次 NX 会话，未作为当前 plugin 状态依据。

## 禁用工具检查结果

会话级 NX 工具发现：

- `tool_search` 查询 `nx_open_tcpart`、`nx-auto-drawing`、`nx_run_auto_drawing`、`nx_updatedrawings`：结果数 `0`。
- 当前 Codex 会话未暴露可直接调用的 NX 工具，也未暴露禁用工具。

打包 manifest 检查：

- `client\client\resources\nx_tools_manifest.json`：20 个工具，包含 `nx_open_tcpart`，禁用工具命中 `0`。
- `mc-design-nx\client\resources\nx_tools_manifest.json`：20 个工具，包含 `nx_open_tcpart`，禁用工具命中 `0`。
- 对 `client\client\resources` 与 `mc-design-nx\client\resources` 执行禁用名称搜索，命中 `0`。

已检查不存在的禁用入口：

- `nx-auto-drawing`
- `nx_run_auto_drawing`
- `nx_updatedrawings`
- `nx_update_drawing`
- `nx_open_tc_drawing`
- `nx_open_drawing_sheet`
- `nx_get_drawing_sheet_name_list`
- `nx_create_auto_drawing_sheet`
- `nx_create_auto_drawing_views`
- `nx_apply_pmi_inheritance_to_drawing_views`
- `nx_delete_drawing_sheets`
- `nx_validate_auto_drawing_plan`
- `nx_get_auto_drawing_tool_guide`
- `nx_enter_drafting_environment`

实际运行时工具列表因 `CLIENT_NOT_RUNNING` 未能从 `/health` 获取；该项记录为环境阻塞，不判定代码失败。

## nx_open_tcpart Schema

`nx_open_tcpart` 存在于当前打包 manifest：

```json
{
  "name": "nx_open_tcpart",
  "namespace": "nx",
  "source": "nx-plugin",
  "description": "打开 TC 主模型/主部件或已绑定 NX 图纸 ItemRevision：根据 itemID 和可选 itemRev 使用 @DB/<item>/<rev> 打开；itemRev 为空时打开最新版本。",
  "danger_level": "write",
  "requires_connection": true,
  "original_name": "OpenTCPart",
  "category": "File",
  "parameters": [
    {
      "name": "itemID",
      "type": "string",
      "isOptional": false
    },
    {
      "name": "itemRev",
      "type": "string",
      "isOptional": true
    }
  ],
  "input_schema": {
    "type": "object",
    "properties": {
      "itemID": {
        "type": "string",
        "description": "string"
      },
      "itemRev": {
        "type": "string",
        "description": "string"
      }
    },
    "required": [
      "itemID"
    ]
  }
}
```

未调用 `nx_open_tcpart`，因为该工具会打开 NX/TC 部件，超出本次只读前置检查范围。

## open_tc_part 网络分类

本次未执行 `nx_open_tcpart`，因此未直接观察到 TC/NX 网络阻塞。当前分类为 `NOT_TESTED_SIDE_EFFECT_AVOIDED`。

如果后续 NX plugin 连接正常但 `@DB/<item>/<rev>` 打开因测试环境网络失败，应记录为：

- `TC_NX_NETWORK_BLOCKED`，或
- `NEED_MANUAL_MODEL_OPEN`

该类问题不应判定为代码失败。

## 人工前置项清单

- `NEED_MANUAL_CLIENT_START_OR_RELEASE`：需要 E2E-SMOKE-002 执行方释放或人工启动 mc-design 客户端后，才能读取实际运行时工具列表。
- `NEED_MANUAL_NX_PLUGIN_LOAD`：NX 已启动，但 mc-design NX plugin 未在 `127.0.0.1:8088` 监听。
- `NEED_MANUAL_MODEL_OPEN`：若 plugin 可用后 TC/NX 网络仍阻塞 `nx_open_tcpart`，需要人工打开目标模型/图纸 ItemRevision。

## 输出文件

- `EXECUTION_RECEIPT.md`
- `NX_PRECHECK_RESULTS.json`
