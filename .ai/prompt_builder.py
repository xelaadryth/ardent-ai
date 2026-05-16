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


def load_contract():
    path = AI_FOLDER / "CONTRACT.md"
    try:
        content = read_file(str(path))
        if not content:
            raise ValueError("CONTRACT.md is empty")
        return content
    except Exception:
        raise RuntimeError("CONTRACT.md not found or invalid")


def build_system_prompt(prompt: str, vault_limit=100) -> str:
    soul = load_soul()
    vault_context = retrieve_vault_context(prompt, limit=vault_limit)
    contract = load_contract()

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

# CONTRACT

{contract}
"""
