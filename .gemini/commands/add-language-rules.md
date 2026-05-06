---
name: add-language-rules
description: Workflow command scaffold for add-language-rules in everything-gemini.
allowed_tools: ["run_shell_command", "replace", "read_file", "grep_search", "glob", "list_directory", "write_file"]
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


# /add-language-rules

Use this workflow when working on **add-language-rules** in `everything-gemini`.

## Goal

Adds a new programming language to the rules system, including coding style, hooks, patterns, security, and testing guidelines.

## Common Files

- `rules/*/coding-style.md`
- `rules/*/hooks.md`
- `rules/*/patterns.md`
- `rules/*/security.md`
- `rules/*/testing.md`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Create a new directory under rules/{language}/
- Add coding-style.md, hooks.md, patterns.md, security.md, and testing.md files with language-specific content
- Optionally reference or link to related skills

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.