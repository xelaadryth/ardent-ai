#!/usr/bin/env bash

set -euo pipefail

VAULT_ROOT="$(cd .. && pwd)"
CONTENT_DIR="content"

echo "Vault root: $VAULT_ROOT"

rm -rf "$CONTENT_DIR"
mkdir -p "$CONTENT_DIR"

# Collect folders for homepage
FOLDERS=()

for dir in "$VAULT_ROOT"/*/; do
  base="$(basename "$dir")"

  if [[ "$base" =~ ^[0-9]{2}\ .+ ]]; then
    echo "Linking: $base"
    ln -s "$dir" "$CONTENT_DIR/$base"
    FOLDERS+=("$base")
  fi
done

# Also link Dashboards folder even though it doesn't have a numbered prefix
if [ -d "$VAULT_ROOT/Dashboards" ]; then
  echo "Linking: Dashboards"
  ln -s "$VAULT_ROOT/Dashboards" "$CONTENT_DIR/Dashboards"
  FOLDERS+=("Dashboards")
fi

# Build homepage
INDEX_FILE="$CONTENT_DIR/index.md"

echo "Generating homepage at $INDEX_FILE"

{
  echo "---"
  echo "title: Home"
  echo "---"
  echo ""
  echo "# Vault Index"
  echo ""
  echo "## Browse"
  echo ""

  for f in "${FOLDERS[@]}"; do
    # Escape closing brackets if needed (rare but safe)
    echo "- [[$f/]]"
  done

} > "$INDEX_FILE"

echo "Done."