# internal/registry — GENERATED + ARCHIVAL snapshot

Three files:

- `runtime-map.json` — GENERATED snapshot (last regenerated 2026-05-14T06:39:55Z)
  produced by the now-dormant `scripts/runtime/discovery.js`. Records the
  hot/cold/shadowed taxonomy of skills and agents.
- `agents-registry.json` — ARCHIVAL inventory (50 entries). Current catalog
  has 62 agents — see `node scripts/ci/catalog.js --text` for the live
  count.
- `skills-registry.json` — ARCHIVAL inventory (182 entries). Current catalog
  has 228 skills.

These files have **no live consumers**:

- CI does not read them.
- The static plugin manifests are the source of truth for plugin discovery.
- `scripts/ci/catalog.js` derives counts from the filesystem.

They remain because the dormant `scripts/runtime/*` subsystem and the
historical record reference them. See `scripts/runtime/README.md` for the
dormancy context and `docs/governance/SUBSYSTEM-MAP.md` for the full
classification.
