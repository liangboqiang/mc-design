---
name: asset-soft-extraction
description: 资产软规则抽取技能
capabilities:
  - tool.asset.read
  - tool.workspace.read
---

# 资产软规则抽取技能

@id: [[skill.asset_soft_extraction]]
@type: skill
@scope: platform
@status: active
@version: 0.1.0

@uses.tool:
- [[tool.asset]]
- [[tool.workspace]]
- [[tool.workspace]]

@governed.by: [[agent.governance_agent]]

## 适用场景

用于导入、审查、提升或重新治理原文件资产时，从资产内容中抽取可检索、可分析、可治理的主题、参数、流程、限制、适用场景和业务问题。

## 目标

以原文件为真相，生成可重建的派生抽取结果。抽取结果必须带证据定位、置信度和抽取 Skill 版本，不能替代原文件事实。

## 工作方法

1. 先定位原文件资产和空间上下文，确认读取权限。
2. 读取原文件或代表性片段，记录文件路径、行号、sheet、段落或对象定位。
3. 抽取基础属性：类型、来源、所有者、更新时间、格式、适用范围。
4. 抽取内容语义：主题、参数、流程、约束、业务问题、外部字段映射。
5. 对每个抽取项给出证据位置和置信度。
6. 将抽取结果作为派生视图交给 Asset Graph Analyzer 或治理 Agent 使用。

## 输出要求

- 输出包括 `source_path`、`source_hash`、`items`、`evidence_refs`、`confidence`。
- 不确定内容必须标注低置信度，不能当作硬规则阻断依据。
- 如果原文件无法读取，必须返回原因和需要人工处理的最小信息。

## 禁止事项

- 禁止为每一种业务文件写死不可迁移的抽取规则。
- 禁止把抽取摘要当作原文件真相。
- 禁止忽略证据位置直接输出结论。
