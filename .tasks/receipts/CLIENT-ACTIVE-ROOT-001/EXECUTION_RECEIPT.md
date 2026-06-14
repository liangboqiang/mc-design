# CLIENT-ACTIVE-ROOT-001 执行回执

更新时间：2026-06-14

## 任务边界

本次只做根目录 `client/` 活跃区收口、工具说明资产到 Python provider/registry/HTTP executor 的映射固化、测试补强和静态/单元测试。未处理 E2E-SMOKE-003，未修改安装/卸载流程，未启动 NX、Teamcenter、K8s 或本地客户端，未修改外部 tjuae 项目。

## 输入依据

- `.tasks/TEST_EXECUTION_RULES.md`
- `.tasks/receipts/CLIENT-ARCH-001/AUDIT_RECEIPT.md`
- `.tasks/receipts/CLIENT-ASSET-001/EXECUTION_RECEIPT.md`
- `.tasks/receipts/CLIENT-LEGACY-001/EXECUTION_RECEIPT.md`
- `.tasks/receipts/CLIENT-LEGACY-001/LEGACY_MANIFEST_BEFORE.json`
- `.tasks/receipts/CLIENT-LEGACY-001/LEGACY_MANIFEST_AFTER.json`
- `mc-design-nx/client/README_TJUAE_RUNTIME.md`
- `mc-design-nx/assets/source/tools/`
- `mc-design-nx/client/src/mc_design_client/tools/`
- `mc-design-nx/client/src/mc_design_client/api/server.py`
- `mc-design-nx/client/src/mc_design_client/app.py`
- `mc-design-nx/client/src/mc_design_client/runtime/tjuae_runtime_adapter.py`
- `mc-design-nx/client/tests/test_tool_registry.py`

## 改动文件清单

- `.gitignore`：新增根 `/client/` 忽略规则，阻止安装 payload/运行数据回流。
- `README.md`：明确根 `client/` 不是源码入口，源码入口是 `mc-design-nx/client`。
- `mc-design-nx/.gitignore`：继续忽略生成资源，但允许跟踪 `client/resources/tool_execution_map.json`。
- `mc-design-nx/assets/source/tools/INDEX.md`：明确 `TOOL.md` 是说明资产，实际执行在 Python provider 和本地 HTTP executor。
- `mc-design-nx/client/README_TJUAE_RUNTIME.md`：新增 Tool Execution Map 说明。
- `mc-design-nx/client/resources/tool_execution_map.json`：新增机器可读工具执行映射。
- `mc-design-nx/client/src/mc_design_client/tools/nx_provider.py`：NX provider manifest spec 显式标记 `tool_group=tool.nx`。
- `mc-design-nx/client/src/mc_design_client/runtime/tjuae_runtime_adapter.py`：本地工具 executor namespace 按 `tool.local_file` / `tool.dfmea` / `tool.nx` 投影。
- `mc-design-nx/client/tests/test_tool_registry.py`：补充映射、TOOL.md、namespace、tjuae executor、根 payload 收口测试。
- `.tasks/receipts/CLIENT-ACTIVE-ROOT-001/ROOT_CLIENT_MANIFEST_BEFORE.json`
- `.tasks/receipts/CLIENT-ACTIVE-ROOT-001/ROOT_CLIENT_MANIFEST_AFTER.json`
- `.tasks/archives/CLIENT-ACTIVE-ROOT-001/client/`

## 根目录 client 审计结论

根目录 `client/` 判定为安装后的 Windows payload 与运行数据形态，不是当前源码目录。当前源码入口是 `mc-design-nx/client/`，工具说明资产入口是 `mc-design-nx/assets/source/tools/`。

归档前磁盘现存结构摘要：

| 项 | 数值 |
| --- | ---: |
| 现存文件数 | 537 |
| 现存总大小 bytes | 272255409 |
| 现存 git tracked 文件数 | 220 |
| 现存 git untracked 文件数 | 26 |
| git status 中 `client/` 相关条目 | 908 |
| 旧 beya/tjuae/governance/.runtime 痕迹文件数 | 248 |
| 大文件数（>=100MB） | 2 |
| 敏感指示项 | 2 |

顶层结构包括 `client/`、`configure/`、`installer/`、`nx-plugin/`、`McDesignClient.exe`、`package-manifest.json`、`install-state.json`、`README_INSTALL.txt`、`start-client.bat`、`smoke-test.bat`、`uninstall.bat`。其中 `client/client/beya-server/`、`client/client/python/Lib/site-packages/beya/`、`client/client/data/.runtime/`、`client/client/data/governance/` 等属于旧运行痕迹或安装 payload。

引用检查结论：

- 当前源码、测试、asset 和 package 逻辑的活跃入口均位于 `mc-design-nx/...`。
- package 脚本中的 `payload/client/...` 和 `client/python/...` 是安装包内部相对路径，不是仓库根 `client/` 源码入口。
- 根 `.gitignore` 旧规则只忽略了 `client/client/data/`；已改为忽略根 `/client/`。
- 历史回执、安装包证据和 `runtime_architecture_render.md` 中存在根 `client/client/data` 运行记录引用，属于历史/证据文本，不作为当前源码入口。

## Manifest 路径

- 归档前：`.tasks/receipts/CLIENT-ACTIVE-ROOT-001/ROOT_CLIENT_MANIFEST_BEFORE.json`
- 归档后：`.tasks/receipts/CLIENT-ACTIVE-ROOT-001/ROOT_CLIENT_MANIFEST_AFTER.json`

## 归档/移除清单

归档目标：

```text
.tasks/archives/CLIENT-ACTIVE-ROOT-001/client
```

归档结果：

| 项 | 数值 |
| --- | ---: |
| 归档文件数 | 536 |
| 归档总大小 bytes | 272255160 |
| 已从根 `client/` 移除的现存非敏感文件数 | 536 |
| 根 `client/` 剩余文件数 | 1 |
| 非敏感现存文件归档校验 | 通过 |

关键归档内容包括 Windows launcher、嵌入式 Python runtime、`mc_design_client.pyz`、资源包、NX plugin 二进制、installer helper、旧 `beya-server` 和旧 beya Python 包。归档后根 `client/` 下不再保留 `McDesignClient.exe`、`client/app`、`client/python`、`client/resources`、`nx-plugin`、`installer` 等 payload 内容。

## 未移除项目及原因

| 路径 | 原因 | 状态 |
| --- | --- | --- |
| `client/configure/mc-design-client.config` | 检测到 `tc_key_configured=true`；按敏感信息边界不复制进任务 archive、不删除、不输出值 | `manual_confirmation_required` |

该文件是唯一剩余的根 `client/` 文件。未输出 Teamcenter 密码、`tc_key`、API key、cookie、token 或任何明文凭据。

## 工具执行映射

映射文件：

```text
mc-design-nx/client/resources/tool_execution_map.json
```

摘要：

| Tool group | Provider | Registry source | Executor | Tjuae namespace | Connection |
| --- | --- | --- | --- | --- | --- |
| `tool.local_file` | `LocalFileToolProvider` | `ClientToolCatalog -> LocalFileToolProvider.specs()` | `POST /api/runtime/tools/execute` | `tool.local_file` | no |
| `tool.dfmea` | `DfmeaToolProvider` | `ClientToolCatalog -> DfmeaToolProvider.specs()` | `POST /api/runtime/tools/execute` | `tool.dfmea` | no |
| `tool.nx` | `NxToolProvider` | `ClientToolCatalog -> NxToolProvider.specs() -> nx_tools_manifest.json` | `POST /api/runtime/tools/execute` | `tool.nx` | yes |

Connector tools 不在本地 Python catalog 中；启动时从 K8s `/api/mc-design/connectors/tools` 动态获取，并由本地 executor 转发到 K8s `/api/mc-design/connectors/execute`。

## TOOL.md 到执行面校验结果

- `tool.local_file/TOOL.md` 声明的 `local_file_exists`、`local_file_read_bytes`、`local_file_write_bytes`、`local_file_copy` 均存在于 `ClientToolCatalog.manifest()`，并可通过 `local`、`local_file`、`tool.local_file` namespace 到达 provider。
- `tool.dfmea/TOOL.md` 声明的 `dfmea_template_list`、`dfmea_template_inspect`、`dfmea_fill_template`、`dfmea_calculate_risk`、`dfmea_validate_workbook` 均存在于 `ClientToolCatalog.manifest()`，并可通过 `dfmea`、`tool.dfmea` namespace 到达 provider。
- `tool.nx/TOOL.md` 正向引用的 `nx_open_tcpart`、`nx_open_part` 存在于 `ClientToolCatalog.manifest()`；NX provider 工具统一 `tool_group=tool.nx`，通过 `nx`、`tool.nx` namespace 执行。
- NX 未连接时标准化返回 `NX_PLUGIN_UNAVAILABLE`；禁用自动出图/Sheet 级图纸工具不进入 manifest，调用返回 `NX_DRAWING_TOOL_DISABLED`。
- `query_ipm_list`、`query_ecr_list`、`connect_qpp`、`mysql_query`、`tc_call` 等 connector 工具不在本地 catalog 中，归属动态 connector。

## 新增/更新测试清单

更新 `mc-design-nx/client/tests/test_tool_registry.py`，新增/增强覆盖：

- `test_tool_execution_map_matches_local_catalog`
- `test_tool_md_declared_tools_resolve_to_catalog_or_dynamic_connector`
- `test_http_tool_namespace_aliases_route_to_expected_provider`
- `test_tjuae_http_executor_namespace_matches_tool_group`
- `test_root_client_payload_is_not_active_source_entrypoint`
- 现有 NX 禁用图纸工具、connector 不进本地 catalog、local_file/dfmea 注册测试继续覆盖。

## 测试命令和结果

执行命令：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx\client\tests\test_tool_registry.py mc-design-nx\client\tests\test_asset_store.py mc-design-nx\client\tests\test_agent_loop_assets.py mc-design-nx\client\tests\test_tjuae_runtime_adapter.py -q
```

结果：

```text
48 passed in 1.78s
```

未启动客户端、NX、Teamcenter 或 K8s；只执行本地静态/单元测试。

## 后续仍需处理事项

- `client/configure/mc-design-client.config` 因含本机 `tc_key` 配置仍留在根 `client/` 下；如需彻底移除根目录，需要项目负责人确认该本机配置的迁移、备份或删除策略。
- 根仓库 `client/` 下 tracked payload 文件已从工作树移除，后续提交时需要明确把这些删除作为目录收口提交处理；本任务未执行 git add/commit。
- 本任务未处理安装/卸载链路、E2E-SMOKE-003、K8s connector 实网验证、NX/Teamcenter 实机通路。

## 失败分类与敏感信息

无执行失败。未触发 `CLIENT_NOT_RUNNING`、`CLIENT_INSTALL_FAILED`、`K8S_NETWORK_BLOCKED`、`NX_PLUGIN_NOT_CONNECTED` 等失败分类。

敏感信息处理：未输出 Teamcenter 密码、`tc_key`、API key、cookie、token 或任何明文凭据；manifest 只包含路径、大小、hash 和 `tc_key_configured=true` 类结构化事实。
