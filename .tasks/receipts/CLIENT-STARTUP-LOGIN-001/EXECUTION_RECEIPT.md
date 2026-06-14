# CLIENT-STARTUP-LOGIN-001 Execution Receipt

## Input

- User log bundle: `F:\Desktop\logs.7z`
- Extracted for analysis under a temporary directory.

## Log Findings

- Installed package in the user log was `dev-20c81bb`.
- User config was accepted:
  - `user_id=yc90114959`
  - `user_name=蔡新朝`
  - `tc_key_configured=true`
- AI bridge connected successfully to cloud:
  - `AI bridge connected`
- Local tjuae-server printed that it was running:
  - `Tjuae API server running at http://127.0.0.1:3456`
- The mc-design client still marked tjuae-server as unhealthy/unready and stopped it because `/ready` and diagnostics did not satisfy the strict startup condition.
- Runtime turn then failed with:
  - `ConnectionRefusedError`
  - `WinError 10061`
- Launcher also reported:
  - local API wait timed out after about 20 seconds
  - repeated `ConnectionAbortedError` from health/status polling clients disconnecting before the server wrote the response

## Root Cause

The startup sequence had two coupled defects:

1. `LocalTjuaeServerManager.start()` treated tjuae-server `/ready` and `/api/status/diagnostics` as hard requirements. The bundled server could listen on `127.0.0.1:3456` but still fail those strict checks, so mc-design killed an otherwise-started local server.
2. The Windows launcher used heavy `/api/status` as its 800 ms local API readiness probe. That endpoint can include sub-checks such as NX/tjuae state, so it is not suitable as a lightweight startup probe.

## Fix

- `mc-design-nx/client/src/mc_design_client/tjuae_server.py`
  - Keep tjuae-server running when strict readiness is unavailable but the expected TCP listener is accepting connections.
  - Reduce health/readiness/diagnostics probe timeout to 0.2 seconds.
  - Add `accepting` to tjuae-server status.
  - Stop the server only when it never starts listening or exits early.
- `mc-design-nx/client-launcher/McDesign.ClientLauncher/ClientProcessManager.cs`
  - Use `/health` instead of `/api/status` for lightweight startup reachability probing.
- `mc-design-nx/client/src/mc_design_client/api/server.py`
  - Ignore expected disconnected-poll-client write failures (`WinError 10053/10054/109`, broken pipe/reset) instead of logging noisy tracebacks.
- Tests updated:
  - `mc-design-nx/client/tests/test_local_tjuae_server.py`
  - `mc-design-nx/client/tests/test_usage_issue_fixes.py`

## Verification

- Syntax compile:
  - `python -m py_compile mc-design-nx/client/src/mc_design_client/tjuae_server.py mc-design-nx/client/src/mc_design_client/api/server.py`
  - Passed.
- Targeted tests:
  - `pytest mc-design-nx/client/tests/test_local_tjuae_server.py mc-design-nx/client/tests/test_usage_issue_fixes.py::test_client_api_json_response_ignores_disconnected_poll_client mc-design-nx/client/tests/test_client_static.py::test_client_launcher_manages_local_tjuae_server_process -q`
  - `8 passed`
- Full client tests:
  - `pytest mc-design-nx/client/tests -q`
  - `209 passed`
- Launcher build:
  - `cmd /c mc-design-nx\client-launcher\build-launcher.bat Release`
  - Passed.
- Installer build:
  - `MC_DESIGN_NO_PAUSE=1 cmd /c mc-design-nx\package\windows\build-installer.bat --skip-msbuild`
  - Passed.
- User confirmation:
  - User reported the client connected successfully after the fix.

## Output Installer

- `E:\A0_Projects\A1_Dynamics_Design_LM\mc-design\mc-design-nx\package\windows\output\installers\McDesignClientSetup-dev-d5d4a60.zip`

## Commits

- `mc-design-nx`: `d5d4a60 Harden local client startup with tjuae fallback`

## Notes

- This fix addresses the logged startup/login symptom. It does not change TC credentials or cloud auth.
- If tjuae later provides stable `/ready` and diagnostics endpoints, mc-design will still prefer strict managed-server validation; TCP listener fallback only applies when those endpoints are unavailable.
