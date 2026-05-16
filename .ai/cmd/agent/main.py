import os
from pathlib import Path
from typing import Optional, Tuple

from internal import inbox
from internal.llm import generate_content
from internal.response_parser import apply_response
from internal.prompt_builder import build_system_prompt
from internal.workflow_integration import compose_commit_message, handle_workflow_error, print_workflow_output
from pkg.vault.io import load_vault_index


def run_agent(file_name=None, extra_prompt="") -> Tuple[str, Optional[str]]:
    request_file = inbox.find_inbox_file(file_name)
    if request_file is None:
        print("No request file found in Inbox.")
        return "", None

    request_name = Path(request_file).stem
    prompt = inbox.load_prompt(request_file, extra_prompt)
    system_prompt = build_system_prompt(prompt, vault_limit=500)

    output = generate_content(prompt=system_prompt)
    print(output)

    apply_response(output, load_vault_index())
    inbox.archive_file(request_file)

    return output, request_name


def main():
    try:
        file_name = os.environ.get("REQUEST_INPUT")
        extra_prompt = os.environ.get("EXTRA_PROMPT", "")
        _output, request_name = run_agent(file_name=file_name, extra_prompt=extra_prompt)
        commit_message = compose_commit_message(request_name, "update")
        print_workflow_output(request_name, commit_message)
    except Exception as e:
        handle_workflow_error(e, "AI agent")


if __name__ == "__main__":
    main()
