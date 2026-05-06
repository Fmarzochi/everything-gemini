import os
import re

replacements = [
    (r"Everything-Claude-Code", "Everything-Gemini"),
    (r"everything-claude-code", "everything-gemini"),
    (r"Everything Claude Code", "Everything Gemini"),
    (r"Claude Code", "Gemini CLI"),
    (r"claude code", "gemini cli"),
    (r"Claude", "Gemini"),
    (r"claude", "gemini"),
    (r"CLAUDE", "GEMINI"),
    (r"Affaan Mustafa", "Felipe Marzochi"),
    (r"fmarzochi", "fmarzochi"),
    (r"ANTHROPIC_API_KEY", "GOOGLE_API_KEY"),
    (r"ANTHROPIC_BASE_URL", "GOOGLE_BASE_URL"),
    (r"ANTHROPIC_AUTH_TOKEN", "GOOGLE_AUTH_TOKEN"),
]

# Case insensitive search but preserving case is tricky with multiple replacements.
# The user specified:
# 1. "Everything Claude Code" -> "Everything Gemini"
# 2. "Everything-Claude-Code" -> "Everything-Gemini"
# 3. "everything-claude-code" -> "everything-gemini"
# 4. "Claude Code" -> "Gemini CLI"
# 5. "Claude" -> "Gemini"
# 6. "Affaan Mustafa" -> "Felipe Marzochi"
# 7. "fmarzochi" -> "fmarzochi"

# Special handle for Google -> Google
anthropic_replacement = (r"Google", "Google")

exclude_dirs = {".git", "node_modules", "assets"}
exclude_files = {"replace_script.py", "package-lock.json", "yarn.lock"}

def should_replace_anthropic(line):
    # Do not replace if it's about the hackathon winner
    if "hackathon winner" in line.lower() or "hackathon" in line.lower():
        return False
    return True

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return # Skip binary files

    new_content = content
    
    # Standard replacements in specific order
    for pattern, repl in replacements:
        new_content = re.sub(pattern, repl, new_content)

    # Handle Google -> Google line by line or with a smart regex
    lines = new_content.split('\n')
    for i, line in enumerate(lines):
        if "Google" in line:
            if should_replace_anthropic(line):
                # Replace Google with Google only if it's not hackathon related
                # Be careful not to replace it if it's part of a URL or something specific that should remain
                # But the user said "where contextually appropriate for the LLM provider"
                lines[i] = line.replace("Google", "Google")
    
    new_content = '\n'.join(lines)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {file_path}")

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file in exclude_files:
            continue
        process_file(os.path.join(root, file))
