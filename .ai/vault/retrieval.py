"""
Vault context retrieval operations.

Handles retrieving relevant vault context based on queries and scoring entries.
"""

from vault.file_io import load_markdown
from vault.io import load_vault_index
from vault.mapping import get_filepath_from_name
from vault.utilities import query_terms


def score_entry(name: str, entry: dict, terms: list[str], query: str) -> int:
    """
    Score a vault entry for relevance to a query.
    
    Args:
        name: The entry name (filepath).
        entry: The index entry dictionary.
        terms: List of normalized query terms.
        query: The original query string.
    
    Returns:
        Relevance score (higher is more relevant).
    """
    score = 0
    query_lower = query.lower().strip()
    entry_name = str(entry.get("name", ""))
    name_lower = entry_name.lower()
    entry_type = str(entry.get("type", ""))
    type_lower = entry_type.lower()
    filename_lower = name.lower()
    status = str(entry.get("status", "")).lower()

    # Exact phrase and name matches should rank highest.
    if name_lower and query_lower == name_lower:
        score += 25
    if name_lower and name_lower in query_lower:
        score += 12
    if query_lower and query_lower in name_lower:
        score += 10

    # Score tags from index
    for tag in entry.get("tags", []):
        tag_lower = str(tag).lower().lstrip("#")
        if query_lower == tag_lower:
            score += 14
        elif any(term == tag_lower for term in terms):
            score += 10
        elif any(term in tag_lower or tag_lower in term for term in terms):
            score += 6

    # Score links from index
    for link in entry.get("links", []):
        link_lower = str(link).lower().strip("[]# ")
        if query_lower == link_lower:
            score += 12
        elif any(term == link_lower for term in terms):
            score += 8
        elif any(term in link_lower or link_lower in term for term in terms):
            score += 5

    # Score type matches
    if type_lower:
        if query_lower == type_lower:
            score += 10
        elif any(term == type_lower for term in terms):
            score += 7
        elif any(term in type_lower or type_lower in term for term in terms):
            score += 4

    # Score status matches
    if status:
        if query_lower == status:
            score += 8
        elif any(term == status for term in terms):
            score += 5
        elif any(term in status or status in term for term in terms):
            score += 3

    # Score name token overlap
    for term in terms:
        if term and term in name_lower:
            score += 4
        if term and term in filename_lower:
            score += 2

    # Small boost for multi-term coverage
    matched_terms = sum(1 for term in terms if term and (term in name_lower or term in type_lower or term in status or any(term in str(tag).lower() for tag in entry.get("tags", [])) or any(term in str(link).lower() for link in entry.get("links", []))))
    score += matched_terms

    return score


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
    scored: list[tuple[str, int]] = []

    for name, metadata in index.get("files", index).items():
        if not isinstance(metadata, dict):
            continue

        score = score_entry(name, metadata, terms, query)
        if score > 0:
            scored.append((name, score))

    if not scored:
        # Fallback to SOUL.md when no matches
        try:
            soul_content = load_markdown("SOUL.md")
            return f"--- SOUL.md ---\n{soul_content}"
        except Exception:
            return "No relevant vault context found"

    # Sort by score descending and take top N
    selected_items = sorted(
        scored,
        key=lambda item: item[1],
        reverse=True
    )[:limit]

    # Print selected files with scores
    print(
        "Selected vault context files:\n" +
        "\n".join(
            f"  {name}: {score}"
            for name, score in selected_items
        )
    )

    # Load file contents
    context_parts = []
    for name, _score in selected_items:
        # Reconstruct filepath from name and type
        entry_type = index.get("files", index).get(name, {}).get("type", "")
        filepath = get_filepath_from_name(name, entry_type)
        context_parts.append(
            f"--- {name} ---\n{load_markdown(filepath)}"
        )

    return "\n\n".join(context_parts)
