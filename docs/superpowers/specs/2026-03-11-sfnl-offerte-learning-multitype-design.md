# Design: SFNL Offerte — Learning-mechanisme & Multi-projecttype structuur

**Datum**: 2026-03-11
**Status**: Goedgekeurd

## Samenvatting

Twee verbeteringen aan de SFNL offerte-plugin:

1. **Learning-mechanisme** — na definitief akkoord schrijft de skill automatisch gegeneraliseerde inzichten (kalibraties, patronen, procesafwijkingen) weg naar `data/learnings.md`. Bij volgende offertes laadt de skill dit bestand en past schattingen stilzwijgend aan; inhoudelijke patronen worden expliciet benoemd.

2. **Multi-projecttype structuur** — de huidige `sfnl-offerte` skill wordt hernoemd naar `sfnl-offerte-mbc`. Dit maakt ruimte voor toekomstige skill-bestanden per projecttype (bijv. `sfnl-offerte-impactscan`), elk met eigen template en workflow.

---

## Probleemstelling

- De skill herhaalt dezelfde vragen en proposities bij elke nieuwe offerte, ook al zijn er inmiddels patronen bekend (bijv. zorgsector duurt langer, NGO-tarief wordt vaker gekozen).
- De skill ondersteunt maar één projecttype. SFNL heeft meerdere proposities die een vergelijkbare workflow volgen maar een eigen template en fases hebben.

---

## Ontwerp

### 1. Projectstructuur

```
sfnl_offerte.schrijven/
  data/
    team.json
    learnings.md              ← nieuw bestand
  skills/
    sfnl-offerte-mbc/
      SKILL.md                ← hernoemd van sfnl-offerte/SKILL.md + leerlogica toegevoegd
    sfnl-offerte-[type2]/
      SKILL.md                ← toekomstige projecttypen
  scripts/
    generate_offerte.py
    review_offerte.py
  templates/
    offerte_mbc_template.pptx
  .claude-plugin/
    plugin.json               ← naam bijwerken naar sfnl-offerte-mbc v1.1.0
```

Geen dispatcher-skill. Elk projecttype heeft een eigen skill als direct entry point.
`install.py` kopieert `skills/sfnl-offerte-mbc/` naar `~/.claude/skills/sfnl-offerte-mbc/`.

---

### 2. `data/learnings.md` — structuur

```markdown
# SFNL Offerte Learnings

## MBC

### Kalibratie
<!-- dag-schattingen, tarieven, betalingstermijnen -->
- [YYYY-MM-DD] [label]: [inzicht]

### Inhoudelijke patronen
<!-- sector-inzichten, terugkerende aandachtspunten, effectieve formuleringen -->
- [YYYY-MM-DD] [label]: [inzicht]

### Procesafwijkingen
<!-- hoe fases of structuur werd aangepast t.o.v. de standaard -->
- [YYYY-MM-DD] [label]: [inzicht]
```

Toekomstige projecttypen krijgen een eigen `## [Type]`-sectie.

**Regels voor inhoud**:
- Geen klantnamen
- Geen specifieke bedragen
- Alleen afwijkingen van defaults of herkenbare patronen
- Beknopt (één regel per inzicht)

---

### 3. Leerlogica in `sfnl-offerte-mbc/SKILL.md`

#### Lezen (begin stap 2a)

De skill laadt `data/learnings.md` vóór het doen van voorstellen.

- **Kalibraties** (bijv. sector duurt langer, tarief-voorkeur): stilzwijgend verwerken in schattingen
- **Inhoudelijke patronen**: expliciet benoemen waar relevant

Voorbeeld expliciete vermelding:
> "Op basis van eerdere offertes voor zorginstellingen: intern draagvlak is bijna altijd een kernbehoefte — ik heb dit als eerste aandachtspunt opgenomen."

#### Schrijven (na akkoord stap 2c, vóór generatie)

Claude analyseert de bevestigde keuzes en vergelijkt met de defaults:
- Afwijking van standaard dag-schattingen → `### Kalibratie`
- Tarief-keuze die een patroon bevestigt → `### Kalibratie`
- Sector-specifiek aandachtspunt dat steeds terugkomt → `### Inhoudelijke patronen`
- Fase-structuur aangepast → `### Procesafwijkingen`

Schrijven gebeurt automatisch, zonder bevestiging van de gebruiker.

---

### 4. Wijzigingen `plugin.json`

```json
{
  "name": "sfnl-offerte-mbc",
  "version": "1.1.0",
  "description": "Schrijft SFNL MBC-offertes voor maatschappelijke businesscases en duurzame financiering",
  "author": { "name": "Social Finance NL" },
  "repository": "https://github.com/robertsben333-cmyk/sfnl_offerte.schrijven",
  "keywords": ["sfnl", "offerte", "mbc", "businesscase", "impact", "financiering"]
}
```

---

### 5. Wijzigingen `install.py`

- Bronpad aanpassen: `skills/sfnl-offerte-mbc/` → `~/.claude/skills/sfnl-offerte-mbc/`
- Lege `data/learnings.md` aanmaken als die nog niet bestaat
- Bestaande `~/.claude/skills/sfnl-offerte/` verwijderen (of waarschuwen)

---

## Niet in scope

- Automatisch genereren van learnings voor andere projecttypen dan MBC (dat volgt bij toevoegen van die skills)
- UI of dashboard voor het beheren van learnings
- Versiebeheer van learnings (eenvoudige append-only file is voldoende)
- Terugschrijven naar historische offertes in `output/`

---

## Succescriteria

- `/sfnl-offerte-mbc` triggert de hernoemde skill correct
- `data/learnings.md` wordt aangemaakt door `install.py` als die niet bestaat
- Na een volledige offerte-run worden relevante inzichten weggeschreven naar de juiste sectie
- Bij een volgende run worden kalibraties stilzwijgend verwerkt en patronen expliciet benoemd
- Een tweede projecttype kan worden toegevoegd door een nieuwe map in `skills/` aan te maken — geen andere wijzigingen nodig
