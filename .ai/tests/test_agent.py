import os
from pathlib import Path

import agent


def test_find_inbox_file_returns_first_matching_file(tmp_path):
    inbox = tmp_path / "Inbox"
    inbox.mkdir()
    file_a = inbox / "a.md"
    file_a.write_text("content", encoding="utf-8")
    file_b = inbox / "b.md"
    file_b.write_text("content", encoding="utf-8")

    agent.INBOX_DIR = inbox
    found = agent.find_inbox_file()

    assert found == file_a


def test_find_inbox_file_can_use_request_input(tmp_path):
    inbox = tmp_path / "Inbox"
    inbox.mkdir()
    request_file = inbox / "request.md"
    request_file.write_text("request", encoding="utf-8")

    agent.INBOX_DIR = inbox
    found = agent.find_inbox_file("request.md")

    assert found == request_file


def test_load_prompt_appends_extra_prompt(tmp_path):
    request_file = tmp_path / "request.md"
    request_file.write_text("Base prompt", encoding="utf-8")

    result = agent.load_prompt(request_file, extra_prompt="More details")

    assert "Base prompt" in result
    assert "More details" in result


def test_archive_file_moves_file(tmp_path):
    archive = tmp_path / "Archive"
    request_file = tmp_path / "request.md"
    request_file.write_text("hello", encoding="utf-8")

    agent.ARCHIVE_DIR = archive
    archived = agent.archive_file(request_file)

    assert archived.parent == archive
    assert archived.name.startswith("0000-")
    assert archived.exists()
    assert not request_file.exists()


def test_run_agent_calls_generate_and_archives(monkeypatch, tmp_path):
    inbox = tmp_path / "Inbox"
    archive = tmp_path / "Archive"
    inbox.mkdir()
    request_file = inbox / "request.md"
    request_file.write_text("hello", encoding="utf-8")

    agent.INBOX_DIR = inbox
    agent.ARCHIVE_DIR = archive

    monkeypatch.setattr(agent, "generate_content", lambda model, prompt: "output-text")
    calls = []
    monkeypatch.setattr(agent, "apply_files", lambda output: calls.append(output))

    output = agent.run_agent(request_input="request.md", extra_prompt="extra")

    assert output == "output-text"
    assert calls == ["output-text"]
    assert not request_file.exists()
    assert any(archive.iterdir())
