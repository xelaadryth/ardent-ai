"""
Vault index parsing operations.

Handles parsing frontmatter from markdown files and building index entries.
"""

import re
import yaml
from datetime import datetime


def extract_wikilinks(content: str) -> list[str]:
    """
    Extract Obsidian-style wikilinks from markdown content.
    
    Args:
        content: Markdown content string.
    
    Returns:
        List of normalized wikilinks in the format [[link]].
    """
    raw_links = re.findall(r"\[\[([^\]]+)\]\]", content)

    normalized = []
    seen = set()

    for link in raw_links:
        cleaned = link.strip()
        key = cleaned.lower()

        if key and key not in seen:
            normalized.append(f"[[{cleaned}]]")
            seen.add(key)

    return normalized


def parse_frontmatter(content: str) -> dict:
    """
    Parse YAML frontmatter from markdown content.
    
    Args:
        content: Markdown content string.
    
    Returns:
        Dictionary containing the parsed frontmatter, or empty dict if none found.
    """
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not frontmatter_match:
        return {}
    
    try:
        return yaml.safe_load(frontmatter_match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def build_index_entry(content: str = "") -> dict:
    """
    Build an index entry from markdown content.
    
    Args:
        content: Markdown content string with frontmatter.
    
    Returns:
        Dictionary containing the index entry with name, type, status, links, tags, and last_updated.
    """
    frontmatter = parse_frontmatter(content)
    
    # Extract required fields from frontmatter
    entry_type = frontmatter.get("type", "")
    tags = frontmatter.get("tags", [])
    status = frontmatter.get("status", "")
    
    # Extract wikilinks from body content
    links = extract_wikilinks(content)
    
    # Ensure tags is a list
    if not isinstance(tags, list):
        tags = []
    
    # Preserve existing last_updated from frontmatter, don't auto-update on reindex
    last_updated = frontmatter.get("last_updated", "")
    # Convert datetime objects to ISO format strings (YAML parses timestamps as datetime)
    if isinstance(last_updated, datetime):
        last_updated = last_updated.isoformat()
    
    return {
        "type": entry_type,
        "status": status,
        "links": links,
        "tags": tags,
        "last_updated": last_updated
    }
