import json

import pytest
import vault
from pathlib import Path


def test_retrieve_vault_context_falls_back_when_no_matches(tmp_path, monkeypatch):
    # Create vault_index.json in the .ai folder (current working directory for tests)
    (Path("vault_index.json")).write_text(json.dumps({"files": {}}), encoding="utf-8")
    
    # Create vault files in tmp_path (VAULT_ROOT)
    (tmp_path / "SOUL.md").write_text("Soul file", encoding="utf-8")
    (tmp_path / "README.md").write_text("Readme file", encoding="utf-8")

    monkeypatch.setattr("vault.io.VAULT_ROOT", tmp_path)

    context = vault.retrieve_vault_context("unlikely query", 10)

    assert "--- SOUL.md ---" in context
    
    # Clean up
    Path("vault_index.json").unlink(missing_ok=True)


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

    entry = vault.build_index_entry(content)

    assert "name" in entry
    assert "type" in entry
    assert "links" in entry
    assert "tags" in entry
    assert entry["name"] == "Aaron"
    assert entry["type"] == "npc"
    # Frontmatter links are preserved, body links are merged, duplicates removed
    assert "[[Town]]" in entry["links"]
    assert "[[Abbey]]" in entry["links"]
    assert entry["tags"] == ["#noble"]


def test_build_index_entry_handles_missing_frontmatter():
    from pathlib import Path

    path = Path("03 NPCs/Aaron.md")
    content = "Some content without frontmatter"

    entry = vault.build_index_entry(content)

    assert entry["name"] == ""
    assert entry["type"] == ""
    assert entry["links"] == []
    assert entry["tags"] == []


def test_get_folder_from_type_returns_folder_prefix():
    assert vault.get_folder_from_type("npc") == "03 NPCs"
    assert vault.get_folder_from_type("player") == "02 Players"
    assert vault.get_folder_from_type("core") == ""


def test_get_oldest_indexed_files_returns_oldest_by_timestamp(tmp_path, monkeypatch):
    # Create test index with different timestamps
    old_timestamp = "2023-01-01T00:00:00Z"
    new_timestamp = "2024-01-01T00:00:00Z"
    
    vault_index_data = {
        "files": {
            "03 NPCs/OldFile.md": {
                "name": "OldFile",
                "type": "npc",
                "last_updated": old_timestamp
            },
            "02 Players/NewFile.md": {
                "name": "NewFile", 
                "type": "player",
                "last_updated": new_timestamp
            }
        }
    }

    # Create vault_index.json in the .ai folder (current working directory for tests)
    (Path("vault_index.json")).write_text(json.dumps(vault_index_data), encoding="utf-8")
    monkeypatch.setattr("vault.io.VAULT_ROOT", tmp_path)

    oldest = vault.get_oldest_indexed_files(1)
    assert oldest == ["03 NPCs/OldFile.md"]
    
    # Clean up
    Path("vault_index.json").unlink(missing_ok=True)


def test_build_index_entry_preserves_last_updated_from_frontmatter():
    from pathlib import Path

    path = Path("03 NPCs/Aaron.md")
    content = """---
name: Aaron
type: npc
last_updated: 2023-01-01T00:00:00Z
---
Some content"""

    entry = vault.build_index_entry(content)

    assert "last_updated" in entry
    # YAML parses timestamps as datetime objects, but we convert them to ISO strings
    assert entry["last_updated"] == "2023-01-01T00:00:00+00:00"


def test_build_index_entry_includes_status_from_frontmatter():
    from pathlib import Path

    path = Path("03 NPCs/Aaron.md")
    content = """---
name: Aaron
type: npc
status: active
tags: ["warrior"]
links: ["Town"]
---
Some content here."""

    entry = vault.build_index_entry(content)

    assert entry["status"] == "active"
    assert entry["name"] == "Aaron"
    assert entry["type"] == "npc"
    assert entry["tags"] == ["warrior"]
    assert entry["links"] == ["Town"]
