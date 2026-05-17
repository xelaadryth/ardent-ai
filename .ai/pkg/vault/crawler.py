"""
Vault file crawling operations.

Handles crawling the vault for markdown files and building the index from disk.
"""

from pathlib import Path

from .file_io import VAULT_ROOT, load_markdown
from .parser import build_index_entry


def crawl_numbered_markdown_files() -> list[Path]:
    """
    Crawl the vault for numbered markdown files.

    Returns:
        List of relative paths to markdown files in numbered folders.
    """
    print(f"Crawling VAULT_ROOT: {VAULT_ROOT}")
    files = []

    for path in VAULT_ROOT.rglob("*.md"):
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

    print(f"Found {len(files)} files")

    return sorted(files)


def build_index() -> dict:
    """
    Build the vault index by crawling all markdown files on disk.
    
    Returns:
        Dictionary mapping document names to index entries.
    """
    index = {}
    for relative_path in crawl_numbered_markdown_files():
        content = load_markdown(str(relative_path))
        entry = build_index_entry(content)
        index[entry["name"]] = relative_path.stem()
    return index
