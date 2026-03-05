# Harness Audit Command

Audit the current repository's agent harness setup and return a prioritized scorecard.

## Usage

`/harness-audit [scope] [--format text|json]`

- `scope` (optional): `repo` (default), `hooks`, `skills`, `commands`, `agents`
- `--format`: output style (`text` default, `json` for automation)

## What to Evaluate

Score each category from `0` to `10`:

1. Tool Coverage
2. Context Efficiency
3. Quality Gates
4. Memory Persistence
5. Eval Coverage
6. Security Guardrails
7. Cost Efficiency

## Output Contract

Return:

1. `overall_score` out of 70
2. Category scores and concrete findings
3. Top 3 actions with exact file paths
4. Suggested ECC skills to apply next

## Checklist

- Inspect `hooks/hooks.json`, `scripts/hooks/`, and hook tests.
- Inspect `skills/`, command coverage, and agent coverage.
- Verify cross-harness parity for `.cursor/`, `.opencode/`, `.codex/`.
- Flag broken or stale references.

## Example Result

```text
Harness Audit (repo): 52/70
- Quality Gates: 9/10
- Eval Coverage: 6/10
- Cost Efficiency: 4/10

Top 3 Actions:
1) Add cost tracking hook in scripts/hooks/cost-tracker.js
2) Add pass@k docs and templates in skills/eval-harness/SKILL.md
3) Add command parity for /harness-audit in .opencode/commands/
```

## Arguments

$ARGUMENTS:
- `repo|hooks|skills|commands|agents` (optional scope)
- `--format text|json` (optional output format)
