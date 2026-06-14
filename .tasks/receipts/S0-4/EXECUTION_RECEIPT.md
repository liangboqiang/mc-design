# S0-4 EXECUTION RECEIPT

执行日期：2026-06-14

工作目录：`E:\A0_Projects\A1_Dynamics_Design_LM\mc-design`

## 改动文件清单

- `mc-design-nx/assets/source/skills/part-design/SKILL.md`
  - 新增模型生命周期状态机。
  - 增加未完成三维模型修改前禁止自行打开二维图纸的总控门禁。
  - 增加 TC 上传清单必须包含三维模型、二维图纸、报告的规则。
- `mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md`
  - 增加 TC/NX 生命周期、打开顺序、上传顺序和缺失上传物确认规则。
  - 明确缺少任一上传物时，确认前不得调用 TC 上传、复制或覆盖工具。
- `mc-design-nx/assets/source/skills/nx-operation/SKILL.md`
  - 增加 NX 生命周期前置条件。
  - 明确有副作用的 NX 工具范围和二维图打开门禁。
  - 调整推荐流程为先参数修改/校验/保存更新，再进入二维图和报告。
- `mc-design-nx/assets/source/skills/nx-parameter/SKILL.md`
  - 增加参数写入前置条件、模型确认门禁和参数校验后置要求。
  - 明确参数修改结果不能替代二维图纸或报告上传物。
- `mc-design-nx/assets/source/tools/tool.nx/TOOL.md`
  - 增加工具层生命周期前置条件、主模型/二维图纸/报告顺序和 TC 上传清单规则。
- `mc-design-nx/client/tests/test_design_skill_contract.py`
  - 新增生命周期状态机、二维图门禁、上传物清单、模型确认门禁相关契约测试。
- `.tasks/receipts/S0-4/EXECUTION_RECEIPT.md`
  - 本执行回执。

## 生命周期状态机

统一状态机：

`任务确认 -> 模板/模型确认 -> 三维模型打开/修改 -> 参数校验 -> 保存/更新 -> 二维图/报告`

阶段规则：

1. `任务确认`：确认设计对象、目标版本、用户意图、输入参数来源和预期交付物。只允许查询、梳理方案和追问。
2. `模板/模型确认`：从 TC 模板库或用户指定来源取得候选，列出主模型候选信息并等待用户确认。
3. `三维模型打开/修改`：只打开确认后的主模型；读取 WorkPart 和真实驱动参数；参数映射和修改方案确认后才允许写入。
4. `参数校验`：写入后重新读取参数或模型状态，核对目标值、失败项和风险。
5. `保存/更新`：参数校验通过后才能保存或更新主模型；无可用保存/更新工具时必须说明需要人工处理。
6. `二维图/报告`：三维模型修改并保存/更新完成后，才允许打开或生成二维图纸；报告最后生成。

## 工具调用前置条件

- 读取状态、读取参数、列候选、查询 TC 对象等无副作用动作可以用于确认阶段。
- 有副作用的 NX/TC 工具包括：打开主模型或二维图、写参数、自动出图、保存/更新、TC 上传、复制和覆盖。
- 找错模型、模型未确认、参数映射未确认时，禁止调用有副作用的 NX/TC 工具。
- `nx_open_tcpart` / `nx_open_part`：必须已确认主模型对象或路径。
- `nx_update_param` / `nx_batch_update_params` / `nx_create_param`：必须已确认 WorkPart、真实 NX 表达式名、参数映射、目标值和用户确认。
- `nx_open_tc_drawing` / `nx_open_drawing_sheet` / `nx_run_auto_drawing`：必须已完成三维模型修改、参数校验和保存/更新；未完成三维模型修改前，不允许自行打开二维图纸。
- `teamcenter_upload_file_function` / `teamcenter_copy_item_content_create`：必须确认目标 item/version、文件名、覆盖策略、`user_id`、`owner_id`、权限和完整上传清单。

## TC 上传物清单规则

- 打开和上传顺序均为：`主模型 -> 二维图纸 -> 报告`。
- TC 上传清单必须包含：三维模型、二维图纸、报告。
- 清单需列出每个上传物的来源、文件名、目标 item/version、覆盖策略、负责人和证据。
- 三维模型、二维图纸或报告任一缺失时，必须说明缺失原因、影响和建议处理方式，并等待用户确认。
- 缺失项未经用户确认前，不得调用 TC 上传、复制或覆盖工具。
- 报告不能替代三维模型或二维图纸；参数修改结果只能作为三维模型产物证据之一。

## 新增/更新测试

更新文件：`mc-design-nx/client/tests/test_design_skill_contract.py`

新增测试：

- `test_model_lifecycle_state_machine_contracts`
  - 覆盖统一状态机和主模型/二维图纸/报告顺序。
- `test_drawing_is_blocked_until_3d_model_update_is_complete`
  - 覆盖未完成三维模型修改前禁止自行打开二维图纸。
- `test_tc_upload_manifest_requires_model_drawing_and_report`
  - 覆盖 TC 上传清单必须包含三维模型、二维图纸、报告，以及缺失项确认门禁。
- `test_model_confirmation_blocks_side_effect_nx_tc_tools`
  - 覆盖找错模型、模型未确认、参数映射未确认时禁止有副作用 NX/TC 工具。

## 测试命令和结果

标准 pytest 命令：

```powershell
python -m pytest mc-design-nx/client/tests/test_design_skill_contract.py -q
```

结果：失败。当前 PATH 中没有 `python`。

仓库打包 Python 执行 pytest：

```powershell
& 'client/client/python/python.exe' -m pytest mc-design-nx/client/tests/test_design_skill_contract.py -q
```

结果：失败。该解释器没有安装 `pytest`，报错 `No module named pytest`。

语法编译检查：

```powershell
& 'client/client/python/python.exe' -m py_compile mc-design-nx/client/tests/test_design_skill_contract.py
```

结果：通过。

临时 runner 执行 `test_design_skill_contract.py` 全部 16 个测试函数：

```powershell
@'
import importlib.util
import inspect
import tempfile
from pathlib import Path
path = Path('mc-design-nx/client/tests/test_design_skill_contract.py').resolve()
spec = importlib.util.spec_from_file_location('test_design_skill_contract', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
passed = 0
with tempfile.TemporaryDirectory() as td:
    tmp_path = Path(td)
    for name, func in sorted(vars(mod).items()):
        if not name.startswith('test_') or not callable(func):
            continue
        sig = inspect.signature(func)
        kwargs = {}
        if 'tmp_path' in sig.parameters:
            case_tmp = tmp_path / name
            case_tmp.mkdir()
            kwargs['tmp_path'] = case_tmp
        func(**kwargs)
        passed += 1
        print(f'PASS {name}')
print(f'PASSED {passed} tests')
'@ | & 'client/client/python/python.exe' -
```

结果：通过，输出 `PASSED 16 tests`。

## 无法实测项及原因

- 未执行真实 `nx_open_tcpart`。当前测试环境该能力可能不可用；涉及真实 TC 主模型打开时，需要项目负责人在 NX/TC 中手动打开模型或提供可用环境。
- 未执行真实二维图打开、自动出图、保存/更新和 TC 上传。原因是这些动作有副作用，且需要真实 NX 会话、Teamcenter 对象、权限、上传物和用户确认。
- 未实测报告内容生成。该任务限制不做报告内容生成优化，本次只加固生命周期和上传清单规则。
- 未修改本地文件工具、未修改 tjuae 代码、未做 beya/tjuae 替换。
