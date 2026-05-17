---
name: Feedback
type: lore
status: active
tags:
  - "#meta"
  - "#organization"
  - "#kb_maintenance"
last_updated: 2024-05-20T12:00:00
---

# Description
As your Ardent Scribe, I have evaluated the current structure of this vault. While the content is rich and deeply interconnected, implementing the following high-level organizational strategies would enhance my ability to curate the knowledge base and your ability to navigate it efficiently.

### 1. Geographical Hierarchies
Currently, locations like [[Stackhouses]] and [[Scarstone Quarter]] are flat entities. I suggest implementing a "Location Parent" field in the YAML frontmatter or a breadcrumb system in the description (e.g., `Part of: [[Revolar]]`). This allows for "Upward" navigation. For instance, the [[Revolar]] page could use a Dataview query to automatically list all locations that claim it as a parent, ensuring that as new districts or shops are added, the city map updates itself automatically.

### 2. Session-to-Scene Atomicity
Your session notes (e.g., [[011 Promotions and Revolar]]) are excellent summaries. However, as the campaign grows, finding specific combat encounters or moral trials becomes difficult. Moving complex scenes like [[The Abandoned Foundry]] or [[The Cinder Evacuation]] into their own files was a great start. I recommend doing this for all major "set-piece" scenes. This allows me to link a character directly to a specific event (e.g., [[Jory]] -> [[The Abandoned Foundry]]) without cluttering their page with the entire session's history.

### 3. Centralized Hook & Rumor Tracking
Hooks are currently buried within individual NPC and Session files. For a knowledge base to be "efficient," I suggest a centralized `Quest Tracker` or `Active Hooks` document. By using a specific tag (e.g., `#hook/active`), I can automatically aggregate these into a single dashboard. This would allow you to see at a glance that [[N'tal]] has a pending meeting with the [[Undertaker]] without having to check both their pages.

### 4. Standardized Relation Fields
While the "Connections" section is great for human reading, adding semantic keys to the YAML would allow for powerful AI and plugin automation. Fields such as `faction_of:`, `allied_with:`, or `enemy_of:` would allow me to generate relationship maps. For example, if I know [[Arbiter Jalis]] is `faction_of: [[Bloodmarks]]`, I can automatically suggest connections to [[Grand Justicar Malice]] even if they haven't shared a scene yet.

### 5. AI Prompt Refinement (The "Soul Core")
To make my curation more proactive, you could update my PURPOSE to include: "When a new NPC is created, the Scribe should automatically check for related items, locations, or factions and suggest cross-links." Currently, I am very reactive to your specific instructions. Allowing me the agency to "propose" new connections in a "Speculations" or "Scribe's Notes" section would make the vault feel more alive.

### 6. Temporal Versioning
The `last_updated` field is helpful, but for a TTRPG, a `timeline_date` (using the Rosharan calendar) in the YAML would be superior. This would allow for a chronological view of events, making it easier to track how much time passed between [[000 Arrival]] and [[011 Promotions and Revolar]].

# Details
These improvements focus on transforming the vault from a collection of notes into a relational database. By standardizing the way "Parent" locations and "Quest" states are handled, the Ardent Scribe can ensure that no thread is ever truly lost in the crem-falls of information.

# Connections
- [[01 Truthkeepers Arc]]
- [[02 Knights of Dusk Arc]]
- [[Ardent Scribe]]