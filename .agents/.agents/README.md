# .agents/.agents — ARCHIVAL recursive mount

This recursive directory is an artifact from the original `mount-all.js`
materialization, committed in the initial public baseline (`f2bc03a7`).

**Status: ARCHIVAL.**

Contents: 228 symlinks (one per skill in the catalog) targeting the
canonical sources under `skills/<namespace>/<name>`. Targets are
repo-relative (`../../../skills/<namespace>/<name>`) — portable across
forks, CI runners, and marketplace installs.

The layout reflects the runtime-map taxonomy:

- one entry per skill (cold mount)
- targets resolve relative to the symlink's own directory

Preserved for two reasons:

1. The `internal/registry/runtime-map.json` snapshot references this
   layout.
2. Removing it would mutate the canonical baseline without an
   architectural decision.

Do not delete or refactor without first replacing the runtime-map
taxonomy. See `docs/governance/SUBSYSTEM-MAP.md`.
