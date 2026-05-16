import os
from pathlib import Path
from typing import Optional, Tuple

import inbox
from llm_client import generate_content
from response_parser import apply_response
from prompt_builder import build_system_prompt
from vault import load_vault_index

INBOX_DIR = inbox.INBOX_DIR
ARCHIVE_DIR = inbox.ARCHIVE_DIR
find_inbox_file = inbox.find_inbox_file
load_prompt = inbox.load_prompt
archive_file = inbox.archive_file


def run_agent(file_name=None, extra_prompt="") -> Tuple[str, Optional[str]]:
    request_file = find_inbox_file(file_name)
    if request_file is None:
        print("No request file found in Inbox.")
        return "", None

    request_name = Path(request_file).stem
    prompt = load_prompt(request_file, extra_prompt)
    system_prompt = build_system_prompt(prompt)

    output = generate_content(prompt=system_prompt)
    print(output)

    apply_response(output, load_vault_index())
    archive_file(request_file)

    return output, request_name


def main() -> Tuple[str, Optional[str]]:
    file_name = os.environ.get("REQUEST_INPUT")
    extra_prompt = os.environ.get("EXTRA_PROMPT", "")

    return run_agent(file_name=file_name, extra_prompt=extra_prompt)


if __name__ == "__main__":
    main()
