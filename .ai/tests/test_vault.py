import os
from pathlib import Path

import vault


def test_read_file_returns_content(tmp_path):
    file_path = tmp_path / "file.md"
    file_path.write_text("content", encoding="utf-8")

    assert vault.read_file(str(file_path)) == "content"
    assert vault.read_file(str(file_path.parent / "missing.md")) == ""


def test_write_file_creates_directories_and_writes_content(tmp_path):
    target = tmp_path / "nested" / "file.md"
    vault.write_file(str(target), "hello")

    assert target.exists()
    assert target.read_text(encoding="utf-8") == "hello"


def test_crawl_vault_includes_root_and_numeric_directories(tmp_path, monkeypatch):
    root_soul = tmp_path / "SOUL.md"
    root_readme = tmp_path / "README.md"
    root_soul.write_text("soul", encoding="utf-8")
    root_readme.write_text("readme", encoding="utf-8")

    numeric = tmp_path / "00 Templates"
    numeric.mkdir()
    file_a = numeric / "template.md"
    file_a.write_text("template", encoding="utf-8")

    ignored = tmp_path / "other"
    ignored.mkdir()
    file_b = ignored / "skip.md"
    file_b.write_text("skip", encoding="utf-8")

    monkeypatch.setattr(vault, "VAULT_ROOT", str(tmp_path))

    context = vault.crawl_vault(limit_files=10)

    assert "--- " in context
    assert "SOUL.md" in context
    assert "README.md" in context
    assert "template.md" in context
    assert "skip.md" not in context
