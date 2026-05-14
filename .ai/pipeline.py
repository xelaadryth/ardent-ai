import os

import inbox
from config import MODEL
from llm_client import generate_content
from response_parser import apply_files
from prompt_builder import build_system_prompt

INBOX_DIR = inbox.INBOX_DIR
ARCHIVE_DIR = inbox.ARCHIVE_DIR
find_inbox_file = inbox.find_inbox_file
load_prompt = inbox.load_prompt
archive_file = inbox.archive_file


def run_agent(request_input=None, extra_prompt=""):
    request_file = find_inbox_file(request_input)
    prompt = load_prompt(request_file, extra_prompt)
    system_prompt = build_system_prompt(prompt)

    output = generate_content(model=MODEL, prompt=system_prompt)
    print(output)

    apply_files(output)
    archive_file(request_file)

    return output


def main():
    request_input = os.environ.get("REQUEST_INPUT")
    extra_prompt = os.environ.get("EXTRA_PROMPT", "")

    return run_agent(request_input=request_input, extra_prompt=extra_prompt)


if __name__ == "__main__":
    main()