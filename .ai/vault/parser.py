"""
Vault index parsing operations.

Handles parsing frontmatter from markdown files and building index entries.
"""

import re
import yaml

from vault.io import current_timestamp


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
        Dictionary containing the index entry with name, type, status, links, tags, and last_index.
    """
    frontmatter = parse_frontmatter(content)
    
    # Extract required fields from frontmatter
    name = frontmatter.get("name", "")
    entry_type = frontmatter.get("type", "")
    links = frontmatter.get("links", [])
    tags = frontmatter.get("tags", [])
    status = frontmatter.get("status", "")
    
    # Ensure links and tags are lists
    if not isinstance(links, list):
        links = []
    if not isinstance(tags, list):
        tags = []
    
    return {
        "name": name,
        "type": entry_type,
        "status": status,
        "links": links,
        "tags": tags,
        "last_index": current_timestamp()
    }
