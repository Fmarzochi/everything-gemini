#!/usr/bin/env node
/**
 * PostToolUse Hook: Auto-format JS/TS files with Prettier after edits
 *
 * Cross-platform (Windows, macOS, Linux)
 *
 * Runs after Edit tool use. If the edited file is a JS/TS file,
 * formats it with Prettier. Fails silently if Prettier isn't installed.
 */

const { execFileSync } = require('child_process');
const fs = require('fs');

let data = '';

process.stdin.on('data', chunk => {
  data += chunk;
});

process.stdin.on('end', () => {
  try {
    const input = JSON.parse(data);
    const filePath = input.tool_input?.file_path;

    if (filePath && /\.(ts|tsx|js|jsx)$/.test(filePath) && fs.existsSync(filePath)) {
      try {
        execFileSync('npx', ['prettier', '--write', filePath], {
          stdio: ['pipe', 'pipe', 'pipe'],
          timeout: 15000
        });
      } catch {
        // Prettier not installed or failed — non-blocking
      }
    }
  } catch {
    // Invalid input — pass through
  }

  console.log(data);
});
