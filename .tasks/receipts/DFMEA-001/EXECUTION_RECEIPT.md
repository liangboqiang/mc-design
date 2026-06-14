# DFMEA-001 Execution Receipt

## Status

Completed.

## Changed Files

- `mc-design-nx/client/src/mc_design_client/tools/dfmea_provider.py`
- `mc-design-nx/client/src/mc_design_client/tools/registry.py`
- `mc-design-nx/client/src/mc_design_client/app.py`
- `mc-design-nx/client/tests/test_dfmea_tools.py`
- `mc-design-nx/client/tests/test_tool_registry.py`
- `mc-design-nx/client/tests/test_design_skill_contract.py`
- `mc-design-nx/assets/source/skills/dfmea-risk-review/SKILL.md`
- `mc-design-nx/assets/source/skills/design-report/SKILL.md`
- `mc-design-nx/assets/source/skills/teamcenter-flow/SKILL.md`
- `mc-design-nx/assets/source/tools/tool.dfmea/TOOL.md`
- `mc-design-nx/assets/source/tools/INDEX.md`
- `mc-design-nx/assets/source/agents/design_agent/runtime.md`

Original files under `references/开发资料/DFMEA模板/` were not modified.

## New Local Tool Group

Tool group: `tool.dfmea`

Provider: `mc_design_client.tools.dfmea_provider.DfmeaToolProvider`

Registry exposure:

- Registered by `ClientToolCatalog` with `requires_connection=false`.
- Routed by `ClientApp.invoke_tool()` through namespace `dfmea` or `tool.dfmea`.
- Does not depend on NX, NX plugin, Teamcenter, Excel COM, or external services.

Tools:

### `dfmea_template_list`

Purpose: list available DFMEA/FMEA `.xlsx` templates.

Input schema:

```json
{
  "type": "object",
  "properties": {
    "include_xls": {"type": "boolean", "default": false}
  },
  "additionalProperties": false
}
```

### `dfmea_template_inspect`

Purpose: inspect workbook sheets, dimensions, key areas, and fillable fields.

Input schema:

```json
{
  "type": "object",
  "properties": {
    "template_name": {"type": "string"},
    "template_path": {"type": "string"},
    "template_root": {"type": "string", "enum": ["runtime_workspace", "report_output", "allowed"], "default": "runtime_workspace"},
    "template_allowed_root_index": {"type": "integer", "minimum": 0, "default": 0}
  },
  "additionalProperties": false
}
```

### `dfmea_fill_template`

Purpose: copy a template and write fields, direct cells, risk rows, AP values, and metadata.

Input schema:

```json
{
  "type": "object",
  "properties": {
    "template_name": {"type": "string"},
    "template_path": {"type": "string"},
    "output_path": {"type": "string"},
    "output_root": {"type": "string", "enum": ["runtime_workspace", "report_output", "allowed"], "default": "runtime_workspace"},
    "allowed_root_index": {"type": "integer", "minimum": 0, "default": 0},
    "overwrite": {"type": "boolean", "default": false},
    "fields": {"type": "object"},
    "field_map": {"type": "object"},
    "cell_values": {},
    "risk_rows": {"type": "array", "items": {"type": "object"}},
    "dfmea_sheet": {"type": "string"},
    "start_row": {"type": "integer", "minimum": 1, "default": 13},
    "row_columns": {"type": "object"},
    "required_fields": {"type": "array", "items": {"type": "string"}},
    "confidence_threshold": {"type": "number", "default": 0.7}
  },
  "additionalProperties": false
}
```

### `dfmea_calculate_risk`

Purpose: calculate RPN and AP H/M/L from S/O/D.

Input schema:

```json
{
  "type": "object",
  "properties": {
    "risks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["severity", "occurrence", "detection"],
        "properties": {
          "severity": {"type": "integer", "minimum": 1, "maximum": 10},
          "occurrence": {"type": "integer", "minimum": 1, "maximum": 10},
          "detection": {"type": "integer", "minimum": 1, "maximum": 10},
          "confidence": {"type": "number", "minimum": 0, "maximum": 1}
        },
        "additionalProperties": true
      }
    },
    "confidence_threshold": {"type": "number", "default": 0.7}
  },
  "required": ["risks"],
  "additionalProperties": false
}
```

### `dfmea_validate_workbook`

Purpose: validate an output workbook, required fields, risk rows, and file metadata.

Input schema:

```json
{
  "type": "object",
  "properties": {
    "path": {"type": "string"},
    "root": {"type": "string", "enum": ["runtime_workspace", "report_output", "allowed"], "default": "runtime_workspace"},
    "allowed_root_index": {"type": "integer", "minimum": 0, "default": 0},
    "required_fields": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["path"],
  "additionalProperties": false
}
```

Unified output keys are present on every tool result:

- `ok`
- `output_path`
- `size_bytes`
- `sha256`
- `template_name`
- `filled_fields`
- `missing_fields`
- `risk_summary`
- `warnings`

## Skill Completion

`dfmea-risk-review` now covers:

- DFMEA/FMEA table generation and update flow.
- Template list/inspect/fill/validate workflow through `tool.dfmea`.
- AP/RPN calculation.
- P 图 and boundary diagram evidence references.
- Missing field questions before generation.
- Generation preview and user confirmation.
- TC upload gate before Teamcenter tools.
- Low-confidence risks marked as manual review required.

`design-report` boundary now states that DFMEA/FMEA xlsx generation and update belong to `tool.dfmea`; reports may only cite confirmed DFMEA output metadata and summaries.

`teamcenter-flow` boundary now states that Teamcenter tools only upload already confirmed DFMEA/FMEA output files, and upload requires user confirmation of target, version, dataset, overwrite policy, owner, file hash, and risk gate state.

NX-DRAW-001 amendment: DFMEA may cite already opened drawings, screenshots, report drafts, and other evidence, but it must not require or call NX automatic drawing tools. The only allowed NX drawing entrypoint is `nx_open_tcpart` for a user-confirmed bound NX drawing ItemRevision after 3D model modification, parameter verification, and save/update are complete.

## Template Field Mapping Strategy

- Preferred path: explicit `field_map`, e.g. `{"dfmea_number": "DFMEA!AL3"}`.
- Direct cell writes: `cell_values`, e.g. `{"DFMEA!AL3": "DFMEA-001"}`.
- Auto mapping: inspect labels such as `DFMEA编号`, `DFMEA开始日期`, `DFMEA修订日期`, `DFMEA版本号`; fill the adjacent cell to the right.
- Risk row mapping defaults to the current DFMEA template structure:
  - `severity` -> `S`
  - `occurrence` -> `Z`
  - `detection` -> `AC`
  - `ap` -> `AD`
  - standard DFMEA text columns such as function, failure effect, failure mode, failure cause, prevention control, detection control, action owner, status, and evidence map to the template columns around `A:AT`.
- `row_columns` can override the default row key -> Excel column mapping.
- `start_row` defaults to the inspected DFMEA data start row, normally 13.

## AP/RPN Calculation Strategy

- RPN = `S * O * D`.
- S/O/D must be integers from 1 to 10.
- AP uses the AP sheet H/M/L matrix:
  - `S=9-10`: H escalates quickly for O >= 4, or D >= 7 when O is 2-3.
  - `S=7-8`: follows the 7-8 AP block, with H for high occurrence/detection combinations.
  - `S=4-6`: mostly L/M, H only for high O and high D.
  - `S=2-3`: L except high O with D >= 5 -> M.
  - `S=1`: always L.
- `confidence < confidence_threshold` returns `manual_review_required=true` and a warning.
- AP is used for action priority; RPN is retained for sorting and regression comparison.

## Safety Boundary

- Read roots:
  - `references/开发资料/DFMEA模板`
  - runtime workspace
  - report output
  - configured allowed directories
- Write roots:
  - runtime workspace
  - report output
  - configured allowed directories
- Default output root: runtime workspace.
- Default overwrite behavior: false.
- Rejected:
  - path traversal
  - arbitrary absolute output paths
  - writing into template directory
  - unsupported formal `.xls` execution
  - original template mutation
- No NX plugin changes.
- No Teamcenter upload implementation.
- No Excel COM dependency.
- No new Python third-party dependency; `openpyxl` was not introduced, so `pyproject.toml` and offline wheel handling did not need dependency changes.

## Tests

Commands run:

```powershell
& "C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m pytest "mc-design-nx\client\tests\test_dfmea_tools.py" "mc-design-nx\client\tests\test_tool_registry.py" -q
```

Result:

```text
21 passed in 2.47s
```

```powershell
& "C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m pytest "mc-design-nx\client\tests\test_client_static.py" "mc-design-nx\client\tests\test_agent_loop_assets.py" "mc-design-nx\client\tests\test_windows_payload_builder.py" -q
```

Result:

```text
46 passed in 0.82s
```

```powershell
& "C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m pytest "mc-design-nx\client\tests" -q
```

Result:

```text
153 passed in 20.58s
```

Covered acceptance points:

- `tool.dfmea` registers without NX connection.
- Lists the 3 reference `.xlsx` templates.
- Inspects a template and detects DFMEA/AP sheets.
- Generates a new xlsx from a template.
- Refuses default overwrite.
- Rejects out-of-bounds output paths.
- Regresses S/O/D -> RPN/AP values.
- Skill text contains generation, confirmation, TC upload gate, and manual review requirements.

## Unable To Complete

- Real Teamcenter upload was not implemented by design; this task explicitly excludes TC upload implementation.
- `.xls` formal execution was not implemented; `.xlsx` is the formal runtime target and `.xls` remains migration/reference-only.
- No NX plugin changes were made, per task boundary.
