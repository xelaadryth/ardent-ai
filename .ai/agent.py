import os
from google import genai

# ---------------- CONFIG ----------------
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

PROMPT = os.environ["PROMPT"]
MODEL = "gemini-3.1-flash-lite"
VAULT_ROOT = "."  # GitHub Actions runs from repo root

# ---------------- HELPERS ----------------
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

def crawl_vault(limit_files=20):
    """
    Lightweight vault crawler:
    - finds markdown files
    - excludes .git and .obsidian
    - returns small context bundle
    """
    md_files = []

    for root, dirs, files in os.walk(VAULT_ROOT):
        # Skip heavy/system folders
        if ".git" in root or ".obsidian" in root:
            continue

        for file in files:
            # 1. Skip hidden files (start with .) 
            # 2. Skip the specific README file
            if file.startswith('.') or file.lower() == 'readme.md':
                continue
                
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))

    # limit for token safety
    # TODO: RAG system for indexing and storing contents, needs folder metadata too
    md_files = md_files[:limit_files]

    context = []
    for f in md_files:
        content = read_file(f)
        if content.strip():
            context.append(f"--- {f} ---\n{content}")

    return "\n\n".join(context)

# ---------------- LOAD SOUL (REQUIRED) ----------------
def load_soul():
    path = "SOUL.md"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                raise ValueError("SOUL.md is empty")
            return content
    except FileNotFoundError:
        raise RuntimeError(
            "❌ SOUL.md not found at vault root. "
            "This file is required for the agent to run."
        )

SOUL = load_soul()

# ---------------- LOAD VAULT CONTEXT ----------------
vault_context = crawl_vault(limit_files=25)

# ---------------- MAIN SYSTEM PROMPT ----------------
system_prompt = f"""
{SOUL}
---

VAULT CONTEXT:
{vault_context}

---

USER REQUEST:
{PROMPT}
"""

# ---------------- CALL MODEL ----------------
response = client.models.generate_content(
    model=MODEL,
    contents=system_prompt
)

output = response.text

# ---------------- WRITE OUTPUT ----------------
print(output)
