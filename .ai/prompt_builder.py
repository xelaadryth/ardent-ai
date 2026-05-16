from vault import AI_FOLDER, read_file, retrieve_vault_context


def load_soul():
    path = AI_FOLDER / "SOUL.md"
    try:
        content = read_file(str(path))
        if not content:
            raise ValueError("SOUL.md is empty")
        content = "SOUL.md contents: " + content
        return content
    except Exception:
        raise RuntimeError("SOUL.md not found or invalid")


def load_output_contract():
    path = AI_FOLDER / "OUTPUT_CONTRACT.md"
    try:
        content = read_file(str(path))
        if not content:
            raise ValueError("OUTPUT_CONTRACT.md is empty")
        return content
    except Exception:
        raise RuntimeError("OUTPUT_CONTRACT.md not found or invalid")


def build_system_prompt(prompt: str, vault_limit=100) -> str:
    soul = load_soul()
    vault_context = retrieve_vault_context(prompt, limit=vault_limit)
    output_contract = load_output_contract()

    return f"""
# SYSTEM (SOUL CORE)
{soul}

---

# VAULT CONTEXT (AUTHORITATIVE STATE)
Each block below is a single vault file. Treat each file as independent and canonical.

{vault_context}

---

# USER REQUEST
{prompt}

---

# INSTRUCTIONS
- Use ONLY vault context + SOUL rules.
- Resolve conflicts by preferring vault files over canon lore.
- Plan all changes before output.
- Output must follow the JSON schema exactly.
- No markdown, no commentary.

---

{output_contract}
"""