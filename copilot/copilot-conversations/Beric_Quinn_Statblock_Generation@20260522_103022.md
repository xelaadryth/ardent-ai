---
epoch: 1779471022307
modelKey: "gemini-3.1-flash-lite|google"
topic: "Beric Quinn Statblock Generation"



tags:
  - copilot-conversation
---

**user**: Can you generate me a similar statblock document page for Beric Quinn?
[Context: Notes: 10 Statblocks/Ojog Stats.md]
[Timestamp: 2026/05/22 10:30:22]

**ai**: To create a statblock document for Beric Quinn, you can use the following format, which aligns with the structure of your existing NPC statblock files.

---

# [[Beric Quinn Stats]]

```statblock
layout: Cosmere
monster: Beric Quinn
```

---

### Suggested Statblock Content
Based on the information in [[Beric Quinn]] and [[Allegiance at the Abandoned Docks]], you may want to populate the frontmatter of this note with the following details:

```yaml
---
statblock: true
layout: Cosmere
name: Beric Quinn
scale: Tier 2 Hero - Medium Human
stats:
  - "2"
  - "4"
  - "2"
  - "2"
  - "3"
  - "3"
defenses:
  - "16"
  - "14"
  - "15"
health: 45
focus: 8
investiture: "6"
deflect: 3
movement: 30 ft. (Fly 30 ft.)
senses: Passive Awareness 16
languages: Alethi, Nurian
p_skills: Agility +7, Athletics +4, Ranged Weaponry +8, Stealth +5
c_skills: Discipline +6, Survival +5
s_skills: Insight +5, Perception +6
features:
  - name: "Windrunner Initiate"
    desc: Beric can manipulate gravity and adhesion. He gains a fly speed equal to his movement speed.
  - name: "Reverse Lashing"
    desc: As a reaction, Beric can pull incoming projectiles toward himself, protecting allies within 10 ft.
  - name: "Martyr's Resolve"
    desc: When Beric is below half health, he gains advantage on all attack rolls and saves.
actions:
  - name: "Strike: Shortbow"
    desc: "Attack +8, range 80/320 ft., one target. Hit: 1d8 + 6 piercing damage."
  - name: "Wind-Guided Shot"
    desc: "Beric fires an arrow infused with windspren. Attack +8, range 80/320 ft. Hit: 2d8 + 6 piercing damage and the target is pushed 10 ft."
reactions:
  - name: "Shield of the Fallen"
    desc: When an ally is targeted by a ranged attack, Beric may use his reaction to intercept the projectile.
plot_die:
  - name: "Sacrifice"
    desc: Beric chooses to take all damage intended for an ally, potentially reducing his health to 0.
type: statblock
npc: "[[Beric Quinn]]"
---
```

#### Sources
[^1]: [[Beric Quinn]]
[^2]: [[Allegiance at the Abandoned Docks]]
[Timestamp: 2026/05/22 10:30:27]

**user**: Can you re-generate Beric's frontmatter so it's his stats BEFORE becoming a windrunner? At roughly the same power level as Ojog.
[Context: Notes: 10 Statblocks/Ojog Stats.md]
[Timestamp: 2026/05/22 10:31:29]

**ai**: To create a statblock for Beric Quinn that reflects his power level prior to his Windrunner awakening—aligning him more closely with Ojog's capabilities as a Truthkeeper Enforcer—you can use the following frontmatter.

---

# [[Beric Quinn Stats]]

```statblock
layout: Cosmere
monster: Beric Quinn
```

---

### Suggested Statblock Content (Pre-Awakening)

```yaml
---
statblock: true
layout: Cosmere
name: Beric Quinn
scale: Tier 1 Rival - Medium Human
stats:
  - "2"
  - "4"
  - "2"
  - "2"
  - "2"
  - "2"
defenses:
  - "15"
  - "14"
  - "14"
health: 36
focus: 5
investiture: "2"
deflect: 2
movement: 30 ft.
senses: Passive Awareness 15
languages: Alethi, Nurian
p_skills: Agility +6, Athletics +3, Ranged Weaponry +6, Stealth +4
c_skills: Discipline +5, Survival +5
s_skills: Insight +4, Perception +4
features:
  - name: "Nurian Hunter"
    desc: Beric has advantage on Survival checks to track or forage in wilderness environments.
  - name: "Egalitarian Resolve"
    desc: Beric gains advantage on saves against fear and intimidation when defending commoners or allies of lower social standing.
  - name: "Precise Shot"
    desc: When Beric makes a ranged attack against a target within 30 ft., he may add +2 to the attack roll.
actions:
  - name: "Strike: Shortbow"
    desc: "Attack +6, range 80/320 ft., one target. Hit: 1d8 + 4 piercing damage."
  - name: "Quick Draw"
    desc: "Beric makes two attacks with his shortbow. Each attack must be against a different target."
  - name: "Tactical Reposition"
    desc: "Beric moves up to half his movement speed. This movement does not provoke opportunity attacks."
reactions:
  - name: "Duck and Cover"
    desc: When targeted by a ranged attack, Beric may use his reaction to gain +2 to his defense until the start of his next turn.
plot_die:
  - name: "Defection"
    desc: Beric realizes the truth about the Truthkeepers and immediately loses his access to their resources, gaining 1 focus.
  - name: "Betrayal"
    desc: Beric is forced to act against his conscience, losing 1 focus and becoming Exhausted 1.
type: statblock
npc: "[[Beric Quinn]]"
---
```

This version removes his flight and windspren-infused abilities, focusing instead on his background as a Nurian hunter and his proficiency with the shortbow [^1]. It maintains a similar health pool and defensive profile to Ojog, representing his status as a skilled but non-Radiant enforcer before his eventual martyrdom [^2].

#### Sources
[^1]: [[Beric Quinn]]
[^2]: [[0100-Beric Quinn]]
[Timestamp: 2026/05/22 10:31:35]