#!/usr/bin/env node
/**
 * Run all tests
 *
 * Usage: node tests/run-all.js
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const testsDir = __dirname;

/**
 * Discover all *.test.js files under testsDir (relative paths for stable output order).
 */
function discoverTestFiles(dir, baseDir = dir, acc = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    const rel = path.relative(baseDir, full);
    if (e.isDirectory()) {
      discoverTestFiles(full, baseDir, acc);
    } else if (e.isFile() && e.name.endsWith('.test.js')) {
      acc.push(rel);
    }
  }
  return acc.sort();
}

const testFiles = discoverTestFiles(testsDir);

const BOX_W = 58; // inner width between ║ delimiters
const boxLine = (s) => `║${s.padEnd(BOX_W)}║`;

console.log('╔' + '═'.repeat(BOX_W) + '╗');
console.log(boxLine('           Everything Claude Code - Test Suite'));
console.log('╚' + '═'.repeat(BOX_W) + '╝');
console.log();

let totalPassed = 0;
let totalFailed = 0;
let totalTests = 0;

for (const testFile of testFiles) {
  const testPath = path.join(testsDir, testFile);

  if (!fs.existsSync(testPath)) {
    console.log(`⚠ Skipping ${testFile} (file not found)`);
    continue;
  }

  console.log(`\n━━━ Running ${testFile} ━━━`);

  const result = spawnSync('node', [testPath], {
    encoding: 'utf8',
    stdio: ['pipe', 'pipe', 'pipe']
  });

  const stdout = result.stdout || '';
  const stderr = result.stderr || '';

  // Show both stdout and stderr so hook warnings are visible
  if (stdout) console.log(stdout);
  if (stderr) console.log(stderr);

  // Parse results from combined output
  const combined = stdout + stderr;
  const passedMatch = combined.match(/Passed:\s*(\d+)/);
  const failedMatch = combined.match(/Failed:\s*(\d+)/);

  if (passedMatch) totalPassed += parseInt(passedMatch[1], 10);
  if (failedMatch) totalFailed += parseInt(failedMatch[1], 10);
}

totalTests = totalPassed + totalFailed;

console.log('\n╔' + '═'.repeat(BOX_W) + '╗');
console.log(boxLine('                     Final Results'));
console.log('╠' + '═'.repeat(BOX_W) + '╣');
console.log(boxLine(`  Total Tests: ${String(totalTests).padStart(4)}`));
console.log(boxLine(`  Passed:      ${String(totalPassed).padStart(4)}  ✓`));
console.log(boxLine(`  Failed:      ${String(totalFailed).padStart(4)}  ${totalFailed > 0 ? '✗' : ' '}`));
console.log('╚' + '═'.repeat(BOX_W) + '╝');

process.exit(totalFailed > 0 ? 1 : 0);
