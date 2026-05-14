import json
import os
import re
import yaml
from datetime import datetime, timezone
from vault import write_file
from vault_index import load_vault_index, save_vault_index


def parse_frontmatter(content: str) -> dict:
    lines = content.split('\n')
    if lines and lines[0].strip() == '---':
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                frontmatter_str = '\n'.join(lines[1:i])
                try:
                    return yaml.safe_load(frontmatter_str) or {}
                except yaml.YAMLError:
                    return {}
    return {}


def parse_json_output(output: str) -> dict:
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", output, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def now_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


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


def apply_operations(operations: list[dict]):
    current_index = load_vault_index()

    for op in operations:
        action = op.get("action", "").lower()
        path = op.get("path")

        if not path:
            raise ValueError("Missing path")

        if action in {"create", "update"}:
            content = op.get("content", "")

            # 1. WRITE FILE
            write_file(path, content)
            print(f"[WRITE] {path}")

            # 2. PARSE FRONTMATTER
            metadata = parse_frontmatter(content) or {}

            # 3. DERIVE LINKS FROM BODY (IMPORTANT STEP)
            body_links = extract_wikilinks(content)

            # 4. MERGE LINKS (frontmatter wins if present)
            fm_links = metadata.get("links", [])
            if not isinstance(fm_links, list):
                fm_links = []

            merged_links = list(dict.fromkeys(fm_links + body_links))
            metadata["links"] = merged_links

            # 5. UPDATE INDEX
            metadata["last_index"] = now_timestamp()
            current_index["files"][path] = metadata

            print(f"[INDEX UPDATE] {path}")

        elif action == "delete":
            if os.path.exists(path):
                os.remove(path)
                print(f"[DELETE] {path}")

            current_index["files"].pop(path, None)
            print(f"[INDEX DELETE] {path}")

    save_vault_index(current_index)


def apply_response(output: str):
    payload = parse_json_output(output)

    operations = payload.get("operations", [])

    if operations:
        apply_operations(operations)
