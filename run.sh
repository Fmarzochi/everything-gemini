#!/usr/bin/env bash
# Determina a raiz do repositório de forma absoluta, independente de CWD
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv"

# Validação de Dependências
node -v >/dev/null 2>&1 || { echo "Node.js não encontrado."; exit 1; }
python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" || { echo "Python >= 3.10 requerido."; exit 1; }

# Ajuste de PATH
export PATH="$PROJECT_ROOT/node_modules/.bin:$VENV_PATH/bin:$PATH"
export PROJECT_ROOT

# Execução do Entrypoint
exec node "$PROJECT_ROOT/scripts/egc.js" "$@"
