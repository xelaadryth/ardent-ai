"""
Workflow integration utilities for GitHub Actions.

Provides standardized functions for output formatting, commit message composition,
and error handling across all entry points.
"""

import sys
from typing import Optional


def print_workflow_output(request_filename: Optional[str] = None, commit_message: str = "") -> None:
    """
    Print workflow output in the format expected by the shell parser.
    
    Args:
        request_filename: Optional request filename to output
        commit_message: Commit message to output
    """
    if request_filename:
        print(f"REQUEST_FILENAME={request_filename}")
    if commit_message:
        print(f"COMMIT_MESSAGE={commit_message}")


def compose_commit_message(request_name: Optional[str], operation_type: str = "update") -> str:
    """
    Compose a standardized commit message.
    
    Args:
        request_name: Optional name of the request/file being processed
        operation_type: Type of operation (e.g., "update", "reindex")
    
    Returns:
        Formatted commit message
    """
    if request_name:
        return f"Ardent AI {operation_type}: {request_name}"
    return f"Ardent AI {operation_type}"


def handle_workflow_error(error: Exception, operation_name: str) -> None:
    """
    Handle workflow errors with standardized output and exit codes.
    
    Args:
        error: The exception that occurred
        operation_name: Name of the operation that failed (for logging)
    """
    print(f"ERROR: {operation_name} failed: {error}", file=sys.stderr)
    sys.exit(1)
