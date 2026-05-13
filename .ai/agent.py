from config import MODEL, PROMPT
from llm import generate_content
from prompts import build_system_prompt

def main():
    system_prompt = build_system_prompt(PROMPT)

    output = generate_content(
        model=MODEL,
        prompt=system_prompt
    )

    print(output)

if __name__ == "__main__":
    main()
