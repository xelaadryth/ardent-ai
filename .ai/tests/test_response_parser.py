import json

import pytest
import response_parser
from response_parser import extract_wikilinks


def test_parse_json_output_handles_embedded_json():
    output = '''Some explanation
{"operations": [{"action": "create", "path": "test.md", "content": "Hello"}]}
More text'''

    payload = response_parser.parse_json_output(output)

    assert payload["operations"][0]["path"] == "test.md"


def test_apply_response_writes_files_and_updates_index(monkeypatch):
    output_payload = {
        "operations": [
            {"action": "create", "path": "foo.md", "content": "---\nname: Foo\ntype: example\ntags:\n  - example\nlinks:\n  - bar\nstatus: active\n---\nHello"}
        ]
    }
    output = json.dumps(output_payload)

    written = []
    index_saved = []

    def fake_write_file(path, content):
        written.append((path, content))

    def fake_load_vault_index():
        return {"files": {"existing.md": {"summary": "Existing"}}}

    def fake_save_vault_index(index_data):
        index_saved.append(index_data)

    monkeypatch.setattr(response_parser, "write_file", fake_write_file)
    monkeypatch.setattr(response_parser, "save_vault_index", fake_save_vault_index)

    response_parser.apply_response(output, fake_load_vault_index())

    assert written == [("foo.md", "---\nname: Foo\ntype: example\ntags:\n  - example\nlinks:\n  - bar\nstatus: active\n---\nHello")]
    assert len(index_saved) == 1
    assert "files" in index_saved[0]
    assert "foo.md" in index_saved[0]["files"]
    assert index_saved[0]["files"]["foo.md"]["name"] == "Foo"
    assert index_saved[0]["files"]["foo.md"]["type"] == "example"
    assert index_saved[0]["files"]["foo.md"]["tags"] == ["example"]
    assert index_saved[0]["files"]["foo.md"]["links"] == ["bar"]
    assert index_saved[0]["files"]["foo.md"]["status"] == "active"
    assert "last_index" in index_saved[0]["files"]["foo.md"]


def test_apply_response_raises_for_invalid_operations():
    output = json.dumps({"operations": [{"action": "unknown", "path": "foo.md"}]})

    with pytest.raises(ValueError, match="Unsupported operation action"):
        response_parser.apply_response(output, current_index={"files": {}})


def test_extract_wikilinks_basic():
    content = "This links to [[Revolar]] and [[Truthkeepers]]."

    result = extract_wikilinks(content)

    assert "[[Revolar]]" in result
    assert "[[Truthkeepers]]" in result
    assert len(result) == 2


def test_extract_wikilinks_deduplicates_case_insensitive():
    content = """
    [[Revolar]]
    [[revolar]]
    [[REVOLAR]]
    """

    result = extract_wikilinks(content)

    assert result == ["[[Revolar]]"]
    assert len(result) == 1


def test_extract_wikilinks_preserves_spacing():
    content = "See [[ Truthkeepers ]] for details."

    result = extract_wikilinks(content)

    assert result == ["[[Truthkeepers]]"]


def test_extract_wikilinks_ignores_non_wikilinks():
    content = "This is not a link: Revolar or [Revolar] or ((Revolar))"

    result = extract_wikilinks(content)

    assert result == []


def test_extract_wikilinks_mixed_content():
    content = """
    Story references:
    - [[Revolar]]
    - [[Truthkeepers]]
    - [[Revolar]] again
    """

    result = extract_wikilinks(content)

    assert result == ["[[Revolar]]", "[[Truthkeepers]]"]