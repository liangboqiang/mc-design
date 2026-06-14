# PACK-VENDOR-TJUAE-SERVER-001 Execution Receipt

## Status

Completed.

## Scope

Fix Windows client packaging so normal testers/operators are not asked for a
`Tjuae server package/dist dir`. The `mc-design-nx` repository now provides both
the Tjuae Python SDK and the Windows Tjuae server as repository-vendored assets.

## Changes

- Added `mc-design-nx/client/vendor/tjuae-server/tjuae-server-win-x64.zip`
  from the Tjuae dist and tracked it with Git LFS. The Windows build extracts
  this archive into the customer package as
  `client/tjuae-server/server/win-x64/tjuae-server.exe`.
- Added `mc-design-nx/client/vendor/tjuae-server/VENDORED_SERVER.json` with
  version, upstream commit, and SHA-256 traceability.
- Removed the interactive `set /p` prompt from
  `mc-design-nx/package/windows/build-installer.bat`.
- Updated packaging validation to reject Git LFS pointer files for
  `tjuae-server.exe` and instruct developers to run `git lfs pull`.
- Added `payload/client/resources/tjuae-server-vendor.json` to packaged
  installer artifacts and archive self-checks.
- Added Tjuae server vendor metadata to client version information for health
  checks and per-conversation logs.
- Updated Windows packaging and runtime documentation to state that normal
  customer builds use repository-vendored SDK/server assets.

## Source Asset

- Tjuae source worktree: `F:\Documents\tjuae`
- Tjuae source commit: `214d3071316cbf24297703053fcf4202d89cd6e0`
- Tjuae server executable SHA-256:
  `272d7a113a59e4a7787bc37c58a4050653fce11330a1990a800e3812a76823df`
- Tjuae server archive SHA-256:
  `fe117de668b323df2753a1fbc00e3312ccd7278c87bc9d97b8b9500f4af6d10c`

## Verification

- `python -m py_compile client/src/mc_design_client/version.py package/windows/build/scripts/payload_builder.py package/windows/build/scripts/build_installer.py`
  - Result: passed.
- `python -m pytest client/tests/test_windows_payload_builder.py client/tests/test_client_static.py client/tests/test_usage_issue_fixes.py -q`
  - Result: `63 passed`.
- `python -m pytest client/tests/test_windows_installer_build.py -q`
  - Result: `26 passed`.
- `MC_DESIGN_NO_PAUSE=1 package/windows/build-installer.bat --dry-run`
  - Result: passed.
  - SDK source: `client/vendor/tjuae-sdk-python/wheelhouse/tjuae_sdk-0.1.0-py3-none-any.whl`.
  - Server source: `client/vendor/tjuae-server/tjuae-server-win-x64.zip`.
- `MC_DESIGN_NO_PAUSE=1 package/windows/build-installer.bat --skip-msbuild`
  - Result: passed.
  - Installer: `mc-design-nx/package/windows/output/installers/McDesignClientSetup-dev-4c22ce7.zip`.
  - Archive self-check included `payload/client/resources/tjuae-server-vendor.json`
    and `payload/client/tjuae-server/server/win-x64/tjuae-server.exe`.

## Residual Notes

- The build still accepts explicit `--tjuae-server-package` for development
  diagnostics, but the normal packaging path does not prompt or require it.
- `mc-design-nx` commit pushed: `4c22ce7d8f4d235629331db363b10102fe882af0`.
