from pathlib import Path

INBOX_DIR = Path("Inbox")
ARCHIVE_DIR = Path("Archive")


def find_inbox_file(request_input=None):
    if request_input:
        return INBOX_DIR / request_input

    files = sorted(
        f for f in INBOX_DIR.glob("*.md")
        if f.is_file() and not f.name.startswith(".")
    )

    if not files:
        raise RuntimeError("No Inbox files found")

    return files[0]


def load_prompt(file_path, extra_prompt=""):
    prompt = file_path.read_text(encoding="utf-8")

    if extra_prompt:
        prompt += f"\n\n---\n\n## Additional Instructions\n\n{extra_prompt}\n"

    return prompt


def archive_file(file_path):
    ARCHIVE_DIR.mkdir(exist_ok=True)

    existing = sorted(ARCHIVE_DIR.glob("[0-9][0-9][0-9][0-9]-*.md"))

    if existing:
        last = int(existing[-1].name.split("-")[0])
        next_num = last + 1
    else:
        next_num = 0

    target = ARCHIVE_DIR / f"{next_num:04d}-{file_path.name}"
    file_path.rename(target)

    return target
