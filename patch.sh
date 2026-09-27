#!/usr/bin/env bash
# Antigravity Smart RTL - macOS & Linux Launcher
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCH_PY="$SCRIPT_DIR/src/patcher.py"
if [ ! -f "$PATCH_PY" ]; then
    PATCH_PY="$SCRIPT_DIR/patcher.py"
fi

PATCH_JS="$SCRIPT_DIR/src/patcher.js"
if [ ! -f "$PATCH_JS" ]; then
    PATCH_JS="$SCRIPT_DIR/patcher.js"
fi

# 1. Try python3
if command -v python3 >/dev/null 2>&1; then
    exec python3 "$PATCH_PY" "$@"
fi

# 2. Try python
if command -v python >/dev/null 2>&1; then
    exec python "$PATCH_PY" "$@"
fi

# 3. Try node
if command -v node >/dev/null 2>&1; then
    exec node "$PATCH_JS" "$@"
fi

echo "[-] Error: Neither Python 3 nor Node.js was found on this system."
echo "Please install Python 3 (https://www.python.org) or Node.js (https://nodejs.org)."
exit 1
