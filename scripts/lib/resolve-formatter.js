/**
 * Shared formatter resolution utilities with caching.
 *
 * Extracts project-root discovery, formatter detection, and binary
 * resolution into a single module so that post-edit-format.js and
 * quality-gate.js avoid duplicating work and filesystem lookups.
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ── Caches (per-process, cleared on next hook invocation) ───────────
const projectRootCache = new Map();
const formatterCache = new Map();
const binCache = new Map();

// ── Public helpers ──────────────────────────────────────────────────

// Markers that indicate a project root (formatter configs included so
// repos without package.json are still detected correctly).
const PROJECT_ROOT_MARKERS = [
  'package.json',
  'biome.json',
  'biome.jsonc',
  '.prettierrc',
  '.prettierrc.json',
  '.prettierrc.js',
  '.prettierrc.cjs',
  '.prettierrc.mjs',
  '.prettierrc.yml',
  '.prettierrc.yaml',
  '.prettierrc.toml',
  'prettier.config.js',
  'prettier.config.cjs',
  'prettier.config.mjs'
];

/**
 * Walk up from `startDir` until a directory containing a known project
 * root marker (package.json or formatter config) is found.
 * Returns `startDir` as fallback when no marker exists above it.
 *
 * @param {string} startDir - Absolute directory path to start from
 * @returns {string} Absolute path to the project root
 */
function findProjectRoot(startDir) {
  if (projectRootCache.has(startDir)) return projectRootCache.get(startDir);

  let dir = startDir;
  while (dir !== path.dirname(dir)) {
    for (const marker of PROJECT_ROOT_MARKERS) {
      if (fs.existsSync(path.join(dir, marker))) {
        projectRootCache.set(startDir, dir);
        return dir;
      }
    }
    dir = path.dirname(dir);
  }

  projectRootCache.set(startDir, startDir);
  return startDir;
}

/**
 * Detect the formatter configured in the project.
 * Biome takes priority over Prettier.
 *
 * @param {string} projectRoot - Absolute path to the project root
 * @returns {'biome' | 'prettier' | null}
 */
function detectFormatter(projectRoot) {
  if (formatterCache.has(projectRoot)) return formatterCache.get(projectRoot);

  const biomeConfigs = ['biome.json', 'biome.jsonc'];
  for (const cfg of biomeConfigs) {
    if (fs.existsSync(path.join(projectRoot, cfg))) {
      formatterCache.set(projectRoot, 'biome');
      return 'biome';
    }
  }

  // Check package.json "prettier" key before config files
  try {
    const pkgPath = path.join(projectRoot, 'package.json');
    if (fs.existsSync(pkgPath)) {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      if ('prettier' in pkg) {
        formatterCache.set(projectRoot, 'prettier');
        return 'prettier';
      }
    }
  } catch {
    // Malformed package.json — continue to file-based detection
  }

  const prettierConfigs = [
    '.prettierrc',
    '.prettierrc.json',
    '.prettierrc.js',
    '.prettierrc.cjs',
    '.prettierrc.mjs',
    '.prettierrc.yml',
    '.prettierrc.yaml',
    '.prettierrc.toml',
    'prettier.config.js',
    'prettier.config.cjs',
    'prettier.config.mjs'
  ];
  for (const cfg of prettierConfigs) {
    if (fs.existsSync(path.join(projectRoot, cfg))) {
      formatterCache.set(projectRoot, 'prettier');
      return 'prettier';
    }
  }

  formatterCache.set(projectRoot, null);
  return null;
}

/**
 * Resolve the runner binary and prefix args for the configured package
 * manager (respects CLAUDE_PACKAGE_MANAGER env and project config).
 *
 * @param {string} projectRoot - Absolute path to the project root
 * @returns {{ bin: string, prefix: string[] }}
 */
// Windows .cmd shim mapping for cross-platform safety
const WIN_CMD_SHIMS = { npx: 'npx.cmd', pnpm: 'pnpm.cmd', yarn: 'yarn.cmd', bunx: 'bunx.cmd' };

function getRunnerFromPackageManager(projectRoot) {
  const isWin = process.platform === 'win32';
  const { getPackageManager } = require('./package-manager');
  const pm = getPackageManager({ projectDir: projectRoot });
  const execCmd = pm?.config?.execCmd || 'npx';
  const [rawBin = 'npx', ...prefix] = execCmd.split(/\s+/).filter(Boolean);
  const bin = isWin ? WIN_CMD_SHIMS[rawBin] || rawBin : rawBin;
  return { bin, prefix };
}

/**
 * Resolve the formatter binary, preferring the local node_modules/.bin
 * installation over the package manager exec command to avoid
 * package-resolution overhead.
 *
 * @param {string} projectRoot - Absolute path to the project root
 * @param {'biome' | 'prettier'} formatter - Detected formatter name
 * @returns {{ bin: string, prefix: string[] } | null}
 *   `bin`    – executable path (absolute local path or runner binary)
 *   `prefix` – extra args to prepend (e.g. ['@biomejs/biome'] when using npx)
 */
function resolveFormatterBin(projectRoot, formatter) {
  const cacheKey = `${projectRoot}:${formatter}`;
  if (binCache.has(cacheKey)) return binCache.get(cacheKey);

  const isWin = process.platform === 'win32';

  if (formatter === 'biome') {
    const localBin = path.join(projectRoot, 'node_modules', '.bin', isWin ? 'biome.cmd' : 'biome');
    if (fs.existsSync(localBin)) {
      const result = { bin: localBin, prefix: [] };
      binCache.set(cacheKey, result);
      return result;
    }
    const runner = getRunnerFromPackageManager(projectRoot);
    const result = { bin: runner.bin, prefix: [...runner.prefix, '@biomejs/biome'] };
    binCache.set(cacheKey, result);
    return result;
  }

  if (formatter === 'prettier') {
    const localBin = path.join(projectRoot, 'node_modules', '.bin', isWin ? 'prettier.cmd' : 'prettier');
    if (fs.existsSync(localBin)) {
      const result = { bin: localBin, prefix: [] };
      binCache.set(cacheKey, result);
      return result;
    }
    const runner = getRunnerFromPackageManager(projectRoot);
    const result = { bin: runner.bin, prefix: [...runner.prefix, 'prettier'] };
    binCache.set(cacheKey, result);
    return result;
  }

  // Unknown formatter — return null so callers can handle gracefully
  binCache.set(cacheKey, null);
  return null;
}

/**
 * Clear all caches. Useful for testing.
 */
function clearCaches() {
  projectRootCache.clear();
  formatterCache.clear();
  binCache.clear();
}

module.exports = {
  findProjectRoot,
  detectFormatter,
  resolveFormatterBin,
  clearCaches
};
