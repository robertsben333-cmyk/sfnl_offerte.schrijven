# Multi-propositie offerte-architectuur — Design Spec

**Datum:** 2026-03-30
**Status:** Goedgekeurd (mondeling)

---

## Context

Het huidige systeem ondersteunt één propositie: de Maatschappelijke Businesscase (MBC). Die werkt via een vaste PPTX-template die met XML-editing wordt ingevuld. Voor de vijf andere SFNL-proposities (Impact Meten & Management, Advies Innovatieve Financiering, Intermediair Innovatieve Financiering, Fondsmanagement, Partnerschappen) bestaat geen volledige template — wel een stijlgids en voorbeeldslides.

Het doel is een plugin-architectuur waarmee een "vrij denkende" agent voor elke propositie een offerte kan genereren: de slide-structuur wordt tijdens de intake samen met de gebruiker uitgewerkt, waarna de agent de juiste slides componeert en een PPTX assembleert.

---

## Plugin-manifest

Het project is een Claude Code plugin en vereist `.claude-plugin/plugin.json`:

```json
{
  "name": "sfnl-offerte",
  "version": "3.0.0",
  "description": "SFNL offerte-generator voor alle proposities",
  "author": { "name": "Social Finance NL" }
}
```

Skills worden automatisch ontdekt vanuit de `skills/`-directory. Alle scriptreferenties in hooks of aanroepen vanuit skills gebruiken de `CLAUDE_PLUGIN_ROOT`-omgevingsvariabele — nooit hardcoded paden.

---

## Directory-structuur

Componenten, templates en referenties leven *binnen* de skill die ze gebruikt — conform de plugin-conventie (progressive disclosure). Gedeelde data op plugin-root.

```
sfnl_offerte.schrijven/               ← Plugin root
├── .claude-plugin/
│   └── plugin.json                  ← Verplicht plugin-manifest
│
├── data/                            ← Gedeeld door alle skills
│   ├── team.json
│   └── style.json                   ← Kleuren, fonts, day rates
│
├── skills/
│   ├── sfnl-offerte/                ← Hoofd-orchestrator skill
│   │   ├── SKILL.md                 ← Lean (≤2.000 woorden), imperatieve vorm
│   │   └── references/              ← Progressive disclosure: geladen als nodig
│   │       ├── mbc.md               ← Propositie-profiel MBC (skeleton, intake, fases)
│   │       ├── impact_meten.md
│   │       ├── advies_innovatieve_financiering.md
│   │       ├── intermediair_innovatieve_financiering.md
│   │       ├── fondsmanagement.md
│   │       ├── partnerschappen.md
│   │       ├── schrijfregels.md     ← Verboden woorden, stijlregels, actieve schrijfwijze
│   │       └── budget_gids.md       ← Tarievens, complexiteitslagen, betaaltermijnen
│   │
│   └── pptx-offerte/                ← Assembler skill (PPTX + Word)
│       ├── SKILL.md                 ← Lean (≤2.000 woorden)
│       ├── assets/
│       │   ├── sfnl_base.pptx       ← Blanco SFNL slide-master + boilerplate 17+
│       │   ├── sfnl_base.docx       ← Blanco SFNL Word-template
│       │   └── offerte_mbc_template.pptx  ← MBC legacy (referentie)
│       ├── scripts/
│       │   ├── slides/              ← PPTX component library
│       │   │   ├── cover.py
│       │   │   ├── aanleiding.py
│       │   │   ├── section_header.py
│       │   │   ├── aanpak_overview.py
│       │   │   ├── fase_detail.py
│       │   │   ├── two_column.py
│       │   │   ├── team.py
│       │   │   ├── budget_table.py
│       │   │   ├── randvoorwaarden.py
│       │   │   ├── tijdslijn.py
│       │   │   └── akkoord.py
│       │   ├── word/                ← Word component library
│       │   │   ├── cover.py
│       │   │   ├── aanleiding.py
│       │   │   ├── aanpak_section.py
│       │   │   ├── team.py
│       │   │   ├── budget_table.py
│       │   │   └── akkoord.py
│       │   ├── assemble.py          ← slide_plan JSON → .pptx
│       │   └── assemble_word.py     ← slide_plan JSON → .docx
│       └── references/
│           ├── slide_components.md  ← Content-schema per component
│           └── xml_editing.md       ← XML-editpatronen voor nauwkeurige plaatsing
│
├── scripts/                         ← Legacy (backward compat)
│   ├── generate_offerte.py
│   └── review_offerte.py
│
└── output/
```

---

## Architectuur

### Gedeelde infrastructuur

**`skills/pptx-offerte/assets/sfnl_base.pptx`**
Blanco SFNL-master: correcte fonts, kleuren en bullet-stijlen via de slide master, plus de vaste boilerplate-slides 17+ ("Over Social Finance NL"). Gemaakt door de MBC-template te strippen. Alle proposities bouwen hierop.

**`skills/pptx-offerte/assets/sfnl_base.docx`**
Blanco SFNL Word-document: correcte heading-stijlen, kleuren, fonts, header/footer met SFNL-logo. Basis voor Word-offertes.

**`data/style.json`**
Stijlconstanten: kleurenpalet (inclusief propositie-accenten), font-namen, standaard marges, day rates (€1.480 / €1.280 NGO).

**`data/team.json`**
Ongewijzigd — gedeeld door alle proposities.

---

### Slide component library (`scripts/slides/`)

Elke component is een Python-functie `add_[type]_slide(prs, content) -> None`. Ze lezen stijlconstanten uit `style.json` en voegen één slide toe aan een `pptx.Presentation`-object. Waar python-pptx niet volstaat voor nauwkeurige plaatsing, wordt aangevuld met XML-editing.

| Component | Beschrijving |
|-----------|-------------|
| `cover.py` | Titel, klant, datum, propositie-type, accent-kleur |
| `aanleiding.py` | Maatschappelijk vraagstuk + uitdagingen + behoefte (3 blokken) |
| `section_header.py` | Gekleurde divider-slide met sectietitel |
| `aanpak_overview.py` | Chevrons (2–5) met fase-namen en korte beschrijving |
| `fase_detail.py` | Twee kolommen: doel/aanpak links, acties/deliverable rechts |
| `two_column.py` | Vrije twee-kolom layout (voor proposities zonder vaste fases) |
| `team.py` | 2–3 teamleden met naam, titel, bio |
| `budget_table.py` | Begroting-tabel + notitie + betaaltermijnen |
| `randvoorwaarden.py` | Bulletlijst van randvoorwaarden |
| `tijdslijn.py` | Tekstuele tijdlijn (de visuele Gantt blijft handmatig) |
| `akkoord.py` | Twee signing-boxes + facturatieschema |

---

### Word component library (`scripts/word/`)

Voor schrijvers die een Word-offerte willen. Elke component is een `python-docx`-functie `add_[type]_section(doc, content) -> None`. Structuur is lineair (geen slides) — de volgorde is: cover-pagina, aanleiding, aanpak, team, begroting, akkoord.

| Component | Beschrijving |
|-----------|-------------|
| `cover.py` | Titelpagina met klant, propositie-type, datum, SFNL-logo |
| `aanleiding.py` | Vraagstuk + uitdagingen + behoefte als doorlopende tekst |
| `aanpak_section.py` | Fases als genummerde secties met doel, aanpak, deliverables |
| `team.py` | Teamleden als tekstblokken |
| `budget_table.py` | Begroting-tabel |
| `akkoord.py` | Randvoorwaarden + betaaltermijnen + signing-sectie |

**`scripts/assemble_word.py`** — ontvangt hetzelfde `slide_plan` JSON-formaat (type-namen zijn identiek), bouwt een `.docx`.

**Keuze tijdens intake:** De agent vraagt vroeg in de intake: *"Wil je de offerte als PowerPoint presentatie of als Word document?"* Daarna loopt hetzelfde intake-proces — alleen de output-stap verschilt.

---

### Assembler (`scripts/assemble.py`)

Ontvangt een `slide_plan` (JSON-lijst van `{type, content}`-dicts), opent `sfnl_base.pptx`, roept de componenten aan in volgorde, en slaat de output op als `.pptx`.

```json
[
  {"type": "cover",     "content": {"client": "Org X", "title": "PROJECTTITEL", "date": "april 2026"}},
  {"type": "aanleiding","content": {"vraagstuk": "...", "uitdagingen": "...", "behoefte": "..."}},
  {"type": "fase_detail","content": {"number": 1, "naam": "Meetplan", "doel": "...", "aanpak": "...",
                                     "acties_sfnl": ["..."], "acties_klant": ["..."],
                                     "deliverable": "...", "dagen": 8, "tijdlijn": "mei–juni 2026"}},
  {"type": "team",      "content": {"members": [{"name": "...", "title": "...", "bio": "..."}]}},
  {"type": "budget_table","content": {"rows": [...], "totaal": 38000, "termijnen": [...]}},
  {"type": "randvoorwaarden","content": {"items": ["..."]}},
  {"type": "akkoord",   "content": {"termijnen": [...]}}
]
```

---

### Propositie-profielen (`skills/sfnl-offerte/references/*.md`)

Per propositie een markdown-referentiebestand. De orchestrator laadt dit alleen wanneer de betreffende propositie aan bod komt (progressive disclosure). Elk bestand bevat: accent-kleur, typische skeleton, intake-vragen, typische fases, en aandachtspunten.

**Voorbeeld: `references/impact_meten.md`**
```markdown
# Impact Meten & Management

**Accent-kleur:** #2B4D8E
**Typische sub-proposities:** Meetplan · Impact meten · Impact monitoring/dashboard

## Typische skeleton
cover → aanleiding → section_header → aanpak_overview →
fase_detail × 2 → tijdslijn → section_header → team →
section_header → budget_table → randvoorwaarden → akkoord

## Intake-vragen
- Wat meet de organisatie al, en wat ontbreekt?
- Is er al een verandertheorie of theory of change beschikbaar?
- Welke stakeholders moeten de meetuitkomsten gebruiken?

## Typische fases
1. Meetplan
2. Impact meten
(Sub-propositie 'Impact monitoring/dashboard' voegt fase 3 toe)
```

Referenties voor alle zes proposities:
- `references/mbc.md`
- `references/impact_meten.md`
- `references/advies_innovatieve_financiering.md`
- `references/intermediair_innovatieve_financiering.md`
- `references/fondsmanagement.md`
- `references/partnerschappen.md`

---

### Skill-specificaties

Beide SKILL.md-bestanden volgen de plugin-dev standaard:
- **Derde persoon in frontmatter description** met concrete trigger-zinnen
- **Imperatieve schrijfvorm** in de body (niet: "je moet...", wel: "Laad het propositie-profiel...")
- **Lean body** (≤2.000 woorden) — details naar `references/`
- **Expliciete verwijzingen** naar alle resources in `references/`, `scripts/`, `assets/`

Trigger-beschrijvingen:

```yaml
# sfnl-offerte/SKILL.md
name: sfnl-offerte
description: >
  This skill should be used when the user asks to "schrijf een offerte",
  "nieuwe offerte", "offerte voor [organisatie]", or mentions a specific
  SFNL proposition (MBC, impact meten, advies innovatieve financiering,
  fondsmanagement, partnerschappen). Guides the full proposal workflow
  from intake to PPTX or Word output.
```

```yaml
# pptx-offerte/SKILL.md
name: pptx-offerte
description: >
  This skill should be used when a slide_plan JSON is ready and needs
  to be assembled into a PowerPoint (.pptx) or Word (.docx) proposal
  in SFNL house style. Called by sfnl-offerte after intake completion.
```

### Skills — enige entry point voor de gebruiker

Werkwijze:
1. Herkent de propositie (of vraagt ernaar)
2. Vraagt vroeg in de intake: *"Wil je de offerte als PowerPoint of als Word document?"*
3. Laadt `profiles/[propositie].json`
4. Voert adaptieve intake uit:
   - Toont typische skeleton → gebruiker bevestigt of past aan
   - Doorloopt propositie-specifieke intake-vragen
   - Stemt slide-compositie af ("Gezien jullie aanpak stel ik voor de Gantt weg te laten en een `two_column` toe te voegen voor de meetmethodiek")
5. Werkt inhoud per slide-type uit (fases, team, budget, randvoorwaarden)
6. Produceert `slide_plan` + config JSON
7. Roept `pptx-offerte` aan met output-formaat vlag (`--format pptx` of `--format docx`)

**`pptx-offerte` (assembler)** — uitgebreid naar PPTX én Word output

- Ontvangt `slide_plan` + output-formaat
- **PPTX**: roept `assemble.py` aan → aangevuld met XML-editing voor nauwkeurige plaatsing
- **Word**: roept `assemble_word.py` aan → python-docx pipeline, geen XML-editing nodig
- Voert visuele QA uit (screenshots voor PPTX; layout-controle voor Word)

---

## Bouwvolgorde

### Fase 1 — Fundament
1. `.claude-plugin/plugin.json` aanmaken
2. `skills/pptx-offerte/assets/sfnl_base.pptx` aanmaken (MBC-template strippen)
3. `skills/pptx-offerte/assets/sfnl_base.docx` aanmaken (op basis van brandbook)
4. `data/style.json` definiëren
5. `skills/pptx-offerte/scripts/assemble.py` + `assemble_word.py` bouwen
6. Eerste componenten (PPTX + Word parallel): `cover`, `section_header`, `aanleiding`, `team`
7. `skills/pptx-offerte/references/slide_components.md` + `xml_editing.md` schrijven

### Fase 2 — MBC-migratie (validatie van de pipeline)
8. Resterende PPTX-componenten: `aanpak_overview`, `fase_detail`, `budget_table`, `randvoorwaarden`, `tijdslijn`, `akkoord`
9. Resterende Word-componenten: `aanpak_section`, `budget_table`, `akkoord`
10. `skills/sfnl-offerte/references/mbc.md` schrijven
11. `sfnl-offerte` SKILL.md herschrijven (lean, imperatief, verwijzingen naar references/)
12. `pptx-offerte` SKILL.md herschrijven (lean, trigger-beschrijving, verwijzingen naar scripts/assets/)
13. `review_offerte.py` compatibel maken met nieuwe output

### Fase 3 — Nieuwe proposities (iteratief)
14. Per propositie: `references/[propositie].md` schrijven + ontbrekende componenten toevoegen
15. Volgorde op basis van vraag: Impact Meten eerst, daarna de rest

### Fase 4 — Agent verdieping
11. Skeleton-afstemming tijdens intake verfijnen
12. Propositie-specifieke intake-vragen kalibreren op basis van echte offertes

---

## Verificatie

Na Fase 1+2 is het systeem verifieerbaar:
- Genereer een MBC-offerte via de nieuwe pipeline
- Vergelijk output visueel met een via de oude pipeline gegenereerde offerte
- Draai `review_offerte.py` — exit code 0 verwacht
- Controleer: boilerplate-slides 17+ aanwezig, geen placeholder-tekst zichtbaar, budget-tabel correct

Per nieuwe propositie (Fase 3): genereer een test-offerte met dummy-content in zowel PPTX als Word, controleer visueel op stijlconsistentie met MBC-output.
