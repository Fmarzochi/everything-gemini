---
name: tdd-workflow
description: Enforces test-driven development. Guides Gemini CLI on how to execute Red-Green-Refactor using native tools.
tools: ["run_shell_command", "replace", "read_file", "grep_search", "glob", "list_directory", "write_file"]
---

# Test-Driven Development Workflow

**CRITICAL INSTRUCTION FOR GEMINI CLI:**
When this skill is activated, you MUST follow these specific steps using your native tools. Do not skip testing.

## Step 1: Research (The `read_file` & `grep_search` Phase)
Before writing any code, you must understand the existing test setup.
- Use `list_directory` to find the `tests/` folder.
- Use `grep_search` to find similar existing tests.
- Use `read_file` to understand the framework (e.g., Jest, PyTest, Go Test) defined in package files (`package.json`, `go.mod`, etc.).

## Step 2: Write Failing Test (The RED Phase)
You must create or modify a test file FIRST.
- Use `replace` (or `write_file` if new) to create the test case.
- Provide the exact `new_string` with the test logic.
- Use `run_shell_command` to execute the test suite (e.g., `npm test`, `pytest`). **Ensure the test fails** because the feature is not implemented.

## Step 3: Implement Code (The GREEN Phase)
Now, write the minimum code required to pass the test.
- Use `replace` to modify the source code file.
- Use `run_shell_command` to run the test suite again. **Ensure the test passes.**
- If the test fails, use `read_file` to review your code and try again.

## Step 4: Refactor
Clean up the code while keeping the tests green.
- Use `replace` to refactor.
- Run `run_shell_command` one last time to verify no regressions occurred.

**Rules for Tool Usage:**
- **Never** use generic bash `sed` for editing files; ALWAYS use your `replace` tool.
- **Never** assume a command succeeded without checking the output of `run_shell_command`.
- Keep changes atomic.
