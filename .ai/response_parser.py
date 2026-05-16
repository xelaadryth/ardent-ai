import json
import os
import re
import yaml
from datetime import datetime, timezone
from vault import write_file


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
    # If the json output is wrapped in a code block, extract it and replace newlines with \n
    if output.startswith("```json") and output.endswith("```"):
        output = output[len("```json"): -len("```")].replace('\n', '\\n').strip()

    try:
        return json.loads(output)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", output, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def now_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def apply_operations(operations: list[dict], current_index: dict):
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

            # 3. ENSURE LINKS IS A LIST
            links = metadata.get("links", [])
            if not isinstance(links, list):
                links = []
            metadata["links"] = links

            # 4. UPDATE INDEX
            metadata["last_updated"] = now_timestamp()
            current_index["files"][path] = metadata

            print(f"[INDEX UPDATE] {path}")

        elif action == "delete":
            if os.path.exists(path):
                os.remove(path)
                print(f"[DELETE] {path}")

            current_index["files"].pop(path, None)
            print(f"[INDEX DELETE] {path}")

        else:
            raise ValueError(f"Unsupported operation action: {action}")


def apply_response(output: str, current_index: dict):
    payload = parse_json_output(output)

    operations = payload.get("operations", [])

    if operations:
        apply_operations(operations, current_index)