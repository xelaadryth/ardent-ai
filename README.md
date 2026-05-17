# Ardent AI

- [Obsidian Site](https://xelaadryth.github.io/ardent-ai/)
- [Google AI Studio Ratelimits](https://aistudio.google.com/rate-limit?timeRange=last-1-day&project=gen-lang-client-0550336497)

A multi-tool system for managing a Cosmere RPG knowledge base.

## TODO:
- Intray Outray
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
- AI Ingest Markdown files in the `Outbox` folder as instructions via GitHub Actions
- Processes files and updates the vault

## Obsidian

- Auto-syncs via Obsidian Git plugin

Can add this dataview for free backlinks, no longer need bidirectional linking.

```dataview
LIST  
FROM ""  
WHERE contains(file.outlinks, this.file.link)  
AND !contains(this.file.outlinks, file.link)  
SORT file.name ASC
```

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


