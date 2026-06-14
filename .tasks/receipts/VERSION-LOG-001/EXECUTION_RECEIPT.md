# VERSION-LOG-001 执行回执

执行时间：2026-06-14

## 任务目标

验证本地客户端在 `test_agent_turn` 通路中能够按 `conversation_id` 生成会话日志，并且日志与返回摘要能够绑定客户端版本、tjuae SDK 版本、源码提交等版本信息，便于后续把用户问题和日志一一对应。

## 执行环境

- 本地客户端地址：`http://127.0.0.1:8765`
- 测试用户：`88000044 / 宋明芮`
- 本地安装目录：`C:\Users\ASUS\AppData\Local\McDesign`
- 当前安装资产包：`PKG-002`
- 本地 runtime：`tjuae-sdk-adapter`
- 本地工具数量：`29`
- NX 状态：`connected=true`
- AI bridge 状态：`connected=true`
- tjuae server 状态：`healthy=true, ready=true`

## 实测结果

### 1. 安装态客户端健康检查

`GET /health` 和 `GET /api/status` 均返回 `ok=true`，客户端、NX、AI bridge、runtime 均处于可运行状态。

但当前安装态响应中没有最新源码要求的 `version` 字段，也没有 `conversation_logs` 摘要字段。这说明当前运行的安装包不是最新源码对应的客户端版本，不能用于验收 VERSION-LOG-001 的最终目标。

### 2. 本地 agent-turn

请求：

- Endpoint：`POST /api/runtime/test/agent-turn`
- conversation_id：`version-log-001-20260614-153011`
- user_id：`88000044`
- agent_id：`design_agent`

结果：

- `ok=true`
- `status=success`
- 返回内容：已收到本地会话日志健康检查请求，当前会话运行正常。
- runtime frames/events 正常返回
- 未返回最新源码中的 `conversation_log` 摘要

判断：本地 agent-turn 主通路能运行，但当前安装态客户端没有最新会话日志增强能力。

### 3. 会话日志查询接口

请求：

- `GET /api/runtime/conversation-log?conversation_id=version-log-001-20260614-153011`

结果：

- HTTP 404

判断：当前安装态客户端未包含最新源码中的 `/api/runtime/conversation-log` 接口。

### 4. 安装目录日志检查

日志目录：

- `C:\Users\ASUS\AppData\Local\McDesign\client\logs`

现有日志：

- `client.log`
- `tjuae-server.log`
- `launcher-start.log`

未发现 `conversations/*.jsonl` 或 `*.summary.json` 会话日志产物。

敏感字段扫描只输出计数，不输出具体值：

- `sensitive_key_words=1`
- `assignment_like_secret_values=0`

判断：未发现形如密钥赋值的明文泄漏。现有安装态日志中没有 per-conversation 日志能力。

## 源码验证

执行命令：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest `
  mc-design-nx/client/tests/test_usage_issue_fixes.py::test_client_api_exposes_conversation_log_status_endpoint `
  mc-design-nx/client/tests/test_usage_issue_fixes.py::test_client_app_local_agent_turn_writes_per_conversation_log `
  mc-design-nx/client/tests/test_usage_issue_fixes.py::test_client_version_info_tracks_vendored_tjuae_sdk `
  mc-design-nx/client/tests/test_client_static.py::test_tjuae_sdk_is_vendored_for_customer_client_builds -q
```

结果：

```text
4 passed in 0.69s
```

源码层面确认：

- `/api/runtime/conversation-log` 已存在。
- `test_agent_turn` 返回体会附带 `conversation_log`。
- per-conversation 日志记录包含 `version` 信息。
- tjuae SDK 已作为客户客户端构建资产内置并被版本信息引用。

## 结论

状态：`SOURCE_PASS / INSTALLED_CLIENT_STALE`

VERSION-LOG-001 的源码实现已通过相关测试，但当前正在运行的安装态客户端不是最新构建，因此真实本地端点无法完成最终验收。

这不是 agent-turn 业务失败，也不是 tjuae runtime 失败；本质原因是“已安装客户端版本滞后于代码仓最新版本”。

## 后续动作

下一步应优先执行客户端最新源码的打包、卸载重装、启动和版本复验：

1. 重新打包 `mc-design-nx/client` 最新源码。
2. 卸载当前 `C:\Users\ASUS\AppData\Local\McDesign` 安装态客户端。
3. 安装最新包并启动客户端。
4. 复验 `/health`、`/api/status` 中是否包含 `version`。
5. 复验 `/api/runtime/test/agent-turn` 是否返回 `conversation_log`。
6. 复验 `/api/runtime/conversation-log?conversation_id=...` 是否返回日志摘要。

