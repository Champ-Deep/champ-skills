#!/bin/bash
# Tiered disk cleanup for Deep's Mac. Dry-run by default; --apply to execute.
# Tier A: pure regenerable caches. Tier B: regenerable with re-download cost.
# Tier C: human review only (Downloads, archives, app data, live models) - sizes only, never removed here.
set -u
APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1

run() {
  if [ "$APPLY" = 1 ]; then eval "$1"; echo "  [applied] $2"; else echo "  [dry] $2"; fi
}

echo "== before =="
df -h /System/Volumes/Data | tail -1

echo "== TIER A: pure caches (safe) =="
run "npm cache clean --force 2>/dev/null" "npm cache"
run "pnpm store prune 2>/dev/null" "pnpm store"
run "brew cleanup --prune=all 2>/dev/null" "brew old versions + cache"
run "rm -rf ~/Library/Caches/pip 2>/dev/null" "pip cache"
run "rm -rf ~/Library/Caches/Google/* 2>/dev/null" "Chrome/Google caches"

echo "== TIER B: regenerable, re-download cost (Playwright intentionally kept) =="
run "rm -rf ~/Library/Caches/camoufox/* 2>/dev/null" "camoufox browser cache, re-downloads on next use"
run "go clean -modcache 2>/dev/null" "go module cache, rebuild deps on next build"

echo "== TIER C: reviewed by Deep, never touched here =="
du -sk ~/Downloads ~/.cache/huggingface/hub/models--* 2>/dev/null | awk '{printf "  %.1fG  %s\n", $1/1048576, $2}'

echo "== after (projected if A+B applied) =="
df -h /System/Volumes/Data | tail -1
[ "$APPLY" = 1 ] && echo "verify survivors: ollama list; ls ~/.cache/huggingface/hub | grep models--; personal folders in ~/Downloads intact"