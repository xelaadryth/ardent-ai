from internal.outbox import archive_file, find_outbox_file, load_prompt


def test_find_outbox_file_returns_first_matching_file(monkeypatch, tmp_path):
    outbox_dir = tmp_path / "Outbox"
    outbox_dir.mkdir()
    file_a = outbox_dir / "a.md"
    file_a.write_text("content", encoding="utf-8")
    file_b = outbox_dir / "b.md"
    file_b.write_text("content", encoding="utf-8")

    monkeypatch.setattr("internal.outbox.OUTBOX_DIR", outbox_dir)
    found = find_outbox_file()

    assert found == file_a


def test_find_outbox_file_can_use_file_name(monkeypatch, tmp_path):
    outbox_dir = tmp_path / "Outbox"
    outbox_dir.mkdir()
    request_file = outbox_dir / "request.md"
    request_file.write_text("request", encoding="utf-8")

    monkeypatch.setattr("internal.outbox.OUTBOX_DIR", outbox_dir)
    found = find_outbox_file("request.md")

    assert found == request_file


def test_find_outbox_file_appends_md_extension(monkeypatch, tmp_path):
    outbox_dir = tmp_path / "Outbox"
    outbox_dir.mkdir()
    request_file = outbox_dir / "request.md"
    request_file.write_text("request", encoding="utf-8")

    monkeypatch.setattr("internal.outbox.OUTBOX_DIR", outbox_dir)
    found = find_outbox_file("request")

    assert found == request_file


def test_find_outbox_file_case_insensitive(monkeypatch, tmp_path):
    outbox_dir = tmp_path / "Outbox"
    outbox_dir.mkdir()
    request_file = outbox_dir / "Request.md"
    request_file.write_text("request", encoding="utf-8")

    monkeypatch.setattr("internal.outbox.OUTBOX_DIR", outbox_dir)
    found = find_outbox_file("request")

    assert found == request_file


def test_load_prompt_appends_extra_prompt(tmp_path):
    request_file = tmp_path / "request.md"
    request_file.write_text("Base prompt", encoding="utf-8")

    result = load_prompt(request_file, extra_prompt="More details")

    assert "Base prompt" in result
    assert "More details" in result


def test_archive_file_moves_file(tmp_path, monkeypatch):
    archive_dir = tmp_path / "Archive"
    archive_dir.mkdir()
    request_file = tmp_path / "request.md"
    request_file.write_text("hello", encoding="utf-8")

    monkeypatch.setattr("internal.outbox.ARCHIVE_DIR", archive_dir)
    archived_stem = archive_file(request_file)

    assert archived_stem == "request"
    assert not request_file.exists()
