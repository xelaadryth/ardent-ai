#!/usr/bin/env python3
"""
Deterministic vault reindex script.

Rebuilds vault_index.json from frontmatter of all markdown files.
No LLM calls - purely deterministic.
"""

import json
import sys
from pathlib import Path

from vault_index import build_index_from_disk, save_vault_index, VAULT_ROOT


def main():
    print("Starting deterministic vault reindex...")
    
    try:
        # Build index from all markdown files
        index = build_index_from_disk()
        
        if not index:
            print("ERROR: No valid markdown files with frontmatter found!")
            sys.exit(1)
        
        # Save the new index
        save_vault_index({"files": index})
        
        print(f"Successfully reindexed {len(index)} files")
        print("COMMIT_MESSAGE=Ardent AI Reindex: Updated vault index from frontmatter")
        
    except Exception as exc:
        print(f"ERROR: Reindex failed: {exc}")
        sys.exit(1)


if __name__ == '__main__':
    main()
