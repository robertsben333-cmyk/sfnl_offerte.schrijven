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
    learnings.md              ← nieuw bestand (aanmaken in install.py als het niet bestaat)
  skills/
    sfnl-offerte-mbc/         ← map hernoemd van sfnl-offerte/ (git mv)
      SKILL.md                ← leerlogica toegevoegd
    sfnl-offerte-[type2]/
      SKILL.md                ← toekomstige projecttypen
  scripts/
    generate_offerte.py
    review_offerte.py
  templates/
    offerte_mbc_template.pptx
  .claude-plugin/
    plugin.json               ← naam bijwerken naar sfnl-offerte-mbc v1.1.0
    marketplace.json          ← plugin naam bijwerken naar sfnl-offerte-mbc
```

**Hernoeming van de skill-map**: gebruik `git mv skills/sfnl-offerte skills/sfnl-offerte-mbc` zodat de git-history bewaard blijft.

Geen dispatcher-skill. Elk projecttype heeft een eigen skill als direct entry point.

**Plugin discovery**: `.claude-plugin/marketplace.json` verwijst via `"source": "./"` naar de root van de repo. Claude Code scant plugins-mappen op `skills/*/SKILL.md` — dit volgt het bestaande patroon van de huidige skill (nu onder `skills/sfnl-offerte/SKILL.md`). Na het hernoemen van de map en het bijwerken van de naam in `plugin.json` en `marketplace.json` is de skill beschikbaar als `sfnl-offerte-mbc`. **Verplichte handmatige test na implementatie**: verwijder de plugin in Claude Code en voeg hem opnieuw toe om te bevestigen dat de hernoemde skill correct wordt herkend.

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

**Bestandsbeheer**: het bestand is append-only. De skill schrijft nooit regels weg; alleen toe. Als het bestand te groot wordt of tegenstrijdige entries bevat, beheert de gebruiker het handmatig.

---

### 3. Leerlogica in `sfnl-offerte-mbc/SKILL.md`

#### 3a. Lezen (begin stap 2a)

De skill laadt `data/learnings.md` aan het begin van de sessie, ná de intake (stap 1) maar vóór het opstellen van voorstellen. Learnings beïnvloeden de intakevragen **niet**.

**Kalibraties** worden toegepast op het moment dat dag-schattingen worden opgesteld in stap 2b — pas dan is de tier bekend. Stilzwijgend verwerken, zonder de reden te noemen:
- Toon het gecorrigeerde getal als default, alsof het de oorspronkelijke schatting is.
- Kalibraties uit onafhankelijke dimensies (bijv. sector én data-beschikbaarheid) worden opgeteld: "+1d zorgsector" + "−1d goede data" = 0 aanpassing.
- Als twee entries binnen dezelfde dimensie conflicteren (bijv. twee "zorgsector fase 2" entries met tegengestelde richting), gebruik dan de meest recente entry.

Voorbeeld stille kalibratie: de learnings zeggen "+1d fase 2 voor zorgsector" en "+1d fase 2 voor beperkte data". De skill stelt voor "Fase 2: 16 dagen" (basiswaarde 14d + 2d) zonder vermelding van de correctie.

**Inhoudelijke patronen** — alle matchende patronen worden expliciet benoemd, zonder filtering. Als twee patronen voor hetzelfde klanttype tegenstrijdig zijn, worden beide getoond zodat de gebruiker kan oordelen:
> "Op basis van eerdere offertes voor zorginstellingen: intern draagvlak is bijna altijd een kernbehoefte — ik heb dit als eerste aandachtspunt opgenomen."

#### 3b. Schrijven (na akkoord stap 2c, vóór generatie)

Claude analyseert de bevestigde keuzes en vergelijkt met de defaults. Er wordt alleen iets weggeschreven als aan één van deze **drempelcriteria** is voldaan:

**Basislijn voor dag-schattingen** (voor het berekenen van afwijkingen):

| Tier | Fase 1 baseline | Fase 2 baseline | Fase 3 baseline |
|------|----------------|----------------|----------------|
| Basic | 6d | 9d | 4d |
| Standaard | 8d | 14d | 6d |
| Complex | 10d | 19d | 8d |

(Midpunt van de tierrange uit SKILL.md, naar beneden afgerond. Ranges: Basic F1 5-7d, F2 8-11d, F3 3-5d; Standaard F1 7-9d, F2 12-16d, F3 5-7d; Complex F1 9-12d, F2 16-22d, F3 7-10d.)

**Drempelcriteria voor schrijven**:

| Categorie | Drempel |
|-----------|---------|
| Kalibratie dag-schatting | Afwijking ≥ 2 dagen t.o.v. de basislijn hierboven, per fase |
| Kalibratie tarief | NGO-tarief gekozen bij een non-profit klant — alleen schrijven als er nog geen entry bestaat die begint met `tarief:ngo-non-profit` (duplicate-check op dit exacte label-prefix) |
| Inhoudelijk patroon | Een aandachtspunt dat direct voortkomt uit klanttype of sector, niet uit projectspecifieke context |
| Procesafwijking | Fase-structuur afwijkt van de standaard 3-fasenopzet |

Als niets aan de drempel voldoet, schrijft de skill niets weg — geen lege commit of placeholder.

Schrijven gebeurt automatisch, zonder bevestiging van de gebruiker.

**Foutafhandeling**: als schrijven naar `learnings.md` mislukt (bijv. bestandsvergrendeling of schrijfrechten), toont de skill een waarschuwing ("Kon learnings niet opslaan: [reden]") en gaat daarna door met de PPTX-generatie. De fout blokkeert de offerte niet.

---

### 4. Wijzigingen `.claude-plugin/plugin.json`

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

En `.claude-plugin/marketplace.json` — volledig bijgewerkte versie (pseudo-code, overige velden uit het bestaande bestand overnemen):

```json
{
  "name": "sfnl-plugins",
  "description": "Claude plugins voor Social Finance NL",
  "owner": { "name": "Social Finance NL", "email": "info@socialfinancenl.nl" },
  "plugins": [
    {
      "name": "sfnl-offerte-mbc",
      "description": "Schrijft SFNL MBC-offertes voor maatschappelijke businesscases en duurzame financiering",
      "version": "1.1.0",
      "source": "./",
      "author": { "name": "Social Finance NL" }
    }
  ]
}
```

---

### 5. Wijzigingen `install.py`

De huidige `install.py` installeert alleen `python-pptx`. De volgende logica wordt toegevoegd (gedeeltelijke uitbreiding, geen volledige herschrijving van de kern):

1. Na de python-pptx check: maak `data/learnings.md` aan als het niet bestaat — initialiseer met de lege sectiestructuur uit sectie 2 hierboven.
2. Druk een instructie af als het oude skill-pad bestaat. Gebruik `Path.home() / ".claude" / "skills" / "sfnl-offerte"` (via `pathlib.Path`) voor cross-platform compatibiliteit — `~/.claude/skills/` is het standaardpad op zowel Windows als macOS/Linux. Het script verwijdert de map niet zelf (destructieve actie) maar toont: "Verwijder handmatig de oude skill: `<pad>`".
3. De skill zelf wordt **niet** door `install.py` gekopieerd — Claude Code detecteert skills via de plugin-map (`skills/sfnl-offerte-mbc/SKILL.md`). Installatie van de skill verloopt via "Manage Plugins" in Claude Code, zoals nu.

---

## Niet in scope

- Automatisch genereren van learnings voor andere projecttypen dan MBC (volgt bij toevoegen van die skills)
- UI of dashboard voor het beheren van learnings
- Versiebeheer of deduplicatie van learnings (gebruiker beheert handmatig)
- Terugschrijven naar historische offertes in `output/`

---

## Succescriteria

- `/sfnl-offerte-mbc` triggert de hernoemde skill correct
- `data/learnings.md` wordt aangemaakt door `install.py` als die niet bestaat, met de juiste sectiestructuur
- Na een volledige offerte-run worden relevante inzichten (boven de drempel) weggeschreven naar de juiste sectie
- Bij een volgende run worden kalibraties stilzwijgend verwerkt en patronen expliciet benoemd
- Een tweede projecttype kan worden toegevoegd door een nieuwe map in `skills/` aan te maken — geen andere wijzigingen nodig
