$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VENV_PATH = Join-Path $PROJECT_ROOT ".venv"

# Validação (Simples)
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { Write-Error "Node.js requerido"; exit 1 }

# Ajuste de PATH local
$env:PATH = (Join-Path $PROJECT_ROOT "node_modules\.bin") + ";" + (Join-Path $VENV_PATH "Scripts") + ";" + $env:PATH
$env:PROJECT_ROOT = $PROJECT_ROOT

# Execução
node (Join-Path $PROJECT_ROOT "scripts\egc.js") @args
