# OUTPUT FORMAT (STRICT)
Return ONLY valid JSON:

{
  "operations": [
    {
      "action": "create" | "update" | "delete",
      "path": "relative/path.md",
      "content": "full file contents including frontmatter"
    }
  ]
}

Rules:
- content is required for create and update.
- omit content for delete.
- path must be relative to the vault root.
- if no changes are needed, return: {"operations":[]}
