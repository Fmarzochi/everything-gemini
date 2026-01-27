# Plugin Manifest Schema Notes

This document captures **undocumented but enforced constraints** of the Claude Code plugin manifest validator.

These rules are based on real installation failures, validator behavior, and comparison with known working plugins.
They exist to prevent silent breakage and repeated regressions.

If you edit `.claude-plugin/plugin.json`, read this first.

---

## Summary (Read This First)

The Claude plugin manifest validator is **strict and opinionated**.
It enforces rules that are not fully documented in public schema references.

The most common failure mode is:

> The manifest looks reasonable, but the validator rejects it with vague errors like
> `agents: Invalid input`

This document explains why.

---

## Required Fields

### `version` (MANDATORY)

The `version` field is required by the validator even if omitted from some examples.

If missing, installation may fail during marketplace install or CLI validation.

Example:

```json
{
  "version": "1.1.0"
}
```

---

## Field Shape Rules

The following fields **must always be arrays**:

* `agents`
* `commands`
* `skills`
* `hooks` (if present)

Even if there is only one entry, **strings are not accepted**.

### Invalid

```json
{
  "agents": "./agents"
}
```

### Valid

```json
{
  "agents": ["./agents/planner.md"]
}
```

This applies consistently across all component path fields.

---

## Path Resolution Rules (Critical)

### Agents MUST use explicit file paths

The validator **does not accept directory paths for `agents`**.

Even the following will fail:

```json
{
  "agents": ["./agents/"]
}
```

Instead, you must enumerate agent files explicitly:

```json
{
  "agents": [
    "./agents/planner.md",
    "./agents/architect.md",
    "./agents/code-reviewer.md"
  ]
}
```

This is the most common source of validation errors.

### Commands and Skills

* `commands` and `skills` accept directory paths **only when wrapped in arrays**
* Explicit file paths are safest and most future-proof

---

## Validator Behavior Notes

* `claude plugin validate` is stricter than some marketplace previews
* Validation may pass locally but fail during install if paths are ambiguous
* Errors are often generic (`Invalid input`) and do not indicate root cause
* Cross-platform installs (especially Windows) are less forgiving of path assumptions

Assume the validator is hostile and literal.

---

## Known Anti-Patterns

These look correct but are rejected:

* String values instead of arrays
* Arrays of directories for `agents`
* Missing `version`
* Relying on inferred paths
* Assuming marketplace behavior matches local validation

Avoid cleverness. Be explicit.

---

## Minimal Known-Good Example

```json
{
  "version": "1.1.0",
  "agents": [
    "./agents/planner.md",
    "./agents/code-reviewer.md"
  ],
  "commands": ["./commands/"],
  "skills": ["./skills/"]
}
```

This structure has been validated against the Claude plugin validator.

---

## Recommendation for Contributors

Before submitting changes that touch `plugin.json`:

1. Use explicit file paths for agents
2. Ensure all component fields are arrays
3. Include a `version`
4. Run:

```bash
claude plugin validate .claude-plugin/plugin.json
```

If in doubt, choose verbosity over convenience.

---

## Why This File Exists

This repository is widely forked and used as a reference implementation.

Documenting validator quirks here:

* Prevents repeated issues
* Reduces contributor frustration
* Preserves plugin stability as the ecosystem evolves

If the validator changes, update this document first.
