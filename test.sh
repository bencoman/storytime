#!/bin/bash
#

git checkout scratchpad
git add .
git status

# Check for staged changes
if git diff --cached --quiet; then
  echo "No changes staged for commit."
else
  read -p "What changed? " commit_msg
  git commit -m "$commit_msg" && git push origin HEAD:refs/heads/scratchpad
fi

if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "⚠️  venv not found. Run: python3 -m venv venv"
    exit 1
fi

export PS4='$ '
echo # blank line
set -x
python3 test.py
