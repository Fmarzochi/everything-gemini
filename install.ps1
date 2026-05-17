#!/usr/bin/env pwsh
# install.ps1 — Windows-native entrypoint for the EGC installer.
#
# This wrapper resolves the real repo/package root when invoked through a
# symlinked path, then delegates to the Node-based installer runtime.
# Runtime paths derive from the wrapper location, never from the cwd.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Fail([string]$Message) {
    Write-Error "[EGC] ERROR: $Message"
    exit 1
}

$scriptPath = $PSCommandPath
if ([string]::IsNullOrEmpty($scriptPath)) { $scriptPath = $MyInvocation.MyCommand.Path }
if ([string]::IsNullOrEmpty($scriptPath)) { Fail 'install.ps1 must be invoked as a script file.' }

while ($true) {
    $item = Get-Item -LiteralPath $scriptPath -Force
    if (-not $item.LinkType) { break }

    $targetPath = $item.Target
    if ($targetPath -is [array]) { $targetPath = $targetPath[0] }
    if (-not $targetPath) { break }

    if (-not [System.IO.Path]::IsPathRooted($targetPath)) {
        $targetPath = Join-Path -Path $item.DirectoryName -ChildPath $targetPath
    }
    $scriptPath = [System.IO.Path]::GetFullPath($targetPath)
}

$scriptDir = Split-Path -Parent $scriptPath
$installerScript = Join-Path -Path (Join-Path -Path $scriptDir -ChildPath 'scripts') -ChildPath 'install-apply.js'

# --- Production-grade environment validation (fail deterministically) ---
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) { Fail 'Node.js not found in PATH. Install Node.js >= 18.' }
$nodeMajor = 0
try {
    $nodeRaw = (& node --version) -replace '^v', ''
    $nodeMajor = [int]($nodeRaw.Split('.')[0])
} catch { $nodeMajor = 0 }
if ($nodeMajor -lt 18) { Fail "Node.js >= 18 required (found: $(& node --version 2>$null))." }

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) { $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $pythonCmd) { Fail 'Python not found in PATH. Install Python >= 3.10.' }
$pyOk = 0
try {
    $pyRaw = (& $pythonCmd.Source --version 2>&1 | Out-String).Trim()
    if ($pyRaw -match '(\d+)\.(\d+)') {
        $pyMaj = [int]$matches[1]
        $pyMin = [int]$matches[2]
        if ($pyMaj -gt 3 -or ($pyMaj -eq 3 -and $pyMin -ge 10)) { $pyOk = 1 }
    }
} catch { $pyOk = 0 }
if ($pyOk -ne 1) { Fail "Python >= 3.10 required (found: $(& $pythonCmd.Source --version 2>&1))." }

# Repository-local binaries always win over host binaries.
$env:PATH = (Join-Path $scriptDir 'node_modules\.bin') + ';' + (Join-Path $scriptDir '.venv\Scripts') + ';' + $env:PATH

# Auto-install Node dependencies when running from a git clone
$nodeModules = Join-Path -Path $scriptDir -ChildPath 'node_modules'
if (-not (Test-Path -LiteralPath $nodeModules)) {
    Write-Host '[EGC] Installing dependencies...'
    Push-Location $scriptDir
    try {
        & npm install --no-audit --no-fund --loglevel=error
        if ($LASTEXITCODE -ne 0) { Fail "npm install failed with exit code $LASTEXITCODE" }
    }
    finally { Pop-Location }
}

& node $installerScript @args
exit $LASTEXITCODE
