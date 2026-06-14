# K8S-CONNECTOR-PRE-001 Execution Receipt

执行时间：2026-06-14 11:43:55 +08:00

工作目录：E:\A0_Projects\A1_Dynamics_Design_LM\mc-design

回执目录：E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\K8S-CONNECTOR-PRE-001

## 执行边界

- 只测已部署 K8s connector
- 未使用本地 test_agent_turn
- 未访问本地 MCP Stream Tool
- 未修改源码
- 未重启 K8s
- 未输出 Teamcenter 密码明文
- 测试身份：user_id=88000044，user_name=宋明芮。
- 外部业务列表正文在结构化结果中只记录长度、SHA-256 和必要状态，不展开业务明细。

## 目标

- BASE：http://ai-powerequip.yuchaiqas.com/mc-design/ai-server
- API KEY：f61***d0e
- 配置来源：只读 mc-design-nx\configure\mc-design-package.config

## 1. K8s Readiness

- HTTP 状态码：200
- ok：True
- version：0.18.8-agent-stream-0af28be-protocol
- connectors_enabled：True
- mysql：configured=True，code=OK，host=10.22.16.49，database=mc_design_data

判定：K8s 可访问，readiness 通过。

## 2. Connector Catalog

- HTTP 状态码：200
- ok：True
- 工具数量：12
- 工具名：mysql_query, connect_qpp, query_ecr_list, query_ipm_list, tc_call, teamcenter_copy_item_content_create, teamcenter_export_dataset_file, teamcenter_get_part_rev_children, teamcenter_get_part_rev_classification_attribute, teamcenter_get_parts_from_specified_folder, teamcenter_get_process_personnel_information, teamcenter_upload_file_function

| Tool | Namespace | Required | Schema 摘要 | Danger |
| --- | --- | --- | --- | ---: |
| mysql_query | connector.mysql | sql_statement | sql_statement:string; params:array | 2 |
| connect_qpp | connector.external | StartDate | worker:string; StartDate:string format=date | 0 |
| query_ecr_list | connector.external |  | item_id:string; change_topic:string; change_reasion_desc:string; ecr_process_state:array; createStartTime:string format=date; createEndTime:string format=date; creator:string; creator_dept:string; module:array; completeStartTime:string format=date; completeEndTime:string format=date; assignee:string; assignee_dept:string; product_platform:array; skip:string; take:string | 0 |
| query_ipm_list | connector.external |  | principle:string; principleName:string; projectName:string; projectCode:string; workTypeList:array; taskName:string; confirmStatusList:array default=["未提交","不通过","已确认"] enum=["未提交","不通过","已确认"]; startTime:string format=date; endTime:string format=date; page:integer default=1 min=1; pageSize:integer default=10 min=1 max=100 | 0 |
| tc_call | connector.teamcenter | path | path:string; payload:object; BEYA_TC_BASE_URL:string; user_id:string; owner_id:string; user_pass:string | 1 |
| teamcenter_copy_item_content_create | connector.teamcenter | item_id, item_rev_id, new_item_id, owner_id | item_id:string; item_rev_id:string; new_item_id:string; BEYA_TC_BASE_URL:string; user_id:string; owner_id:string; user_pass:string | 2 |
| teamcenter_export_dataset_file | connector.teamcenter | uid | uid:string; BEYA_TC_BASE_URL:string; user_id:string; owner_id:string; user_pass:string | 1 |
| teamcenter_get_part_rev_children | connector.teamcenter | item_id, item_rev_id | item_id:string; item_rev_id:string; BEYA_TC_BASE_URL:string; user_id:string; owner_id:string; user_pass:string | 1 |
| teamcenter_get_part_rev_classification_attribute | connector.teamcenter | item_id, item_rev_id | item_id:string; item_rev_id:string; BEYA_TC_BASE_URL:string; user_id:string; owner_id:string; user_pass:string | 1 |
| teamcenter_get_parts_from_specified_folder | connector.teamcenter | folder_name | owner_id:string; folder_name:string; BEYA_TC_BASE_URL:string; user_id:string; user_pass:string | 1 |
| teamcenter_get_process_personnel_information | connector.teamcenter | item_id, item_rev_id | item_id:string; item_rev_id:string; BEYA_TC_BASE_URL:string; user_id:string; owner_id:string; user_pass:string | 1 |
| teamcenter_upload_file_function | connector.teamcenter | item_id, item_rev_id, file_name, file_content, owner_id | item_id:string; item_rev_id:string; overwrite_or_not:string; file_name:string; file_content:string; BEYA_TC_BASE_URL:string; user_id:string; owner_id:string; user_pass:string | 2 |

Schema 判定：external_contract_consistent=True；必需工具缺失：

## 3. MySQL Smoke

- 工具：mysql_query
- 参数：select 1
- HTTP 状态码：200
- connector_ok：True
- result_sha256：7621d056f5917674d11d14b0511cd33b4121036eb20f5e9516143c2026741935
- 返回摘要：{   "query_result": [     {       "1": 1     }   ],   "sql_statement": "select 1" }

判定：mysql_query select 1 执行成功。

## 4. External 最小预检查

| Case | Tool | HTTP | connector_ok | nested_ok | message | elapsed_ms | result_sha256 |
| --- | --- | ---: | --- | --- | --- | ---: | --- |
| ipm_defaults_empty_arguments | query_ipm_list | 200 | True | True | 调用成功 | 240.7 | f44196c66ffdeda0d63aa0137dbd7a3e7b54970c60f8313508b215337e502389 |
| ipm_pagination_page1_pageSize1 | query_ipm_list | 200 | True | True | 调用成功 | 234.9 | 304e4fbccf9760084c37639f8c77a8514b2e7eccfeb6b5cf4dd8c3d618760204 |
| ecr_pagination_skip0_take1 | query_ecr_list | 200 | True | True | 调用成功 | 207 | 4fe2167eafc71aede0c349c73059d1569cccfbbddcaa2c9e0d1e98aa50363084 |
| qpp_startDate_today_worker_default | connect_qpp | 200 | True | False | 网络请求失败: HTTPConnectionPool(host='ycqpp.app.yuchai.com', port=80): Read timed out. (read timeout=10.0) | 19146.5 | 00360e1d7b6cbaaccaa5b630a7f4397db1e11e32b7081dade8c700564166a071 |

判定：query_ipm_list 默认参数、query_ipm_list 分页、query_ecr_list 分页均返回成功；connect_qpp 使用当天 StartDate 与默认 worker 时 QPP 上游访问超时，归类为外部接口不可用。

## 5. 默认值、状态枚举、分页、错误返回

- connect_qpp：StartDate 必填；worker 省略时使用 runtime user_name；catalog 无分页入参。
- query_ipm_list：confirmStatusList 默认且枚举为 未提交、不通过、已确认；page 默认 1；pageSize 默认 10、最大 100；默认参数实测成功。
- query_ecr_list：筛选项默认不传；skip/take 为字符串分页参数；skip=0,take=1 实测成功；ECR 状态枚举不在本地契约固化。
- 错误返回稳定：True

| Error Case | Stable | HTTP | Code | Message |
| --- | --- | ---: | --- | --- |
| missing_tool_name | True | 400 | TOOL_REQUIRED | tool is required |
| connect_qpp_missing_required_StartDate | True | 502 | BUSINESS_TOOL_ARGUMENT_ERROR | ExternalTools.connect_qpp() missing 1 required positional argument: 'StartDate' |
| unknown_tool | True | 502 | BUSINESS_TOOL_UNSUPPORTED | unsupported business tool: __unknown_connector_tool__ |

## 6. 5 次一致性测试

查询：mysql_query select 1

一致性结论：consistent=True；5 次 HTTP body 与 result 摘要完全一致。

| Run | HTTP | connector_ok | elapsed_ms | result_sha256 | result |
| ---: | ---: | --- | ---: | --- | --- |
| 1 | 200 | True | 108.2 | 7621d056f5917674d11d14b0511cd33b4121036eb20f5e9516143c2026741935 | {   "query_result": [     {       "1": 1     }   ],   "sql_statement": "select 1" } |
| 2 | 200 | True | 114.2 | 7621d056f5917674d11d14b0511cd33b4121036eb20f5e9516143c2026741935 | {   "query_result": [     {       "1": 1     }   ],   "sql_statement": "select 1" } |
| 3 | 200 | True | 106.7 | 7621d056f5917674d11d14b0511cd33b4121036eb20f5e9516143c2026741935 | {   "query_result": [     {       "1": 1     }   ],   "sql_statement": "select 1" } |
| 4 | 200 | True | 107.5 | 7621d056f5917674d11d14b0511cd33b4121036eb20f5e9516143c2026741935 | {   "query_result": [     {       "1": 1     }   ],   "sql_statement": "select 1" } |
| 5 | 200 | True | 104.9 | 7621d056f5917674d11d14b0511cd33b4121036eb20f5e9516143c2026741935 | {   "query_result": [     {       "1": 1     }   ],   "sql_statement": "select 1" } |

单独记录文件：E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\K8S-CONNECTOR-PRE-001\MYSQL_SELECT_1_CONSISTENCY_5_RUNS.json

## 7. 阻塞分类

| 分类 | 是否触发 |
| --- | --- |
| K8s 未部署 | False |
| VPN 未开 | False |
| 外部接口不可用 | True |
| schema 不一致 | False |
| 查询失败 | False |
| 返回不稳定 | False |

Active blockers：外部接口不可用

## 结论

connector 预回归完成，存在阻塞分类：外部接口不可用

本回执只输出 connector 预回归结果，不判定问题表最终通过。

结构化结果文件：E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\K8S-CONNECTOR-PRE-001\CONNECTOR_PRECHECK_RESULTS.json
