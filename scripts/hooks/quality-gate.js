#!/usr/bin/env node
/**
 * Quality Gate Hook
 *
 * Runs lightweight quality checks after file edits.
 * - Targets one file when file_path is provided
 * - Falls back to no-op when language/tooling is unavailable
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const MAX_STDIN = 1024 * 1024;
let raw = '';

function run(command, args, cwd = process.cwd()) {
  return spawnSync(command, args, {
    cwd,
    encoding: 'utf8',
    env: process.env,
  });
}

function log(msg) {
  process.stderr.write(`${msg}\n`);
}

function maybeRunQualityGate(filePath) {
  if (!filePath || !fs.existsSync(filePath)) {
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const fix = String(process.env.ECC_QUALITY_GATE_FIX || '').toLowerCase() === 'true';
  const strict = String(process.env.ECC_QUALITY_GATE_STRICT || '').toLowerCase() === 'true';

  if (['.ts', '.tsx', '.js', '.jsx', '.json', '.md'].includes(ext)) {
    // Prefer biome if present
    if (fs.existsSync(path.join(process.cwd(), 'biome.json')) || fs.existsSync(path.join(process.cwd(), 'biome.jsonc'))) {
      const args = ['biome', 'check', filePath];
      if (fix) args.push('--write');
      const result = run('npx', args);
      if (result.status !== 0 && strict) {
        log(`[QualityGate] Biome check failed for ${filePath}`);
      }
      return;
    }

    // Fallback to prettier when installed
    const prettierArgs = ['prettier', '--check', filePath];
    if (fix) {
      prettierArgs[1] = '--write';
    }
    const prettier = run('npx', prettierArgs);
    if (prettier.status !== 0 && strict) {
      log(`[QualityGate] Prettier check failed for ${filePath}`);
    }
    return;
  }

  if (ext === '.go' && fix) {
    run('gofmt', ['-w', filePath]);
    return;
  }

  if (ext === '.py') {
    const args = ['format'];
    if (!fix) args.push('--check');
    args.push(filePath);
    const r = run('ruff', args);
    if (r.status !== 0 && strict) {
      log(`[QualityGate] Ruff check failed for ${filePath}`);
    }
  }
}

process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => {
  if (raw.length < MAX_STDIN) {
    const remaining = MAX_STDIN - raw.length;
    raw += chunk.substring(0, remaining);
  }
});

process.stdin.on('end', () => {
  try {
    const input = JSON.parse(raw);
    const filePath = String(input.tool_input?.file_path || '');
    maybeRunQualityGate(filePath);
  } catch {
    // Ignore parse errors.
  }

  process.stdout.write(raw);
});
