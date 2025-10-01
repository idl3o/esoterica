#!/bin/bash
# Esoterica CLI Launcher

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the Python CLI
python3 "$SCRIPT_DIR/cli/esoterica.py" "$@"
