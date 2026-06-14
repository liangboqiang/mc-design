# SKILL-CONSIST-001 Audit Receipt

审计日期：2026-06-14

审计类型：静态审计。未修改源码、skill、工具实现，未执行安装包流程；只读取指定范围并生成本回执。

## 审计范围

- `mc-design-nx/assets/source/skills/`
- `mc-design-nx/assets/source/tools/`
- `mc-design-nx/client/resources/`
- `mc-design-nx/client/src/mc_design_client/tools/`
- `mc-design-ai-service/tools/business/`
- `.tasks/skill_tool_asset_audit_2026-06-14.md`

## 结论摘要

未发现 P0 级运行资产缺失、禁用自动出图工具误暴露或静态 tool 资产缺包问题。`agent_assets.mcdpkg` 解包后包含 13 个 source skill 和 3 个 source tool，和 source 目录一致；`nx_tools_manifest.json` 当前包含 20 个 NX 工具，未包含 `nx-auto-drawing`、`nx_run_auto_drawing`、`nx_open_tc_drawing`、sheet 级打开/更新工具。

发现 1 个 P0、4 个 P1、2 个 P2 问题。最高风险仍是零件规则硬编码：连杆公式、规则和脚本逻辑仍在 skill 文本中，后续新增零件或规则变更需要改 skill，和 part-rules 方向冲突。

## 已验证通过项

- 运行资产包 `mc-design-nx/client/resources/agent_assets.mcdpkg` 解包后无用户可见 Beya 文案。
- `mc-design-nx/client/resources/nx_tools_manifest.json` 对 `beya`、`nx-auto-drawing`、`nx_run_auto_drawing`、`nx_open_tc_drawing`、`auto_drawing`、`open_drawing_sheet` 无命中。
- 自动出图相关词在 source skill/tool 中只出现在禁止或禁用语境；`registry.py` 中的旧自动出图工具名为防护性禁用名单。
- 静态工具组仍为 `tool.nx`、`tool.local_file`、`tool.dfmea`；业务 connector 由 K8s catalog 动态同步，方向符合 tjuae 边界。
- 未发现 skill 引用不存在的核心工具；但 capabilities 元数据存在不完整和抽象别名混写，见 P1-003。

## P0 问题

### SKILL-CONSIST-001-P0-001

文件路径：

- `mc-design-nx/assets/source/skills/part-design/SKILL.md:21`
- `mc-design-nx/assets/source/skills/part-design/SKILL.md:42`
- `mc-design-nx/assets/source/skills/logic-expression-design/SKILL.md:12`
- `mc-design-nx/assets/source/skills/conrod-design/SKILL.md:16`
- `mc-design-nx/assets/source/skills/conrod-design/SKILL.md:50`

问题描述：零件规则仍硬编码在 skill 中。`part-design` 和 `logic-expression-design` 明确要求连杆任务继续加载 `conrod-design`，`conrod-design` 内嵌连杆变量、公式、计算脚本模板和输出表。

影响：新增零件、调整公式或替换规则来源都需要修改 skill 正文，无法通过统一 part-rules 资源包治理；规则审计、版本追踪和测试扩展都会被 skill 文本耦合阻断。

建议后续任务编号：`SK-003`

## P1 问题

### SKILL-CONSIST-001-P1-001

文件路径：

- `mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md:19`
- `mc-design-ai-service/tools/business/teamcenter/teamcenter.py:11`
- `mc-design-ai-service/tools/business/teamcenter/teamcenter.py:226`
- `mc-design-ai-service/tools/business/teamcenter/teamcenter.py:246`
- `mc-design-ai-service/tools/business/teamcenter/teamcenter.py:252`

问题描述：Teamcenter skill 与 connector schema 的基础地址参数不一致。skill 说明使用 `TJUAE_TC_BASE_URL`，但 AI Service `tc_call` 函数、schema 和描述仍暴露 `BEYA_TC_BASE_URL`。

影响：按 skill 调用时参数名无法直接匹配当前 connector schema；同时 connector catalog 会向运行时暴露用户可见 Beya 旧命名，违反 tjuae 中性边界。

建议后续任务编号：`RT-NAME-001`

### SKILL-CONSIST-001-P1-002

文件路径：

- `mc-design-nx/assets/source/skills/design-report/SKILL.md:10`
- `mc-design-nx/assets/source/skills/design-report/SKILL.md:12`
- `mc-design-nx/assets/source/skills/design-report/scripts/design_report.py:34`
- `mc-design-nx/assets/source/skills/design-report/scripts/design_report.py:40`
- `mc-design-nx/assets/source/skills/design-report/scripts/design_report.py:1244`

问题描述：报告模板仍硬编码为连杆模板。skill 只允许 `<asset_root>/skills/design-report/templates/conrod_design_report_template.docx`，脚本默认模板与槽位快照也固定为 conrod 命名。

影响：报告生成能力无法自然泛化到活塞销、止推片或后续零件规则包；报告模板治理和零件规则治理会继续分裂。

建议后续任务编号：`REPORT-TEMPLATE-001`

### SKILL-CONSIST-001-P1-003

文件路径：

- `mc-design-nx/assets/source/skills/design-report/SKILL.md:3`
- `mc-design-nx/assets/source/skills/design-report/SKILL.md:54`
- `mc-design-nx/assets/source/skills/design-report/SKILL.md:58`
- `mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md:4`
- `mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md:30`
- `mc-design-nx/assets/source/skills/nx-parameter/SKILL.md:5`
- `mc-design-nx/assets/source/skills/nx-visual/SKILL.md:5`

问题描述：skill capabilities 与调用说明不一致且缺少统一机器语义。`design-report` 正文调用 Teamcenter、External、MySQL、DFMEA、NX 和 local_file 能力，但 frontmatter 无 capabilities；`teamcenter-flow` capabilities 只列 `tc_call` 和 `teamcenter_get_parts_from_specified_folder`，正文还要求 children、upload、copy 等工具；`tool.nx.health` 是抽象 capability，实际 manifest 工具名是 `nx_test`。

影响：如果 runtime 或治理测试依赖 capabilities 做预加载、授权或审计，会出现漏启工具、误判缺工具或把抽象能力当真实 tool 名的问题。

建议后续任务编号：`ASSET-GOV-001`

### SKILL-CONSIST-001-P1-004

文件路径：

- `mc-design-nx/assets/source/skills/logic-expression-design/SKILL.md:56`
- `mc-design-nx/assets/source/skills/logic-expression-design/resources/minimal_test_cases.json:5`
- `mc-design-nx/assets/source/skills/logic-expression-design/resources/minimal_test_cases.json:66`
- `mc-design-nx/assets/source/skills/logic-expression-design/resources/minimal_test_cases.json:104`

问题描述：`minimal_test_cases.json` 仍承担连杆、活塞销、止推片三类零件 fixture 职责，并引用开发资料 Excel 规则来源，和后续 part-rules 资源方向重叠。

影响：测试 fixture 与规则资源会形成双写；规则迁移后容易出现用例与真实规则包不同步。

建议后续任务编号：`SK-003-FIXTURE-001`

## P2 问题

### SKILL-CONSIST-001-P2-001

文件路径：

- `mc-design-nx/client/resources/nx_tools_manifest.json:520`
- `mc-design-nx/client/resources/nx_tools_manifest.json:523`
- `mc-design-nx/client/resources/nx_tools_manifest.json:527`
- `mc-design-nx/assets/source/skills/nx-operation/SKILL.md:36`
- `mc-design-nx/assets/source/skills/nx-operation/SKILL.md:57`

问题描述：NX 连接检查工具仍以 `nx_test`、`测试检查`、`TestTool` 暴露；skill 也要求调用 `nx_test` 判断连接。

影响：该工具实际承担 health/check 语义，但名称和描述像开发测试工具，容易被用户或治理规则误判为不应出现在生产资产中的测试能力。

建议后续任务编号：`NX-TOOL-NAMING-001`

### SKILL-CONSIST-001-P2-002

文件路径：

- `mc-design-nx/client/resources/agent_assets.mcdpkg:static/indexes/agents/INDEX.md`

问题描述：运行资产包内 agent 索引的“主要 Skill”列表少列 `nx-parameter`、`nx-visual`、`design-verification`、`dfmea-risk-review`，但同一运行包的 skills 列表和 `indexes/skills/INDEX.md` 包含这些 skill。

影响：不影响 skill 实际加载，但会误导后续人工审计或依赖索引的智能体路由判断。

建议后续任务编号：`ASSET-GOV-001`

## 静态证据摘要

- `agent_assets.mcdpkg` SHA256：`D5F22FBD8D2C63F60831E7FBE1F78784340777B63DAB3B55808FD58FB42B4221`
- `mc-design-package.mcdpkg` SHA256：`7A30D53840AF49950616C1BC6C466B1B0A4BC9AD2FE0741A739BBCD1F9108212`
- `nx_tools_manifest.json` SHA256：`6A7CAEFB6F2F25A49A89DF182CF5E888782EE0C80A39F4D4E6F8900AD39FF9A9`
- source/package skill 一致：13/13。
- source/package tool 一致：3/3。
- NX manifest 工具数：20。
