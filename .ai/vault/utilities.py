"""
Vault utility functions.

Provides general utility functions for text normalization, timestamps,
and index management operations.
"""

import re
from datetime import datetime, timezone

from vault.crawler import build_index_from_disk
from vault.io import load_vault_index, save_vault_index
from vault.mapping import get_filepath_from_name


def normalize_text(value: str) -> str:
    """
    Normalize text for comparison.
    
    Args:
        value: Text to normalize.
    
    Returns:
        Normalized lowercase text with special characters replaced by spaces.
    """
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def query_terms(query: str) -> list[str]:
    """
    Extract normalized query terms from a query string.
    
    Args:
        query: The query string.
    
    Returns:
        List of normalized query terms.
    """
    return [term for term in normalize_text(query).split() if term]


def normalize_index_keys(files: dict) -> tuple[dict, bool]:
    """
    Ensure all index keys are full relative filepaths.
    
    Args:
        files: Dictionary of index entries.
    
    Returns:
        Tuple of (normalized dict, changed flag).
    """
    normalized = {}
    changed = False

    for key, entry in files.items():
        if not isinstance(entry, dict):
            normalized[key] = entry
            continue

        normalized_key = key
        if isinstance(key, str):
            path = re.sub(r'\.md$', '', key) if key.endswith('.md') else key
            if path != key:
                normalized_key = path
                changed = True
            if not entry.get("name"):
                entry["name"] = path
                changed = True
        else:
            name = str(entry.get("name", "")).strip()
            entry_type = str(entry.get("type", ""))
            if name:
                normalized_key = get_filepath_from_name(name, entry_type)
                if normalized_key != key:
                    changed = True

        if normalized_key in normalized:
            normalized[normalized_key] = merge_index_entries(normalized[normalized_key], entry)
        else:
            normalized[normalized_key] = entry

    return normalized, changed


def merge_index_entries(existing: dict, new_entry: dict) -> dict:
    """
    Choose the most up-to-date index entry when duplicate names occur.
    
    Args:
        existing: The existing index entry.
        new_entry: The new index entry to merge.
    
    Returns:
        The more up-to-date entry.
    """
    if existing == new_entry:
        return existing

    existing_last = existing.get("last_index", "")
    new_last = new_entry.get("last_index", "")
    try:
        if existing_last and new_last:
            existing_dt = datetime.fromisoformat(existing_last.replace("Z", "+00:00"))
            new_dt = datetime.fromisoformat(new_last.replace("Z", "+00:00"))
            return new_entry if new_dt > existing_dt else existing
    except ValueError:
        pass

    return new_entry if len(new_entry) > len(existing) else existing


def augment_index_with_disk(files: dict) -> tuple[dict, bool]:
    """
    Augment the index with data from disk.
    
    Args:
        files: Current index dictionary.
    
    Returns:
        Tuple of (augmented dict, changed flag).
    """
    files, normalized = normalize_index_keys(files)
    updated = dict(files)
    changed = normalized

    disk_index = build_index_from_disk()
    for filepath, entry in disk_index.items():
        if filepath not in updated or updated[filepath] != entry:
            updated[filepath] = entry
            changed = True

    return updated, changed


def get_oldest_indexed_files(limit: int = 10) -> list[str]:
    """
    Get the oldest indexed files by last_index timestamp.
    
    Args:
        limit: Maximum number of files to return.
    
    Returns:
        List of file paths sorted by oldest last_index timestamp.
    """
    index = load_vault_index()
    entries = []

    for name, metadata in index["files"].items():
        if not isinstance(metadata, dict):
            continue
        last_index = metadata.get('last_index', '')
        if last_index:
            try:
                timestamp = datetime.fromisoformat(last_index.replace('Z', '+00:00')).timestamp()
                entries.append((name, timestamp))
            except ValueError:
                # Invalid timestamp, treat as very old
                entries.append((name, 0.0))

    entries.sort(key=lambda item: item[1])
    return [name for name, _ in entries[:limit]]


def get_unindexed_files() -> list[str]:
    """
    Get files that have no entities (unindexed).
    
    Returns:
        List of file paths with no entities.
    """
    index = load_vault_index()
    unindexed = []

    for name, metadata in index.items():
        if not isinstance(metadata, dict):
            continue
        entities = metadata.get('entities', [])
        if len(entities) == 0:
            unindexed.append(name)

    return unindexed
