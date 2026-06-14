# RT-002 Execution Receipt

Date: 2026-06-14

## Scope

- `mc-design-ai-service`
- `mc-design-nx/package/windows/build/scripts`
- `mc-design-nx/client/README_TJUAE_RUNTIME.md`
- Related tests

## Changed Files

AI service:

- `mc-design-ai-service/.env.example`
- `mc-design-ai-service/beya.toml`
- `mc-design-ai-service/beya_mcp/server.py`
- `mc-design-ai-service/integrations/config.py`
- `mc-design-ai-service/integrations/external/client.py`
- `mc-design-ai-service/integrations/llm.py`
- `mc-design-ai-service/integrations/teamcenter/client.py`
- `mc-design-ai-service/tools/business/external/TOOL.md`
- `mc-design-ai-service/tools/business/external/external.py`
- `mc-design-ai-service/tools/business/mysql/TOOL.md`
- `mc-design-ai-service/tools/business/mysql/mysql.py`
- `mc-design-ai-service/tools/business/teamcenter/TOOL.md`
- `mc-design-ai-service/tools/business/teamcenter/teamcenter.py`
- `mc-design-ai-service/tests/test_runtime_bridge_architecture.py`
- `mc-design-ai-service/tests/test_runtime_replacement_policy.py`

NX Windows packaging / docs:

- `mc-design-nx/client/README_TJUAE_RUNTIME.md`
- `mc-design-nx/package/windows/README.md`
- `mc-design-nx/package/windows/build/scripts/build_installer.py`
- `mc-design-nx/package/windows/build/scripts/payload_builder.py`
- `mc-design-nx/client/tests/test_windows_payload_builder.py`
- `mc-design-nx/client/tests/test_windows_installer_build.py`

Note: the worktree already contains many RT-001/NX replacement changes outside this list. They were not normalized in RT-002.

## Beya Residual Audit And Strategy

Cleaned user-visible/business wording in AI-service connector exposure:

- Connector Markdown now describes dynamic `connector catalog` and local runtime plugin sync, not Beya static tool assets or Beya SDK.
- QPP/ECR/IPM, MySQL, and Teamcenter tool descriptions now use `Runtime`, `runtime config`, `connector`, or `Teamcenter` wording.
- Connector catalog test asserts `/api/mc-design/connectors/tools` contains no user-visible `Beya` branding and no `beya.toml` references.

Compatibility names intentionally retained:

- `beya_mcp` package name: retained for import path compatibility with `start_mcp.py`, existing tests, and current deployment entrypoints.
- `beya.toml`: retained as the runtime config file name for K8s/deployment compatibility. Comments now identify it as a legacy compatibility file name.
- `BeyaApiKeyMiddleware`: retained as an internal class name. It is not exposed through connector catalog or business docs.
- `BEYA_*` environment variables and `BEYA_TC_BASE_URL`: retained as deployment/config/schema compatibility keys.

This task did not perform destructive package/config/class renames. Renaming those items safely requires coordinated K8s config changes and full-path deployment validation.

## stream_agent_turn Test Entry

Added authenticated HTTP test endpoint:

- `POST /api/mc-design/test/agent-turn`
- Prefixed route: `POST /mc-design/ai-server/api/mc-design/test/agent-turn`
- Auth: same API-key handling as connector routes (`x-api-key`, Bearer token, or `api_key` query parameter).

Request body:

```json
{
  "user_id": "88000044",
  "agent_id": "design_agent",
  "conversation_id": "full-path-test",
  "query": "run a test turn",
  "files": [],
  "timeout": 900
}
```

The endpoint calls `RuntimeStreamHub.stream(...)`, which calls `RuntimeBridgeManager.stream_agent_turn(...)`, and returns collected `content`, `reasoning`, `tools`, `frames`, and final `result`. This is the intended later full-path test entry when local MCP Stream Tool cannot be called directly.

## Real Tjuae Packaging Validation

Added support for a real tjuae dist root shaped like:

- `F:\Documents\tjuae\dist\tjuae-sdk\python\wheelhouse\tjuae_sdk-*.whl`
- `F:\Documents\tjuae\dist\tjuae-sdk\server\win-x64\tjuae-server.exe`

Dry-run command:

```powershell
mc-design-nx\package\windows\build-installer.bat --dry-run --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk
```

Build command:

```powershell
mc-design-nx\package\windows\build-installer.bat --bundle-version tjuae-real-001 --tjuae-sdk-dist F:\Documents\tjuae\dist\tjuae-sdk
```

Verified dry-run result:

```json
{
  "ok": true,
  "sdk_python_source": "F:\\Documents\\tjuae\\dist\\tjuae-sdk\\python\\wheelhouse\\tjuae_sdk-0.1.0-py3-none-any.whl",
  "server_executable": "F:\\Documents\\tjuae\\dist\\tjuae-sdk\\server\\win-x64\\tjuae-server.exe",
  "failures": []
}
```

## Manual Full-Path Prerequisites

Documented in `mc-design-nx/client/README_TJUAE_RUNTIME.md`, `mc-design-nx/package/windows/README.md`, and generated `README_INSTALL.txt` template:

- After `mc-design-ai-service` is updated, the project owner must manually update K8s.
- If K8s route fails and the issue is identified as intranet/network not started, the project owner must manually start VPN.
- If NX is not running, the project owner must manually start NX.
- In the current test environment `nx_open_tcpart` is unavailable, so the project owner must manually open the target model in NX before tests that depend on an active work part.

## Test Commands And Results

`python` was not available on PATH in this shell, so tests used Codex bundled Python:

`C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`

Commands:

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest -q
```

Result in `mc-design-ai-service`: `72 passed, 3 warnings`.

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pytest client/tests/test_windows_payload_builder.py client/tests/test_windows_installer_build.py -q
```

Result in `mc-design-nx`: `19 passed`.

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' package\windows\build\scripts\build_installer.py --dry-run --tjuae-sdk-dist 'F:\Documents\tjuae\dist\tjuae-sdk'
```

Result: `ok=true`, wheel and server executable resolved from the real dist root.

```powershell
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m py_compile beya_mcp\server.py integrations\config.py integrations\llm.py tools\business\external\external.py tools\business\teamcenter\teamcenter.py tools\business\mysql\mysql.py
& 'C:\Users\ASUS\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m py_compile package\windows\build\scripts\payload_builder.py package\windows\build\scripts\build_installer.py
```

Result: both compile commands passed.

## Unhandled Risks

- No broad rename of `beya_mcp`, `beya.toml`, `BeyaApiKeyMiddleware`, or `BEYA_*` keys was done. Reason: these are compatibility surfaces and require coordinated K8s/deployment changes plus full-path validation.
- K8s was not updated from this task. Reason: the requirement explicitly assigns K8s update to the project owner.
- VPN/NX/model full-path validation was not executed. Reason: it depends on manual VPN startup, manual NX startup, and manual target model opening because `nx_open_tcpart` is unavailable in the current test environment.
- No NX plugin tool implementation or part-design skill rules were changed.
