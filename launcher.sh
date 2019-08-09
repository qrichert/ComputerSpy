#!/bin/bash
ABSPATH=$(cd "$(dirname "$0")"; pwd)
cd "$ABSPATH"
nohup python3 main.py </dev/null >/dev/null 2>&1 &
