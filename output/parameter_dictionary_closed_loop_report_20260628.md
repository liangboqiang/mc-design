# 参数词典查询闭环测试报告

生成时间：2026-06-28 14:55（Asia/Shanghai）

## 结论

参数词典查询链路当前可以正常使用。两次真实会话测试均完成，智能体能够通过完整 MCP 工具名调用参数词典工具，未再调用裸 `mysql_query`，也未向参数词典工具传入 SQL、旧字段或硬编码参数。

## 环境

- 客户端：`http://127.0.0.1:8765`
- K8s AI 服务：已连接
- 当前用户：`88000044 / 宋明芮`
- NX WorkPart：`K08_1004201_21_conrod_body`
- 本地参数词典 MCP 工具：只注册 `parameter_dictionary_query`，未注册 `mysql_query`
- 证据 JSON：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\output\parameter_dictionary_closed_loop_evidence_20260628.json`

## 测试 1：三参数真实核对

- 会话 ID：`codex-param-dic-20260628-143636-01`
- 日志：`C:\Users\ASUS\AppData\Local\McDesign\client\logs\conversations\codex-param-dic-20260628-143636-01.jsonl`
- 结果：完成
- 参数词典调用次数：1
- 调用工具名：`mcp__plugin_mc-design_connector_mysql__parameter_dictionary_query`
- 旧 `mysql_query` 调用：0
- 裸 `parameter_dictionary_query` 调用：0
- SQL/旧字段命中：0
- 查询入参：`连杆大头孔径`、`连杆中心距`、`连杆厚度`
- 结果证据：日志中出现 `CR_B_DIA`、`CR_A_CEN`、`CR_B_T`、`CR_S_T` 等候选和 NX 驱动参数证据。

说明：该轮对“连杆厚度”触发了一次用户澄清，因为它在词典/NX 中确实可能对应大头厚度、小头厚度或腹板厚度。补答 `CR_B_T 连杆大头厚度` 后会话正常完成。

## 测试 2：短回归核对

- 会话 ID：`codex-param-dic-20260628-145248-02c`
- 日志：`C:\Users\ASUS\AppData\Local\McDesign\client\logs\conversations\codex-param-dic-20260628-145248-02c.jsonl`
- 结果：完成
- 参数词典调用次数：1
- 调用工具名：`mcp__plugin_mc-design_connector_mysql__parameter_dictionary_query`
- 旧 `mysql_query` 调用：0
- 裸 `parameter_dictionary_query` 调用：0
- SQL/旧字段命中：0
- Excel 公式读取调用：0
- 查询入参：`连杆大头孔径`、`连杆中心距`、`腹板厚度`
- 结果证据：日志中出现 `CR_B_DIA`、`CR_A_CEN`、`连杆大头直径`、`连杆中心距` 等候选证据。

## 中途发现并处理的问题

中间一次测试 `codex-param-dic-20260628-144150-02` 暴露出模型会按裸名 `parameter_dictionary_query` 调用，Tjuae 返回 `No such tool available`。这不是 MySQL 工具源码问题，而是 agent/skill 对“调用工具名”的表达不够硬。

已修复：

- `design-agent.md`：主智能体转交参数词典任务时必须写完整 MCP 工具名。
- `parameter-intelligence-agent.md`：必须调用 `mcp__plugin_mc-design_connector_mysql__parameter_dictionary_query`，不要调用裸名。
- `parameter-evidence-extraction/SKILL.md`：同步完整 MCP 工具名和入参规则。
- 同步到本机安装目录后重新测试，问题消失。

## 硬编码检查

已扫描 `parameter_dictionary_query/tool.py`，以下硬编码候选或业务映射均未命中：

- `ROOT_TERMS`
- `TERM_EXPANSIONS`
- `COMPONENT_SUFFIXES`
- `CR_B_DIA`
- `CR_A_CEN`
- `连杆大头直径`
- `连杆中心距`
- `孔径.*直径`
- `直径.*孔径`

当前工具仍以 MySQL 表 `nx_param_dic_cn_v2` 为唯一参数词典事实源，工具只做召回、排序和候选输出，不内置固定查询结果。

## 最终判断

目标 1：通过。真实会话测试显示功能已可正常使用，基本无阻塞问题。

目标 2：通过。源码中未发现硬编码候选词、硬编码结果或业务映射。

目标 3：通过。报告包含两次真实会话测试，并附本地日志和机器可读证据文件。
