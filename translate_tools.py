import os
import re

# Targeted directories
DIRECTORIES = ['agents', 'skills', '.gemini', 'commands', 'rules', 'docs', 'manifests', 'mcp-configs']
ROOT_FILES = ['README.md', 'CONTRIBUTING.md', 'AGENTS.md', 'README.zh-CN.md']

# Tool replacements
REPLACEMENTS = {
    'Read': 'read_file',
    'Grep': 'grep_search',
    'Glob': 'glob',
    'Bash': 'run_shell_command',
    'edit_file': 'replace',
    'Edit': 'replace', # Often used as short for edit_file in tool contexts
}

def should_replace_ls(line):
    # Replace 'ls' if it's in a list of tools or looks like a tool reference
    if re.search(r'tools:|allowed_tools:|allowed-tools:|allowedTools:', line):
        return True
    if re.search(r'\buse ls\b|\bls tool\b|\bls command\b', line, re.IGNORECASE):
        return True
    if re.search(r'\[.*"ls".*\]|\[.*\'ls\'.*\]', line):
        return True
    return False

def translate_content(content):
    # 1. Replace tool parameters if explicitly mentioned
    content = content.replace('edit_file with old_string', 'replace with old_string')
    
    # 2. Handle tool lists in YAML frontmatter and similar structures
    def replace_in_list(match):
        list_str = match.group(0)
        for old, new in REPLACEMENTS.items():
            list_str = re.sub(rf'\b{old}\b', new, list_str)
        # Handle ls in lists
        list_str = re.sub(rf'\b"ls"\b', '"list_directory"', list_str)
        list_str = re.sub(rf"\b'ls'\b", "'list_directory'", list_str)
        list_str = re.sub(rf"\bls\b(?=,)|(?<=,)\s*\bls\b", "list_directory", list_str)
        return list_str

    content = re.sub(r'(tools|allowed_tools|allowed-tools|allowedTools|allowed_tools|customTools):\s*\[?.*\]?', replace_in_list, content, flags=re.IGNORECASE)

    # 3. Replace mentions in text like "Read tool", "Bash tool", etc.
    for old, new in REPLACEMENTS.items():
        content = re.sub(rf'\b{old}\b\s+tool', f'{new} tool', content)
        content = re.sub(rf'\b{old}\b\s+command', f'{new} command', content)

    # 4. Replace standalone tool names if they look like tool calls or specific mentions
    # This is the most aggressive part, we need to be careful with 'Read'
    # The prompt says: "Replace any mention of the tool 'Read' with 'read_file'"
    # We'll target capitalized 'Read', 'Grep', 'Glob', 'Bash' when they stand alone as tool names.
    
    # If a line starts with "- Read", it's likely a tool list
    content = re.sub(r'^-\s+Read\b', '- read_file', content, flags=re.MULTILINE)
    content = re.sub(r'^-\s+Grep\b', '- grep_search', content, flags=re.MULTILINE)
    content = re.sub(r'^-\s+Glob\b', '- glob', content, flags=re.MULTILINE)
    content = re.sub(r'^-\s+Bash\b', '- run_shell_command', content, flags=re.MULTILINE)
    content = re.sub(r'^-\s+Edit\b', '- replace', content, flags=re.MULTILINE)

    # Handle 'ls' mentions
    content = re.sub(rf'\bls tool\b', 'list_directory tool', content, flags=re.IGNORECASE)
    content = re.sub(rf'\bls command\b', 'list_directory command', content, flags=re.IGNORECASE)

    return content

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = translate_content(content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    for root_file in ROOT_FILES:
        if os.path.exists(root_file):
            process_file(root_file)
            
    for directory in DIRECTORIES:
        if not os.path.exists(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.md', '.json', '.yaml', '.yml')):
                    process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
