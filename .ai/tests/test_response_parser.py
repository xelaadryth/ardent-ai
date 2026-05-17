import json

import pytest
from internal.response_parser import parse_json_output, apply_response
from pkg.vault.parser import extract_wikilinks


def test_parse_json_output_handles_embedded_json():
    output = '''Some explanation
{"operations": [{"action": "create", "name": "Test", "content": "Hello"}]}
More text'''

    payload = parse_json_output(output)

    assert payload["operations"][0]["name"] == "Test"


def test_apply_response_writes_files_and_updates_index(monkeypatch):
    output_payload = {
        "operations": [
            {"action": "create", "name": "Foo", "content": "---\nname: Foo\ntype: npc\ntags:\n  - example\nlinks:\n  - bar\nstatus: active\n---\nHello [[OtherLink]]"}
        ]
    }
    output = json.dumps(output_payload)

    written = []

    def fake_write_file(path, content):
        written.append((path, content))

    def fake_load_vault_index():
        return {"files": {"Existing": {"summary": "Existing"}}}

    monkeypatch.setattr("internal.response_parser.write_file", fake_write_file)

    current_index = fake_load_vault_index()
    apply_response(output, current_index, request_stem="test")

    assert written == [("03 NPCs/Foo.md", "---\nname: Foo\ntype: npc\ntags:\n  - example\nlinks:\n  - bar\nstatus: active\n---\nHello [[OtherLink]]")]
    # Index is NOT updated (only reindex updates the index)
    assert "Foo" not in current_index["files"]
    assert current_index["files"] == {"Existing": {"summary": "Existing"}}


def test_apply_response_raises_for_invalid_operations():
    output = json.dumps({"operations": [{"action": "unknown", "name": "Foo"}]})

    with pytest.raises(ValueError, match="Unsupported operation action"):
        apply_response(output, current_index={"files": {}})


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
