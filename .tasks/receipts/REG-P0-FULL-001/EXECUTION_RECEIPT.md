# REG-P0-FULL-001 Execution Receipt

## 任务边界

- 工作目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design`
- 回执目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\.tasks\receipts\REG-P0-FULL-001`
- 测试身份：`user_id=88000044`，`user_name=宋明芮`
- 敏感信息：未在回执中输出 Teamcenter 密码或 API key；仅记录 `tc_key_configured=false`、`api_key_configured=true/false`。
- 执行性质：按 `.tasks/TEST_EXECUTION_RULES.md` 做当前运行时真实链路回归；环境前置不满足的 TC/NX 项按阻塞分类，不伪造通过。

## 结果总览

- 矩阵覆盖：35 行问题表记录。
- 通过：11；失败：17；阻塞：7。
- 关键结论：K8s connector 只读链路可用；本地 agent-turn 基础入口可用，但 IPM connector 未集成进本地 agent-turn 的可用工具面；参数四分支均为业务断言失败；报告本地预览/保存/读取通过，截图导出失败；DFMEA 工具链在补齐模板资产后通过；TC/NX 生命周期因 `tc_key_configured=false` 和未完成三维修改被阻塞。

## 安装包门禁结果

- 使用安装包：`mc-design-nx/package/windows/output/installers/McDesignClientSetup-PKG-002.zip`。
- 卸载：执行旧客户端卸载，`uninstall-result.json` 记录 exit_code=1；日志中 helper 已输出 `Uninstall succeeded.`，随后批处理报 `The batch file cannot be found.`，因此门禁分类保留为 `CLIENT_UNINSTALL_FAILED`，但未阻止继续做 K8s 直连与本地可用性检查。
- 安装：`install-result.json` 记录 exit_code=0，安装 PKG-002 成功。
- 启动：启动后 `/health` 与 `/api/status` 均 HTTP 200；bundle_version=PKG-002；bridge connected；本地工具列表 29 项；`nx_open_tcpart_present=true`，禁用自动出图工具未出现在 manifest。
- 配置审计：`safe-config-audit.json` 显示 user_id/user_name 匹配，`tc_key_configured=false`。

证据：`uninstall-output.log`、`uninstall-result.json`、`install-output.log`、`install-result.json`、`client-start-result.json`、`postinstall-health-status.json`、`safe-config-audit.json`。

## 本地 agent-turn 结果

- 健康检查入口：`POST http://127.0.0.1:8765/api/runtime/test/agent-turn`。
- Smoke：`local-agent-turn-smoke.json` 返回 HTTP 200，`entrypoint=local_runtime_host`，`status=success`，未调用工具。
- IPM 任务选择两轮：`ipm_task_selection_context_summary.json` 显示第一轮返回 `needs_input`，表示未找到 IPM 查询工具或接口定义；第二轮返回 failed，未识别用户选择的 `2024K15HSKQG6023T00022`。这说明本地 agent-turn 与 K8s connector 的任务查询/选择链路没有闭环。

## K8s connector 结果

- `/health`、`/readiness`：HTTP 200，connector enabled，MySQL configured。
- 旧 K8s `agent-turn` 路径：`/api/mc-design/test/agent-turn` 与带前缀旧路径均返回 404，符合规则。
- `mysql_query select 1`：ok。
- `query_ipm_list`：默认 page1/page2 ok；3 个月到期窗口使用当前日期 `2026-06-14` 到 `2026-09-14`；连续 5 次查询业务字段一致。
- IPM 状态：authenticated 调用显式传 `confirmStatusList=[未提交,不通过,已确认]` 返回 ok，未传数字枚举。
- `query_ecr_list`：分页返回 ok。
- `connect_qpp`：HTTP wrapper 200，但嵌套结果为上游 QPP read timeout；按任务规则归类为 `QPP_EXTERNAL_UNAVAILABLE`，不是 mc-design 代码失败。

证据：`k8s_direct_summary.json`、`k8s_ipm_default_page1.json`、`k8s_ipm_page2.json`、`k8s_ipm_three_month_due.json`、`ipm_consistency_analysis.json`、`k8s_ipm_status_list_authenticated.json`、`k8s_ecr_page.json`、`k8s_qpp_current.json`。

## 参数四分支结果

- 连杆参数齐全：transport 成功，但中心距计算与参考逻辑不一致，且仍判定缺失大量参数，未达到“参数完备可建模”。
- 活塞销参数不全：transport 成功，但缺参列表泛化，未按参考逻辑精准定位，未形成二次校验闭环。
- 止推片仅边界参数：transport 成功，但使用通用经验范围，未按止推片 3.0 表输出确定值。
- 连杆混合参数：transport 成功，但换算公式/数值不符合参考逻辑，参数 ID 为未验证自定义 ID。
- 共同问题：四分支均未调用 NX 参数读取工具确认真实表达式 ID，也没有执行确认后的建模闭环；判定为 `BUSINESS_ASSERTION_FAILED`。

证据：`parameter_four_branch_summary.json` 与 4 个 `local_agent_turn_PARAM-BRANCH-*.json`。

## 报告、截图、DFMEA 结果

- 设计报告：prepare/validate-preview/save-final 成功；生成 preview/final docx，并复制到本回执目录。
- 本地下载/读取：`local_file_read_bytes` 对最终报告读取成功，sha256=`f68e53895ce25b7d2d3b1675335d24f850a53128c5e706f260b63864de626c9b`。
- TC 上传门禁：save-final 输出 `tc_upload_allowed=false` 与 `needs_tc_upload_confirmation`，未把 TC 上传当成本地完成。
- 截图：Front/Right/Left 三次 `nx_create_image` 均失败，未生成图片；因此截图链路不通过，也没有伪造“全是正视图”的证据。
- DFMEA：安装后客户端 DFMEA 允许模板目录初始为空；从工作区受控参考模板复制 3 个 xlsx 到允许目录后，`template_list/inspect/fill/validate/local_file_read_bytes` 第二版全部通过，输出 `K09LN-1004201-01A-DFMEA01-reg-p0-full-001-v2.xlsx`。

证据：`design_report_validate_preview_v2.json`、`design_report_save_final.json`、`local_tool_local_file_read_report_final_full.json`、`nx_screenshot_captures.json`、`dfmea_template_bootstrap.json`、`dfmea_v2_standard_keys_summary.json`。

## TC/NX 生命周期结果

- NX 当前连接可用，Work Part 为本地模板路径：`F:/Documents/beya/runtime/mc-design/dependencies/templates/K08_1004201_21_conrod_body.prt`。
- Manifest 中 `nx_open_tcpart` 存在，禁用自动出图工具未出现。
- 因 `tc_key_configured=false`、未能打开 TC 绑定模型/图纸、未完成三维修改，本轮未执行 TC 上传、TC 历史报告下载、二维图纸打开或生命周期闭环。
- 生命周期相关项按 `TEST_PRECONDITION_NOT_MET`、`SIDE_EFFECT_NOT_ALLOWED` 或 `BUSINESS_ASSERTION_FAILED` 记录，未伪造通过。

证据：`local_tool_nx_get_work_part_info.json`、`nx_tool_manifest_check.json`、`safe-config-audit.json`。

## 仍未开展/无法开展清单

- TC 历史设计说明书下载与复制：`tc_key_configured=false`，需项目负责人配置 TC 凭据/网络并提供目标 item/revision。
- TC 上传清单验证：缺少 TC 前置，无法验证图号、三维模型、二维图纸、报告/DFMEA 的真实上传清单。
- 二维图纸生命周期：未完成三维修改前按规则不得打开二维图纸；自动出图工具保持禁用。
- NX 截图证据：当前 `nx_create_image` 导出失败，需项目负责人确认 NX 图像导出权限/会话状态。
- 本地 agent-turn IPM/ECMS/QPP 集成：K8s connector 可用，但本地 agent-turn 未暴露 IPM 查询工具，需修复工具同步/agent 工具注册后复测任务选择和多轮上下文。
- QPP：外部上游当前不可用，继续归类为 `QPP_EXTERNAL_UNAVAILABLE`。

## 输出文件

- `P0_REGRESSION_MATRIX.csv`
- `EXECUTION_RECEIPT.md`
- `matrix_status_summary.json`

所有日志、请求响应摘要、导出 docx/xlsx 均存放在本回执目录。
