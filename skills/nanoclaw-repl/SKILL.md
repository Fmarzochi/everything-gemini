---
name: nanoclaw-repl
description: Operate and extend NanoClaw v2, ECC's zero-dependency session-aware REPL built on gemini -p.
origin: ECC
tools: ["run_shell_command", "replace", "read_file", "grep_search", "glob", "list_directory", "write_file"]
---


**CRITICAL INSTRUCTION FOR GEMINI CLI:**
When executing the logic of this skill, you MUST map the conceptual steps to your native toolset:
- Use `read_file` to read file contents.
- Use `replace` to edit files exactly (do not use sed or echo).
- Use `write_file` to create new files.
- Use `grep_search` and `glob` to search across the codebase.
- Use `list_directory` to explore folders.
- Use `run_shell_command` to execute tests, builds, or other terminal commands.
Always verify the output of your tools before proceeding to the next logical step.


# NanoClaw REPL

Use this skill when running or extending `scripts/claw.js`.

## Capabilities

- persistent markdown-backed sessions
- model switching with `/model`
- dynamic skill loading with `/load`
- session branching with `/branch`
- cross-session search with `/search`
- history compaction with `/compact`
- export to md/json/txt with `/export`
- session metrics with `/metrics`

## Operating Guidance

1. Keep sessions task-focused.
2. Branch before high-risk changes.
3. Compact after major milestones.
4. Export before sharing or archival.

## Extension Rules

- keep zero external runtime dependencies
- preserve markdown-as-database compatibility
- keep command handlers deterministic and local
