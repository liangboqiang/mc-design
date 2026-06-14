# ASSET-001R Audit Receipt

日期：2026-06-14

## 结论

- 审计结论：runtime.md 资产打包路径当前已完整。
- 归属判断：独立 ASSET-001 修复，不归入 RT-001。理由是改动面在资产源文件命名、资产导出脚本、资产包哈希/投影和资产打包测试；未改运行时 adapter，未改 NX plugin，未处理 AI Service beya_mcp 命名。
- 补审发现：初始工作树中 `export_assets.py` 只枚举 `runtime.md`，缺少 `beya.md` 回退；本轮仅做最小补齐：`AGENT_ASSET_FILENAMES = ("runtime.md", "beya.md")`，并补充对应测试断言。
- 测试复跑还暴露 `export_assets.py` 未过滤既有禁用 skill，导致资产打包测试失败；本轮在同一脚本内补齐 `DISABLED_SKILLS` 跳过逻辑，以满足现有资产打包测试约束。

## 检查文件清单

- `mc-design-nx/package/windows/build/scripts/export_assets.py`
  - 第 22 行：按 `runtime.md`、`beya.md` 顺序选择 agent 资产文件。
  - 第 23 行：声明资产打包阶段应跳过的禁用 skill。
  - 第 38-55 行：逐 agent 目录选择第一个存在的候选文件并打入 payload。
  - 第 60-63 行：跳过禁用 skill，避免重新打入已停用资产。
- `mc-design-nx/client/tests/test_asset_store.py`
  - 第 100-112 行：资产包加载测试要求 source 中存在 `agents/design_agent/runtime.md`。
  - 第 170-171 行：投影结果要求写出 `agents/design_agent/runtime.md`。
  - 第 211-225 行：验证 design_agent 使用 source `runtime.md` 内容并产生 `agents/design_agent/runtime.md` hash。
  - 第 228-259 行：验证 runtime 优先与 beya-only 回退，且回退后的 hash 仍归一到 `runtime.md` 路径。
- `mc-design-nx/assets/source/agents/design_agent/runtime.md`
  - 当前 source agent 入口，内容为 `agent.design_agent` 运行时定义。
- `mc-design-nx/assets/source/agents/INDEX.md`
  - 第 5 行：索引入口已指向 `agents/design_agent/runtime.md`。
- `mc-design-nx/assets/source/INDEX.md`
  - 第 19 行：说明 agent 可见身份来自 `agents/{agent_id}/runtime.md`。
- `mc-design-nx/client/src/mc_design_client/assets/package.py`
  - `build_hashes()` 对 agent 内容生成 `agents/{name}/runtime.md` hash。
- `mc-design-nx/client/src/mc_design_client/assets/store.py`
  - `AssetStore.project_to()` 将 agent payload 投影为 `agents/{agent_id}/runtime.md`。
- `mc-design-nx/package/windows/build/scripts/payload_builder.py`
  - 第 362-399 行：Windows payload 从 `mc-design-nx/assets/source` 重新导出 `.build/agent_assets.mcdpkg`，再复制到 payload 的 `client/resources/agent_assets.mcdpkg`。

## runtime.md 打包验证

解码 `mc-design-nx/client/resources/agent_assets.mcdpkg`：

- `bundle_version = test-local-dev`
- `agent_id = design_agent`
- `agents = ["design_agent"]`
- agent hash 列表：`["agents/design_agent/runtime.md"]`
- `agents/design_agent/beya.md` hash：不存在
- agent 文本与 `mc-design-nx/assets/source/agents/design_agent/runtime.md` 完全一致
- 禁用 skill 命中列表为空：`[]`
- agent 文本无 BOM
- agent 文本包含当前 runtime 中的 `[[tool.local_file]]`

手工临时源树验证：

- `design_agent` 同时存在 `runtime.md` 和 `beya.md` 时，payload 取 `runtime agent content`。
- `legacy_agent` 只有 `beya.md` 时，payload 取 `legacy-only content`。
- 两个 agent 的 hash 路径均归一为：
  - `agents/design_agent/runtime.md`
  - `agents/legacy_agent/runtime.md`

## beya.md 兼容回退说明

- 回退只存在于导出阶段的候选文件选择：`runtime.md` 优先，`beya.md` 作为 legacy fallback。
- payload 结构不保留 beya 文件名；`build_hashes()` 与 `AssetStore.project_to()` 都使用 `runtime.md` 路径。
- 因此旧 source tree 如果只有 `beya.md` 仍能打包，但输出包和投影统一呈现为 `runtime.md`。

## beya.md 未改名入口检查

命令：

```powershell
rg -n "beya\.md" mc-design-nx\assets\source mc-design-nx\package\windows\build\scripts mc-design-nx\client\tests\test_asset_store.py -S
```

结果：

- 仅命中 `mc-design-nx/package/windows/build/scripts/export_assets.py:22` 的兼容 fallback 候选。
- `mc-design-nx/assets/source` 下未发现仍需改名的 `beya.md` 资产入口。
- `mc-design-nx/assets/source/agents/design_agent/beya.md` 当前为 tracked deletion，`runtime.md` 为新增 source 文件；提交时需要一起纳入 ASSET-001 变更。

## 测试命令和结果

尝试：

```powershell
& 'client\client\python\python.exe' -m pytest mc-design-nx\client\tests\test_asset_store.py -q
```

结果：失败，原因是安装态 Python 无 `pytest` 模块。

实际执行：

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx\client\tests\test_asset_store.py -q
```

结果：`7 passed in 0.36s`

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest mc-design-nx\client\tests\test_windows_payload_builder.py -q
```

结果：`5 passed in 0.54s`

## 剩余风险

- 工作树中 `mc-design-nx/assets/source/agents/design_agent/runtime.md` 仍是未跟踪文件，`mc-design-nx/assets/source/agents/design_agent/beya.md` 是未提交删除；需要在最终提交中一起纳入。
- 安装态旧产物 `client/client/resources/agent_assets.mcdpkg` 仍是历史包：内部 agent hash 为 `agents/design_agent/beya.md`，且用当前 `package.py` 校验会出现 `asset package content hash mismatch`。Windows payload builder 会重新导出并覆盖该资源包，因此不阻塞源码侧和 payload 构建侧验证；但直接运行该旧安装态目录前应重新生成安装产物。
- 未审计也未处理 AI Service `beya_mcp` 命名，符合本任务限制。
