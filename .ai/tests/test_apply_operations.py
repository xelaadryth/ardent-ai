import pytest
from unittest.mock import patch

from response_parser import apply_operations


SAMPLE_CONTENT = """---
name: Test NPC
type: npc
links:
  - "[[Truthkeepers]]"
tags:
  - "#npc"
---

This character knows [[Revolar]] and [[Truthkeepers]].
"""


def test_apply_operations_creates_file_and_merges_links():
    fake_index = {"files": {}}

    operations = [
        {
            "action": "create",
            "path": "03 NPCs/Test NPC.md",
            "content": SAMPLE_CONTENT
        }
    ]

    with patch("vault.write_file") as mock_write, \
         patch("vault_index.load_vault_index", return_value=fake_index), \
         patch("vault_index.save_vault_index") as mock_save:

        apply_operations(operations)

        # 1. file written
        mock_write.assert_called_once()

        # 2. index updated
        saved_index = mock_save.call_args[0][0]

        assert "03 NPCs/Test NPC.md" in saved_index["files"]

        entry = saved_index["files"]["03 NPCs/Test NPC.md"]

        # frontmatter link
        assert "[[Truthkeepers]]" in entry["links"]

        # body links extracted
        assert "[[Revolar]]" in entry["links"]

        # no duplicates
        assert entry["links"].count("[[Truthkeepers]]") == 1


def test_apply_operations_deletes_file():
    fake_index = {
        "files": {
            "03 NPCs/Test NPC.md": {"name": "Test"}
        }
    }

    operations = [
        {
            "action": "delete",
            "path": "03 NPCs/Test NPC.md"
        }
    ]

    with patch("os.path.exists", return_value=True), \
         patch("os.remove") as mock_remove, \
         patch("vault_index.load_vault_index", return_value=fake_index), \
         patch("vault_index.save_vault_index") as mock_save:

        apply_operations(operations)

        mock_remove.assert_called_once_with("03 NPCs/Test NPC.md")

        saved_index = mock_save.call_args[0][0]
        assert "03 NPCs/Test NPC.md" not in saved_index["files"]