#!/bin/bash
set -e
cd ~/Code/mstr-paper

echo "⏳ Waiting for all theory agents to finish..."

# Wait until no more claude --permission processes are running
while true; do
  count=$(ps aux | grep "claude --permission" | grep -v grep | wc -l | tr -d ' ')
  if [ "$count" -eq "0" ]; then
    echo "✅ All agents finished!"
    break
  fi
  echo "   $count agent(s) still running... waiting 30s"
  sleep 30
done

echo "📦 Collecting all theory files..."

# Find all theory tex files in the working tree
find . -name "theory_*.tex" -exec echo "Found: {}" \;

# Checkout main and merge everything
git stash 2>/dev/null || true
git checkout main

# Collect uncommitted theory files from working tree
for f in paper/sections/theory_*.tex; do
  if [ -f "$f" ]; then
    git add "$f"
    echo "Added: $f"
  fi
done

# Check all branches for theory files
for b in theory-core greeks-etf optimal-cap optimal-cap2; do
  echo "Checking branch $b..."
  for f in $(git ls-tree -r --name-only "$b" 2>/dev/null | grep "theory_" || true); do
    git show "$b:$f" > "$f" 2>/dev/null && git add "$f" && echo "  Extracted $f from $b"
  done
done

# Also grab any committed files from those branches
git merge optimal-cap2 --no-edit 2>/dev/null || git checkout --theirs . 2>/dev/null && git add -A && git commit -m "merge optimal-cap2" 2>/dev/null || true

git status
git add -A
git commit -m "Collect all theory sections before restructure" 2>/dev/null || echo "Nothing new to commit"
git push origin main 2>/dev/null || true

echo "🏗️ Launching restructure agent..."

export PATH="/Library/TeX/texbin:$PATH"
claude --permission-mode bypassPermissions --print "$(cat prompts/restructure.md)"

echo "🎉 Restructure complete!"
