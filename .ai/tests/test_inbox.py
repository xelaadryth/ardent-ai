import inbox


def test_find_inbox_file_returns_first_matching_file(monkeypatch, tmp_path):
    inbox_dir = tmp_path / "Inbox"
    inbox_dir.mkdir()
    file_a = inbox_dir / "a.md"
    file_a.write_text("content", encoding="utf-8")
    file_b = inbox_dir / "b.md"
    file_b.write_text("content", encoding="utf-8")

    monkeypatch.setattr(inbox, "INBOX_DIR", inbox_dir)
    found = inbox.find_inbox_file()

    assert found == file_a


def test_find_inbox_file_can_use_request_input(monkeypatch, tmp_path):
    inbox_dir = tmp_path / "Inbox"
    inbox_dir.mkdir()
    request_file = inbox_dir / "request.md"
    request_file.write_text("request", encoding="utf-8")

    monkeypatch.setattr(inbox, "INBOX_DIR", inbox_dir)
    found = inbox.find_inbox_file("request.md")

    assert found == request_file


def test_load_prompt_appends_extra_prompt(tmp_path):
    request_file = tmp_path / "request.md"
    request_file.write_text("Base prompt", encoding="utf-8")

    result = inbox.load_prompt(request_file, extra_prompt="More details")

    assert "Base prompt" in result
    assert "More details" in result


def test_archive_file_moves_file(monkeypatch, tmp_path):
    archive_dir = tmp_path / "Archive"
    request_file = tmp_path / "request.md"
    request_file.write_text("hello", encoding="utf-8")

    monkeypatch.setattr(inbox, "ARCHIVE_DIR", archive_dir)
    archived = inbox.archive_file(request_file)

    assert archived.parent == archive_dir
    assert archived.name.startswith("0000-")
    assert archived.exists()
    assert not request_file.exists()
