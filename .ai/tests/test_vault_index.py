from pkg.vault import mapping
from pkg.vault import parser


def test_build_index_entry_extracts_frontmatter_links():
    content = """---
name: Aaron
type: npc
tags:
  - "#noble"
---
[[Town]] is near [[Abbey]]. [[Town]] is also important. [[town]] is a duplicate."""

    entry = parser.build_index_entry(content)

    assert "name" in entry
    assert "type" in entry
    assert "links" in entry
    assert "tags" in entry
    assert entry["name"] == "Aaron"
    assert entry["type"] == "npc"
    assert "[[Town]]" in entry["links"]
    assert "[[Abbey]]" in entry["links"]
    assert entry["tags"] == ["#noble"]


def test_build_index_entry_handles_missing_frontmatter():
    from pathlib import Path

    content = "Some content without frontmatter"

    entry = parser.build_index_entry(content)

    assert entry["name"] == ""
    assert entry["type"] == ""
    assert entry["links"] == []
    assert entry["tags"] == []


def test_get_folder_from_type_returns_folder_prefix():
    assert mapping.get_folder_from_type("npc") == "03 NPCs"
    assert mapping.get_folder_from_type("player") == "02 Players"
    assert mapping.get_folder_from_type("core") == ""


def test_build_index_entry_preserves_last_updated_from_frontmatter():
    content = """---
name: Aaron
type: npc
last_updated: 2023-01-01T00:00:00Z
---
Some content"""

    entry = parser.build_index_entry(content)

    assert "last_updated" in entry
    # YAML parses timestamps as datetime objects, but we convert them to ISO strings
    assert entry["last_updated"] == "2023-01-01T00:00:00+00:00"


def test_build_index_entry_includes_status_from_frontmatter():
    content = """---
name: Aaron
type: npc
status: active
tags: ["warrior"]
---
Some content here."""

    entry = parser.build_index_entry(content)

    assert entry["status"] == "active"
    assert entry["name"] == "Aaron"
    assert entry["type"] == "npc"
    assert entry["tags"] == ["warrior"]
