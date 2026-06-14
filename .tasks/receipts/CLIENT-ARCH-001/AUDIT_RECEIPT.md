# CLIENT-ARCH-001 审计回执

更新时间：2026-06-14

## 任务边界

本次只做 `mc-design-client` 架构边界静态审计和说明，未修改源码，未删除文件，未运行安装/卸载，未启动或重启客户端，未处理 `E2E-SMOKE-002` 卸载失败整改，未做 beya/tjuae 替换实现，未修改外部 `tjuae` 项目。

## 输入依据

- `.tasks/TEST_EXECUTION_RULES.md`
- `.tasks/project_health_2026-06-14.md`
- `.tasks/project_supervision_plan.md`
- `mc-design-nx/client/README_TJUAE_RUNTIME.md`
- `mc-design-nx/client/src/mc_design_client/`
- `mc-design-nx/client/resources/`
- `mc-design-nx/client/data/`
- `mc-design-nx/client/cc_haha_agent_runtime_migration_pack/`
- `mc-design-nx/assets/source/`
- `mc-design-nx/package/windows/`

## 执行步骤和命令

只执行静态读取、目录枚举、引用搜索和只读解码：

- `Get-Content -Raw .tasks/TEST_EXECUTION_RULES.md`
- `Get-Content -Raw mc-design-nx/client/README_TJUAE_RUNTIME.md`
- `Get-Content -Raw .tasks/project_health_2026-06-14.md`
- `Get-Content -Raw .tasks/project_supervision_plan.md`
- `rg -n --hidden --no-ignore "agent_assets|asset_views|asset_view|\\.tjuae|install_or_update|tools\\.list|chat\\.stream|chat\\.respond|cc_haha|mcdpkg|assets/source" ...`
- `git -C mc-design-nx ls-files ...`
- `git -C mc-design-nx check-ignore -v ...`
- PowerShell 只读解码 `client/resources/agent_assets.mcdpkg` 元数据。

未执行 pytest、构建、安装、卸载、启动、健康检查或任何外部服务调用。

## 结果摘要

1. `assets/source` 是当前智能体资产源。`client/resources/agent_assets.mcdpkg` 是从该 source 导出的只读打包快照。`client/data/asset_views/runtime-agentloop` 是运行期从 `.mcdpkg` 解包生成的投影/cache。`client/data/workspace/.tjuae/skills` 是再从投影同步给 Tjuae 原生 workspace skill discovery 的托管副本。
2. `tjuae-sdk` 不直接读取 `agent_assets.mcdpkg`，也不直接读取 `asset_views`。这些由 mc-design 本地代码读取和投影。`tjuae-sdk` 通过 `sessions.create(work_dir=...)`、`plugins.install_or_update(...)`、`plugins.list(cwd=...)`、`tools.list(..., cwd=...)`、`chat.stream(...)` 和 `chat.respond(...)` 使用 mc-design 准备好的 workspace、inline plugin 工具和 Tjuae server 会话。
3. `tjuae-server`/Tjuae workspace 会间接看见 `client/data/workspace/.tjuae/skills`，因为 mc-design 把当前投影 skill 同步到 `workspace/.tjuae/skills`，并以 `client/data/workspace` 作为 work_dir/cwd 创建 session 和检查 plugin/tool 可见性。
4. `cc_haha_agent_runtime_migration_pack` 当前只有 `reference/cc-haha/bin/claude-haha` 一个 Bash/Bun CLI 包装脚本。源码、测试、打包脚本和任务资料均未引用它；该文件还被 `mc-design-nx/.gitignore` 的 `**/bin/` 命中。它应视为外部 runtime 迁移参考残留，不应继续放在 `mc-design-nx/client` 的运行边界内。
5. `mc-design-nx/client` 的异常点在于源码区旁边混入了生成资源、运行数据、Tjuae workspace、历史 Beya/governance asset projection、迁移参考材料。`package/windows/output` 还保留了约 3.65 GB 生成安装包/解包产物。它们多数被 git ignore，但仍会干扰人工审计和边界判断。

## 必答结论

### 1. asset 和 asset_view 谁是源、谁是投影、tjuae-sdk 到底看谁

- 源：`mc-design-nx/assets/source/`。
- 打包快照：`mc-design-nx/client/resources/agent_assets.mcdpkg`，由 `package/windows/build/scripts/export_assets.py` 从 source 生成，当前资源包只读解码为 `bundle_version=test-local-dev`、1 个 agent、13 个 skill、3 个 tool、14 个 static 文件。
- 运行投影：`mc-design-nx/client/data/asset_views/runtime-agentloop/`，由 `AssetStore.project_to(...)` 从 `.mcdpkg` 生成。
- Tjuae skill workspace：`mc-design-nx/client/data/workspace/.tjuae/skills/`，由 `RuntimeEnvironment._sync_project_skills()` 从 `runtime-agentloop/skills` 复制。
- `tjuae-sdk` 实际不解析 mc-design 的 `.mcdpkg` 或 `asset_views`；它通过 mc-design adapter 调用 Tjuae server 的 session/plugin/tool/chat API，并由 Tjuae server 在 workspace 中发现 `.tjuae/skills`。

### 2. cc_haha 是什么，是否应留在 mc-design-client

`cc_haha_agent_runtime_migration_pack` 是外部 cc-haha/Claude Code 风格运行时迁移参考残留，不是当前 mc-design-client 运行时、测试或打包依赖。建议不留在 `mc-design-nx/client`。如仍需保留证据，应归档到 `references/legacy-runtime/cc-haha/` 或任务回执引用区；否则后续单独任务删除。

### 3. mc-design-client 怪在哪里

主要问题不是功能代码错误，而是目录边界混杂：

- `client/src` 是源码，但同级有 `client/resources` 生成资源。
- `client/data` 是本机运行数据，却位于源码工程内。
- `client/data/asset_views` 同时存在当前投影 `runtime-agentloop` 和旧投影 `runtime-live`、`test-local-dev`，旧投影仍含 `beya`、`nx-auto-drawing`、governance tool 等历史内容。
- `client/data/workspace` 同时有 `.tjuae` 当前 workspace 和 `.beya` 历史 workspace。
- `client/cc_haha_agent_runtime_migration_pack` 是迁移参考，却放在 client 运行边界内。
- `package/windows/output` 是生成安装包/解包输出，体量大且不应作为源码审计对象。

### 4. 是否建议优化，如何分阶段优化

建议优化，但分阶段做，且不要把本审计描述为整改已经落地：

1. 阶段 0：冻结边界文档和清理候选，不删除运行数据。
2. 阶段 1：把 `assets/source -> agent_assets.mcdpkg -> asset_views/runtime-agentloop -> workspace/.tjuae/skills` 的生成链路固化为文档和自检。
3. 阶段 2：将开发态运行数据从源码树迁到明确的本机 runtime data 根，或至少把 `client/data` 标成纯 runtime cache。
4. 阶段 3：归档或删除旧 `runtime-live`、`test-local-dev`、`.beya`、governance overlay、`cc_haha` 迁移参考。
5. 阶段 4：建立安装包输出保留策略，清理 `package/windows/output` 历史解包目录。

## 证据文件

- `.tasks/receipts/CLIENT-ARCH-001/CLIENT_ARCHITECTURE_MAP.md`
- `.tasks/receipts/CLIENT-ARCH-001/CLIENT_CLEANUP_CANDIDATES.csv`
- `.tasks/receipts/CLIENT-ARCH-001/CLIENT_RESTRUCTURE_PROPOSAL.md`

## 失败分类

无执行失败。本任务为静态审计，不涉及客户端运行、安装、卸载、K8s、NX 或外部系统。适用分类：`TEST_PRECONDITION_NOT_MET` 不适用，`CLIENT_NOT_RUNNING` 不适用。

## 人工前置条件

本次审计不需要人工启动客户端、K8s、VPN、NX 或 TC/NX 模型。

## 敏感信息

本次未读取本机 Teamcenter 密码文件，未输出 `tc_key`、API key、cookie、token 或任何明文凭据。文档中仅引用规则要求，不包含敏感值。
