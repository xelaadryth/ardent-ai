import os

import pipeline


def compose_commit_message(request_name: str | None) -> str:
    if request_name:
        return f"Ardent AI update: {request_name}"
    return "Ardent AI update"


if __name__ == "__main__":
    pipeline.main()
    request_name = pipeline.LAST_REQUEST_NAME
    commit_message = compose_commit_message(request_name)

    if request_name:
        print(f"REQUEST_FILENAME={request_name}")
    print(f"COMMIT_MESSAGE={commit_message}")
