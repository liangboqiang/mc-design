# REG-EVIDENCE-001 执行回执

任务编号：REG-EVIDENCE-001
生成日期：2026-06-14
工作目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design`
回执目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\REG-EVIDENCE-001`

## 执行边界

- 本任务只整理回归证据模板和问题卡片。
- 未执行真实业务回归，未调用真实 IPM/QPP/ECMS/TC/NX 链路，未修改源码，未安装/卸载/重启客户端。
- 已解决/已完成/已优化条目仅标为待复测，不依据原表状态关闭。

## 输入依据

- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\references\开发资料\零件设计智能体试用问题跟踪表.xlsx`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\S0-6\ACCEPTANCE_MATRIX.csv`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\REG-001-PREP\AUDIT_RECEIPT.md`
- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\project_health_2026-06-14.md`

## 整理结果

| 项 | 数量 |
|---|---:|
| S0-6 矩阵总记录 | 59 |
| P0 数量 | 35 |
| P1 数量 | 13 |
| P2 数量 | 11 |
| P0 证据卡片整理条数 | 35 |
| 无法整理项 | 0 |

## 输出文件

- `REGRESSION_EVIDENCE_CARDS.md`
- `REGRESSION_EVIDENCE_CARDS.csv`
- `EXECUTION_RECEIPT.md`

## 无法整理项及原因

- 无。35 条 P0 均已按来源行匹配到 S0-6 矩阵与 REG-001-PREP P0 清单。

## 校验说明

- 原 Excel 已通过 xlsx XML 读取确认包含主表 `零件设计智能体试用问题跟踪表`，维度为 `AS150`；因样式层兼容问题，数据整理以 S0-6 矩阵和 REG-001-PREP 结构化清单为准。
- 输出卡片逐条包含：问题编号/来源行、问题摘要、预期行为、测试入口、前置条件、需要人工介入项、通过标准、失败分类、证据清单。
- 输出卡片逐条区分：可本地 agent-turn 测、可 K8s connector 测、需 NX 启动、需 TC/NX 手动打开模型、需外部接口。
- 输出不把准备状态改写为结果性关闭结论。
