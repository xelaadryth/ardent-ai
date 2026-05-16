import json
import os
import re
import yaml
from datetime import datetime, timezone
from pkg.vault.file_io import write_file
from pkg.vault.mapping import get_filepath_from_name


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
    output = output.strip()
    
    # If the json output is wrapped in a code block, extract it
    if output.startswith("```") and output.endswith("```"):
        # Remove opening marker (with or without language tag)
        first_newline = output.find("\n")
        if first_newline != -1:
            output = output[first_newline + 1:]  # Skip past first newline
        else:
            output = output[3:]  # Just strip the opening backticks
        output = output[:-3].strip()  # Strip closing backticks

    try:
        return json.loads(output, strict=False)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", output, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0), strict=False)


def now_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def apply_operations(operations: list[dict], current_index: dict):
    for op in operations:
        action = op.get("action", "").lower()
        name = op.get("name")

        if not name:
            raise ValueError("Missing name")

        if action in {"create", "update"}:
            content = op.get("content", "")

            # 1. PARSE FRONTMATTER TO GET TYPE
            metadata = parse_frontmatter(content) or {}
            entry_type = metadata.get("type", "")

            if not entry_type:
                raise ValueError(f"Missing type in frontmatter for {name}")

            # 2. RECONSTRUCT PATH FROM NAME AND TYPE
            path = get_filepath_from_name(name, entry_type)

            # 3. WRITE FILE
            write_file(path, content)
            print(f"[WRITE] {path}")

            # 4. ENSURE LINKS IS A LIST
            links = metadata.get("links", [])
            if not isinstance(links, list):
                links = []
            metadata["links"] = links

        elif action == "delete":
            # LOOK UP EXISTING ENTRY BY NAME
            if name not in current_index.get("files", {}):
                print(f"[DELETE] {name} not found in index, skipping")
                continue

            # RECONSTRUCT PATH FROM NAME AND TYPE
            entry = current_index["files"][name]
            entry_type = entry.get("type", "")
            path = get_filepath_from_name(name, entry_type)

            if os.path.exists(path):
                os.remove(path)
                print(f"[DELETE] {path}")

        else:
            raise ValueError(f"Unsupported operation action: {action}")


def apply_response(output: str, current_index: dict):
    payload = parse_json_output(output)

    operations = payload.get("operations", [])

    if operations:
        apply_operations(operations, current_index)
