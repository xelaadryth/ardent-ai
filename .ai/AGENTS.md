# AI Agent Development Notes

## Project Overview

This is an Obsidian vault management system with AI-powered content generation. The Python code lives in the `.ai` folder and helps manage the Obsidian markdown repository.

## Architecture

### Entry Points
- `main.py` - AI agent workflow entry point (processes Inbox requests)
- `reindex.py` - Deterministic vault reindexing (no LLM calls)

Both entry points use `workflow_integration.py` for standardized output formatting and error handling.

### Core Modules

**Workflow Commands**
- `cmd/agent/main.py` - Main AI agent workflow command (processes Inbox requests)
- `cmd/reindex/main.py` - Manual vault reindexing command (deterministic, no LLM calls, but already happens in the agent workflow)

**Internal Modules**
- `internal/inbox.py` - Inbox file management (find, load, archive)
- `internal/llm.py` - LLM client initialization and configuration
- `internal/prompt_builder.py` - Prompt construction for AI interactions
- `internal/response_parser.py` - Response frontmatter parsing and actual file editing
- `internal/workflow_integration.py` - Standardized output formatting and error handling

**Obsidian Vault**
- `pkg/vault/crawler.py` - File crawling and index building from disk
- `pkg/vault/file_io.py` - File I/O operations (read, write, load_markdown)
- `pkg/vault/io.py` - Vault index I/O (load_vault_index, save_vault_index)
- `pkg/vault/mapping.py` - Type-to-folder mapping for vault organization
- `pkg/vault/parser.py` - Frontmatter parsing and index entry building
- `pkg/vault/retrieval.py` - Context retrieval with scoring
- `pkg/vault/scoring.py` - Scoring logic for context retrieval

**Supporting Modules**
- `inbox.py` - Inbox file management (find, load, archive)
- `config.py` - Configuration (models, vault root, environment variables)

## Important Patterns

### Path Resolution
**CRITICAL:** Never use `Path(__file__).parent` to calculate paths to the vault root or .ai folder. Always use the centralized constants from `vault.file_io`:

- `VAULT_ROOT` - The repository root (parent of the .ai folder)
- `AI_FOLDER` - The .ai folder where scripts and index live

These are defined in `vault/file_io.py` and exported from the vault module. Using `.parent` calculations leads to fragile code that breaks when scripts run from different working directories (e.g., GitHub Actions vs local development).

**Example:**
```python
from vault import AI_FOLDER, VAULT_ROOT

# Correct
soul_path = AI_FOLDER / "SOUL.md"
vault_file = VAULT_ROOT / "03 NPCs/Aaron.md"

# Incorrect - DO NOT DO THIS
soul_path = Path(__file__).parent / "SOUL.md"
vault_root = Path(__file__).parent.parent.parent
```

### GitHub Actions Integration
Entry points output variables in specific format for shell parsing:
```
REQUEST_FILENAME=<filename>
COMMIT_MESSAGE=<message>
```

This is handled by `internal/workflow_integration.print_workflow_output()`.

### Vault Index System
- `vault_index.json` tracks all markdown files with frontmatter
- Each entry has: name, type, status, tags, last_updated
- Type-to-folder mapping organizes content (e.g., "npc" → "03 NPCs")
- Index can be rebuilt deterministically from disk via `reindex.py`
- `last_updated` is only set by the AI workflow when making operational changes, not by reindex

### AI Workflow
1. Find inbox file (or use specific file from input)
2. Load prompt with optional extra instructions
3. Build system prompt with SOUL.md + vault context
4. Call LLM with retry logic across multiple models
5. Parse JSON response and apply operations (create/update/delete files)
6. Update vault index
7. Archive processed inbox file

### Testing
- Uses pytest with monkeypatch for mocking
- Tests patch `vault.io.VAULT_ROOT` for file system isolation
- Run with: `uv run pytest tests -q`

## Development Notes

### Python Environment
- Python root is `.ai` folder (not repo root)
- Uses `uv` for dependency management
- Virtual environment in `.ai/.venv`

### Type System
Vault entry types map to numbered folders:
- core: root level
- template: 00 Templates
- player: 02 Players
- npc: 03 NPCs
- session: 04 Sessions
- faction: 05 Factions
- location: 06 Locations
- hook: 07 Hooks
- scene: 08 Scenes
- item: 09 Items
- lore: 10 Lore
- spren: 31 Spren

### Error Handling
All entry points use `internal/workflow_integration.handle_workflow_error()` for consistent error output and exit codes.
