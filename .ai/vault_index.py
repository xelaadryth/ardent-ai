import json
import re
from pathlib import Path

from vault import load_core_context, load_markdown, VAULT_ROOT


def get_index_file() -> Path:
    return VAULT_ROOT / "vault_index.json"


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


def build_index_entry(path: Path, content: str = "") -> dict:
    summary = re.sub(r"[_\-]+", " ", path.stem).strip()
    tags = []
    tag_set = set()
    for part in path.parts[:-1]:
        cleaned = re.sub(r"^\d+\s*", "", part).strip()
        if cleaned:
            for tag in re.split(r"[^\w]+", cleaned):
                if tag:
                    tag_lower = tag.lower()
                    if tag_lower not in tag_set:
                        tags.append(tag_lower)
                        tag_set.add(tag_lower)

    links = extract_wikilinks(content)

    return {
        "summary": summary,
        "tags": tags,
        "links": links,
        "entities": []
    }


def build_index_from_disk() -> dict:
    index = {}
    for relative_path in crawl_numbered_markdown_files():
        content = load_markdown(str(relative_path))
        index[relative_path.as_posix()] = build_index_entry(relative_path, content)
    return index


def augment_index_with_disk(files: dict) -> tuple[dict, bool]:
    disk_index = build_index_from_disk()
    updated = dict(files)
    changed = False

    for path, entry in disk_index.items():
        if path not in updated:
            updated[path] = entry
            changed = True

    return updated, changed


def score_entry(path: str, entry: dict, terms: list[str], query: str) -> int:
    score = 0
    query_lower = query.lower()
    summary = str(entry.get("summary", ""))
    summary_lower = summary.lower()
    filename_lower = Path(path).name.lower()

    for tag in entry.get("tags", []):
        tag_lower = str(tag).lower()
        if any(term in tag_lower or tag_lower in term for term in terms):
            score += 5

    for link in entry.get("links", []):
        link_lower = str(link).lower()
        if any(term in link_lower or link_lower in term for term in terms) or any(term in query_lower for term in link_lower.split()):
            score += 5

    for entity in entry.get("entities", []):
        entity_lower = str(entity).lower()
        if any(term in entity_lower or entity_lower in term for term in terms) or any(term in query_lower for term in entity_lower.split()):
            score += 5

    matched_summary_terms = set()
    for term in terms:
        if term in summary_lower:
            matched_summary_terms.add(term)
    score += 3 * len(matched_summary_terms)

    for term in terms:
        if term in filename_lower:
            score += 2

    return score


def retrieve_vault_context(query: str, limit: int = 15) -> str:
    if not query or not query.strip():
        return load_core_context()

    terms = query_terms(query)
    try:
        index = load_vault_index()
    except FileNotFoundError:
        return load_core_context()

    scored = []

    for path, entry in index.items():
        if not isinstance(entry, dict):
            continue

        score = score_entry(path, entry, terms, query)
        if score > 0:
            scored.append((path, score))

    if not scored:
        return load_core_context()

    selected = [path for path, _ in sorted(scored, key=lambda item: item[1], reverse=True)[:limit]]
    
    index_metadata = {}
    for path in selected:
        if path in index:
            index_metadata[path] = index[path]
    
    context_parts = []
    context_parts.append("--- VAULT INDEX METADATA ---")
    context_parts.append(json.dumps(index_metadata, indent=2))
    context_parts.append("")
    
    for path in selected:
        content = load_markdown(path)
        if content:
            context_parts.append(f"--- {path} ---\n{content}")

    return "\n\n".join(context_parts)
