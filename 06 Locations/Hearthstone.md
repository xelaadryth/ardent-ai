---
name: Hearthstone
type: location
status: active
tags:
  - "#location"
last_updated: 2026-05-13T23:35:12
location: "[[Alethkar]]"
---
# Description
A rural settlement currently serving as the site for an official miracle investigation.

# Background
Hearthstone is a small town that has recently come under the scrutiny of the [[Truthkeepers]]. The investigation centers on identifying the nature of local anomalies to determine if they constitute a legal or security threat.

# Hooks
- 

# Connections
- [[001 First Blood]]
- [[002 Whitespine]]

# People
```dataview
TABLE
FROM "03 NPCs"
WHERE location = this.file.link
SORT file.name ASC
```
