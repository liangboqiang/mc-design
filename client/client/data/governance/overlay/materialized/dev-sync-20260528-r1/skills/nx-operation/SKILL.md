---
name: nx-operation
description: NX 操作总控技能
capabilities:
  - tool.nx.health
  - tool.nx.query
  - tool.nx.parameter
  - tool.nx.modeling
  - tool.nx.visual
---

# NX 操作总控技能

## 适用场景

用于连接 NX、打开模板零件、确认当前 WorkPart、读取参数/视图/图纸页，并决定是否继续加载参数修改、凸轮轴建模、自动出图、优化或视图截图技能。

## 连接规则

NX 连接由 Beya 统一 WebSocket bridge 管理。Agent 只调用 `nx_*` 工具，不向用户索要 user_id、IP、端口、base_path 或 API Key。

## 设计路线

除凸轮轴专用建模工具外，零部件设计优先采用模板参数化建模：打开既有模板或 TC 零件，读取驱动参数，形成修改方案，用户确认后更新表达式并由 NX 刷新模型。不要在普通零部件任务中凭空创成模型特征。

## 推荐流程

1. 调用 `nx_health_check` 判断用户侧 NX bridge 是否连接。
2. 调用 `nx_get_work_part_info` 确认当前操作对象。
3. 需要打开文件时，先确认模板路径或文件路径，再调用 `nx_open_part` 或 `nx_open_tc_part`。
4. 需要参数修改时，转入 `nx-parameter`。
5. 需要凸轮轴建模时，转入 `nx-camshaft-modeling`；这是允许使用专用构造工具的例外。
6. 需要优化时，转入 `nx-optimization`，先生成方案并让用户确认。
7. 需要二维工程图时，转入 `nx-auto-drawing`。
8. 需要截图或视图展示时，转入 `nx-visual`。

## 权限边界

读取状态、参数列表、图纸页列表可以直接执行；创建零件、修改参数、建模、出图、删除图纸页、导出文件等副作用动作必须先确认目标对象和变更范围。
