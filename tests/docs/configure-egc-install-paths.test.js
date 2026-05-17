'use strict';

const assert = require('assert');
const { maybeSkipBaselineAbsent } = require('../lib/baseline-absent');

const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..', '..');

const configureEccDocs = [
  'skills/general/configure-egc/SKILL.md',
  'docs/zh-CN/skills/configure-egc/SKILL.md',
  'docs/ja-JP/skills/configure-egc/SKILL.md',
];

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  ✓ ${name}`);
    passed++;
  } catch (error) {
    if (maybeSkipBaselineAbsent(error, name)) return true;
    console.log(`  ✗ ${name}`);
    console.log(`    Error: ${error.message}`);
    failed++;
  }
}

function readConfigureEccDoc(relativePath) {
  return fs.readFileSync(path.join(repoRoot, relativePath), 'utf8');
}

console.log('\n=== Testing configure-egc install path guidance ===\n');

for (const relativePath of configureEccDocs) {
  test(`${relativePath} separates core and niche skill source roots`, () => {
    const content = readConfigureEccDoc(relativePath);

    assert.ok(
      content.includes('$EGC_ROOT/.agents/skills/<skill-name>'),
      'Expected configure-egc to document the core skill source root'
    );
    assert.ok(
      content.includes('$EGC_ROOT/skills/<skill-name>'),
      'Expected configure-egc to document the niche skill source root'
    );
  });

  test(`${relativePath} documents defensive copy form for trailing slash sources`, () => {
    const content = readConfigureEccDoc(relativePath);

    assert.ok(
      content.includes('${src%/}'),
      'Expected configure-egc to strip trailing slash before copying'
    );
    assert.ok(
      content.includes('$(basename "${src%/}")'),
      'Expected configure-egc to preserve the skill directory name explicitly'
    );
  });
}

if (failed > 0) {
  console.log(`\nFailed: ${failed}`);
  process.exit(1);
}

console.log(`\nPassed: ${passed}`);
