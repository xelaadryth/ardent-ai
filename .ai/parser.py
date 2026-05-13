import re
from vault import write_file

def extract_files(output: str):
    """
    Extracts file blocks from LLM output.
    """

    pattern = r"### FILE: (.*?)\n(.*?)(?=### FILE:|$)"
    matches = re.findall(pattern, output, re.DOTALL)

    files = []
    for path, content in matches:
        files.append((path.strip(), content.strip()))

    return files


def apply_files(output: str):
    files = extract_files(output)

    for path, content in files:
        write_file(path, content)
        print(f"[WRITE] {path}")
