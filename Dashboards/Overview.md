# Players

<!-- QueryToSerialize:
TABLE
player AS "Player",
link(spren) AS "Spren",
link(spren).order AS "Order",
status AS "Status"
FROM "02 Players"
SORT file.name ASC
-->
<!-- SerializedQuery: TABLE player AS "Player", link(spren) AS "Spren", link(spren).order AS "Order", status AS "Status" FROM "02 Players" SORT file.name ASC -->

| File                                                 | Player  | Spren                                  | Order        | Status |
| ---------------------------------------------------- | ------- | -------------------------------------- | ------------ | ------ |
| [[Fina]]                         | Shirley | [[Verdae]]         | Edgedancer   | active |
| [[Galeth-son-Thald]] | Corin   | [[Kun'ahu]]       | Stoneward    | active |
| [[Iiko]]                         | Truong  | [[Dreamwaker]] | Truthwatcher | active |
| [[Kuma]]                         | Dan     | [[Viscose]]       | Elsecaller   | active |
| [[Mallow]]                     | Audrey  | [[Cadence]]       | Willshaper   | active |
| [[N'tal]]                       | Ryan    | [[Pyre]]             | Dustbringer  | active |


<!-- SerializedQuery END -->
# Arcs
<!-- QueryToSerialize:
TABLE
status AS "Status"
FROM "01 Arcs"
SORT file.name ASC
-->
<!-- SerializedQuery: TABLE status AS "Status" FROM "01 Arcs" SORT file.name ASC -->

| File                                                                          | Status   |
| ----------------------------------------------------------------------------- | -------- |
| [[01 Truthkeepers Arc]]                       | inactive |
| [[02 Knights of Dusk Arc]]                 | active   |
| [[03 Stormblessed Arc]]                       | planned  |
| [[04 Nurian Gems Arc]]                         | planned  |
| [[05 Kharbranth Infiltration Arc]] | planned  |


<!-- SerializedQuery END -->
# Sessions
<!-- QueryToSerialize:
TABLE
link(arc) AS "Arc",
status AS "Status"
FROM "04 Sessions"
SORT file.name ASC
-->
<!-- SerializedQuery: TABLE link(arc) AS "Arc", status AS "Status" FROM "04 Sessions" SORT file.name ASC -->

| File                                                                                        | Arc                                                           | Status  |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ------- |
| [[000 Arrival]]                                                 | [[01 Truthkeepers Arc]]       | active  |
| [[001 First Blood]]                                         | [[01 Truthkeepers Arc]]       | active  |
| [[002 Whitespine]]                                           | [[01 Truthkeepers Arc]]       | active  |
| [[003 Yenev and the Axe]]                             | [[01 Truthkeepers Arc]]       | active  |
| [[004 The Sathir Estate]]                             | [[01 Truthkeepers Arc]]       | active  |
| [[005 Hearthstone]]                                         | [[01 Truthkeepers Arc]]       | active  |
| [[006 Dillind and the Temple]]                   | [[01 Truthkeepers Arc]]       | active  |
| [[007 Lavrik and the Soulcaster]]             | [[01 Truthkeepers Arc]]       | active  |
| [[008 The Envisagers of Talinan]]             | [[01 Truthkeepers Arc]]       | active  |
| [[009 Slavers]]                                                 | [[01 Truthkeepers Arc]]       | active  |
| [[010 Soulcaster and Shared Employers]] | [[01 Truthkeepers Arc]]       | active  |
| [[011 Promotions and Revolar]]                   | [[01 Truthkeepers Arc]]       | active  |
| [[012 Following Chip]]                                   | [[02 Knights of Dusk Arc]] | active  |
| [[013 Shadow War in the Driftwards]]       | [[02 Knights of Dusk Arc]] | planned |


<!-- SerializedQuery END -->
