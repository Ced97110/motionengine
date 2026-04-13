#!/bin/bash
# Ingest all 9 PDFs sequentially (avoids index.md race conditions)
# Usage: ANTHROPIC_API_KEY=sk-... bash scripts/ingest-all.sh

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "Error: ANTHROPIC_API_KEY not set"
  exit 1
fi

PDFS=(
  knowledge-base/raw/basketball-for-coaches.pdf
  knowledge-base/raw/basketball-shooting.pdf
  knowledge-base/raw/basketball-anatomy.pdf
  knowledge-base/raw/offensive-skill-development.pdf
  knowledge-base/raw/lets-talk-defense.pdf
  knowledge-base/raw/speed-agility-quickness.pdf
  knowledge-base/raw/footwork-balance-pivoting.pdf
  knowledge-base/raw/explosive-calisthenics.pdf
  knowledge-base/raw/nba-coaches-playbook.pdf
)

echo ""
echo "🏀 Ingesting ${#PDFS[@]} books sequentially..."
echo "   Estimated time: ~60-90 minutes"
echo ""

TOTAL=${#PDFS[@]}
DONE=0
FAILED=0

for pdf in "${PDFS[@]}"; do
  DONE=$((DONE + 1))
  name=$(basename "$pdf" .pdf)
  echo "════════════════════════════════════════"
  echo "[$DONE/$TOTAL] $name"
  echo "════════════════════════════════════════"

  if npx tsx scripts/ingest.ts "$pdf"; then
    echo "  ✅ $name complete"
  else
    echo "  ❌ $name failed"
    FAILED=$((FAILED + 1))
  fi
  echo ""
done

echo "════════════════════════════════════════"
if [ $FAILED -eq 0 ]; then
  echo "✅ All $TOTAL books ingested successfully"
else
  echo "⚠  $FAILED/$TOTAL books had errors"
fi

WIKI_COUNT=$(ls -1 knowledge-base/wiki/*.md 2>/dev/null | grep -v index.md | grep -v log.md | wc -l | xargs)
echo "   Wiki pages generated: $WIKI_COUNT"
echo "════════════════════════════════════════"
