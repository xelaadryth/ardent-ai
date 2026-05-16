"""
Vault index I/O operations.

Handles loading and saving the vault index file.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from vault.file_io import AI_FOLDER, VAULT_ROOT


def current_timestamp() -> str:
    """
    Get current UTC timestamp in ISO format.
    
    Returns:
        Current timestamp as ISO string without microseconds.
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


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
    print(f"[DEBUG] Looking for vault_index.json at: {index_file}")
    print(f"[DEBUG] Absolute path: {index_file.resolve()}")
    print(f"[DEBUG] Exists: {index_file.exists()}")
    if not index_file.exists():
        raise FileNotFoundError(f"vault_index.json is required for retrieval but was not found. Looked for: {index_file}")

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
