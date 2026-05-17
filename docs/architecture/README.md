# EGC Architecture

EGC ships as two coexisting runtimes plus a documented future kernel.
This page is the index — read it first, then drill into the specific
documents below.

## Current runtimes (v1.x — shipping)

### Node.js plugin runtime (CI-covered)

The production surface that powers the Gemini Code, Codex, Cursor,
Antigravity, OpenCode, Kiro, Trae, and Codebuddy harnesses.

| Layer | Path | Role |
|---|---|---|
| Manifests | `.gemini-plugin/`, `.codex-plugin/`, `.gemini-plugin/marketplace.json` | Static plugin discovery |
| Install adapters | `scripts/lib/install-targets/` | Per-target materialization |
| Install entry | `scripts/install-apply.js`, `install.sh`, `install.ps1` | User-facing installers |
| Hooks pipeline | `hooks/hooks.json` + `scripts/hooks/*` | Pre/Post-tool, session, governance hooks |
| CI gates | `scripts/ci/validate-*.js`, `scripts/ci/catalog.js` | Workflow validation |

The Node runtime is fully exercised by the CI matrix
(`.github/workflows/ci.yml`, `reusable-test.yml`,
`reusable-validate.yml`) across Linux/macOS/Windows × Node 18/20/22 ×
npm/pnpm/yarn/bun.

### Python autonomous-platform runtime (CI-isolated)

The persistent orchestration substrate referenced by the EGC 2.0
blueprint. Importable and functionally tested in `tests/test_*.py`,
but not driven by the JS-based CI matrix.

| Layer | Path | Role |
|---|---|---|
| LLM provider abstraction | `src/llm/{providers,core,prompt,cli,tools}` | Multi-provider dispatch (Gemini, Claude, OpenAI, OpenRouter, Ollama) |
| Execution | `scripts/execution/` | Execution queue, agent executor, sandbox, tool runner |
| Orchestration | `scripts/orchestration/` | DAG validator, router, orchestrator, fallback |
| Workflows | `scripts/workflows/` | Task planner, workflow engine, workflow state |
| Memory | `scripts/memory/` | Experience store, persistent memory |
| Runtime primitives | `scripts/runtime/*.py` | Async task queue, event bus, memory mesh, profiler, runtime context, session manager, tracer |
| Dashboard | `egc_dashboard.py` | Tkinter control plane |

The Python tests under `tests/test_*.py` are functional (e.g.
`test_orchestrator.py`, `test_concurrency.py`, `test_deadlock_protection.py`)
but the JS test runner glob excludes them. See
`governance/SUBSYSTEM-MAP.md` for the formal status.

### Dormant scaffolding (preserved)

- `scripts/runtime/{router,discovery,mount-all,unmount-all,activator}.js`
- `scripts/orchestration/router.py`
- `scripts/health-check.js`, `scripts/generate-plugin-manifest.js`

These resolve a non-existent `registry/` path and have no callers.
See `scripts/runtime/README.md` and `governance/SUBSYSTEM-MAP.md` for the
DORMANT status.

## Target runtime — EGC 2.0 (design proposal)

See `EGC_2.0_BLUEPRINT.md` and `EGC_2.0_TECHNICAL_DESIGN.md` for the
full unified-control-plane (Rust kernel + Python LLM engine + Node hook
worker + SQLite state store) target model.

The Rust scaffold at `egc/` is reserved as the kernel host once
promotion to v2.0 occurs.

## Documents in this folder

| File | Scope |
|---|---|
| `ARCHITECTURE-IMPROVEMENTS.md` | Cross-cutting improvements and refactors landed during v1 stabilization |
| `EGC_2.0_BLUEPRINT.md` | Vision for the v2.0 Agent OS |
| `EGC_2.0_TECHNICAL_DESIGN.md` | v2.0 component integration and IPC contracts |
| `SELECTIVE-INSTALL-ARCHITECTURE.md` | Module/profile system in `manifests/install-*.json` |
| `SELECTIVE-INSTALL-DESIGN.md` | Selective install design rationale and per-target rules |
| `SINGLE-AGENT-OPERATIONAL-MODEL.md` | Authoritative single-agent execution model |
| `continuous-learning-v2-spec.md` | Continuous-learning v2 skill specification |
| `cross-harness.md` | How a single skill source surfaces across Gemini Code, Codex, Cursor, OpenCode |
