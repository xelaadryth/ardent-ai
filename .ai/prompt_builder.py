from vault import read_file
from vault_index import retrieve_vault_context


def load_soul():
    path = "SOUL.md"
    try:
        content = read_file(path)
        if not content:
            raise ValueError("SOUL.md is empty")
        return content
    except Exception:
        raise RuntimeError("SOUL.md not found or invalid")


def build_system_prompt(prompt: str, vault_limit=25) -> str:
    soul = load_soul()
    vault_context = retrieve_vault_context(prompt, limit=vault_limit)

    return f"""
{soul}

---

VAULT CONTEXT:
{vault_context}

---

USER REQUEST:
{prompt}
"""
