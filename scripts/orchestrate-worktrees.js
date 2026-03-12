#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const {
  buildOrchestrationPlan,
  executePlan,
  materializePlan
} = require('./lib/tmux-worktree-orchestrator');

function usage() {
  console.log([
    'Usage:',
    '  node scripts/orchestrate-worktrees.js <plan.json> [--execute]',
    '  node scripts/orchestrate-worktrees.js <plan.json> [--write-only]',
    '',
    'Placeholders supported in launcherCommand:',
    '  Shell-safe defaults: {worker_name} {worker_slug} {session_name} {repo_root}',
    '  Shell-safe defaults: {worktree_path} {branch_name} {task_file} {handoff_file} {status_file}',
    '  Raw variants: {worker_name_raw} {worker_slug_raw} {session_name_raw} {repo_root_raw}',
    '  Raw variants: {worktree_path_raw} {branch_name_raw} {task_file_raw} {handoff_file_raw} {status_file_raw}',
    '  Explicit shell-safe aliases also exist with the _sh suffix.',
    '',
    'Without flags the script prints a dry-run plan only.'
  ].join('\n'));
}

function parseArgs(argv) {
  const args = argv.slice(2);
  const planPath = args.find(arg => !arg.startsWith('--'));
  return {
    execute: args.includes('--execute'),
    planPath,
    writeOnly: args.includes('--write-only')
  };
}

function loadPlanConfig(planPath) {
  const absolutePath = path.resolve(planPath);
  const raw = fs.readFileSync(absolutePath, 'utf8');
  const config = JSON.parse(raw);
  config.repoRoot = config.repoRoot || process.cwd();
  return { absolutePath, config };
}

function printDryRun(plan, absolutePath) {
  const preview = {
    planFile: absolutePath,
    sessionName: plan.sessionName,
    repoRoot: plan.repoRoot,
    coordinationDir: plan.coordinationDir,
    workers: plan.workerPlans.map(worker => ({
      workerName: worker.workerName,
      branchName: worker.branchName,
      worktreePath: worker.worktreePath,
      seedPaths: worker.seedPaths,
      taskFilePath: worker.taskFilePath,
      handoffFilePath: worker.handoffFilePath,
      launchCommand: worker.launchCommand
    })),
    commands: [
      ...plan.workerPlans.map(worker => worker.gitCommand),
      ...plan.tmuxCommands.map(command => [command.cmd, ...command.args].join(' '))
    ]
  };

  console.log(JSON.stringify(preview, null, 2));
}

function main() {
  const { execute, planPath, writeOnly } = parseArgs(process.argv);

  if (!planPath) {
    usage();
    process.exit(1);
  }

  const { absolutePath, config } = loadPlanConfig(planPath);
  const plan = buildOrchestrationPlan(config);

  if (writeOnly) {
    materializePlan(plan);
    console.log(`Wrote orchestration files to ${plan.coordinationDir}`);
    return;
  }

  if (!execute) {
    printDryRun(plan, absolutePath);
    return;
  }

  const result = executePlan(plan);
  console.log([
    `Started tmux session '${result.sessionName}' with ${result.workerCount} worker panes.`,
    `Coordination files: ${result.coordinationDir}`,
    `Attach with: tmux attach -t ${result.sessionName}`
  ].join('\n'));
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(`[orchestrate-worktrees] ${error.message}`);
    process.exit(1);
  }
}

module.exports = { main };
