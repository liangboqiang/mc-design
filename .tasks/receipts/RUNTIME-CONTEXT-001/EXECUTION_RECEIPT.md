# RUNTIME-CONTEXT-001 执行回执

执行日期：2026-06-14

## 任务边界

- 处理范围：`mc-design-nx/client` runtime adapter、本地 `test_agent_turn` 传参、必要契约测试。
- 未处理范围：NX plugin、参数规则 skill、打包安装链路、`mc-design-ai-service`。
- QPP 当前按公共规则归类为外部接口不可用，不作为本轮 mc-design 代码缺陷整改。
- 未输出 Teamcenter 密码、API key、cookie、token 或其他明文凭据。

## 改动文件清单

- `mc-design-nx/client/src/mc_design_client/runtime/tjuae_runtime_adapter.py`
- `mc-design-nx/client/tests/test_tjuae_runtime_adapter.py`
- `mc-design-nx/client/tests/test_usage_issue_fixes.py`
- `.tasks/receipts/RUNTIME-CONTEXT-001/EXECUTION_RECEIPT.md`

未修改 `mc-design-ai-service`。

## 根因确认

确认根因成立：

1. `TurnCommand.files` 已在本地入口和 runtime host 中保留，但 `McDesignTjuaeAdapter._compose_sdk_input()` 之前只返回 `command.query`，导致 files 未进入 `client.chat.stream(input=...)`。
2. `RuntimeEnvironment.runtime_system_prompt()`、`prompt_metadata()`、agent skill/tool asset 信息和动态 connector tool definitions 已存在，但之前没有稳定进入 SDK input，模型侧只能看到过薄 query，容易在本地 agent-turn 中判断 `query_ipm_list` 等 connector 不存在。

## 输入结构示例

`_compose_sdk_input()` 现在输出一个普通字符串，仍走 tjuae 通用 `chat.stream(input=...)`，不引入 mc-design 专用 tjuae 协议字段。结构示例：

```text
# Runtime System Prompt
<runtime_system_prompt，最多 24000 chars>

# Prompt Metadata
{"asset_root":"...","prompt_asset_refs":[...],"asset_hashes":{...}}

# Runtime Skill And Tool Assets
Skills available through Tjuae native skill loading:
- external-connector-adapter: ...
Tool asset groups enabled for this agent:
- tool.local_file: ...

# Runtime Tool Directory
Local tool groups:
- `local_file_read_bytes` group=`tool.local_file` ...
Dynamic connector tools:
- `query_ipm_list` group=`connector.external` ...
Required connector visibility:
- `query_ipm_list`: visible
- `query_ecr_list`: visible
- `connect_qpp`: visible
- `mysql_query`: visible
- `tc_call`: visible

# Files
<受限 metadata / inline_text 摘要 / local_file 读取提示>

# User Query
<用户 query>
```

## files 处理策略

- 文本内容只在安全条件下限量内联：单文件最多 `8192` bytes，单 turn files 总内联最多 `16384` bytes。
- metadata 单项摘要限制为 `1200` chars；二进制、base64、bytes 编码内容不内联。
- 大文本只注入截断摘要，并标记 `truncated`，不会无界进入上下文。
- 文件名或正文命中敏感模式时不内联正文，例如 Teamcenter 密钥字段、`password`、`secret`、`token`、API key、cookie 等。
- 只有路径或元数据的 files 会明确提示 agent 在允许目录内使用 `local_file_exists` / `local_file_read_bytes` 读取。
- 嵌套 metadata 中的 key/secret/token/password/pass 字段会脱敏。

## connector 可见性证明

新增/更新测试覆盖：

- `test_tjuae_adapter_syncs_connector_tools_from_k8s_schema`
  - fake K8s connector catalog 返回 `query_ipm_list`、`query_ecr_list`、`connect_qpp`、`mysql_query`、`tc_call`。
  - 断言五个 connector 均进入 tjuae plugin tool definitions。
  - 断言五个 connector 在 SDK input 的 `Required connector visibility` 中均为 `visible`。
  - 断言 `query_ipm_list` 出现在 `Dynamic connector tools` 目录中。
- `test_tjuae_adapter_includes_turn_files_in_sdk_input`
  - 断言普通文本 file 内容和 path-only file 元数据进入最终 SDK input。
- `test_tjuae_adapter_bounds_large_and_sensitive_file_inline_content`
  - 断言大文件未完整内联，敏感正文未进入 SDK input。
- `test_client_app_local_agent_turn_collects_runtime_frames_and_events`
  - 断言本地 `ClientApp.test_agent_turn()` 构造的 `TurnCommand.files` 保留到 runtime 调用。

## 测试命令和结果

使用 Codex bundled Python：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx/client/tests/test_tjuae_runtime_adapter.py mc-design-nx/client/tests/test_usage_issue_fixes.py
```

结果：`32 passed in 2.01s`

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx/client/tests
```

结果：`197 passed in 30.13s`

## K8s 和人工前置

- `K8S_UPDATE_REQUIRED=false`
- 是否需要手动更新 K8s：否，本轮未修改 `mc-design-ai-service`。
- 未执行 live K8s/QPP 调用；QPP 外部接口不可用按公共规则不作为代码失败。

## 结果摘要

本轮已修复 runtime SDK input 过薄问题：用户 query、runtime prompt、prompt metadata/asset_root、skill/tool asset 摘要、本地工具目录、动态 connector 目录和 files 安全摘要都会进入 tjuae `chat.stream(input=...)`。聚焦测试和客户端全量单测均通过。
