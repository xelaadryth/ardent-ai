import json
import os
from datetime import datetime
from pathlib import Path

from llm_client import generate_content
from response_parser import apply_response
from vault import load_core_context
from vault_index import load_vault_index
from config import MODEL

VAULT_ROOT = Path('.')


def parse_timestamp(value: str) -> float:
    if not value:
        return 0.0
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()
    except ValueError:
        return 0.0


def select_oldest_markdown_files(limit=10) -> list[Path]:
    index = load_vault_index()
    entries = []

    for path, metadata in index.items():
        if not isinstance(metadata, dict):
            continue
        last_index = metadata.get('last_index')
        entries.append((path, parse_timestamp(last_index)))

    entries.sort(key=lambda item: item[1])
    selected_paths = [Path(path) for path, _ in entries[:limit]]

    return [path for path in selected_paths if (VAULT_ROOT / path).exists()]


def load_index_json() -> str:
    index = load_vault_index()
    return json.dumps({'files': index}, indent=2)


def build_file_section(path: Path) -> str:
    content = path.read_text(encoding='utf-8')
    return f'--- {path.as_posix()} ---\n{content}'


def build_reindex_prompt(extra_prompt: str = '') -> str:
    core_context = load_core_context()
    vault_index_json = load_index_json()
    oldest_files = select_oldest_markdown_files(10)
    oldest_sections = '\n\n'.join(build_file_section(path) for path in oldest_files)

    prompt = f"""
Perform a reindex action.

{core_context}

---

VAULT INDEX JSON:
{vault_index_json}

---

OLDEST 10 MARKDOWN FILES:
{oldest_sections}

{extra_prompt}
"""
    return prompt


def main():
    extra_prompt = os.environ.get('EXTRA_PROMPT', '')
    prompt = build_reindex_prompt(extra_prompt)
    output = generate_content(model=MODEL, prompt=prompt)
    print(output)

    try:
        apply_response(output)
    except Exception as exc:
        raise RuntimeError(f'Failed to apply reindex response: {exc}')

    print('COMMIT_MESSAGE=Ardent AI Reindex')


if __name__ == '__main__':
    main()
