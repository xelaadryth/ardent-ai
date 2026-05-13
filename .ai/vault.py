import os

VAULT_ROOT = "."

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def write_file(path, content):
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

def crawl_vault(limit_files=25):
    md_files = []

    for root, dirs, files in os.walk(VAULT_ROOT):
        if ".git" in root or ".obsidian" in root:
            continue

        for file in files:
            if file.startswith('.') or file.lower() == 'readme.md':
                continue

            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))

    md_files = md_files[:limit_files]

    context = []
    for f in md_files:
        content = read_file(f)
        if content.strip():
            context.append(f"--- {f} ---\n{content}")

    return "\n\n".join(context)
