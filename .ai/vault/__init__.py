"""
Vault module - provides vault operations split by domain.

This module re-exports the public API from vault_index.py for backward compatibility.
"""

# Import from file_io module (formerly vault.py)
from vault.file_io import (
    CORE_FILES,
    VAULT_ROOT,
    load_core_context,
    load_markdown,
    read_file,
    write_file,
)

# Re-export from submodules for backward compatibility
from vault.io import current_timestamp, get_index_file, load_vault_index, save_vault_index
from vault.parser import build_index_entry, parse_frontmatter
from vault.crawler import build_index_from_disk, crawl_numbered_markdown_files
from vault.retrieval import retrieve_vault_context, score_entry
from vault.mapping import (
    get_folder_from_type,
    get_folder_prefix_for_type,
    get_filepath_from_name,
    get_filepath_from_name_and_type,
)
from vault.utilities import (
    augment_index_with_disk,
    get_oldest_indexed_files,
    get_unindexed_files,
    merge_index_entries,
    normalize_index_keys,
    normalize_text,
    query_terms,
)

__all__ = [
    # From file_io module
    "VAULT_ROOT",
    "CORE_FILES",
    "read_file",
    "write_file",
    "load_markdown",
    "load_core_context",
    # I/O
    "get_index_file",
    "load_vault_index",
    "save_vault_index",
    # Parsing
    "parse_frontmatter",
    "build_index_entry",
    # Crawling
    "crawl_numbered_markdown_files",
    "build_index_from_disk",
    # Retrieval
    "retrieve_vault_context",
    "score_entry",
    # Mapping
    "get_folder_prefix_for_type",
    "get_folder_from_type",
    "get_filepath_from_name_and_type",
    "get_filepath_from_name",
    # Utilities
    "current_timestamp",
    "normalize_text",
    "query_terms",
    "normalize_index_keys",
    "merge_index_entries",
    "augment_index_with_disk",
    "get_oldest_indexed_files",
    "get_unindexed_files",
]
