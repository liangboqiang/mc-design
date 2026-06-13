---
name: camshaft-design
description: 凸轮轴设计技能
capabilities:
  - tool.workspace.read
  - tool.mysql.query
  - tool.nx.health
  - tool.nx.query
  - tool.nx.parameter
  - tool.nx.modeling
  - tool.nx.visual
---

# 凸轮轴设计技能

## 适用场景

用于凸轮轴设计需求归口。具体 NX 建模动作应继续加载 `nx-camshaft-modeling`，参数调整加载 `nx-parameter`，截图加载 `nx-visual`。

## 推荐流程

1. 确认用户是新建凸轮轴、修改现有凸轮轴，还是只查询参数/生成报告。
2. 模板和参数标准使用 `mysql_query` 查询。
3. 新建或重建几何转入 `nx-camshaft-modeling`。
4. 现有模型参数调整转入 `nx-parameter`。
5. 输出总结时说明轴体、型线、凸轮、阵列、装配、轴颈、端部凸台等步骤的完成情况。
