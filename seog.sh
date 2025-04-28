#!/bin/bash

REAL_SCRIPT_PATH=$(readlink -f "${BASH_SOURCE[0]}")
SCRIPT_DIR=$(dirname "$REAL_SCRIPT_PATH")

cd "$SCRIPT_DIR" || exit 1

if [[ -x "$SCRIPT_DIR/.venv/bin/seog" ]]; then
    "$SCRIPT_DIR/.venv/bin/seog" "$@"
elif [[ -f "$SCRIPT_DIR/pyproject.toml" ]]; then
    poetry run seog "$@"
else
    echo "Error: Neither virtualenv nor poetry project found!" >&2
    exit 2
fi