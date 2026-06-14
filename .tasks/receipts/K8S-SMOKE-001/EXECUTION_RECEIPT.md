# K8S-SMOKE-001 Execution Receipt

执行时间：2026-06-14 10:22:33 +08:00

工作目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design`

回执文件：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\K8S-SMOKE-001\EXECUTION_RECEIPT.md`

## 执行边界

- 未修改代码。
- 未修改 K8s 配置。
- 未修改本地 client 配置。
- 未启动 NX。
- 未执行真实零部件设计链路。
- 未调用本地 `/api/runtime/test/agent-turn`。

## 实际测试输入

- BASE：`http://ai-powerequip.yuchaiqas.com/mc-design/ai-server`
- API KEY：`f61***d0e`
- 输入来源：只读读取 `mc-design-nx\configure\mc-design-package.config` 中的 `websocket_base_url`、`websocket_path`、`api_key`，未修改该配置。

## 1. Readiness

请求：

```bash
curl -sS -H "x-api-key: <masked>" "http://ai-powerequip.yuchaiqas.com/mc-design/ai-server/api/readiness"
```

HTTP 状态码：`200`

原始返回摘要：

```json
{
  "ok": true,
  "version": "0.18.8-agent-stream-0af28be-protocol",
  "runtime_connections": 0,
  "router": {
    "llm": {
      "configured": true,
      "base_url": "https://ai-gateway.linkskycloud.com/v1",
      "models": [
        "doubao-seed-2.0-pro",
        "doubao-seed-2.0-lite",
        "deepseek-v3-1"
      ],
      "has_api_key": true
    },
    "connectors": {
      "enabled": true,
      "mysql": {
        "configured": true,
        "code": "OK",
        "missing": [],
        "host": "10.22.16.49",
        "port": 3306,
        "database": "mc_design_data",
        "user": "mc_design_data_user",
        "has_password": true
      }
    }
  }
}
```

判定：`router/connectors/mysql.code = OK`，readiness 通过。

## 2. Connector Catalog

请求：

```bash
curl -sS -H "x-api-key: <masked>" "http://ai-powerequip.yuchaiqas.com/mc-design/ai-server/api/mc-design/connectors/tools"
```

HTTP 状态码：`200`

返回摘要：

```json
{
  "ok": true,
  "tools": "<connector catalog returned>"
}
```

已确认存在的必需工具：

- `mysql_query`
- `query_ipm_list`
- `query_ecr_list`
- `connect_qpp`
- `tc_call`

判定：connector catalog 通过。

## 3. MySQL Smoke

请求：

```bash
curl -sS -X POST \
  -H "x-api-key: <masked>" \
  -H "content-type: application/json" \
  "http://ai-powerequip.yuchaiqas.com/mc-design/ai-server/api/mc-design/connectors/execute" \
  -d '{"tool":"mysql_query","namespace":"connector.mysql","arguments":{"sql_statement":"select 1"},"metadata":{"mc_design_user_id":"88000044"}}'
```

HTTP 状态码：`200`

原始返回摘要：

```json
{
  "ok": true,
  "tool": "mysql_query",
  "result": {
    "query_result": [
      {
        "1": 1
      }
    ],
    "sql_statement": "select 1"
  }
}
```

判定：`mysql_query select 1` 执行成功。

## 4. K8s test_agent_turn 移除确认

请求：

```bash
curl -sS -o /dev/null -w "%{http_code}" \
  -X POST \
  -H "x-api-key: <masked>" \
  -H "content-type: application/json" \
  "http://ai-powerequip.yuchaiqas.com/mc-design/ai-server/api/mc-design/test/agent-turn" \
  -d '{}'
```

HTTP 状态码：`404`

返回体摘要：`Not Found`

判定：K8s `/api/mc-design/test/agent-turn` 已移除，404 为预期结果，通过。

## 结论

结论：通过

失败归类：不适用

网络状态：K8s 可访问，未出现 `LOCAL_K8S_UNREACHABLE`。

是否建议进入下一步全通路测试：是。
