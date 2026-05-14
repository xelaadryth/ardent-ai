import os
from pathlib import Path

import inbox
from llm_client import generate_content
from response_parser import apply_response
from prompt_builder import build_system_prompt

INBOX_DIR = inbox.INBOX_DIR
ARCHIVE_DIR = inbox.ARCHIVE_DIR
find_inbox_file = inbox.find_inbox_file
load_prompt = inbox.load_prompt
archive_file = inbox.archive_file


LAST_REQUEST_NAME = None


def run_agent(request_input=None, extra_prompt=""):
    global LAST_REQUEST_NAME

    request_file = find_inbox_file(request_input)
    if request_file is None:
        print("No request file found in Inbox.")
        return None

    LAST_REQUEST_NAME = Path(request_file).stem
    prompt = load_prompt(request_file, extra_prompt)
    system_prompt = build_system_prompt(prompt)

    output = generate_content(prompt=system_prompt)
    print(output)

    apply_response(output)
    archive_file(request_file)

    return output


def main():
    request_input = os.environ.get("REQUEST_INPUT")
    extra_prompt = os.environ.get("EXTRA_PROMPT", "")

    return run_agent(request_input=request_input, extra_prompt=extra_prompt)


if __name__ == "__main__":
    main()