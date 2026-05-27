# mc-design workspace

This repository is a local aggregation workspace for the two active mc-design codebases.

## Repositories

- `mc-design-ai-service`: cloud AI-service and FastMCP runtime bridge.
- `mc-design-nx`: customer-side client, packaged agent runtime, assets, and NX integration.

Both child repositories are Git submodules pinned to their `dev` branch commits. The child repositories keep their own history and remotes.

## Sync

Initialize or refresh submodules:

```powershell
git submodule update --init --recursive
git submodule foreach "git checkout dev; git pull --ff-only origin dev"
```

After updating a child repository, commit the updated submodule pointer in this root repository:

```powershell
git status
git add mc-design-ai-service mc-design-nx
git commit -m "chore: update workspace submodules"
```

## Development Entry Points

- AI-service work starts in `mc-design-ai-service`.
- Client and NX runtime work starts in `mc-design-nx`.
- The streaming AgentLoop upgrade plan is in `mc-design-nx/docs/runtime-streaming-agentloop-plan.md`.

Do not use older local copies as implementation sources.
