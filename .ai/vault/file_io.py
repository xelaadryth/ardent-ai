import json
from pathlib import Path

# AI_FOLDER is the .ai folder where scripts and index live
AI_FOLDER = Path(__file__).parent.parent
# VAULT_ROOT is the repository root (parent of the .ai folder)
VAULT_ROOT = AI_FOLDER.parent
CORE_FILES = ["SOUL.md"]


def read_file(path):
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = VAULT_ROOT / file_path

    try:
        return file_path.read_text(encoding="utf-8")
    except Exception:
        return ""


def write_file(path, content):
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = VAULT_ROOT / file_path

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def load_markdown(path: str) -> str:
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = VAULT_ROOT / file_path

    if not file_path.exists() or not file_path.is_file():
        return ""

    # Resolve to absolute path to avoid double resolution in read_file
    return read_file(file_path.resolve())


def load_core_context() -> str:
    context = []
    for core_file in CORE_FILES:
        content = load_markdown(core_file)
        if content:
            context.append(f"--- {core_file} ---\n{content}")

    return "\n\n".join(context)
