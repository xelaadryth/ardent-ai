import re
from vault_context import write_file

def extract_files(output: str):
    """
    Extracts file blocks from LLM output using the fenced markdown format.
    """
    # Regex breakdown:
    # 1. Look for '### FILE: ' and capture the path (non-greedy)
    # 2. Match the start of the code fence: ```markdown
    # 3. Capture everything inside (re.DOTALL allows matching newlines)
    # 4. Match the closing code fence: ```
    pattern = r"### FILE: (.*?)\s*\n\s*```markdown\n(.*?)\n\s*```"
    
    matches = re.findall(pattern, output, re.DOTALL)

    files = []
    for path, content in matches:
        # Strip ensures no stray whitespace from the capture group
        files.append((path.strip(), content))

    return files


def apply_files(output: str):
    files = extract_files(output)

    for path, content in files:
        write_file(path, content)
        print(f"[WRITE] {path}")
