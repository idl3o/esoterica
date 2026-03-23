#!/bin/bash
# Post-Compact Hook: Inject vault awareness after context compression
# This fires AFTER compaction — context has been compressed.
# Reminds Claude that the memory vault exists and should be consulted.

cat <<'EOF'
MEMORY VAULT: Session context was compacted. The memory vault at
~/.claude/projects/C--Users-Sam-Documents-GitHub-esoterica/memory/
contains atomic notes with full context. MEMORY.md (already in your prompt)
is the router. Read relevant thread/pattern files to restore context for
the current work stream.
EOF
