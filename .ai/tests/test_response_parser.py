import json

import pytest
import response_parser
from vault import extract_wikilinks


def test_parse_json_output_handles_embedded_json():
    output = '''Some explanation
{"operations": [{"action": "create", "path": "test.md", "content": "Hello"}]}
More text'''

    payload = response_parser.parse_json_output(output)

    assert payload["operations"][0]["path"] == "test.md"


def test_apply_response_writes_files_and_updates_index(monkeypatch):
    output_payload = {
        "operations": [
            {"action": "create", "path": "foo.md", "content": "---\nname: Foo\ntype: example\ntags:\n  - example\nlinks:\n  - bar\nstatus: active\n---\nHello [[OtherLink]]"}
        ]
    }
    output = json.dumps(output_payload)

    written = []

    def fake_write_file(path, content):
        written.append((path, content))

    def fake_load_vault_index():
        return {"files": {"existing.md": {"summary": "Existing"}}}

    monkeypatch.setattr(response_parser, "write_file", fake_write_file)

    current_index = fake_load_vault_index()
    response_parser.apply_response(output, current_index)

    assert written == [("foo.md", "---\nname: Foo\ntype: example\ntags:\n  - example\nlinks:\n  - bar\nstatus: active\n---\nHello [[OtherLink]]")]
    # Index is updated in memory but not saved to disk
    assert "foo.md" in current_index["files"]
    assert current_index["files"]["foo.md"]["name"] == "Foo"
    assert current_index["files"]["foo.md"]["type"] == "example"
    assert current_index["files"]["foo.md"]["tags"] == ["example"]
    # Note: response_parser no longer extracts body links, only uses frontmatter
    assert current_index["files"]["foo.md"]["links"] == ["bar"]
    assert current_index["files"]["foo.md"]["status"] == "active"
    assert "last_updated" in current_index["files"]["foo.md"]


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