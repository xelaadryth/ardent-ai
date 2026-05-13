from config import MODEL, PROMPT
from llm import generate_content
from prompts import build_system_prompt
from parser import apply_files

def main():
    prompt = build_system_prompt(PROMPT)

    output = generate_content(
        model=MODEL,
        prompt=prompt
    )

    print(output)

    apply_files(output)

if __name__ == "__main__":
    main()