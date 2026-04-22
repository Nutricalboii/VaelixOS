# Graph Report - .  (2026-04-22)

## Corpus Check
- Corpus is ~224 words - fits in a single context window. You may not need a graph.

## Summary
- 13 nodes · 13 edges · 3 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Vaelix OS Infrastructure & Desktop|Vaelix OS Infrastructure & Desktop]]
- [[_COMMUNITY_Vaelix Control Center Development|Vaelix Control Center Development]]
- [[_COMMUNITY_Project Authors & Contributors|Project Authors & Contributors]]

## God Nodes (most connected - your core abstractions)
1. `Vaelix OS` - 11 edges
2. `Vaelix Control Center` - 2 edges
3. `Vaibhav Sharma` - 2 edges
4. `src/` - 2 edges
5. `Ubuntu` - 1 edges
6. `KDE Plasma` - 1 edges
7. `XanMod Kernel` - 1 edges
8. `Nutricalboii` - 1 edges
9. `branding/` - 1 edges
10. `scripts/` - 1 edges

## Surprising Connections (you probably didn't know these)
- `Vaelix OS` --references--> `Vaelix Control Center`  [EXTRACTED]
  README.md → README.md  _Bridges community 0 → community 1_
- `Vaelix OS` --references--> `Vaibhav Sharma`  [EXTRACTED]
  README.md → README.md  _Bridges community 0 → community 2_

## Communities

### Community 0 - "Vaelix OS Infrastructure & Desktop"
Cohesion: 0.22
Nodes (9): branding/, iso/, KDE Plasma, meta/, Pandit Build, scripts/, Ubuntu, Vaelix OS (+1 more)

### Community 1 - "Vaelix Control Center Development"
Cohesion: 1.0
Nodes (2): src/, Vaelix Control Center

### Community 2 - "Project Authors & Contributors"
Cohesion: 1.0
Nodes (2): Nutricalboii, Vaibhav Sharma

## Knowledge Gaps
- **9 isolated node(s):** `Ubuntu`, `KDE Plasma`, `XanMod Kernel`, `Nutricalboii`, `branding/` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Vaelix Control Center Development`** (2 nodes): `src/`, `Vaelix Control Center`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Project Authors & Contributors`** (2 nodes): `Nutricalboii`, `Vaibhav Sharma`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Vaelix OS` connect `Vaelix OS Infrastructure & Desktop` to `Vaelix Control Center Development`, `Project Authors & Contributors`?**
  _High betweenness centrality (0.970) - this node is a cross-community bridge._
- **Why does `Vaibhav Sharma` connect `Project Authors & Contributors` to `Vaelix OS Infrastructure & Desktop`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **What connects `Ubuntu`, `KDE Plasma`, `XanMod Kernel` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._