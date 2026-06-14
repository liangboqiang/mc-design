# LOG-COMPACT-001 执行回执

## 任务定位

优化客户端会话日志体积，保留按 `conversation_id` 还原问题所需的关键诊断信息，同时避免把流式 delta、工具大返回、base64、完整最终答案等内容完整落盘。

## 改动文件

- `mc-design-nx/client/src/mc_design_client/runtime/conversation_log.py`
- `mc-design-nx/client/tests/test_usage_issue_fixes.py`

## 优化内容

- 日志 schema 升级为 `LOG_SCHEMA = 2`。
- JSONL 每行不再重复写完整客户端/tjuae 版本信息；版本保留在 `turn.started` 和 `.summary.json`。
- `llm.delta`、`content.delta`、`reasoning.delta`、`text.delta` 不再逐条落盘，只在 summary 中记录 `frame_type_counts` 和 `omitted_frame_count`。
- 工具事件只记录：
  - frame id/seq/type
  - tool 名称
  - code/error_type
  - 短 message
  - 原始 data 的长度和 sha256 摘要
- `turn.completed` 和 `turn.response` 的结果只记录：
  - chars
  - sha256
  - 短 preview
- base64/raw bytes/data_url 等字段只记录长度和 sha256。
- dict/list 增加数量上限，超出后记录截断数量和 hash。
- 单条 JSONL 记录增加硬上限，超过预算时自动降级为 `record_exceeded_log_budget` 摘要。
- `.summary.json` 改为紧凑 JSON，不再 indent。
- 接口返回的 `conversation_log.summary()` 也走脱敏，避免响应体泄漏敏感错误信息。

## 验证结果

命令：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest mc-design-nx/client/tests/test_usage_issue_fixes.py mc-design-nx/client/tests/test_client_static.py
```

结果：`59 passed`

命令：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest mc-design-nx/client/tests/test_tjuae_runtime_adapter.py mc-design-nx/client/tests/test_tool_registry.py
```

结果：`52 passed`

新增大日志回归用例：

- 60 条 `llm.delta`，每条 5000 字符，不落盘明细。
- 1 条 `tool.completed`，包含 20000 字符 base64，只落摘要。
- 断言 JSONL `< 12000` bytes，summary `< 9000` bytes。

## 当前边界

- 这是未来日志优化，不会自动重写用户机器上已经生成的旧大日志。
- 如需要清理旧日志，应另做 `LOG-RETENTION-001`：按日期、大小和 conversation_id 白名单执行归档/删除策略。
