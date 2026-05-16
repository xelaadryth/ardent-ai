#!/usr/bin/env bash

set -euo pipefail

# Script is inside .quartz/, so vault root is the parent directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_ROOT="$(dirname "$SCRIPT_DIR")"
CONTENT_DIR="$SCRIPT_DIR/content"

echo "Vault root: $VAULT_ROOT"
echo "Content dir: $CONTENT_DIR"

# Clean and recreate content directory
rm -rf "$CONTENT_DIR"
mkdir -p "$CONTENT_DIR"

# Collect folders for homepage
FOLDERS=()

# Process all directories in vault root
for dir in "$VAULT_ROOT"/*/; do
  # Skip hidden folders (like .quartz itself)
  [[ "$dir" =~ /\. ]] && continue
  
  base="$(basename "$dir")"

  if [[ "$base" =~ ^[0-9]{2}\ .+ ]]; then
    echo "Copying: $base"
    cp -r "$dir" "$CONTENT_DIR/$base"
    FOLDERS+=("$base")
  fi
done

# Also copy Dashboards folder even though it doesn't have a numbered prefix
if [ -d "$VAULT_ROOT/Dashboards" ]; then
  echo "Copying: Dashboards"
  cp -r "$VAULT_ROOT/Dashboards" "$CONTENT_DIR/Dashboards"
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
    echo "- [[$f/]]"
  done

} > "$INDEX_FILE"

echo "Done. Folders added to homepage: ${FOLDERS[*]}"
