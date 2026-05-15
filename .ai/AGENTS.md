# AI Agent Development Notes

## Project Overview

This is an Obsidian vault management system with AI-powered content generation. The Python code lives in the `.ai` folder and helps manage the Obsidian markdown repository.

## Architecture

### Entry Points
- `main.py` - AI agent workflow entry point (processes Inbox requests)
- `reindex.py` - Deterministic vault reindexing (no LLM calls)

Both entry points use `workflow_integration.py` for standardized output formatting and error handling.

### Core Modules

**Workflow Integration**
- `workflow_integration.py` - Centralized GitHub Actions integration (output formatting, commit messages, error handling)

**AI Pipeline**
- `pipeline.py` - Orchestrates the AI agent workflow (no global state, returns tuples)
- `llm_client.py` - Google Gemini API client with retry logic and model fallback
- `prompt_builder.py` - Builds system prompts with vault context
- `response_parser.py` - Parses LLM responses and applies operations to vault

**Vault Operations** (split by domain in `vault/` folder)
- `vault/file_io.py` - File I/O operations (read, write, load_markdown)
- `vault/io.py` - Vault index I/O (load_vault_index, save_vault_index)
- `vault/parser.py` - Frontmatter parsing and index entry building
- `vault/crawler.py` - File crawling and index building from disk
- `vault/retrieval.py` - Context retrieval with scoring
- `vault/mapping.py` - Type-to-folder mapping for vault organization
- `vault/utilities.py` - General utilities (normalization, index management)

**Supporting Modules**
- `inbox.py` - Inbox file management (find, load, archive)
- `config.py` - Configuration (models, vault root, environment variables)

## Important Patterns

### GitHub Actions Integration
Entry points output variables in specific format for shell parsing:
```
REQUEST_FILENAME=<filename>
COMMIT_MESSAGE=<message>
```

This is handled by `workflow_integration.print_workflow_output()`.

### Vault Index System
- `vault_index.json` tracks all markdown files with frontmatter
- Each entry has: name, type, status, links, tags, last_index
- Type-to-folder mapping organizes content (e.g., "npc" → "03 NPCs")
- Index can be rebuilt deterministically from disk via `reindex.py`

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

### Circular Import Prevention
The vault package was split to avoid circular imports:
- `current_timestamp` moved to `vault/io.py` (not utilities)
- Submodules import from specific locations to avoid cycles
- `vault/__init__.py` re-exports all public API for backward compatibility

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
All entry points use `workflow_integration.handle_workflow_error()` for consistent error output and exit codes.

## Key Files to Understand

1. `pipeline.py` - Main AI orchestration logic
2. `vault/__init__.py` - Public API for vault operations
3. `workflow_integration.py` - GitHub Actions integration
4. `response_parser.py` - How LLM responses become file changes
5. `vault/retrieval.py` - How vault context is retrieved for prompts
