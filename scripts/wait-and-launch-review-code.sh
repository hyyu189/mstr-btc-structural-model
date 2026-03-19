#!/bin/bash
set -e
cd ~/Code/mstr-paper
ROLE=$1  # "review" or "code"
PROMPT_FILE=$2

echo "⏳ [$ROLE] Waiting for theory agents to finish..."

while true; do
  # Count claude processes but exclude ourselves (grep for "TASK:" which is in theory agent prompts)
  count=$(ps aux | grep "claude --permission" | grep "TASK:" | grep -v grep | wc -l | tr -d ' ')
  if [ "$count" -eq "0" ]; then
    echo "✅ [$ROLE] All theory agents done!"
    break
  fi
  echo "   [$ROLE] $count theory agent(s) still running... waiting 20s"
  sleep 20
done

# Wait a bit more for git operations from other scripts
sleep 10

echo "📦 [$ROLE] Syncing to latest main..."
git stash 2>/dev/null || true
git checkout main 2>/dev/null || true
git pull origin main 2>/dev/null || true

# Collect any theory files from all branches
for b in theory-core greeks-etf optimal-cap optimal-cap2; do
  for f in $(git ls-tree -r --name-only "$b" 2>/dev/null | grep "theory_" || true); do
    if [ ! -f "$f" ]; then
      git show "$b:$f" > "$f" 2>/dev/null && git add "$f" && echo "  [$ROLE] Extracted $f from $b"
    fi
  done
done

git add -A 2>/dev/null
git commit -m "[$ROLE] Collect theory files" 2>/dev/null || true

echo "🚀 [$ROLE] Launching $ROLE agent..."
export PATH="/Library/TeX/texbin:$PATH"
claude --permission-mode bypassPermissions --print "$(cat "$PROMPT_FILE")"

echo "🎉 [$ROLE] Complete!"
