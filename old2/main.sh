#!/bin/bash
#

source venv/bin/activate

git push origin HEAD:refs/heads/scratchcopy --force

python3 main.py
