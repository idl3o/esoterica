#!/bin/bash
# Pre-Compact Hook: Extract session learnings before context compression
# This fires BEFORE compaction — the full conversation is still available.
#
# What this does:
# 1. Reads the transcript file passed via environment
# 2. Outputs a reminder to the compaction summary about vault updates
#
# The actual memory extraction happens via Claude's own reasoning during
# the compaction process — this hook ensures the vault is mentioned in
# the compact summary so post-compact Claude knows to check for updates.

MEMORY_DIR="$HOME/.claude/projects/C--Users-Sam-Documents-GitHub-esoterica/memory"

# Emit context that will be included in the compaction
cat <<'EOF'
MEMORY VAULT ACTIVE: Before compacting, ensure any session learnings, new patterns,
or thread updates have been written to the memory vault at:
  memory/threads/  — for new or updated work streams
  memory/patterns/ — for confirmed patterns
  memory/open/     — for new charging questions
Update MEMORY.md MOC if new files were created.
Use ADD/UPDATE/DELETE/NOOP protocol from protocol/vault-protocol.md.
EOF
