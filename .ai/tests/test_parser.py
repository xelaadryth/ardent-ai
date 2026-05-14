import parser


def test_extract_files_returns_path_and_content():
    output = """### FILE: path/to/file.md
```markdown
Hello world
```
"""

    files = parser.extract_files(output)

    assert files == [("path/to/file.md", "Hello world")]


def test_apply_files_writes_each_file(monkeypatch):
    output = """### FILE: foo.txt
```markdown
Hello
```
"""
    written = []

    def fake_write_file(path, content):
        written.append((path, content))

    monkeypatch.setattr(parser, "write_file", fake_write_file)

    parser.apply_files(output)

    assert written == [("foo.txt", "Hello")]
