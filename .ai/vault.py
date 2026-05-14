import os

VAULT_ROOT = "."

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

import os
import re

def crawl_vault(limit_files=25):
    """
    Crawl only:
    - SOUL.md at vault root
    - README.md at vault root
    - Markdown files inside top-level folders whose names begin with digits
      (e.g. "00 Templates", "03 NPCs")

    Excludes:
    - .git
    - .obsidian
    - hidden files/folders
    """

    md_files = []

    # Always include these root-level files first if they exist.
    priority_files = ["SOUL.md", "README.md"]
    for filename in priority_files:
        path = os.path.join(VAULT_ROOT, filename)
        if os.path.isfile(path):
            md_files.append(path)

    # Only scan top-level directories that start with one or more digits.
    # Examples:
    #   "00 Templates"
    #   "01 Sessions"
    #   "03 NPCs"
    numeric_dir_pattern = re.compile(r"^\d+")

    for entry in sorted(os.listdir(VAULT_ROOT)):
        full_path = os.path.join(VAULT_ROOT, entry)

        # Only process directories whose names begin with digits.
        if not os.path.isdir(full_path):
            continue
        if entry.startswith("."):
            continue
        if not numeric_dir_pattern.match(entry):
            continue

        # Walk the directory recursively.
        for root, dirs, files in os.walk(full_path):
            # Remove hidden/system directories from traversal.
            dirs[:] = [
                d for d in dirs
                if not d.startswith(".")
                and d not in {".git", ".obsidian"}
            ]

            for file in sorted(files):
                if file.startswith("."):
                    continue
                if not file.endswith(".md"):
                    continue

                md_files.append(os.path.join(root, file))

    # Limit total files for token safety.
    md_files = md_files[:limit_files]

    # Build context bundle.
    context = []
    for path in md_files:
        content = read_file(path)
        if content.strip():
            context.append(f"--- {path} ---\n{content}")

    return "\n\n".join(context)
