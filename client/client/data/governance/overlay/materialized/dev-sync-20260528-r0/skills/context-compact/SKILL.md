---
name: context-compact
description: 上下文压缩技能
capabilities:
  - tool.builtin.compact
---

# 上下文压缩技能

@id: [[skill.context_compact]]
@type: skill
@scope: platform
@status: active
@version: 0.1.0

@uses.skill:
- [[skill.asset_governance]]

@uses.tool:
- [[tool.asset]]
- [[tool.workspace]]
- [[tool.workspace]]

@governed.by: [[agent.governance_agent]]

## 适用场景

用于长会话中整理任务事实、文件变化、工具结果和后续行动，不替代正式输出。

## 目标

帮助 Agent 在保持工具原子性的前提下，正确选择资料、确认前置条件、调用必要工具，并把最终回复放入 `content`，把可见阶段性思考或阶段提示放入 `reasoning_content`。

## 工作方法

1. 先确认用户目标、当前会话状态和已上传/可访问文件。
2. 需要资料时，先使用当前可见的 workspace 读取工具定位相关资产，再读取原始文件。
3. 需要外部系统动作时，只调用与本技能相关的原子工具，不自行假设存在“大包装流程”。
4. 缺少关键输入时，通过 question 机制让系统在 `content` 中向用户提问。
5. 涉及写入、上传、导出、NX 修改、Teamcenter 变更等副作用动作时，必须通过权限确认。
6. 工具失败时，先读取错误信息和当前状态，再选择降级、重试、改问用户或输出可操作失败说明。

## 必查资料

- `AssetMap`：用于定位参数词典、模板、DFMEA、设计案例、PRT、DAT 和报告模板。

## 输出要求

- 最终结论、用户问题、权限确认必须进入 `content`。
- 分析阶段、工具进度、风险提示可进入 `reasoning_content`，但不要泄露隐藏推理链。
- 输出必须说明依据、已用文件、已调用工具和仍需用户确认的事项。

## 禁止事项

- 禁止绕过当前 workspace 和已加载 Skill 的可见边界直接猜测文件路径。
- 禁止在参数不确定时直接修改 NX。
- 禁止把用户未确认的假设当成事实。
- 禁止把本技能当成业务大包装工具；流程由 Skill 指导，动作由原子工具完成。
