# PARAM-RULES-002 执行回执

## 任务边界

- 已先阅读 `.tasks/TEST_EXECUTION_RULES.md`。
- 本轮只做 skill 规则资源、脚本和脚本级测试整改。
- 未处理 QPP 网络问题；未修改 runtime adapter、launcher、NX plugin 或 NX C# 源码。

## 输入依据

- `references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表(1).xlsx`
- `references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表（活塞销）3.0.xlsx`
- `references/开发资料/零部件设计智能体功能开发测试案例逻辑表达式表（止推片）3.0.xlsx`
- `references/开发资料/零件设计智能体试用问题跟踪表.xlsx`
- `.tasks/receipts/REG-P0-FULL-001/parameter_four_branch_summary.json`
- `mc-design-nx/assets/source/skills/logic-expression-design/resources/minimal_test_cases.json`

说明：连杆中心距规则以 Excel `逻辑表达!F7=B7+B10-B8-B14-B9` 和 `minimal_test_cases.json` 的 212mm 为准；REG-P0 摘要中出现过 206.1mm/210mm 变体，后续如采纳需业务确认。

## 改动文件清单

- `mc-design-nx/assets/source/skills/logic-expression-design/resources/part_rules.json`
- `mc-design-nx/assets/source/skills/logic-expression-design/scripts/part_rule_calculator.py`
- `mc-design-nx/assets/source/skills/logic-expression-design/tests/test_part_rule_calculator.py`
- `mc-design-nx/assets/source/skills/logic-expression-design/SKILL.md`
- `mc-design-nx/assets/source/skills/parameter-mapping/SKILL.md`
- `.tasks/receipts/PARAM-RULES-002/EXECUTION_RECEIPT.md`

## 规则资源结构

`part_rules.json` 结构：

- `runtime_contract`：声明固定脚本、标准库/JSON 依赖、禁止 Excel/openpyxl/COM 运行时依赖、必含输出字段。
- `sources`：记录 Excel、minimal cases、REG-P0 四分支摘要来源。
- `branches`：四分支 ID 与中文标签。
- `parts.<part>.required_input_ids`：规则计算所需输入。
- `parts.<part>.parameters`：边界参数、发动机参数、经验/关联参数定义、单位、示例和追问。
- `parts.<part>.design_outputs`：设计输出、公式、来源单元格、候选 NX 参数 ID。
- `parts.<part>.required_modeling_questions`：进入 NX 建模前仍需确认的结构/材料/公差/工艺项。

## 脚本调用示例

```powershell
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\.runtime\python-3.8.10-embed-amd64\python.exe `
  mc-design-nx/assets/source/skills/logic-expression-design/scripts/part_rule_calculator.py `
  --input input.json `
  --output output.json
```

输入 JSON 示例：

```json
{
  "part_type": "conrod",
  "boundary_parameters": {
    "机体高度": 350,
    "压缩余隙": 0.7,
    "活塞压缩高度": 71.5,
    "缸盖垫厚度": 1.7,
    "连杆轴颈直径": 83,
    "活塞销直径": 47,
    "连杆瓦厚度": 2.5,
    "曲柄半径": 67.5,
    "连杆小头衬套厚度": 2
  },
  "engine_parameters": {
    "行程": 135,
    "缸径": 110
  }
}
```

## 四分支样例输出

参数齐全：

```json
{
  "ok": true,
  "part_type": "conrod",
  "input_branch": "complete_design_parameters",
  "missing_questions": [],
  "calculated_parameter_map": {
    "连杆中心距": 212,
    "连杆大头直径": 88,
    "连杆小头直径": 51,
    "连杆厚度": 20.31009601159
  },
  "nx_parameter_candidate_ids": [
    "K08_CON_L_CENTER",
    "K08_CON_D_BIG",
    "K08_CON_D_SMALL",
    "K08_CON_THICKNESS"
  ],
  "blocked_preconditions": [
    "required_modeling_specs_confirmed",
    "nx_workpart_confirmed",
    "nx_drive_parameters_read",
    "nx_parameter_mapping_confirmed",
    "write_scope_confirmed"
  ]
}
```

参数不全/无参数：

```json
{
  "ok": false,
  "part_type": "piston_pin",
  "input_branch": "incomplete_or_empty_parameters",
  "missing_questions": [
    "活塞销孔挡圈轴向间距",
    "连杆小头内径",
    "连杆衬套厚度"
  ],
  "calculated_parameter_map": {},
  "nx_parameter_candidate_ids": [
    "K08_PIN_L",
    "K08_PIN_D_OUT",
    "K08_PIN_D_IN"
  ]
}
```

仅边界参数：

```json
{
  "ok": true,
  "part_type": "thrust_washer",
  "input_branch": "boundary_only_parameters",
  "missing_questions": [],
  "calculated_parameter_map": {
    "止推片外径": 123,
    "止推片内径": 98,
    "止推片厚度（轴向）": 3.1,
    "止推片卡扣边距": 70,
    "止推片卡扣宽度": 10,
    "止推片斜接口水平交点边距": 56.5,
    "止推片斜接口斜度": "30°"
  },
  "blocked_preconditions": [
    "calculation_result_confirmed",
    "required_modeling_specs_confirmed",
    "nx_workpart_confirmed",
    "nx_drive_parameters_read",
    "nx_parameter_mapping_confirmed",
    "write_scope_confirmed"
  ]
}
```

混合参数：

```json
{
  "ok": true,
  "part_type": "conrod",
  "input_branch": "mixed_parameters",
  "missing_questions": [],
  "calculated_parameter_map": {
    "连杆中心距": 212,
    "连杆大头直径": 88,
    "连杆小头直径": 51,
    "连杆厚度": 20.31009601159
  },
  "blocked_preconditions": [
    "calculation_result_confirmed",
    "required_modeling_specs_confirmed",
    "nx_workpart_confirmed",
    "nx_drive_parameters_read",
    "nx_parameter_mapping_confirmed",
    "write_scope_confirmed"
  ]
}
```

## 测试命令和结果

```powershell
E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\.runtime\python-3.8.10-embed-amd64\python.exe `
  mc-design-nx/assets/source/skills/logic-expression-design/tests/test_part_rule_calculator.py
```

结果：

```text
Ran 5 tests in 0.971s
OK
```

补充验证：

```powershell
C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe `
  mc-design-nx/assets/source/skills/logic-expression-design/tests/test_part_rule_calculator.py
```

结果：

```text
Ran 5 tests in 0.704s
OK
```

另执行：

- `python -m json.tool mc-design-nx/assets/source/skills/logic-expression-design/resources/part_rules.json`：通过。
- `python -m py_compile mc-design-nx/assets/source/skills/logic-expression-design/scripts/part_rule_calculator.py mc-design-nx/assets/source/skills/logic-expression-design/tests/test_part_rule_calculator.py`：通过。

## 仍需 NX 实机确认的参数 ID 清单

这些 ID 均为候选，不能直接当作真实 NX expression name 写入：

- 连杆：`K08_CON_L_CENTER`、`K08_CON_D_BIG`、`K08_CON_D_SMALL`、`K08_CON_THICKNESS`
- 活塞销：`K08_PIN_L`、`K08_PIN_D_OUT`、`K08_PIN_D_IN`
- 止推片：`K08_THRUST_D_OUT`、`K08_THRUST_D_IN`、`K08_THRUST_T_AXIAL`、`K08_THRUST_TAB_OFFSET`、`K08_THRUST_TAB_WIDTH`、`K08_THRUST_BEVEL_X`、`K08_THRUST_BEVEL_ANGLE`

NX 阶段必须先读取 `nx_get_drive_params_list` 或 `nx_get_all_params_list`，再由用户确认候选到真实 `drive_parameter.nx_expression_name` 的映射和写入范围。

## 结果摘要

- 已新增固定规则计算脚本，不再依赖临时 SKILL.md 文字推导。
- 已把连杆、活塞销、止推片最小规则资源化为 JSON。
- 脚本支持参数齐全、参数不全/无参数、仅边界参数、混合参数四类分支。
- 输出包含任务要求的七个结构化字段。
- 已更新 skill 门禁：先跑结构化规则脚本，再进入 NX 参数确认；禁止根据中文参数名随机写 NX 表达式。

## 失败分类与人工前置

- 失败分类：无代码测试失败。
- 人工前置：需要 NX 实机打开目标 WorkPart，读取真实驱动参数并确认映射；未执行 NX 实机写入。
- 敏感信息：未读取、未输出 Teamcenter 密码、API key、cookie、token 或任何明文凭据。
