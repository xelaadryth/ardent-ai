"""
Vault context retrieval operations.

Handles retrieving relevant vault context based on queries and scoring entries.
"""

from .file_io import load_markdown
from .io import load_vault_index
from .mapping import get_filepath_from_name


def retrieve_vault_context(limit: int) -> str:
    """
    Retrieve relevant vault context.

    Args:
        limit: Maximum number of files to retrieve.

    Returns:
        String containing the newest `limit` vault files, ordered from
        oldest to newest.
    """
    index = load_vault_index()

    entries = []

    for name, metadata in index.get("files", index).items():
        if not isinstance(metadata, dict):
            continue

        if metadata:
            entries.append((name, metadata))

    if not entries:
        raise ValueError("No relevant vault context found")

    # Sort all entries by last_updated with oldest entries first.
    sorted_entries = sorted(
        entries,
        key=lambda item: item[1].get("last_updated", "")
    )

    # Take the newest `limit` entries (the last N items),
    # while preserving oldest-to-newest order.
    selected_items = sorted_entries[-limit:] if limit > 0 else []

    # Print selected files
    print(
        "Selected vault context files:\n"
        + "\n".join(
            f"  {name}: {metadata.get('last_updated', 'no timestamp')}"
            for name, metadata in selected_items
        )
    )

    # Load file contents
    context_parts = []
    for name, metadata in selected_items:
        # Reconstruct filepath from name and type
        entry_type = metadata.get("type", "")
        filepath = get_filepath_from_name(name, entry_type)
        context_parts.append(
            f"--- {name} ---\n{load_markdown(filepath)}"
        )

    return "\n\n".join(context_parts)
