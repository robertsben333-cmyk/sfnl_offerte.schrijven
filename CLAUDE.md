# SFNL Offerte Project

This project contains the assets for the `/sfnl-offerte` skill, which writes SFNL proposals
for the "maatschappelijke businesscase en duurzame financiering" proposition.

## Directory structure

```
templates/
  offerte_mbc_template.pptx   — Standard proposal template (do not modify)
data/
  team.json                    — All SFNL team members with bios and contact info
scripts/
  generate_offerte.py          — PPTX generator; takes config JSON → output PPTX
  review_offerte.py            — Review script; checks budget, placeholders, forbidden words
output/
  config_*.json                — Generated config files (one per proposal)
  *.pptx                       — Generated proposal files
```

## Running the generator

```bash
py scripts/generate_offerte.py output/config_[client].json "output/YYYYMMDD Offerte [Client] SFNL.pptx"
```

Fases 4+ are NOT auto-inserted (the overview slide only has 3 chevrons). Use `insert_extra_fase()` from the module explicitly, then adjust slide 6 manually in PowerPoint.

## Running the reviewer

```bash
py scripts/review_offerte.py "output/YYYYMMDD Offerte [Client] SFNL.pptx" output/config_[client].json
```

Exit codes: 0 = clean, 1 = issues found, 2 = file error.

## Template slide map

| Slide | Content | Status |
|-------|---------|--------|
| 1  | Cover (title + date) | Variable |
| 2  | Inhoudsopgave | Fixed |
| 3  | Aanleiding offerte | Variable |
| 4  | Plan van aanpak (header) | Fixed |
| 5  | Wat is een MBC? | Fixed |
| 6  | Onze aanpak (overview chevrons) | Variable |
| 7  | Fase 1 detail | Variable |
| 8  | Fase 2 detail | Variable |
| 9  | Fase 3 detail | Variable |
| 10 | Tijdslijn | Variable |
| 11 | Randvoorwaarden voor succes | Fixed |
| 12 | Team (section header) | Fixed |
| 13 | Team (members) | Variable |
| 14 | Begroting (section header) | Fixed |
| 15 | Begroting (detail) | Variable |
| 16 | Randvoorwaarden en akkoord | Variable |
| 17+ | Over Social Finance NL (boilerplate) | Fixed — never modify |

## Day rates
- Standard: €1.480/dag
- NGO: €1.280/dag
- Always confirm with user before calculating budget

## Adding a new team member
Edit `data/team.json` and add to the appropriate role array (supervisors / managers / associates / analysts).
