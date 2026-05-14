import json
import os
import re
from datetime import datetime, timezone
from vault import write_file
from vault_index import load_vault_index, save_vault_index


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


def apply_index_changes(index_updates: dict, index_deletes: list[str]):
    try:
        current_index = {"files": load_vault_index()}
    except FileNotFoundError:
        current_index = {"files": {}}

    if index_updates:
        if not isinstance(index_updates, dict):
            raise ValueError("index_updates must be an object mapping names to metadata.")
        for name, metadata in index_updates.items():
            if not isinstance(metadata, dict):
                raise ValueError("Each index metadata entry must be an object.")
            metadata["last_index"] = now_timestamp()
            current_index["files"][name] = metadata
            print(f"[INDEX UPDATE] {name}")

    if index_deletes:
        if not isinstance(index_deletes, list):
            raise ValueError("index_deletes must be a list of names.")
        for name in index_deletes:
            current_index["files"].pop(name, None)
            print(f"[INDEX DELETE] {name}")

    save_vault_index(current_index)


def apply_response(output: str):
    payload = parse_json_output(output)

    operations = payload.get("operations", [])
    index_updates = payload.get("index_updates", {})
    index_deletes = payload.get("index_deletes", [])

    if operations:
        apply_file_operations(operations)

    if index_updates or index_deletes:
        apply_index_changes(index_updates, index_deletes)
