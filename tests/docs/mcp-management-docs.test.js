'use strict';

const assert = require('assert');
const { maybeSkipBaselineAbsent } = require('../lib/baseline-absent');

const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..', '..');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  \u2713 ${name}`);
    passed++;
  } catch (error) {
    if (maybeSkipBaselineAbsent(error, name)) return true;
    console.log(`  \u2717 ${name}`);
    console.log(`    Error: ${error.message}`);
    failed++;
  }
}

function read(relativePath) {
  return fs.readFileSync(path.join(repoRoot, relativePath), 'utf8');
}

console.log('\n=== Testing MCP management docs ===\n');

test('token optimization guide separates Gemini MCP disables from EGC config filters', () => {
  const source = read('docs/token-optimization.md');

  assert.ok(
    source.includes('Use `/mcp` to disable Gemini Code MCP servers'),
    'Token guide should direct Gemini Code users to /mcp for runtime MCP disables'
  );
  assert.ok(
    source.includes('Gemini Code persists those runtime disables in `~/.gemini.json`'),
    'Token guide should name ~/.gemini.json as the observed runtime disable store'
  );
  assert.ok(
    source.includes('`EGC_DISABLED_MCPS` only affects EGC-generated MCP config output'),
    'Token guide should scope EGC_DISABLED_MCPS to config generation'
  );
  assert.ok(
    !source.includes('Use `disabledMcpServers` in project config to disable servers per-project'),
    'Token guide should not tell users that project settings disable Gemini runtime MCP servers'
  );
});

test('README MCP guidance avoids settings.json disable instructions', () => {
  const source = read('README.md');

  assert.ok(
    source.includes('Use `/mcp` for Gemini Code runtime disables; Gemini Code persists those choices in `~/.gemini.json`.'),
    'README should route runtime MCP disables through /mcp and ~/.gemini.json'
  );
  assert.ok(
    source.includes('`EGC_DISABLED_MCPS` is an EGC install/sync filter, not a live Gemini Code toggle.'),
    'README should explain EGC_DISABLED_MCPS scope'
  );
  assert.ok(
    !source.includes('// In your project\'s .gemini/settings.json\n{\n  "disabledMcpServers"'),
    'README should not show disabledMcpServers under .gemini/settings.json'
  );
  assert.ok(
    !source.includes('Use `disabledMcpServers` in project config to disable unused ones'),
    'README quick reference should not repeat stale project-config guidance'
  );
});

if (failed > 0) {
  console.log(`\nFailed: ${failed}`);
  process.exit(1);
}

console.log(`\nPassed: ${passed}`);
