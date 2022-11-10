#!/usr/bin/env bash

cd "$(dirname "$0")"

VENV=tmp_env

if [[ ! -d "$VENV" ]]; then
    python3 -m venv "$VENV"
    . "$VENV"/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    . "$VENV"/bin/activate
fi

rm .gitignore
rm *.php
rm *.md
rm *.txt
rm dry_run.sh

nohup python3 main.py < /dev/null > /dev/null 2>&1 &

clear
