# CLIENT-USER-CONFIG-001 Execution Receipt

## Status

Completed.

## Problem

Customer feedback showed the installed client UI could not start. The screenshot
showed a real user identity:

- `user_id=yc90114959`
- `user_name=蔡新朝`

The installed `client` folder containing `app`, `python`, `resources`, and
`tjuae-server` is expected. The startup failure was not caused by that folder
layout. Root cause was product code incorrectly enforcing the internal test
identity `88000044/宋明芮` as a required startup identity.

## Changes

- Removed fixed test identity validation from the C# launcher.
- Removed fixed test identity validation from Python client startup config
  validation.
- Kept generic product validation:
  - `client.user_id` must be present and cannot be `local`, `anonymous`, or
    `anon`.
  - `client.user_name` must be present.
  - `ai_service.tc_key` must be configured before startup.
- Changed installer smoke helper so fixed expected user identity is only checked
  when `--expected-user-id` or `--expected-user-name` is explicitly provided.
- Added test coverage proving a non-test real user identity can pass startup
  validation without exposing the TC password.

## Verification

- `python -m py_compile mc-design-nx/client/src/mc_design_client/config/__init__.py mc-design-nx/package/windows/build/scripts/build_installer.py`
  - Result: passed.
- `python -m pytest mc-design-nx/client/tests/test_client_static.py mc-design-nx/client/tests/test_windows_installer_build.py -q`
  - Result: `68 passed`.
- `cmd /c mc-design-nx/client-launcher/build-launcher.bat Release`
  - Result: passed.
- `MC_DESIGN_NO_PAUSE=1 cmd /c mc-design-nx/package/windows/build-installer.bat --skip-msbuild`
  - Result: passed.
  - Installer: `mc-design-nx/package/windows/output/installers/McDesignClientSetup-dev-20c81bb.zip`.
  - Archive self-check: passed.

## Notes

- The public testing rule still uses `user_id=88000044` and `user_name=宋明芮`
  for our own controlled tests.
- Product builds must not require that identity for other users.
- No Teamcenter password was printed or written to this receipt.
- `mc-design-nx` commit pushed:
  `20c81bbd82c97975584f14375443285dbbcd2f3f`.
