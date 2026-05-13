import os
import google.generativeai as genai

# ---------------- CONFIG ----------------
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
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

# ---------------- LOAD SOUL ----------------
SOUL = read_file("SOUL.md")

if not SOUL:
    SOUL = """
You are a GM assistant embedded inside a Cosmere-inspired RPG wiki.
You help maintain consistency, lore, and narrative continuity.
"""

# ---------------- LOAD VAULT CONTEXT ----------------
vault_context = crawl_vault(limit_files=25)

# ---------------- MAIN SYSTEM PROMPT ----------------
system_prompt = f"""
{SOUL}

You operate on a Markdown-based Obsidian campaign vault.

RULES:
- You may create, update, or extend markdown files.
- Always preserve existing lore unless explicitly overwritten.
- Use wiki links like [[Location Name]].
- Keep outputs compatible with Obsidian.
- Avoid duplicating existing entities.
- Prefer updating existing notes if they exist.

You are given:
1. The user's request
2. Full vault context (sampled)

---

VAULT CONTEXT:
{vault_context}

---

USER REQUEST:
{PROMPT}

---

OUTPUT FORMAT:
Return ONLY ONE markdown file.

If you create a new NPC:
- Put it in valid Obsidian markdown format
- Include frontmatter:
  type: npc
  status: active
"""

# ---------------- CALL MODEL ----------------
model = genai.GenerativeModel(MODEL)

response = model.generate_content(system_prompt)

output = response.text

# ---------------- WRITE OUTPUT ----------------
write_file("03 NPCs/AI-Generated-NPC.md", output)

print("Agent run complete. Output written to vault.")
