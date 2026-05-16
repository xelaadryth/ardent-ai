# Ardent AI

A multi-tool system for managing a Cosmere RPG knowledge base.

TODO:
- Add to frontmatter
	- Party reputation (faction)
	- Date (in-world)
- Content organization
	- Migrate session scenes to their own pages
	- Centralized tag for active rumors/hooks with dataview for current session
- Code changes
	- Undertext - scribe notes on each page
- Obsidian optimization
	- Fantasy Map (Leaflet)
- Implement Feedback.md

## Dev Setup

- Windsurf free tier, let it know to read `.ai/AGENTS.md` for context

## AI Agent

- Python code generates `vault_index.json` from frontmatter via GitHub Actions
- AI Ingest Markdown files in the `Inbox` folder as instructions via GitHub Actions
- Processes files and updates the vault

### TODO
- Fix links not properly parsing on the frontmatter on the document itself (correct on the indedx)
- Full RAG implementation to replace or augment `vault_index.json`, move it into the .ai folder

## Obsidian

- Auto-syncs via Obsidian Git plugin

### Setup
- Install Community Plugins
	- Templater
		- Disable core plugin "Templates"
		- Set template folder location
	- Git
		- Auto commit-and-sync interval 5 minutes
		- Auto commit-and-sync after stopping file edits - ON
		- Pull on Startup
		- Pull strategy - Rebase, prefer Their
	- Dataview
	- QuickAdd

## Quartz

- Deploy to GitHub Pages via GitHub Actions

### Setup
- Run `.quartz/link_content.sh` to symlink the Obsidian Vault into the Quartz `content` folder


