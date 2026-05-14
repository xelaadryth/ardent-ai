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


def apply_file_operations(operations: list[dict]):
    for operation in operations:
        action = str(operation.get("action", "")).lower()
        path = operation.get("path")
        if not path:
            raise ValueError("Each operation requires a 'path'.")

        if action in {"create", "update"}:
            content = operation.get("content", "")
            write_file(path, content)
            print(f"[WRITE] {path}")
        elif action == "delete":
            file_path = os.path.join(path)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[DELETE] {path}")
        else:
            raise ValueError(f"Unsupported operation action: {action}")


def now_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def apply_index_changes(operations: list[dict]):
    try:
        current_index = {"files": load_vault_index()}
    except FileNotFoundError:
        current_index = {"files": {}}

    for operation in operations:
        action = str(operation.get("action", "")).lower()
        path = operation.get("path")
        if not path:
            continue

        if action in {"create", "update"}:
            content = operation.get("content", "")
            metadata = parse_frontmatter(content)
            if metadata:
                metadata["last_index"] = now_timestamp()
                current_index["files"][path] = metadata
                print(f"[INDEX UPDATE] {path}")
        elif action == "delete":
            current_index["files"].pop(path, None)
            print(f"[INDEX DELETE] {path}")

    save_vault_index(current_index)


def apply_response(output: str):
    payload = parse_json_output(output)

    operations = payload.get("operations", [])

    if operations:
        apply_file_operations(operations)
        apply_index_changes(operations)
