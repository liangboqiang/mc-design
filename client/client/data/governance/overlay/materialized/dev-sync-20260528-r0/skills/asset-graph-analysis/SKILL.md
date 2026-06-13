---
name: asset-graph-analysis
description: 资产图谱分析技能
capabilities:
  - tool.asset.read
  - tool.workspace.read
---

# 资产图谱分析技能

@id: [[skill.asset_graph_analysis]]
@type: skill
@scope: platform
@status: active
@version: 0.1.0

@uses.skill:
- [[skill.asset_soft_extraction]]

@uses.tool:
- [[tool.asset]]
- [[tool.workspace]]
- [[tool.workspace]]

@governed.by: [[agent.governance_agent]]

## 适用场景

用于分析资产之间的引用、依赖、替代、重复、冲突、证据、派生和风险传播关系。

## 目标

把原文件资产和软规则抽取结果组织为可检索、可解释、可重建的资产图谱，辅助查询、治理和内容冲突发现。

## 工作方法

1. 从资产索引和软抽取结果中读取候选节点。
2. 构建资产节点、主题节点、参数节点、流程节点、业务问题节点、风险节点和外部字段节点。
3. 建立 `references / depends_on / duplicates / conflicts_with / replaces / evidences / derived_from` 等关系。
4. 计算孤岛、重复簇、冲突簇、风险传播路径和关键资产。
5. 将图谱分析结论返回给治理 Agent 或查询引擎。

## 输出要求

- 每个节点和边必须包含证据位置、置信度和来源资产。
- 图谱结论必须区分强规则事实与软规则推断。
- 对低置信度关系只建议复核，不直接阻断。

## 禁止事项

- 禁止让图谱关系覆盖原文件事实。
- 禁止在缺少证据时生成确定性冲突结论。
- 禁止把资产图谱作为不可删除的 L1 资产维护。
