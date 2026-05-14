import prompts


def test_load_soul_returns_content(monkeypatch):
    monkeypatch.setattr(prompts, "read_file", lambda path: "Soul data")

    assert prompts.load_soul() == "Soul data"


def test_load_soul_raises_when_empty(monkeypatch):
    monkeypatch.setattr(prompts, "read_file", lambda path: "")

    try:
        prompts.load_soul()
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass


def test_build_system_prompt_includes_soul_context_and_request(monkeypatch):
    monkeypatch.setattr(prompts, "read_file", lambda path: "Soul data")
    monkeypatch.setattr(prompts, "crawl_vault", lambda limit_files: "vault context")

    result = prompts.build_system_prompt("My request")

    assert "Soul data" in result
    assert "vault context" in result
    assert "My request" in result
