# cc-haha Legacy Runtime Reference

`cc_haha_agent_runtime_migration_pack` is retained here only as an external runtime migration reference.

It is not an mc-design-client runtime dependency. The active mc-design-client runtime does not load this directory, does not include it in the Windows payload contract, and does not use it for tjuae server skill discovery.

Current mc-design-client runtime assets are resolved through:

```text
mc-design-nx/assets/source
  -> mc-design-nx/client/resources/agent_assets.mcdpkg
  -> mc-design-nx/client/data/asset_views/runtime-agentloop
  -> mc-design-nx/client/data/workspace/.tjuae/skills
```

Do not use this archived cc-haha reference as a runtime entrypoint.
