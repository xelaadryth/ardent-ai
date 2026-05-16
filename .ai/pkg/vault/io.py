"""
Vault index I/O operations.

Handles loading and saving the vault index file.
"""

import json
from pathlib import Path

from .file_io import AI_FOLDER


def get_index_file() -> Path:
    """Get the path to the vault index file."""
    return AI_FOLDER / "vault_index.json"


def load_vault_index() -> dict:
    """
    Load the vault index from disk.
    
    Returns:
        Dictionary containing the vault index with a 'files' key.
    
    Raises:
        FileNotFoundError: If vault_index.json does not exist.
        ValueError: If the index file is malformed.
    """
    index_file = get_index_file()
    if not index_file.exists():
        raise FileNotFoundError("vault_index.json is required for retrieval but was not found.")

    with index_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict) or "files" not in data or not isinstance(data["files"], dict):
        raise ValueError("vault_index.json must contain a top-level 'files' object.")

    return data


def save_vault_index(data: dict):
    """
    Save the vault index to disk.
    
    Args:
        data: Dictionary containing the vault index data.
    """
    index_file = get_index_file()
    with index_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
