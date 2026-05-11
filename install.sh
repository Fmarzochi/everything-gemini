#!/usr/bin/env bash
set -e
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validação de Versão
python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" || { echo "Python >= 3.10 requerido"; exit 1; }
node -v >/dev/null 2>&1 || { echo "Node.js requerido"; exit 1; }

# Setup Python
python3 -m venv "$PROJECT_ROOT/.venv"
"$PROJECT_ROOT/.venv/bin/pip" install --upgrade pip
"$PROJECT_ROOT/.venv/bin/pip" install -e .

# Setup Node (Yarn local)
node "$PROJECT_ROOT/.yarn/releases/yarn-4.9.2.cjs" install
EOF
