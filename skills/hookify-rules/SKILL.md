---
name: hookify-rules
description: This skill should be used when the user asks to create a hookify rule, write a hook rule, configure hookify, add a hookify rule, or needs guidance on hookify rule syntax and patterns.
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


# Writing Hookify Rules

## Overview

Hookify rules are markdown files with YAML frontmatter that define patterns to watch for and messages to show when those patterns match. Rules are stored in `.gemini/hookify.{rule-name}.local.md` files.

## Rule File Format

### Basic Structure

```markdown
---
name: rule-identifier
enabled: true
event: bash|file|stop|prompt|all
pattern: regex-pattern-here
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


Message to show Gemini when this rule triggers.
Can include markdown formatting, warnings, suggestions, etc.
```

### Frontmatter Fields

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| name | Yes | kebab-case string | Unique identifier (verb-first: warn-*, block-*, require-*) |
| enabled | Yes | true/false | Toggle without deleting |
| event | Yes | bash/file/stop/prompt/all | Which hook event triggers this |
| action | No | warn/block | warn (default) shows message; block prevents operation |
| pattern | Yes* | regex string | Pattern to match (*or use conditions for complex rules) |

### Advanced Format (Multiple Conditions)

```markdown
---
name: warn-env-api-keys
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: \.env$
  - field: new_text
    operator: contains
    pattern: API_KEY
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


You're adding an API key to a .env file. Ensure this file is in .gitignore!
```

**Condition fields by event:**
- bash: `command`
- file: `file_path`, `new_text`, `old_text`, `content`
- prompt: `user_prompt`

**Operators:** `regex_match`, `contains`, `equals`, `not_contains`, `starts_with`, `ends_with`

All conditions must match for rule to trigger.

## Event Type Guide

### bash Events
Match run_shell_command command patterns:
- Dangerous commands: `rm\s+-rf`, `dd\s+if=`, `mkfs`
- Privilege escalation: `sudo\s+`, `su\s+`
- Permission issues: `chmod\s+777`

### file Events
Match Edit/Write/MultiEdit operations:
- Debug code: `console\.log\(`, `debugger`
- Security risks: `eval\(`, `innerHTML\s*=`
- Sensitive files: `\.env$`, `credentials`, `\.pem$`

### stop Events
Completion checks and reminders. Pattern `.*` matches always.

### prompt Events
Match user prompt content for workflow enforcement.

## Pattern Writing Tips

### Regex Basics
- Escape special chars: `.` to `\.`, `(` to `\(`
- `\s` whitespace, `\d` digit, `\w` word char
- `+` one or more, `*` zero or more, `?` optional
- `|` OR operator

### Common Pitfalls
- **Too broad**: `log` matches "login", "dialog" — use `console\.log\(`
- **Too specific**: `rm -rf /tmp` — use `rm\s+-rf`
- **YAML escaping**: Use unquoted patterns; quoted strings need `\\s`

### Testing
```bash
python3 -c "import re; print(re.search(r'your_pattern', 'test text'))"
```

## File Organization

- **Location**: `.gemini/` directory in project root
- **Naming**: `.gemini/hookify.{descriptive-name}.local.md`
- **Gitignore**: Add `.gemini/*.local.md` to `.gitignore`

## Commands

- `/hookify [description]` - Create new rules (auto-analyzes conversation if no args)
- `/hookify-list` - View all rules in table format
- `/hookify-configure` - Toggle rules on/off interactively
- `/hookify-help` - Full documentation

## Quick Reference

Minimum viable rule:
```markdown
---
name: my-rule
enabled: true
event: bash
pattern: dangerous_command
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

Warning message here
```
