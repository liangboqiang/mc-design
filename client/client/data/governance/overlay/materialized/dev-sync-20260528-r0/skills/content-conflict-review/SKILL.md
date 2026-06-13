---
name: content-conflict-review
description: 内容冲突审查技能
capabilities:
  - tool.asset.read
  - tool.workspace.read
---

# 内容冲突审查技能

@id: [[skill.content_conflict_review]]
@type: skill
@scope: platform
@status: active
@version: 0.1.0

@uses.skill:
- [[skill.asset_soft_extraction]]
- [[skill.asset_graph_analysis]]

@uses.tool:
- [[tool.asset]]
- [[tool.workspace]]
- [[tool.workspace]]

@governed.by: [[agent.governance_agent]]

## 适用场景

用于发现不同资产之间的参数、单位、范围、流程、模板槽位、外部字段、版本语义和业务适用边界冲突。

## 目标

让治理结果不仅指出协议和规则问题，还能说明资产内容之间真实矛盾、影响范围和可执行处理建议。

## 工作方法

1. 收集待审查资产及其关联资产、风险快照和图谱邻居。
2. 读取原文件证据，而不是只读取摘要或 sidecar。
3. 对比参数定义、单位/范围、流程顺序、模板槽位、工具输出字段、外部系统字段映射和适用场景。
4. 形成冲突项：类型、涉及资产、证据位置、影响、严重度、置信度。
5. 给出处理建议：修复、合并、保留差异、补充适用边界、创建白名单或阻断发布。

## 输出要求

- 每个冲突必须包含涉及资产、证据定位、影响范围和建议。
- 输出必须区分“确定冲突”“疑似冲突”“缺证据风险”。
- 阻断建议必须说明命中的强规则或高置信度业务风险。

## 禁止事项

- 禁止只基于命名相似就判断冲突。
- 禁止在未读取原文件证据时给出最终治理结论。
- 禁止删除风险；只能解决、关闭、白名单压制或重新评估。
