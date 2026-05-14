import pipeline
import inbox
from prompt_builder import build_system_prompt


def test_run_agent_calls_generate_and_archives(monkeypatch, tmp_path):
    inbox_dir = tmp_path / "Inbox"
    archive_dir = tmp_path / "Archive"
    inbox_dir.mkdir()
    request_file = inbox_dir / "request.md"
    request_file.write_text("hello", encoding="utf-8")

    monkeypatch.setattr(inbox, "INBOX_DIR", inbox_dir)
    monkeypatch.setattr(inbox, "ARCHIVE_DIR", archive_dir)

    monkeypatch.setattr(pipeline, "generate_content", lambda model, prompt: "output-text")
    calls = []
    monkeypatch.setattr(pipeline, "apply_response", lambda output: calls.append(output))
    
    # Mock load_soul to return dummy content
    import prompt_builder
    monkeypatch.setattr(prompt_builder, "load_soul", lambda: "SOUL.md contents: test soul")
    
    # Mock load_vault_index to return empty index
    import vault_index
    monkeypatch.setattr(vault_index, "load_vault_index", lambda: {})

    output = pipeline.run_agent(request_input="request.md", extra_prompt="extra")

    assert output == "output-text"
    assert calls == ["output-text"]
    assert not request_file.exists()
    assert any(archive_dir.iterdir())
