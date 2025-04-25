#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -x "$SCRIPT_DIR/.venv/bin/seog" ]]; then
    "$SCRIPT_DIR/.venv/bin/seog" "$@"
else
    poetry run seog "$@"
fi
