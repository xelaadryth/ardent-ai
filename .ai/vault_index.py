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
    status = frontmatter.get("status", "")
    
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
        "status": status,
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

    # Score tags from frontmatter
    for tag in entry.get("tags", []):
        tag_lower = str(tag).lower().lstrip("#")
        if query_lower == tag_lower:
            score += 14
        elif any(term == tag_lower for term in terms):
            score += 10
        elif any(term in tag_lower or tag_lower in term for term in terms):
            score += 6

    # Score links from frontmatter
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


def retrieve_vault_context(query: str, limit: int = 10) -> str:
    """Retrieve relevant vault context based on query."""
    index = load_vault_index()
    
    terms = query_terms(query)
    scored = []

    for name, metadata in index.items():
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
        except:
            return "No relevant vault context found"

    selected = [name for name, _ in sorted(scored, key=lambda item: item[1], reverse=True)[:limit]]

    context_parts = []
    for name in selected:
        entry = index[name]
        filepath = get_filepath_from_name(name, entry.get('type', ''))
        context_parts.append(f"--- {filepath} ---\n{load_markdown(filepath)}")

    return "\n\n".join(context_parts)


def get_oldest_indexed_files(limit: int = 10) -> list[str]:
    """Get the oldest indexed files by last_index timestamp."""
    index = load_vault_index()
    entries = []

    for name, metadata in index.items():
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
    """Get files that have no entities (unindexed)."""
    index = load_vault_index()
    unindexed = []

    for name, metadata in index.items():
        if not isinstance(metadata, dict):
            continue
        entities = metadata.get('entities', [])
        if len(entities) == 0:
            unindexed.append(name)

    return unindexed


def get_filepath_from_name(name: str, file_type: str) -> str:
    """Reconstruct filepath from name and type."""
    folder = get_folder_from_type(file_type)
    if folder:
        return f"{folder}/{name}.md"
    else:
        return f"{name}.md"
