# Working Context

Last updated: 2026-04-01

## Purpose

Public ECC plugin repo for agents, skills, commands, hooks, rules, install surfaces, and ECC 2.0 platform buildout.

## Current Truth

- Default branch: `main`
- Immediate blocker addressed: CI lockfile drift and hook validation breakage fixed in `a273c62`
- Local full suite status after fix: `1723/1723` passing
- Main active operational work:
  - keep default branch green
  - audit and classify remaining open PR backlog by full diff
  - continue ECC 2.0 control-plane and operator-surface buildout

## Current Constraints

- No merge by title or commit summary alone.
- No arbitrary external runtime installs in shipped ECC surfaces.
- Overlapping skills, hooks, or agents should be consolidated when overlap is material and runtime separation is not required.

## Active Queues

- PR backlog: audit and classify remaining open PRs into merge, port/rebuild, close, or park
- Product:
  - selective install cleanup
  - control plane primitives
  - operator surface
  - self-improving skills
- Security:
  - keep dependency posture clean
  - preserve self-contained hook and MCP behavior

## Open PR Classification

- Closed on 2026-04-01 under backlog hygiene / merge policy:
  - `#1069` `feat: add everything-claude-code ECC bundle`
  - `#1068` `feat: add everything-claude-code-conventions ECC bundle`
  - `#1064` `chore(deps-dev): bump @eslint/js from 9.39.2 to 10.0.1`
  - `#1063` `chore(deps-dev): bump eslint from 9.39.2 to 10.1.0`
- Closed on 2026-04-01 because the content is sourced from external ecosystems and should only land via manual ECC-native re-port:
  - `#852` openclaw-user-profiler
  - `#851` openclaw-soul-forge
  - `#640` harper skills
- Native-support candidates to fully diff-audit next:
  - `#1055` Dart / Flutter support
  - `#1043` C# reviewer and .NET skills
  - `#834` localized catalog sync and antigravity target filtering
- Port or rebuild inside ECC after full audit:
  - `#894` Jira integration
  - `#844` ui-demo skill
  - `#814` + `#808` rebuild as a single consolidated notifications lane for Opencode and cross-harness surfaces

## Interfaces

- Public truth: GitHub issues and PRs
- Internal execution truth: linked Linear work items under the ECC program
- Current linked Linear items:
  - `ECC-206` ecosystem CI baseline
  - `ECC-207` PR backlog audit and merge-policy enforcement
  - `ECC-208` context hygiene

## Update Rule

Keep this file detailed for only the current sprint, blockers, and next actions. Summarize completed work into archive or repo docs once it is no longer actively shaping execution.

## Latest Execution Notes

- 2026-04-01: `main` CI was restored locally with `1723/1723` tests passing after lockfile and hook validation fixes.
- 2026-04-01: Auto-generated ECC bundle PRs `#1068` and `#1069` were closed instead of merged; useful ideas must be ported manually after explicit diff audit.
- 2026-04-01: Major-version ESLint bump PRs `#1063` and `#1064` were closed; revisit only inside a planned ESLint 10 migration lane.
- 2026-04-01: Notification PRs `#808` and `#814` were identified as overlapping and should be rebuilt as one unified feature instead of landing as parallel branches.
- 2026-04-01: External-source skill PRs `#640`, `#851`, and `#852` were closed under the new ingestion policy; copy ideas from audited source later rather than merging branded/source-import PRs directly.
- 2026-04-01: The remaining low GitHub advisory on `ecc2/Cargo.lock` was addressed by moving `ratatui` to `0.30` with `crossterm_0_28`, which updated transitive `lru` from `0.12.5` to `0.16.3`. `cargo build --manifest-path ecc2/Cargo.toml` still passes.
