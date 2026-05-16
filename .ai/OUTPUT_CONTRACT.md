# OUTPUT FORMAT (STRICT)
Return ONLY valid JSON:

{
  "operations": [
    {
      "action": "create" | "update" | "delete",
      "name": "Page Name",
      "content": "full file contents including frontmatter"
    }
  ]
}

Rules:
- content is required for create and update.
- omit content for delete.
- name is the page title.
- if no changes are needed, return: {"operations":[]}
