import prompt_builder


def test_load_soul_returns_content(monkeypatch):
    monkeypatch.setattr(prompt_builder, "read_file", lambda path: "Soul data")

    assert prompt_builder.load_soul() == "SOUL.md contents: Soul data"


def test_load_soul_raises_when_empty(monkeypatch):
    monkeypatch.setattr(prompt_builder, "read_file", lambda path: "")

    try:
        prompt_builder.load_soul()
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass


def test_build_system_prompt_includes_soul_context_and_request(monkeypatch):
    monkeypatch.setattr(prompt_builder, "read_file", lambda path: "Soul data")
    monkeypatch.setattr(prompt_builder, "retrieve_vault_context", lambda query, limit=25: "vault context")

    result = prompt_builder.build_system_prompt("My request")

    assert "Soul data" in result
    assert "vault context" in result
    assert "My request" in result
