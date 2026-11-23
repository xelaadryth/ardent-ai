---
statblock: true
layout: Cosmere
name: Grand Justicar Malice
scale: Tier 4 Boss - Medium Scadrian (Bloodmarks Grand Justicar)
stats:
  - "5"
  - "6"
  - "4"
  - "5"
  - "4"
  - "5"
defenses:
  - "22"
  - "20"
  - "20"
health: 120
focus: 8
investiture: 12
deflect: 4
movement: 40 ft.
features:
  - name: Chromium Compounder (Spinner)
    desc: Malice can spend 1 Investiture to store Fortune in her metalminds as a free action. As a reaction, she can tap stored Fortune to force an attacker to reroll an attack roll or force a failed save on an ally, taking the worse result.
  - name: Investiture Drain (Chromium Allomancy)
    desc: Whenever Malice hits a target with a melee attack, the target loses 2 focus. If the target has no focus, they lose 2 Investiture.
  - name: Fortune's Favor
    desc: Malice gains Advantage on all Initiative and Perception tests. Once per round, if she misses an attack, she may re-roll the test.
  - name: Master of the Syndicate
    desc: Allies within 30 feet gain Advantage on saves against being Frightened or Charmed.
actions:
  - name: "Strike: Shard-Dagger"
    desc: "Attack +12, reach 5 ft., one target. Hit: 1d6 + 9 keen damage. If the target is an Invested creature (Radiant or Spren-bonded), they must succeed on a DC 18 Willpower test or be Silenced until the end of their next turn."
  - name: "Draining Lunge"
    desc: "2 actions. Malice moves up to her movement speed and makes a melee attack. If it hits, the target loses 4 Focus instead of 2."
reactions:
  - name: "Spin the Odds"
    desc: "Trigger: Malice is hit by an attack. Effect: Tap 1 charge of Fortune to force the attacker to re-roll the attack with Disadvantage. If the attack misses, Malice may immediately make a reactive strike."
plot_die:
  - name: Opportunity
    desc: "Malice's metalminds flare, blinding everyone within 15 feet until the end of their next turn."
  - name: Complication
    desc: "Malice's internal Investiture feedback causes her to lose 1d6 Investiture and she is stunned for 1 round."
type: statblock
npc: "[[Grand Justicar Malice]]"
---

```statblock
layout: Cosmere
monster: Grand Justicar Malice
```