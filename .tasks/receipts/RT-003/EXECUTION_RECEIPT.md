# RT-003 Execution Receipt

## Scope

本次执行目标是把 `test_agent_turn` 从 K8s AI Service 移回本地 `mc-design-client`，同时修整 K8s connector execute/MySQL 错误分层，保证后续重启/更新 K8s 后可以进入真实通路测试。

## Changed Files

- `mc-design-nx/client/src/mc_design_client/api/server.py`
- `mc-design-nx/client/src/mc_design_client/app.py`
- `mc-design-nx/client/tests/test_usage_issue_fixes.py`
- `mc-design-ai-service/beya_mcp/server.py`
- `mc-design-ai-service/beya_mcp/runtime_bridge.py`
- `mc-design-ai-service/integrations/config.py`
- `mc-design-ai-service/integrations/mysql/client.py`
- `mc-design-ai-service/beya.toml`
- `mc-design-ai-service/.env.example`
- `mc-design-ai-service/tests/test_runtime_bridge_architecture.py`
- `mc-design-ai-service/tests/test_mysql_connector_errors.py`

## Local test_agent_turn Entry

本地通路测试入口已放在本地 client：

- `POST /api/runtime/test/agent-turn`
- 运行位置：本地 `mc-design-client`
- 不依赖 K8s 提供 agent turn HTTP 测试入口
- 内部调用：`ClientApp.test_agent_turn(...)` -> `RuntimeHost.run(...)`

请求体支持：

```json
{
  "user_id": "88000044",
  "agent_id": "design_agent",
  "conversation_id": "rt-003-smoke",
  "query": "hello",
  "files": [],
  "metadata": {},
  "timeout": 300
}
```

返回包含：

- `ok`
- `entrypoint`
- `turn_id`
- `status`
- `content`
- `reasoning`
- `tools`
- `frames`
- `events`
- `final_result`
- `result`
- `code/message/error` when failed

本地 connector tool 仍通过本地 Runtime/Tjuae 工具链触发；当工具需要 MySQL/IPM/QPP/TC 时，再由本地 client 转发到 K8s `/api/mc-design/connectors/execute`。

## K8s test_agent_turn Removal

K8s AI Service 已移除：

- `POST /api/mc-design/test/agent-turn`
- `POST /mc-design/ai-server/api/mc-design/test/agent-turn`
- `agents` discovery 中的 `test_agent_turn` 字段

K8s AI Service 保留：

- `/api/health`
- `/api/readiness`
- `/api/mc-design/agents`
- `/api/mc-design/connectors/tools`
- `/api/mc-design/connectors/execute`
- `/api/mc-design/llm/v1/models`
- `/api/mc-design/llm/v1/chat/completions`
- runtime WebSocket bridge

## MySQL Connector Fix

MySQL 链路保持为：

`mc-design-client` -> K8s `/api/mc-design/connectors/execute` -> `RuntimeBridgeManager.call_business_tool` -> `mysql_query` -> `MySQLClient` -> MySQL 服务

修复点：

- `ConnectSettings.mysql_config()` 不再把缺失 host 默认成 `127.0.0.1`。
- `readiness` 的 `router.connectors.mysql` 会显示 MySQL 配置状态，缺项为 `MYSQL_CONFIG_MISSING`。
- MySQL 密码不会出现在 readiness 或错误 details 中，只显示 `has_password`。
- `MySQLClient` 将 PyMySQL 缺失、连接失败、SQL 执行失败拆成独立错误码。
- `RuntimeBridgeManager.call_business_tool` 会保留异常上的 `code/details`，不再压成泛化 `BUSINESS_TOOL_ERROR`。

## K8s Route/Prefix Fix

本地 client 转发 connector execute 时使用：

- `websocket_base_url = http://host:port`
- `websocket_path = /mc-design/ai-server/ws`
- 推导 API base：`http://host:port/mc-design/ai-server`
- 最终 execute：`http://host:port/mc-design/ai-server/api/mc-design/connectors/execute`

若 `websocket_base_url` 已显式包含 `/mc-design/ai-server`，不会重复拼接前缀。

## Error Codes

- `LOCAL_K8S_UNREACHABLE`: 本地 client 无法连接 K8s AI Service。
- `CONNECTOR_ROUTE_NOT_FOUND`: K8s connector execute 路由不存在、路径前缀错误、或被错误 ingress rewrite。
- `MYSQL_CONFIG_MISSING`: K8s MySQL 配置缺失。
- `MYSQL_DEPENDENCY_MISSING`: AI Service runtime 缺少 PyMySQL。
- `MYSQL_CONNECT_FAILED`: AI Service 收到 mysql_query，但 K8s 内部连接 MySQL 失败。
- `MYSQL_QUERY_FAILED`: MySQL 已连接，但 SQL 执行失败。
- `CONNECTOR_HTTP_ERROR`: K8s 返回其它非 2xx HTTP 错误且无结构化 connector payload。
- `RUNTIME_TURN_TIMEOUT`: 本地 RuntimeHost turn 超时。
- `LOCAL_TEST_AGENT_TURN_FAILED`: 本地测试入口自身执行失败。

## Local Test Commands And Results

系统 PATH 中 `python` 不可用，已使用 Codex bundled Python：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx/client/tests/test_usage_issue_fixes.py mc-design-nx/client/tests/test_client_static.py -q
```

结果：

```text
49 passed in 0.74s
```

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-ai-service/tests/test_runtime_bridge_architecture.py mc-design-ai-service/tests/test_bridge_contract.py mc-design-ai-service/tests/test_mysql_connector_errors.py mc-design-ai-service/tests/test_runtime_replacement_policy.py -q
```

结果：

```text
56 passed, 1 warning in 2.25s
```

## K8s Smoke Test After Update

项目负责人更新/重启 K8s 后，可执行：

```bash
BASE="http://<k8s-host>:<port>/mc-design/ai-server"
KEY="<BEYA_MCP_API_KEY>"

curl -sS -H "x-api-key: ${KEY}" "${BASE}/api/readiness"

curl -sS -H "x-api-key: ${KEY}" \
  "${BASE}/api/mc-design/connectors/tools"

curl -sS -X POST \
  -H "x-api-key: ${KEY}" \
  -H "content-type: application/json" \
  "${BASE}/api/mc-design/connectors/execute" \
  -d '{"tool":"mysql_query","namespace":"connector.mysql","arguments":{"sql_statement":"select 1"},"metadata":{"mc_design_user_id":"88000044"}}'
```

本地 client agent turn smoke test：

```bash
curl -sS -X POST \
  -H "content-type: application/json" \
  "http://127.0.0.1:8765/api/runtime/test/agent-turn" \
  -d '{"user_id":"88000044","agent_id":"design_agent","conversation_id":"rt-003-smoke","query":"hello","files":[],"metadata":{},"timeout":300}'
```

## Manual Actions Required

- 项目负责人需要手动更新/重启 K8s AI Service。
- 如果返回 `LOCAL_K8S_UNREACHABLE`，先确认本地网络和 K8s 服务地址；如需内网/VPN，项目负责人手动开启 VPN。
- 如果 `readiness.router.connectors.mysql.code = MYSQL_CONFIG_MISSING`，需要在 K8s Secret/ConfigMap/env 中补齐 `BEYA_MYSQL_HOST/PORT/DATABASE/USER/PASSWORD`。
- 如果返回 `MYSQL_DEPENDENCY_MISSING`，需要确认 AI Service 镜像安装了 `PyMySQL>=1.1.0`。
- 如果返回 `MYSQL_CONNECT_FAILED`，K8s 已收到请求，但 Pod 到 MySQL 的网络、DNS、账号或安全策略仍需排查。
- 本地真实 NX 工具链测试前，需要项目负责人手动启动 NX。
- 当前测试环境 `nx_open_tcpart` 不可用时，需要项目负责人手动打开目标模型。
- 本次未恢复 NX plugin 自动出图能力，自动出图插件保持禁用。
