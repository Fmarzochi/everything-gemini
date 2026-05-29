'use strict';

let validateCommand;
let validateWrite;
let isProtectedPath;

const ready = import('../mcp/servers/egc-guardian/build/validator.js').then((mod) => {
  validateCommand = mod.validateCommand;
  validateWrite = mod.validateWrite;
  isProtectedPath = mod.isProtectedPath;
});

module.exports.fuzz = async function (data) {
  await ready;

  const input = data.toString('utf-8');

  try { validateCommand(input); } catch (_) {}
  try { validateWrite(input); } catch (_) {}
  try { isProtectedPath(input); } catch (_) {}

  try { validateCommand('\x00' + input); } catch (_) {}
  try { validateWrite('../../../etc/passwd' + input); } catch (_) {}
  try { validateCommand('cat ~/' + input); } catch (_) {}
};
