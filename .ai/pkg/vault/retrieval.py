"""
Vault context retrieval operations.

Handles retrieving relevant vault context based on queries and scoring entries.
"""

from .file_io import load_markdown
from .io import load_vault_index
from .mapping import get_filepath_from_name
from .score import query_terms, score_entry


def retrieve_vault_context(query: str, limit: int) -> str:
    """
    Retrieve relevant vault context based on a query.

    Args:
        query: The search query.
        limit: Maximum number of files to retrieve.

    Returns:
        String containing the concatenated content of relevant files.
    """
    index = load_vault_index()

    terms = query_terms(query)
    scored: list[tuple[str, int, dict]] = []

    for name, metadata in index.get("files", index).items():
        if not isinstance(metadata, dict):
            continue

        score = score_entry(name, metadata, terms, query)
        if score > 0:
            scored.append((name, score, metadata))

    if not scored:
        # Fallback to SOUL.md when no matches
        try:
            soul_content = load_markdown("SOUL.md")
            return f"--- SOUL.md ---\n{soul_content}"
        except Exception:
            return "No relevant vault context found"

    # Sort by last_updated with oldest entries first
    selected_items = sorted(
        scored,
        key=lambda item: item[2].get("last_updated", "")
    )[:limit]

    # Print selected files
    print(
        "Selected vault context files:\n" +
        "\n".join(
            f"  {name}: {metadata.get('last_updated', 'no timestamp')}"
            for name, _score, metadata in selected_items
        )
    )

    # Load file contents
    context_parts = []
    for name, _score, metadata in selected_items:
        # Reconstruct filepath from name and type
        entry_type = metadata.get("type", "")
        filepath = get_filepath_from_name(name, entry_type)
        context_parts.append(
            f"--- {name} ---\n{load_markdown(filepath)}"
        )

    return "\n\n".join(context_parts)
