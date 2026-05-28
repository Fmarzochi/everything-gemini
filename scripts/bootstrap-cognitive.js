#!/usr/bin/env node
'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const MARKER = '<!-- egc-memory-protocol -->';

const BLOCK = `
<!-- egc-memory-protocol -->
## EGC Session Memory

The \`egc-memory\` MCP server is installed. Use it to maintain cross-session memory:

**Start of every session:** Call \`get_state({})\` to restore project context — decisions made, what failed, what to pick up next.
**End of every session:** Call \`update_state({...})\` to save decisions, preferences, and next steps.

State files live at \`~/.egc/state/<project-slug>.md\` — plain Markdown, one file per project.
<!-- /egc-memory-protocol -->
`;

function injectProtocol(filepath, label) {
  const exists = fs.existsSync(filepath);

  if (exists) {
    const content = fs.readFileSync(filepath, 'utf8');
    if (content.includes(MARKER)) {
      console.log(`  [cognitive] ${label}: already configured`);
      return;
    }
    fs.writeFileSync(filepath + '.egc.bak', content, 'utf8');
    fs.writeFileSync(filepath, content + BLOCK, 'utf8');
  } else {
    const dir = path.dirname(filepath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(filepath, BLOCK, 'utf8');
  }

  console.log(`  [cognitive] ${label}: memory protocol installed (${filepath.replace(os.homedir(), '~')})`);
}

const HOME = os.homedir();

if (fs.existsSync(path.join(HOME, '.claude'))) {
  injectProtocol(path.join(HOME, '.claude', 'CLAUDE.md'), 'Claude Code');
}

if (fs.existsSync(path.join(HOME, '.gemini'))) {
  injectProtocol(path.join(HOME, '.gemini', 'GEMINI.md'), 'Gemini CLI');
}
