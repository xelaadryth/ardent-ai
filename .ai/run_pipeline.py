import os
import subprocess
from pathlib import Path
from google import genai

# ---------------- CONFIG ----------------
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

VAULT_ROOT = Path(".")
REQUEST_INPUT = os.environ.get("REQUEST_INPUT")
EXTRA_PROMPT = os.environ.get("EXTRA_PROMPT", "")
BRANCH = os.environ.get("BRANCH", "")
GH_TOKEN = os.environ.get("GH_TOKEN")

MODEL = "gemini-3.1-flash-lite"


# ---------------- HELPERS ----------------
def run(cmd):
    subprocess.run(cmd, shell=True, check=True)


def find_inbox_file():
    inbox = VAULT_ROOT / "Inbox"

    if REQUEST_INPUT:
        return inbox / REQUEST_INPUT

    files = sorted([f for f in inbox.glob("*.md") if f.is_file() and not f.name.startswith(".")])
    if not files:
        raise RuntimeError("No Inbox files found")

    return files[0]


def load_prompt(file_path):
    text = file_path.read_text(encoding="utf-8")

    if EXTRA_PROMPT:
        text += f"\n\n---\n\n## Additional Instructions\n\n{EXTRA_PROMPT}\n"

    return text


def archive_file(file_path):
    archive = VAULT_ROOT / "Archive"
    archive.mkdir(exist_ok=True)

    existing = sorted(archive.glob("[0-9][0-9][0-9][0-9]-*.md"))

    if existing:
        last = int(existing[-1].name.split("-")[0])
        next_num = last + 1
    else:
        next_num = 0

    new_name = f"{next_num:04d}-{file_path.name}"
    target = archive / new_name

    file_path.rename(target)

    return target


# ---------------- LOAD PROMPT ----------------
request_file = find_inbox_file()
prompt = load_prompt(request_file)


# ---------------- RUN LLM ----------------
response = client.models.generate_content(
    model=MODEL,
    contents=prompt
)

output = response.text
print(output)


# ---------------- ARCHIVE REQUEST ----------------
archived = archive_file(request_file)
