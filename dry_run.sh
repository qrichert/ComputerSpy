#!/usr/bin/env bash

cd "$(dirname "$0")"

echo "Installing dependencies..."

VENV=tmp_env

if [[ ! -d "$VENV" ]]; then
    python3 -m venv "$VENV"
    . "$VENV"/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    . "$VENV"/bin/activate
fi

clear

echo "Checking authorizations..."
echo "Make sure to click 'Allow screen recording' if asked."
echo "If not, it's probably OK, wait a few seconds and exit."
echo ""
echo "Press Ctrl+C or Cmd+Shift+. to exit."

python3 main.py
