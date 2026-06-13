MC Design Client Installer
==========================

Bundle version: dev-sync-20260528

Install on Windows 7 + NX 11:

1. Extract this package to a temporary folder.
2. Run install.bat.
   - Double-clicking install.bat prompts for the install directory.
   - Press Enter to use the default install dir: %LOCALAPPDATA%\McDesign.
   - If UGII_BASE_DIR is missing or invalid, install.bat prompts for the NX11
     install dir. Automated installs may pass both paths:
     install.bat D:\McDesign C:\Siemens\NX11.
   - Upgrade is incremental: the installer cleans files it owns, preserves
     configure\mc-design-client.config, and replaces the managed mc-design block in
     UGII\menus\custom_dirs.dat.
   - Install and uninstall automatically stop the running MC Design client.
     If NX ugraf.exe is running, the command asks before stopping it; declining
     the prompt fails the command so plugin files are not modified while NX is
     open.
   - The legacy UGII_CUSTOM_DIRECTORY_FILE variable is removed so NX11 uses
     the standard custom_dirs.dat path.
3. Edit configure\mc-design-client.config in the installed directory.
    - Put real user_id, user_name, runtime port, NX plugin port, and tc_key there.
    - AI service route, API key, and AIWebForm URL are repository-owned values
      packaged into client\resources\mc-design-package.mcdpkg.
   - Local API host, asset paths, logs, workspace, and reconnect interval are
     fixed by the client and are not installer configuration.
   - Do not edit package-manifest.json.
4. Restart NX 11 so it reads UGII\menus\custom_dirs.dat.
5. Start MC Design Client from McDesignClient.exe in the install directory.
   start-client.bat is kept only as a diagnostic command-line entry.
6. Open NX and run smoke-test.bat --online --require-nx.

Smoke test modes:

- smoke-test.bat
  Checks installed files and local asset package. It allows the client and NX
  to be offline.
- smoke-test.bat --online
  Also requires the local Python client API on 127.0.0.1 to be running.
- smoke-test.bat --online --require-nx
  Also requires the NX plugin loopback API to be available.
- smoke-test.bat --release
  Requires release_eligible=true and bundled client/python/python.exe.

Runtime rules:

- Users start the Python client explicitly. NX must not start it.
- NX plugin talks only to 127.0.0.1 loopback.
- AI service access uses one Kubernetes-routed host:port from mc-design-package.mcdpkg.
- Customer package contains agent_assets.mcdpkg, not assets/source.
- install-state.json records installed files and the NX custom_dirs.dat target
  for future upgrades and uninstall.
