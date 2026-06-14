# CLIENT-ARCH-001 目标结构建议

更新时间：2026-06-14

## 目标原则

1. 源码、打包只读资源、本机运行数据、投影/cache、workspace、安装包输出、legacy/reference 必须分区。
2. `assets/source` 永远是资产源码，不让 `asset_views` 或 `.tjuae/skills` 反向成为源。
3. `client/resources/*.mcdpkg` 是生成快照，不手工编辑。
4. `client/data` 是本机运行态，不能进入源代码审计或提交边界。
5. 外部 runtime 迁移参考不放在 active client 目录内。

## 推荐目标结构

```text
mc-design-nx/
  assets/
    source/                         # 资产源码区，git 跟踪
  client/
    src/mc_design_client/            # Python 客户端源码
    tests/                           # 客户端测试
    resources/                       # 开发态生成资源，只读快照，可重建，不作为源码
      agent_assets.mcdpkg
      mc-design-package.mcdpkg
      nx_tools_manifest.json
  .local/                            # 建议新增，本机开发运行数据根，git ignored
    client-data/
      asset_views/
        runtime-agentloop/
      workspace/
        .tjuae/skills/
      runtime/
      logs/
  package/windows/
    build/                           # 打包脚本源码
    runtime/                         # 离线构建依赖，明确保留
    output/                          # 安装包输出区，git ignored，有保留策略
references/
  legacy-runtime/
    cc-haha/                         # 迁移参考归档区，不在 client active boundary
```

如暂不迁移运行数据根，也应在文档中明确当前临时分区：

- `mc-design-nx/client/data/asset_views/runtime-agentloop` 是可重建 cache。
- `mc-design-nx/client/data/workspace/.tjuae/skills` 是可重建 managed skill projection。
- `mc-design-nx/client/data/workspace/.beya`、`asset_views/runtime-live`、`asset_views/test-local-dev` 是 legacy evidence/cache。

## 分阶段优化建议

### 阶段 0：审计冻结

任务编号建议：`CLIENT-ARCH-FOLLOW-001`

目标：

- 保留本次四份审计产物。
- 不删除任何文件。
- 由负责人确认哪些历史运行数据需要留作证据。

验收：

- 所有后续任务都引用本审计。
- 不把本审计描述为整改已经落地。

### 阶段 1：资产生成链路自检

任务编号建议：`CLIENT-ASSET-001`

目标：

- 文档化并脚本化 `assets/source -> agent_assets.mcdpkg -> asset_views/runtime-agentloop -> workspace/.tjuae/skills`。
- 增加只读自检：source skill/tool 数量、resource package 数量、runtime projection marker、managed skills manifest 必须一致。
- 明确 `client/resources` 是生成物，缺失时如何重建。

不做：

- 不修改业务 skill 内容。
- 不改变 tjuae 外部项目。

### 阶段 2：运行数据根治理

任务编号建议：`CLIENT-DATA-001`

目标：

- 将开发态 `client/data` 迁到明确本机数据根，例如 `mc-design-nx/.local/client-data` 或环境变量指定路径。
- 安装态继续使用 `%LOCALAPPDATA%\McDesign\client\data`。
- 保留兼容策略，避免破坏现有本机调试。

验收：

- 源码树不再默认混入 `.tjuae`、`.beya`、asset projection、session state。
- `load_config()` 或启动入口能清楚报告 data root。

### 阶段 3：托管 skills 与用户 skills 分离

任务编号建议：`CLIENT-TJUAE-001`

目标：

- `workspace/.tjuae/skills` 下区分 mc-design managed skills 和用户自定义 skills。
- cleanup 只删除带 `.mc-design-managed` 的目录。
- 明确 Tjuae server 通过 work_dir/cwd 间接读取 `.tjuae/skills`，而不是 SDK 直接读 `.mcdpkg`。

验收：

- 删除 managed skill 后可从 `agent_assets.mcdpkg` 自动重建。
- 用户非托管 skill 不被覆盖或删除。

### 阶段 4：legacy/reference 归档

任务编号建议：`CLIENT-LEGACY-001`

目标：

- 将 `client/cc_haha_agent_runtime_migration_pack` 移入 `references/legacy-runtime/cc-haha/`，或在确认无证据价值后删除。
- 对 `client/data/workspace/.beya`、旧 `asset_views/runtime-live`、旧 `asset_views/test-local-dev` 做归档清理任务。

验收：

- `mc-design-nx/client` 不再包含外部 runtime 迁移参考。
- 当前运行资产审计不会再扫到旧 `beya`、`nx-auto-drawing`、governance tool 作为当前内容。

### 阶段 5：打包输出保留策略

任务编号建议：`CLIENT-PKG-OUTPUT-001`

目标：

- 为 `package/windows/output` 建立保留策略。
- 只保留当前 E2E/回执需要的 installer zip、manifest 和日志。
- 清理 `.work`、extract-*、旧 logs 时先归档证据索引。

验收：

- `package/windows/output` 不再长期堆积多 GB 历史解包目录。
- 回执引用的证据仍可定位。

## 风险提示

- 不要在客户端运行时删除 `client/data/asset_views/runtime-agentloop` 或 `workspace/.tjuae/skills`。
- 不要把 `runtime-live`、`test-local-dev` 的旧内容当作当前运行事实。
- 不要把 `client/resources/*.mcdpkg` 当源码修改；它们应由生成脚本产出。
- 不要把 `cc_haha` 参考包留在 active client 目录，否则会继续造成“运行时边界是否仍依赖外部 CLI”的误判。
