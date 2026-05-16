#!/usr/bin/env python3
"""
Deterministic vault reindex script.

Rebuilds vault_index.json from frontmatter of all markdown files.
No LLM calls - purely deterministic.
"""

ai_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ai_dir))

from internal.workflow_integration import compose_commit_message, handle_workflow_error, print_workflow_output
from pkg.vault.crawler import build_index_from_disk
from pkg.vault.io import save_vault_index


def main():
    print("Starting deterministic vault reindex...")
    
    try:
        # Build index from all markdown files
        index = build_index_from_disk()
        
        if not index:
            raise ValueError("No valid markdown files with frontmatter found!")
        
        # Save the new index
        save_vault_index({"files": index})
        
        print(f"Successfully reindexed {len(index)} files")
        commit_message = compose_commit_message(None, "Reindex: Updated vault index from frontmatter")
        print_workflow_output(commit_message=commit_message)
        
    except Exception as exc:
        handle_workflow_error(exc, "Reindex")


if __name__ == '__main__':
    main()
