import json
import re
from datetime import datetime, timezone
from pathlib import Path
import yaml

from vault import load_core_context, load_markdown, VAULT_ROOT


def get_index_file() -> Path:
    return VAULT_ROOT / "vault_index.json"


def current_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def load_vault_index() -> dict:
    index_file = get_index_file()
    if not index_file.exists():
        disk_files = build_index_from_disk()
        if disk_files:
            save_vault_index({"files": disk_files})
            return disk_files
        raise FileNotFoundError("vault_index.json is required for retrieval but was not found.")

    with index_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict) or "files" not in data or not isinstance(data["files"], dict):
        raise ValueError("vault_index.json must contain a top-level 'files' object.")

    files = data["files"]
    if not files:
        disk_files = build_index_from_disk()
        if disk_files:
            data["files"] = disk_files
            save_vault_index(data)
            return disk_files
        return files

    augmented_files, changed = augment_index_with_disk(files)
    if changed:
        data["files"] = augmented_files
        save_vault_index(data)
    return augmented_files


def save_vault_index(data: dict):
    index_file = get_index_file()
    with index_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def query_terms(query: str) -> list[str]:
    return [term for term in normalize_text(query).split() if term]


def crawl_numbered_markdown_files() -> list[Path]:
    files = []
    for path in VAULT_ROOT.rglob("*.md"):
        if path == get_index_file():
            continue

        relative_path = path.relative_to(VAULT_ROOT)
        folder_parts = relative_path.parts[:-1]
        if any(re.match(r"^\d+", part) for part in folder_parts):
            files.append(relative_path)

    return sorted(files)


def get_folder_prefix_for_type(entry_type: str) -> str:
    """Map entry type to folder prefix."""
    type_to_prefix = {
        "core": "",
        "template": "00 Templates",
        "player": "02 Players",
        "npc": "03 NPCs",
        "session": "04 Sessions",
        "faction": "05 Factions",
        "location": "06 Locations",
        "hook": "07 Hooks",
        "scene": "08 Scenes",
        "item": "09 Items",
        "lore": "10 Lore",
        "spren": "31 Spren"
    }
    return type_to_prefix.get(entry_type, "")


def get_folder_from_type(entry_type: str) -> str:
    """Return the folder path for a vault entry type."""
    return get_folder_prefix_for_type(entry_type)


def get_filepath_from_name_and_type(name: str, entry_type: str) -> str:
    """Reconstruct filepath from name and type."""
    prefix = get_folder_from_type(entry_type)
    if prefix:
        return f"{prefix}/{name}.md"
    else:
        return f"{name}.md"


def extract_wikilinks(content: str) -> list[str]:
    wikilinks = re.findall(r"\[\[([^\]]+)\]\]", content)
    normalized = []
    seen = set()
    for link in wikilinks:
        lower = link.lower().strip()
        if lower and lower not in seen:
            normalized.append(link.strip())
            seen.add(lower)
    return normalized


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content."""
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not frontmatter_match:
        return {}
    
    try:
        return yaml.safe_load(frontmatter_match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def build_index_entry(path: Path, content: str = "") -> dict:
    frontmatter = parse_frontmatter(content)
    
    # Extract required fields from frontmatter
    name = frontmatter.get("name", "")
    entry_type = frontmatter.get("type", "")
    links = frontmatter.get("links", [])
    tags = frontmatter.get("tags", [])
    
    # Ensure links and tags are lists
    if not isinstance(links, list):
        links = []
    if not isinstance(tags, list):
        tags = []
    
    return {
        "name": name,
        "type": entry_type,
        "links": links,
        "tags": tags,
        "entities": [],
        "last_index": current_timestamp()
    }


def build_index_from_disk() -> dict:
    index = {}
    for relative_path in crawl_numbered_markdown_files():
        content = load_markdown(str(relative_path))
        entry = build_index_entry(relative_path, content)
        if entry.get("name"):
            # Use name as key instead of filepath
            index[entry["name"]] = entry
    return index


def augment_index_with_disk(files: dict) -> tuple[dict, bool]:
    disk_index = build_index_from_disk()
    updated = dict(files)
    changed = False

    for name, entry in disk_index.items():
        if name not in updated:
            updated[name] = entry
            changed = True

    return updated, changed


def score_entry(name: str, entry: dict, terms: list[str], query: str) -> int:
    score = 0
    query_lower = query.lower()
    entry_name = str(entry.get("name", ""))
    name_lower = entry_name.lower()
    entry_type = str(entry.get("type", ""))
    type_lower = entry_type.lower()
    filename_lower = name.lower()

    # Score tags from frontmatter
    for tag in entry.get("tags", []):
        tag_lower = str(tag).lower()
        if any(term in tag_lower or tag_lower in term for term in terms):
            score += 5

    # Score links from frontmatter
    for link in entry.get("links", []):
        link_lower = str(link).lower()
        if any(term in link_lower or link_lower in term for term in terms) or any(term in query_lower for term in link_lower.split()):
            score += 5

    # Score body wikilinks
    for link in entry.get("body_links", []):
        link_lower = str(link).lower()
        if any(term in link_lower or link_lower in term for term in terms) or any(term in query_lower for term in link_lower.split()):
            score += 3

    # Score type matches
    if any(term in type_lower for term in terms):
        score += 4

    entities = entry.get("entities", [])
    if len(entities) == 0:
        # Mark unindexed entries
        score += 1
    for entity in entities:
        entity_lower = str(entity).lower()
        if any(term in entity_lower or entity_lower in term for term in terms) or any(term in query_lower for term in entity_lower.split()):
            score += 5

    # Score name matches
    matched_name_terms = set()
    for term in terms:
        if term in name_lower:
            matched_name_terms.add(term)
    score += 3 * len(matched_name_terms)

    # Score filename matches
    for term in terms:
        if term in filename_lower:
            score += 2

    return score


def retrieve_vault_context(query: str, limit: int = 10) -> str:
    if not query or not query.strip():
        return load_core_context()

    terms = query_terms(query)
    try:
        index = load_vault_index()
    except FileNotFoundError:
        return load_core_context()

    scored = []

    for name, entry in index.items():
        if not isinstance(entry, dict):
            continue

        score = score_entry(name, entry, terms, query)
        if score > 0:
            scored.append((name, score))

    if not scored:
        return load_core_context()

    selected = [name for name, _ in sorted(scored, key=lambda item: item[1], reverse=True)[:limit]]
    
    index_metadata = {}
    for name in selected:
        if name in index:
            index_metadata[name] = index[name]
    
    context_parts = []
    context_parts.append("--- VAULT INDEX METADATA ---")
    context_parts.append(json.dumps(index_metadata, indent=2))
    context_parts.append("")
    
    for name in selected:
        entry = index[name]
        filepath = get_filepath_from_name_and_type(name, entry.get("type", ""))
        content = load_markdown(filepath)
        if content:
            context_parts.append(f"--- {filepath} ---\n{content}")

    return "\n\n".join(context_parts)
