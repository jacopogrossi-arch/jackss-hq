#!/bin/bash
# Copia la memoria di Claude nella posizione giusta per questo Mac.
# Esegui una volta sola dopo git clone:  bash setup-mac.sh

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_KEY=$(echo "$REPO_DIR" | sed 's|/|-|g' | sed 's/^-//')
MEMORY_DEST="$HOME/.claude/projects/$PROJECT_KEY/memory"

echo "Copio la memoria in: $MEMORY_DEST"
mkdir -p "$MEMORY_DEST"
cp "$REPO_DIR/.claude/memory/"* "$MEMORY_DEST/"
echo "Fatto! Riapri Claude Code e trovi tutto."
