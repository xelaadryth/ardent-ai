import os
from pathlib import Path
import sys
from typing import Optional, Tuple

ai_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ai_dir))

from internal.outbox import archive_file, find_outbox_file, load_outbox_file
from internal.llm import generate_content
from internal.response_parser import apply_response
from internal.prompt_builder import build_system_prompt
from internal.git import compose_commit_message, print_workflow_output
from internal.vault.index import load_vault_index


def run_agent(file_name=None, extra_prompt="") -> Tuple[str, Optional[str]]:
    request_file = find_outbox_file(file_name)

    # Only exit early if both request file and extra_prompt are missing
    if request_file is None and not extra_prompt:
        print("No request file found in Outbox.")
        return "", None

    # Build prompt from file or extra_prompt
    if request_file:
        request_name = Path(request_file).stem
        prompt = load_outbox_file(request_file, extra_prompt)
    else:
        request_name = "direct-prompt"
        prompt = extra_prompt

    system_prompt = build_system_prompt(prompt, vault_limit=500)

    output = generate_content(prompt=system_prompt)
    print(output)

    # Archive file if it exists, otherwise use the request_name for response saving
    if request_file:
        request_stem = archive_file(request_file)
    else:
        request_stem = request_name

    apply_response(output, load_vault_index(), request_stem)

    return output, request_name


def main():
    file_name = os.environ.get("REQUEST_INPUT")
    extra_prompt = os.environ.get("EXTRA_PROMPT", "")
    _output, request_name = run_agent(file_name=file_name, extra_prompt=extra_prompt)
    commit_message = compose_commit_message(request_name, "update")
    print_workflow_output(request_name, commit_message)


if __name__ == "__main__":
    main()
