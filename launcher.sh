#!/usr/bin/env bash
ABSPATH=$(cd "$(dirname "$0")"; pwd)
nohup python3 $ABSPATH/main.py </dev/null >/dev/null 2>&1 &
