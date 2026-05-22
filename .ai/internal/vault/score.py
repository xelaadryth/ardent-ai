"""
Vault utility functions.

Provides general utility functions for text normalization, timestamps,
and index management operations.
"""

import re


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
    name_lower = name.lower()
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


def sort_by_score(items: list[tuple[str, int, dict]]) -> list[tuple[str, int, dict]]:
    """
    Sort items by score in descending order.
    
    NOTE: This function is not currently used. We're sorting by last_updated instead.
    Kept for potential future use if we want to return to score-based ranking.
    
    Args:
        items: List of tuples (name, score, metadata)
    
    Returns:
        Sorted list with highest scores first
    """
    return sorted(items, key=lambda item: item[1], reverse=True)
