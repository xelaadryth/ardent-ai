"""
Vault file crawling operations.

Handles crawling the vault for markdown files and building the index from disk.
"""

import re
from pathlib import Path

from vault.file_io import VAULT_ROOT, load_markdown
from vault.io import get_index_file
from vault.parser import build_index_entry


def crawl_numbered_markdown_files() -> list[Path]:
    """
    Crawl the vault for numbered markdown files.

    Returns:
        List of relative paths to markdown files in numbered folders.
    """
    files = []

    for path in VAULT_ROOT.rglob("*.md"):
        if path == get_index_file():
            continue

        relative_path = path.relative_to(VAULT_ROOT)
        parts = relative_path.parts

        # skip root-level markdown files
        if len(parts) < 2:
            continue

        # ignore any hidden folders anywhere in the path
        if any(part.startswith(".") for part in parts):
            continue

        top_folder = parts[0]

        # only include top-level numbered folders (e.g. "02 Players")
        if top_folder[:2].isdigit():
            files.append(relative_path)

    return sorted(files)


def build_index_from_disk() -> dict:
    """
    Build the vault index by crawling all markdown files on disk.
    
    Returns:
        Dictionary mapping file paths to index entries.
    """
    index = {}
    for relative_path in crawl_numbered_markdown_files():
        content = load_markdown(str(relative_path))
        entry = build_index_entry(content)
        if entry.get("name"):
            filepath = relative_path.as_posix()
            index[filepath] = entry
    return index
