# LOG-001 Execution Receipt

更新时间：2026-06-14

## 任务边界

- 本任务由监管方插队直接执行。
- 范围：`mc-design-nx/client` 客户端运行时会话日志。
- 未修改：`tjuae` 协议、NX plugin、AI Service connector、参数规则脚本、DFMEA 工具。
- 敏感信息规则：不得输出 Teamcenter 密码、API key、cookie、token 或明文凭据。

## 改动文件

- `mc-design-nx/client/src/mc_design_client/runtime/conversation_log.py`
- `mc-design-nx/client/src/mc_design_client/app.py`
- `mc-design-nx/client/src/mc_design_client/api/server.py`
- `mc-design-nx/client/tests/test_usage_issue_fixes.py`
- `mc-design-nx/client/tests/test_client_static.py`
- `.tasks/project_health_2026-06-14.md`
- `.tasks/project_supervision_plan.md`
- `.tasks/skill_tool_asset_audit_2026-06-14.md`
- `.tasks/receipts/LOG-001/EXECUTION_RECEIPT.md`

## 实现说明

新增客户端会话日志能力：

1. 每个 `conversation_id` 写一份 JSONL：
   - `client/logs/conversations/<safe_conversation_id>.jsonl`
2. 每个 `conversation_id` 写一份摘要：
   - `client/logs/conversations/<safe_conversation_id>.summary.json`
3. 本地 `test_agent_turn` 返回 `conversation_log` 字段，包含日志和摘要路径。
4. 远程 bridge `runtime.turn.run` 也写入同一会话日志。
5. 新增只读查询入口：
   - `GET /api/runtime/conversation-log?conversation_id=<id>`

## 记录内容

日志记录以下信息：

- turn started
- query 摘要与 sha256
- files 元数据摘要
- runtime frames
- runtime events
- tool started/completed/failed 摘要
- turn response
- last status / last error

## 脱敏策略

日志模块对以下内容做字段级脱敏或摘要化：

- `tc_key`
- `user_pass`
- `password`
- `passwd`
- `secret`
- `token`
- `api_key`
- `cookie`
- `authorization`
- `x-tc-key`
- `base64` / `bytes` / `content_bytes` / `raw_bytes` / `data_url`

长文本会截断并保留 sha256，避免日志无限增长。

## 测试命令和结果

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx/client/tests/test_usage_issue_fixes.py -q
```

结果：`13 passed in 2.15s`

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx/client/tests -q
```

结果：`199 passed in 26.71s`

## 后续使用规则

测试人员提交新问题时，应同时提供：

1. `conversation_id`
2. 复现输入
3. 期望表现和实际表现
4. `conversation_log.log_path` 或对应 JSONL 日志文件

监管方可根据会话日志还原用户输入、工具调用、失败分类和最终回答，用于绑定问题表或新增缺陷。
