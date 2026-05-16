from pkg.vault import file_io

def test_read_file_returns_content(tmp_path):
    file_path = tmp_path / "file.md"
    file_path.write_text("content", encoding="utf-8")

    assert file_io.read_file(str(file_path)) == "content"
    assert file_io.read_file(str(file_path.parent / "missing.md")) == ""


def test_write_file_creates_directories_and_writes_content(tmp_path):
    target = tmp_path / "nested" / "file.md"
    file_io.write_file(str(target), "hello")

    assert target.exists()
    assert target.read_text(encoding="utf-8") == "hello"
