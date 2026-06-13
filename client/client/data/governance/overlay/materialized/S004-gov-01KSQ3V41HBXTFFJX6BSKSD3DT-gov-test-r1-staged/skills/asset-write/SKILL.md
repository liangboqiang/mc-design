---
name: asset-write
description: 热治理资产安全写入 Skill
capabilities:
  - tool.governance.write
  - tool.governance.asset
---

# asset-write

@id: [[skill.asset_write]]
@type: skill
@scope: platform
@status: active
@version: 0.4.0

@uses.tool:
- [[tool.governance]]

## 写入原则

资产写入只允许在 `/gov` 治理模式内进行，并且只能通过 `gov_asset_stage`、`gov_schema_policy_stage`、`gov_tool_adapter_stage`、`gov_asset_diff`、`gov_asset_validate` 等治理工具完成。默认写入用户端 hot overlay，不直接写 `assets/source`、`asset_views`、安装目录或 runtime 历史。

`stage` 只生成待确认变更，不代表生效。最终应用必须由用户输入 `/confirm`，该命令由控制面执行，不进入 LLM。

## 标准流程

1. 读取原文件、原始工具 schema 或当前 adapter，确认治理目标和引用关系。
2. 生成完整候选内容，调用 stage 工具暂存。
3. 调用 diff 工具展示 unified diff。
4. 调用 validate 工具检查元数据、路径、引用和安全边界。
5. 向用户说明影响范围、风险、验证结果、热生效范围和回退方式。
6. 明确提示：输入 `/confirm` 后生效。

## 禁止事项

- 禁止物理删除资产；删除语义统一改成 `@status: disabled`、disable marker 或归档。
- 禁止写 `asset_views`、runtime 历史、安装目录和系统目录。
- 禁止修改云端工具 handler、真实平台 schema、NX 插件或 runtime 核心代码。
- 禁止在没有 diff 和 validate 的情况下请求确认。
- 禁止把一次性会话内容沉淀成长效规则。
