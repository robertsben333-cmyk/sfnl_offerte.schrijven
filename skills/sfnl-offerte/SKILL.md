---
name: sfnl-offerte
description: >
  Write a Social Finance NL proposal (offerte) for a maatschappelijke businesscase en duurzame
  financiering project. Trigger when the user types /sfnl-offerte, asks to "schrijf een offerte",
  "nieuwe offerte", or wants to create a proposal for Social Finance NL's MBC proposition.
  This skill orchestrates a structured conversation across 3 steps and then generates a PPTX file.
---

# SFNL Offerte Skill — Maatschappelijke Businesscase

## Project files
All skill assets are bundled with this plugin at `${CLAUDE_PLUGIN_ROOT}`:

- **Template**: `${CLAUDE_PLUGIN_ROOT}/templates/offerte_mbc_template.pptx`
- **Team data**: `${CLAUDE_PLUGIN_ROOT}/data/team.json`
- **Generator**: `${CLAUDE_PLUGIN_ROOT}/scripts/generate_offerte.py`
- **Reviewer**: `${CLAUDE_PLUGIN_ROOT}/scripts/review_offerte.py`
- **Output**: ask user for output folder; default to current working directory

## Workflow overview

```
STEP 1  →  Ask intake questions (1 message)
STEP 2a →  Propose: doel, doelgroep, context, aandachtspunten (user confirms/edits)
STEP 2b →  Propose: fases + dag-schattingen + tijdlijn (user confirms/edits)
STEP 2c →  Propose: outcomes-tier, team, tarief, budget, betalingsschema (user confirms/edits)
GENERATE → Build config JSON → run generator → open review
```

---

## STEP 1 — Intake

Ask all of these in **one Dutch message**. Keep it brief and conversational — no long preambles.

1. Naam van de organisatie en contactpersoon
2. Beschrijf de interventie kort: wat doen ze, voor wie, hoe lang al?
3. Wat is de aanleiding voor de offerte — waarom nu?
4. Zijn er al relevante documenten (businessplan, evaluatierapport, eerdere studies) die je kunt delen?
5. Zijn er bijzondere omstandigheden (deadline, lopende gesprekken met financiers, politieke gevoeligheden)?

Do **not** ask about goals, target groups, phases, budget or team yet. You will propose all of that in step 2.

---

## STEP 2a — Propose: Doel & Doelgroep

Based on the intake, propose all of the following **in one message**. Present them clearly so the user can confirm or edit each item inline.

### 2a.1 Project title (slide 3 header)
One punchy sentence in ALL CAPS, max 15 words. Pattern: `[INTERVENTIENAAM] [ORGANISATIE]: [KERNBOODSCHAP]`
Example: `VROUWENSPREEKUUR BIJ AMSTERDAM UMC: INVESTEREN IN TOEGANKELIJKE ZORG MET IMPACT OP GEZONDHEID, WERK EN MAATSCHAPPIJ`

### 2a.2 Maatschappelijk vraagstuk (1 paragraph, 80-120 words)
Describe the societal problem the intervention addresses. Specific, data-grounded where possible. No fluffy language.

### 2a.3 Grootste uitdagingen (1 paragraph, 60-100 words)
What makes this problem hard to solve — fragmented funding, system barriers, attribution, lack of data?

### 2a.4 Behoefte van de klant (1 paragraph, 80-120 words)
What does this client specifically want from the businesscase? Link to their strategic goals (intern draagvlak / opschaling / duurzame financiering / combinatie).

### 2a.5 Doelgroep + stakeholders
- Primaire doelgroep (who benefits)
- Betalende partijen (who pays currently)
- Potentiële financiers (who should pay in the future: gemeente, zorgverzekeraar, werkgever, fonds, etc.)

### 2a.6 Aandachtspunten voor de klant
Suggest 3-5 specific points that this client will likely care about, based on context. Label each with a short heading. For example:
- "Intern draagvlak: Amsterdam UMC wil intern aantonen dat het spreekuur structureel bekostigd moet worden"
- "Werkgeversbaten: verzuimreductie en productiviteitswinst zijn financieel kwantificeerbaar voor HR-directors"
- "Opschaalbaarheid: de businesscase moet ook andere ziekenhuizen overtuigen"

Then ask: "Wil je iets toevoegen of aanpassen?"

---

## STEP 2b — Propose: Fases & Tijdlijn

Based on 2a, propose the phase structure **in one message**.

### Default phase structure (always start with this unless there's a clear reason to deviate)

**Fase 1: Impactnarratief**
- Verandertheorie opstellen
- Effectenkaart ontwikkelen + outcomes selecteren
- Kick-off en validatiesessie

**Fase 2: Maatschappelijke businesscase**
- Outcomes financieel waarderen
- Data verzamelen en analyseren
- Businesscase opstellen en valideren

**Fase 3: Advies duurzame financiering en communicatie**
- Financieringsopties in kaart brengen
- Kernboodschappen formuleren
- Eindrapport + publiekssamenvatting

**Deviation rule**: If context clearly calls for a different structure (e.g. a Phase 4 for financial business planning, or a combined Phase 1+2 for a small impact scan), propose the alternative AND explicitly state why you are deviating from the standard. Ask for explicit user confirmation before proceeding.

### Day estimates by complexity tier

Use the outcomes complexity (determined in step 2c) and these benchmarks from past proposals:

| Tier         | Outcomes | Fase 1  | Fase 2   | Fase 3  | Total    | Budget (@€1.480) |
|--------------|----------|---------|----------|---------|----------|------------------|
| Basic        | 6-8      | 5-7d    | 8-11d    | 3-5d    | 16-23d   | €24K-34K         |
| Standaard    | 9-12     | 7-9d    | 12-16d   | 5-7d    | 24-32d   | €36K-47K         |
| Complex      | 13+      | 9-12d   | 16-22d   | 7-10d   | 32-44d   | €47K-65K         |

**Adjustment factors** (add days on top):
- +2-4d: meer dan 3 stakeholdertypen voor financiering (fase 3)
- +2-3d: beperkte beschikbaarheid van data of complexe attributie (fase 2)
- +1-2d per extra interviewgroep (bijv. patiënten én werkgevers én gemeente)
- Optional fase 4 (financieel businessplan / implementatieadvies): 8-15d extra

**Propose the day estimates with brief reasoning.** Example:
> "Op basis van de beschrijving stel ik een standaard businesscase voor (9-12 outcomes):
> Fase 1: 8 dagen, Fase 2: 14 dagen, Fase 3: 6 dagen. Totaal: 28 dagen.
> De extra 2 dagen in fase 2 zijn voor de beperkte data-beschikbaarheid vanuit de pilotfase."

### Timeline
Propose a realistic total timeline in months based on total days + delivery rhythm.
Rule of thumb: 1 month per 8 workdays (accounting for review cycles, vacation, parallel work).
Express as: "BINNEN [N] MAANDEN STELLEN WE DE MAATSCHAPPELIJKE BUSINESSCASE OP EN BRENGEN WE DE HAALBAARHEID VAN EEN DUURZAAM FINANCIERINGSMODEL IN KAART"

---

## STEP 2c — Propose: Outcomes, Team, Tarief & Budget

### Outcomes tier
State your proposed tier explicitly and include the count in the proposal text for fase 1.
The phrase to use in the offerte (inside the fase 1 description):
`"Binnen het huidige budget werken we [N] outcomes financieel uit."`
For a range: `"Binnen het huidige budget werken we 8 tot 10 outcomes financieel uit; bij een verruimd budget kunnen we dit uitbreiden naar 12 outcomes."`

### Team
Read `${CLAUDE_PLUGIN_ROOT}/data/team.json`. Based on the project type and client, suggest:
- 1 supervisor from: Els, Björn, Ruben, Laura, Michalli
- 1 project manager from: managers list
- 1-2 associates/analysts

Prefer team members with relevant domain experience (healthcare → Laura; international/scaling → Björn; etc.).
Ask the user to confirm or select differently: "Kloppen deze teamleden, of wil je anderen?"

### Day rate
**Always ask explicitly**: "Geldt het standaardtarief van €1.480 per dag, of het NGO-tarief van €1.280?"
Only use a different rate if the user explicitly specifies one.

### Budget calculation
Calculate: `total_days × day_rate = total_excl_btw`
BTW: 21% on top.
Propose payment schedule (choose based on project size):
- **Small (<20d)**: 50% bij aanvang, 50% bij oplevering
- **Medium (20-35d)**: 33% bij aanvang, 33% na fase 2, 34% bij oplevering eindrapport
- **Large (>35d)**: 33% bij start, 33% na fase 1, 34% bij oplevering

Show all numbers clearly so user can confirm.

---

## GENERATE — Build config & run script

Once all 3 steps are confirmed, build the config JSON and run the generator.

### 1. Build the config file
Ask the user where to save the output if not specified. Save config alongside the PPTX.

Config structure:
```json
{
  "client_name": "...",
  "contact_person": "...",
  "project_title": "...",
  "proposal_date": "maand jaar",
  "day_rate": 1480,
  "factuuradres": null,

  "aanleiding": {
    "summary_line": "...",
    "maatschappelijk_vraagstuk": "...",
    "grootste_uitdagingen": "...",
    "behoefte_van_klant": "..."
  },

  "aanpak": {
    "overview_subtitle": "IN DRIE FASES BRENGEN WE...",
    "fases": [
      {
        "number": 1,
        "name": "IMPACTNARRATIEF",
        "overview_description": "Het impactnarratief beschrijft...",
        "doel": "...",
        "aanpak": "...",
        "acties_sfnl": ["Deskresearch", "Kick-off meeting organiseren", "..."],
        "acties_klant": ["Documentatie aanleveren", "Deelname interviews", "..."],
        "deliverable": "Verandertheorie, effectenkaart en geselecteerde outcomes",
        "dagen": 8,
        "tijdlijn": "november - december 2025",
        "outcomes_note": "Binnen het huidige budget werken we 9 outcomes financieel uit."
      },
      { "number": 2, "name": "MAATSCHAPPELIJKE BUSINESSCASE", "...": "..." },
      { "number": 3, "name": "ADVIES DUURZAME FINANCIERING EN COMMUNICATIE", "...": "..." }
    ]
  },

  "tijdslijn": {
    "maanden": 4,
    "header": "BINNEN VIER MAANDEN STELLEN WE DE MAATSCHAPPELIJKE BUSINESSCASE OP"
  },

  "team": [
    { "name": "Laura Brouwer", "title_short": "ASSOCIATE DIRECTOR", "bio": "..." },
    { "name": "Dieuwertje Roos", "title_short": "MANAGER", "bio": "..." },
    { "name": "Dorine Klein Gunnewiek", "title_short": "ANALYST", "bio": "..." }
  ],

  "begroting": {
    "rows": [
      { "fase": "Fase 1: Impactnarratief", "dagen": 8, "tarief": 1480, "totaal": 11840 },
      { "fase": "Fase 2: Maatschappelijke businesscase", "dagen": 14, "tarief": 1480, "totaal": 20720 },
      { "fase": "Fase 3: Advies duurzame financiering", "dagen": 6, "tarief": 1480, "totaal": 8880 }
    ],
    "total_excl_btw": 41440,
    "btw_percentage": 21,
    "btw": 8702,
    "total_incl_btw": 50142,
    "betaaltermijnen": [
      { "description": "Bij aanvang project (33%)", "amount": 13675 },
      { "description": "Na afronding fase 2 (33%)", "amount": 13675 },
      { "description": "Bij oplevering eindrapport (34%)", "amount": 14090 }
    ]
  }
}
```

### 2. Run the generator
```bash
py "${CLAUDE_PLUGIN_ROOT}/scripts/generate_offerte.py" \
   "config_[slug].json" \
   "[OUTPUT_PATH]/[YYYYMMDD] Offerte [Klant] SFNL.pptx"
```

**Extra fases (4+)**: If there are more than 3 fases, the generator prints a notice but does NOT insert them automatically — the overview slide (slide 6) only has 3 chevrons, so mechanical insertion would create a visual inconsistency. Handle extra fases as an explicit step after generation:
1. First check: does fase 4 warrant its own slide, or can it be integrated into fase 3's text?
2. If it needs a slide, use `insert_extra_fase()` from the module:
```python
from pathlib import Path; import sys; sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
from generate_offerte import Presentation, insert_extra_fase
prs = Presentation("output/[file].pptx")
insert_extra_fase(prs, cfg["aanpak"]["fases"][3], "[client_name]", extra_count=0)
prs.save("output/[file].pptx")
```
3. Tell the user to adjust the overview slide (slide 6) manually in PowerPoint — add or relabel the 4th chevron.

---

## REVIEW

After generation, launch a **general-purpose sub-agent** to review the output. The sub-agent should:

### 1. Run the deterministic review script
```bash
py "${CLAUDE_PLUGIN_ROOT}/scripts/review_offerte.py" \
   "[output_pptx_path]" \
   "[config_json_path]"
```

This checks: budget math, placeholder text, forbidden words, em-dash bullets, long sentences.

### 2. Read the PPTX and do qualitative assessment
```bash
py -c "
from pptx import Presentation
prs = Presentation(r'[output_path]')
for i, slide in enumerate(prs.slides[:16]):
    print(f'\n=== Slide {i+1} ===')
    for shape in slide.shapes:
        if hasattr(shape, 'text') and shape.text.strip():
            print(shape.text[:400])
"
```

Check qualitatively:
- Passive voice where active would be clearer
- Vague claims without concrete evidence ("uitstekende resultaten", "sterke track record")
- Tone consistency — professional but not stiff
- Whether the summary_line on the aanleiding slide is punchy and specific

### 3. Extra slides assessment
Based on the client context, flag any slides worth adding manually:
- A "Samenwerking" / collaboration slide if the engagement involves co-creation
- A reference project slide if there's a directly comparable past case
- An optional fase 4 slide if a financial business plan was discussed

### 4. Return a structured report
```
SFNL REVIEW RAPPORT — [klant naam]

AUTOMATISCHE CHECKS (review_offerte.py)
  [paste script output here]

KWALITATIEVE BEVINDINGEN
  ✗ [issue] / ✓ [OK]
  ...

AANBEVOLEN EXTRA SLIDES
  - [slide suggestion or "Geen"]

EINDOORDEEL: KLAAR VOOR VERZENDING / AANPASSINGEN NODIG
```

After the sub-agent returns, share the report with the user and offer to fix any flagged issues.

---

## Writing rules (Dutch)

These rules apply to ALL text you write for the proposals:

**Language**: Dutch throughout. Professional but direct.

**Never use**:
- "alsmede", "tevens", "waarbij", "derhalve", "teneinde", "ten behoeve van", "in het kader van"
- Em-dash (–) to introduce sub-clauses or bullet points
- "gedegen", "robuust", "uitstekend", "innovatief" (without concrete support)
- "wij zijn verheugd", "graag", "hierbij" to open sentences
- Passive voice when active is available

**Always use**:
- Active voice: "We brengen de kosten in kaart" not "De kosten worden in kaart gebracht"
- Concrete numbers and specifics: "8 outcomes", "4 interviews", "28 werkdagen"
- Short sentences (max ~25 words for body text)
- The client's specific intervention name, not generic "de interventie"

**Slide header style** (all caps, wide tracking):
- Pattern: `[ACTIE/RESULTAAT]: [SPECIFIEK VOOR DEZE KLANT]`
- Example: `BINNEN VIER MAANDEN STELLEN WE DE MAATSCHAPPELIJKE BUSINESSCASE OP EN BRENGEN WE DE HAALBAARHEID VAN EEN DUURZAAM FINANCIERINGSMODEL IN KAART`

---

## Historical reference benchmarks

| Project          | Fases | Outcomes | Totaal dagen | Budget (excl. BTW) | Tarief/dag |
|------------------|-------|----------|--------------|--------------------|------------|
| AUMC Vrouwenspreekuur (2025) | 3 | 6 (basic) | ~27 | €44.831 | €1.480 |
| Jeroen Pit Huis (2025) | 4 | ~12 | 29 | €44.080 | ~€1.520 |
| Welzijn op Recept Venlo (2025) | 4 | ~14 | 52 | €77.066 | €1.440 |
| Het Beweeghuis (2023) | 3 | ~10 | 30 | €39.600 | €1.320 |
| CCN (2023) | 3 | ~8 | 15 | €21.840 | €1.456 |
| Impact Scan Lichthuis (2022) | 1 | ~4 | 10 | €10.000 | €1.000 |
