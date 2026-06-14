# AGENT-TURN-TOOLS-001 Execution Receipt

## Task

Fix the local `agent-turn` tool-surface gap so local full-path testing can verify K8s connector tools before and during runtime turns.

## Changed Scope

- `mc-design-nx/client/src/mc_design_client/runtime/tjuae_runtime_adapter.py`
  - Added connector catalog status normalization for dynamic K8s connector tools.
  - Added per-adapter connector catalog cache and structured catalog error reporting.
  - Marked required connector tools as `alwaysLoad=true` in the Tjuae runtime plugin:
    - `query_ipm_list`
    - `query_ecr_list`
    - `connect_qpp`
    - `mysql_query`
    - `tc_call`
  - Added trace events for connector catalog loaded/catalog/failed diagnostics.
- `mc-design-nx/client/src/mc_design_client/runtime/host.py`
  - Added `connector_tool_status(command)` runtime host preflight method.
- `mc-design-nx/client/src/mc_design_client/app.py`
  - Added `connector_tool_status(...)`.
  - Included `connector_tools` in `/api/runtime/test/agent-turn` responses when runtime supports it.
- `mc-design-nx/client/src/mc_design_client/api/server.py`
  - Added local diagnostic endpoint:
    - `GET /api/runtime/connector-tools?conversation_id=...&agent_id=...&user_id=...`
- `mc-design-nx/client/src/mc_design_client/runtime/conversation_log.py`
  - Added connector tool visibility summary into per-conversation summary logs.
- Tests updated:
  - `mc-design-nx/client/tests/test_tjuae_runtime_adapter.py`
  - `mc-design-nx/client/tests/test_usage_issue_fixes.py`

## Result

- Business connector tools remain dynamic K8s connector tools and are not registered in the local `ClientToolCatalog`.
- Local `test_agent_turn` now returns auditable connector status:
  - visible tool names
  - required connector visibility
  - missing required tools
  - catalog error summary if K8s connector catalog is unavailable
- Required connector tools are strongly exposed to Tjuae plugin loading through `alwaysLoad=true`.
- Conversation logs now preserve connector visibility summary for later issue-to-log binding.

## Verification

- Syntax compile:
  - `python -m py_compile ...`
  - Passed.
- Targeted tests:
  - `pytest mc-design-nx/client/tests/test_tjuae_runtime_adapter.py::test_tjuae_adapter_syncs_connector_tools_from_k8s_schema mc-design-nx/client/tests/test_usage_issue_fixes.py::test_client_api_exposes_connector_tool_status_endpoint mc-design-nx/client/tests/test_usage_issue_fixes.py::test_client_app_local_agent_turn_collects_runtime_frames_and_events mc-design-nx/client/tests/test_usage_issue_fixes.py::test_client_app_local_agent_turn_writes_per_conversation_log -q`
  - `4 passed`
- Full client tests:
  - `pytest mc-design-nx/client/tests -q`
  - `207 passed`

## Follow-Up Notes

- For local full-path preflight, call:
  - `GET http://127.0.0.1:8765/api/runtime/connector-tools?conversation_id=<id>&agent_id=design_agent`
- For local full-path turn testing, call:
  - `POST http://127.0.0.1:8765/api/runtime/test/agent-turn`
- If `connector_tools.missing_required` is non-empty, do not start business validation for IPM/ECR/QPP/MySQL/TC until the connector catalog is visible.
- QPP network timeout remains an external connectivity issue and is not counted as a mc-design defect.
