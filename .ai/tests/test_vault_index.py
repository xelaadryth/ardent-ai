import json

import pytest
import vault
import vault_index


def test_retrieve_vault_context_scores_files_and_loads_content(tmp_path, monkeypatch):
    vault_index_data = {
        "files": {
            "npc/Aaron.md": {
                "type": "npc",
                "summary": "A heroic noble warrior in the town.",
                "tags": ["noble", "warrior", "human"],
                "links": ["location/Town.md"]
            },
            "location/Town.md": {
                "type": "location",
                "summary": "A busy market town surrounded by hills.",
                "tags": ["market", "town"],
                "links": ["npc/Aaron.md"]
            }
        }
    }

    (tmp_path / "vault_index.json").write_text(json.dumps(vault_index_data), encoding="utf-8")
    (tmp_path / "npc").mkdir(parents=True)
    (tmp_path / "npc" / "Aaron.md").write_text("Aaron content", encoding="utf-8")
    (tmp_path / "location").mkdir(parents=True)
    (tmp_path / "location" / "Town.md").write_text("Town content", encoding="utf-8")

    monkeypatch.setattr(vault_index, "VAULT_ROOT", tmp_path)
    monkeypatch.setattr(vault, "VAULT_ROOT", tmp_path)

    context = vault_index.retrieve_vault_context("noble town", limit=2)

    assert "--- npc/Aaron.md ---" in context
    assert "--- location/Town.md ---" in context
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
    assert "--- README.md ---" in context


def test_retrieve_vault_context_builds_index_from_empty_vault_index(tmp_path, monkeypatch):
    (tmp_path / "03 NPCs").mkdir(parents=True)
    (tmp_path / "03 NPCs" / "Aaron.md").write_text("Aaron content", encoding="utf-8")

    monkeypatch.setattr(vault_index, "VAULT_ROOT", tmp_path)
    monkeypatch.setattr(vault, "VAULT_ROOT", tmp_path)

    context = vault_index.retrieve_vault_context("Aaron")

    assert "--- 03 NPCs/Aaron.md ---" in context
    assert "Aaron content" in context
    assert (tmp_path / "vault_index.json").exists()


def test_build_index_entry_extracts_wikilinks_and_deduplicates():
    from pathlib import Path

    path = Path("03 NPCs/Aaron.md")
    content = "[[Town]] is near [[Abbey]]. [[Town]] is also important. [[town]] is a duplicate."

    entry = vault_index.build_index_entry(path, content)

    assert "summary" in entry
    assert "tags" in entry
    assert entry["links"] == ["Town", "Abbey"]


def test_build_index_entry_deduplicates_tags():
    from pathlib import Path

    path = Path("03 NPCs/Aaron.md")
    content = ""

    entry = vault_index.build_index_entry(path, content)

    assert len(entry["tags"]) == len(set(entry["tags"]))


def test_build_index_entry_includes_last_index_timestamp():
    from pathlib import Path

    path = Path("03 NPCs/Aaron.md")
    content = ""

    entry = vault_index.build_index_entry(path, content)

    assert "last_index" in entry
    assert isinstance(entry["last_index"], str)
    assert entry["last_index"].endswith("Z")
