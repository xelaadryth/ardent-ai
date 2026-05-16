import pipeline
from workflow_integration import compose_commit_message, handle_workflow_error, print_workflow_output


def main():
    try:
        output, request_name = pipeline.main()
        commit_message = compose_commit_message(request_name, "update")
        print_workflow_output(request_name, commit_message)
    except Exception as e:
        handle_workflow_error(e, "AI agent")


if __name__ == "__main__":
    main()
