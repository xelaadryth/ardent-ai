import json

import pytest
import vault
import vault_index


def test_retrieve_vault_context_scores_files_and_loads_content(tmp_path, monkeypatch):
    vault_index_data = {
        "files": {
            "Aaron": {
                "name": "Aaron",
                "type": "npc",
                "status": "active",
                "tags": ["#noble", "#warrior", "#human"],
                "links": ["[[Town]]"]
            },
            "Town": {
                "name": "Town",
                "type": "location",
                "status": "active",
                "tags": ["#market", "#town"],
                "links": ["[[Aaron]]"]
            }
        }
    }

    (tmp_path / "vault_index.json").write_text(json.dumps(vault_index_data), encoding="utf-8")
    (tmp_path / "03 NPCs").mkdir(parents=True)
    (tmp_path / "03 NPCs" / "Aaron.md").write_text("Aaron content", encoding="utf-8")
    (tmp_path / "06 Locations").mkdir(parents=True)
    (tmp_path / "06 Locations" / "Town.md").write_text("Town content", encoding="utf-8")

    monkeypatch.setattr(vault_index, "VAULT_ROOT", tmp_path)
    monkeypatch.setattr(vault, "VAULT_ROOT", tmp_path)

    context = vault_index.retrieve_vault_context("noble town", limit=2)

    assert "--- 03 NPCs/Aaron.md ---" in context
    assert "--- 06 Locations/Town.md ---" in context
    assert "Aaron content" in context
    assert "Town content" in context


def test_retrieve_vault_context_falls_back_when_no_matches(tmp_path, monkeypatch):
    (tmp_path / "vault_index.json").write_text(json.dumps({"files": {}}), encoding="utf-8")
    (tmp_path / "SOUL.md").write_text("Soul file", encoding="utf-8")
    (tmp_path / "README.md").write_text("Readme file", encoding="utf-8")

    monkeypatch.setattr(vault_index, "VAULT_ROOT", tmp_path)
    monkeypatch.setattr(vault, "VAULT_ROOT", tmp_path)

    context = vault_index.retrieve_vault_context("unlikely query")

    assert "--- SOUL.md ---" in context


def test_retrieve_vault_context_builds_index_from_empty_vault_index(tmp_path, monkeypatch):
    (tmp_path / "03 NPCs").mkdir(parents=True)
    (tmp_path / "03 NPCs" / "Aaron.md").write_text("""---
name: Aaron
type: npc
links: []
tags: []
---
Aaron content""", encoding="utf-8")

    monkeypatch.setattr(vault_index, "VAULT_ROOT", tmp_path)
    monkeypatch.setattr(vault, "VAULT_ROOT", tmp_path)

    context = vault_index.retrieve_vault_context("Aaron")

    assert "--- 03 NPCs/Aaron.md ---" in context
    assert "Aaron content" in context
    assert (tmp_path / "vault_index.json").exists()


def test_build_index_entry_extracts_frontmatter_links():
    from pathlib import Path

    path = Path("03 NPCs/Aaron.md")
    content = """---
name: Aaron
type: npc
links:
  - "[[Town]]"
tags:
  - "#noble"
---
[[Town]] is near [[Abbey]]. [[Town]] is also important. [[town]] is a duplicate."""

    entry = vault_index.build_index_entry(path, content)

    assert "name" in entry
    assert "type" in entry
    assert "links" in entry
    assert "tags" in entry
    assert entry["name"] == "Aaron"
    assert entry["type"] == "npc"
    assert entry["links"] == ["[[Town]]"]
    assert entry["tags"] == ["#noble"]


def test_build_index_entry_handles_missing_frontmatter():
    from pathlib import Path

    path = Path("03 NPCs/Aaron.md")
    content = "Some content without frontmatter"

    entry = vault_index.build_index_entry(path, content)

    assert entry["name"] == ""
    assert entry["type"] == ""
    assert entry["links"] == []
    assert entry["tags"] == []


def test_get_folder_from_type_returns_folder_prefix():
    assert vault_index.get_folder_from_type("npc") == "03 NPCs"
    assert vault_index.get_folder_from_type("player") == "02 Players"
    assert vault_index.get_folder_from_type("core") == ""


def test_build_index_entry_includes_last_index_timestamp():
    from pathlib import Path

    path = Path("03 NPCs/Aaron.md")
    content = ""

    entry = vault_index.build_index_entry(path, content)

    assert "last_index" in entry
    assert isinstance(entry["last_index"], str)
    assert entry["last_index"].endswith("Z")
