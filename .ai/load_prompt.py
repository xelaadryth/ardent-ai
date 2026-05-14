import os
from pathlib import Path

def find_inbox_file():
    request_input = os.environ.get("REQUEST_INPUT")

    if request_input:
        return request_input

    inbox = Path("Inbox")
    files = sorted([f for f in inbox.glob("*.md") if not f.name.startswith(".")])

    if not files:
        raise RuntimeError("No Inbox markdown files found")

    return str(files[0])

file_path = find_inbox_file()

with open(file_path, "r", encoding="utf-8") as f:
    base_prompt = f.read()

extra = os.environ.get("EXTRA_PROMPT", "")

if extra:
    base_prompt += f"\n\n---\n\n## Additional Instructions\n\n{extra}\n"

with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as env:
    env.write(f"REQUEST_FILE={file_path}\n")
    env.write("PROMPT<<EOF\n")
    env.write(base_prompt + "\n")
    env.write("EOF\n")
