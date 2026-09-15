---
statblock: true
layout: Cosmere
name: Fearspren
scale: Tier 2 Minion - Small Spren (Cognitive Entity)
stats:
  - "1"
  - "3"
  - "1"
  - "2"
  - "-1"
  - "2"
defenses:
  - "14"
  - "13"
  - "12"
health: 12
focus: 2
investiture: 0
deflect: 0
movement: 30 ft., 20 ft. climb
senses: Darkvision 60 ft., Emotion-Sensing (Fear) 30 ft.
languages: None
p_skills: Agility +5, Stealth +5
c_skills: Intimidation +4
s_skills: Perception +1
features:
  - name: Swarm Mechanics (Minion)
    desc: Fearspren appear as tiny, flat, purple humanoid figures with oversized orange hands. Individually weak, they gain +1 die on attack rolls for each additional Fearspren minion adjacent to the same target (up to +3).
  - name: Cognitive Form (Shadesmar)
    desc: In the Cognitive Realm, fearspren take up physical space. Their flat, rubbery bodies grant them resistance to Impact damage, reducing it by 3.
  - name: Clinging Panic
    desc: Enemies starting their turn adjacent to two or more Fearspren must spend 1 additional foot of movement for every foot moved due to tiny orange hands grabbing and pulling at them.
actions:
  - name: "Strike: Slapping Hands"
    desc: "Attack +5 vs. Physical Defense, reach 5 ft., one target. Hit: 1d4 + 3 impact damage. Graze: 3 impact damage."
  - name: Mobbing Terror
    desc: "2 actions. The Fearspren swarm swarms over a creature in its reach. The target must succeed on a DC 13 Discipline test or become Afraid until the end of their next turn."
reactions:
  - name: Scatter
    desc: "Trigger: The Fearspren takes damage from an area effect. Effect: Spend 1 focus to gain +2 Physical Defense against the triggering attack as they flatten themselves into cracks or under glass beads."
plot_die:
  - name: Opportunity
    desc: The fearspren's grip slips; the target breaks free of all grab effects and gains Advantage on their next attack against the swarm.
  - name: Complication
    desc: The fearspren's frantic chattering attracts a larger predator in Shadesmar or incites nearby spren.
type: statblock
npc:
---
```statblock
layout: Cosmere
monster: Fearspren
```
