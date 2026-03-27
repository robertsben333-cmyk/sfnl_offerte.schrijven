---
name: sfnl-offerte
description: >
  Write a Social Finance NL proposal (offerte) for a maatschappelijke businesscase (MBC) en
  duurzame financiering project. Use this skill whenever the user wants to create, draft, or
  generate an SFNL proposal or offerte — including when they say "schrijf een offerte",
  "nieuwe offerte", "maak een offerte", "offerte voor [klant]", "MBC voorstel", or "/sfnl-offerte".
  Also trigger when a colleague mentions they're preparing a pitch, voorstel, or aanbieding for
  a new client, or wants to start the offerte process for any organisation. This skill guides the
  user through a structured 3-step conversation (intake → inhoud → budget/team) and then generates
  a formatted PPTX proposal file using the SFNL house template.
---

# SFNL Offerte Skill — Maatschappelijke Businesscase

## Setup voor nieuwe gebruikers
Eenmalig uitvoeren na het uitpakken van de plugin-zip:
```bash
py install.py
# of, als de template PPTX ergens op je schijf staat:
py install.py --template "pad/naar/offerte_mbc_template.pptx"
```
Dit installeert python-pptx, kopieert de SKILL naar `~/.claude/skills/sfnl-offerte/` en zet de projectbestanden klaar in `~/.projects SFNL/sfnl_offerte.schrijven/`. De template kun je opvragen bij een collega of via SharePoint.

---

## Project files
Alle skill-assets staan in: `~/.projects SFNL/sfnl_offerte.schrijven/`
(op Windows: `%USERPROFILE%\.projects SFNL\sfnl_offerte.schrijven\`)

- **Template**: `templates\offerte_mbc_template.pptx`
- **Team data**: `data\team.json`
- **Review script**: `scripts\review_offerte.py` (budget math, placeholders, forbidden words)
- **Output**: ask user for output folder; default to `output\`

## Workflow overview

```
STEP 1  →  Ask intake questions (1 message)
STEP 2a →  Propose: doel, doelgroep, context, aandachtspunten (user confirms/edits)
STEP 2b →  AskUserQuestion: complexity tier → Propose: fases + dag-schattingen + tijdlijn
STEP 2c →  AskUserQuestion: tarief + team → Propose: outcomes, budget, betalingsschema
GENERATE → Build config JSON → invoke pptx skill to fill template → review
```

**Interactivity rule**: Use the `AskUserQuestion` tool at every key decision point (marked ⬡ below) to present 3 concrete options. Always include an open "Andere keuze / eigen input" option as the fourth. Never assume — always let the user pick before you calculate.

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

### 2a.2 Maatschappelijk vraagstuk — use AskUserQuestion with 3 formulations

Write 3 versions of the maatschappelijk vraagstuk paragraph (80-120 words each). The variants should differ meaningfully — not just word-by-word, but in angle or emphasis. For example:
- **Variant A**: Opens with a striking statistic or concrete scale of the problem
- **Variant B**: Opens from the perspective of the affected person/doelgroep
- **Variant C**: Opens with the systemic or structural framing

Present all 3 using `AskUserQuestion`:
- **Header**: `"Maatschappelijk vraagstuk"`
- **Question**: `"Welke formulering van het maatschappelijk vraagstuk past het best?"`
- **Option A / B / C**: the three paragraph texts (shown in full as the option description)
- **Option D**: `"Geen van deze — ik pas zelf aan"`

### 2a.3 Grootste uitdagingen — use AskUserQuestion with 3 formulations

Write 3 versions (60-100 words each) that differ in which barriers they foreground. For example:
- **Variant A**: Emphasises data/attribution challenges
- **Variant B**: Emphasises fragmented funding landscape and multiple payers
- **Variant C**: Emphasises organisational or political barriers to change

Present all 3 using `AskUserQuestion`:
- **Header**: `"Grootste uitdagingen"`
- **Question**: `"Welke formulering van de uitdagingen klopt het best?"`
- **Option A / B / C**: the three texts
- **Option D**: `"Geen van deze — ik pas zelf aan"`

### 2a.4 Behoefte van de klant — use AskUserQuestion with 3 formulations

Write 3 versions (80-120 words each) that differ in strategic emphasis. For example:
- **Variant A**: Focuses on intern draagvlak / intern bewijs
- **Variant B**: Focuses on opschaling en nieuwe financiers aantrekken
- **Variant C**: Focuses on duurzame bekostiging / continuïteit

Present all 3 using `AskUserQuestion`:
- **Header**: `"Behoefte van de klant"`
- **Question**: `"Welke omschrijving van de behoefte sluit het best aan?"`
- **Option A / B / C**: the three texts
- **Option D**: `"Geen van deze — ik pas zelf aan"`

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
- Overzicht van stakeholders met wie het initiatief in gesprek kan gaan (op basis van analyse-uitkomsten)
- Stakeholdergerichte communicatielijn: kernboodschappen per stakeholder voor de drie belangrijkste stakeholders
- Presentatieslides per stakeholder (top 3) met communicatielijn
- Stappenplan om de inzichten van de businesscase in te zetten voor toekomstige financiering
- **Optioneel: publiekssamenvatting** — dit is een bewuste keuze met bijbehorende extra kosten. Altijd expliciet als aparte optie benoemen met prijskaartje. NIET standaard meenemen — voorkomen dat dit in volgende offertes als vanzelfsprekend wordt opgenomen.

**Deviation rule**: If context clearly calls for a different structure (e.g. a Phase 4 for financial business planning, or a combined Phase 1+2 for a small impact scan), propose the alternative AND explicitly state why you are deviating from the standard. Ask for explicit user confirmation before proceeding.

### ⬡ Complexity tier — use AskUserQuestion BEFORE proposing day estimates

Read the intake notes and form your own recommendation. Then present the choice using `AskUserQuestion`:

- **Header**: `"Complexiteit"`
- **Question**: `"Op basis van de intake schat ik dit in als [jouw aanbeveling]. Welk complexiteitsniveau kies je?"`
- **Option A**: `"Basic — 6-8 outcomes · 16-23 werkdagen · ~€24K-34K excl. BTW"`
- **Option B**: `"Standaard — 9-12 outcomes · 24-32 werkdagen · ~€36K-47K excl. BTW"`
- **Option C**: `"Complex — 13+ outcomes · 32-44 werkdagen · ~€47K-65K excl. BTW"`
- **Option D**: `"Andere inschatting (vul zelf in)"`

Mention your recommendation in the question text, e.g. "Op basis van de complexe doelgroep en beperkte data stel ik **Standaard** voor." Use the confirmed tier for all subsequent day estimates.

### Day estimates by complexity tier

Use the outcomes complexity (determined above) and these benchmarks from past proposals:

| Tier         | Outcomes | Fase 1  | Fase 2   | Fase 3  | Total    | Budget (@€1.480) |
|--------------|----------|---------|----------|---------|----------|------------------|
| Basic        | 6-8      | 5-7d    | 8-11d    | 3-5d    | 16-23d   | €24K-34K         |
| Standaard    | 9-12     | 7-9d    | 12-16d   | 5-7d    | 24-32d   | €36K-47K         |
| Complex      | 13+      | 9-12d   | 16-22d   | 7-10d   | 32-44d   | €47K-65K         |

**Adjustment factors** (add days on top):
- +2-4d: meer dan 3 stakeholdertypen voor financiering (fase 3)
- +2-3d: beperkte beschikbaarheid van data of complexe attributie (fase 2)
- +1-2d per extra interviewgroep (bijv. patiënten én werkgevers én gemeente)
- +2-3d: persona-methodiek voor diverse doelgroep (fase 1-2) — altijd voorstellen bij complex tier of wanneer doelgroep meerdere duidelijk verschillende subgroepen heeft; hogere validiteit maar extra tijd voor karakterisering en validatiesessies
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

### ⬡ Team + Tarief — use AskUserQuestion (both in one call)

Read `data/team.json` first. Then present **both choices in a single `AskUserQuestion` call** with 2 questions — this keeps the conversation flowing without two separate interruptions.

**Question 1 — Team:**
- **Header**: `"Team"`
- **Question**: `"Welk team stel je voor deze opdracht voor?"`
- **Option A / B / C**: Each = 1 supervisor + 1 manager + 1-2 associates/analysts + 1-line rationale. Example: `"Laura Brouwer + Dieuwertje Roos + Dorine Klein Gunnewiek — Laura heeft sterke achtergrond in zorg en preventie"`
- **Option D**: `"Andere samenstelling (vul zelf in)"`

Domain hints: healthcare/GGZ → Laura; international/scaling → Björn; finance/systemic → Ruben; government/policy → Els; social enterprise → Michalli.

**Question 2 — Tarief:**
- **Header**: `"Tarief"`
- **Question**: `"Welk dagtarief hanteren we voor deze opdracht?"`
- **Option A**: `"Standaard — €1.480 per dag (commercieel tarief)"`
- **Option B**: `"NGO-tarief — €1.280 per dag (maatschappelijke organisatie)"`
- **Option C**: `"Ander tarief (specificeer)"`

Only calculate the budget after both are confirmed.

### Tarief kanttekening
Always include this note in the begroting slide:
> "Het tarief is een teamtarief gebaseerd op een team bestaande uit een director, manager en associate/analyst."

If a **reduced rate** is agreed (NGO-tarief or custom discount), draft a motivation paragraph covering:
1. Waarom SFNL gelooft dat dit project bijdraagt aan sociale impact
2. Het gereduceerde tarief en het standaardtarief ter vergelijking
3. Waarom SFNL dit wil honoreren

Stel dit als concepttekst voor en vraag de gebruiker om het te bevestigen voor het in de offerte gaat. Voorbeeld-structuur (altijd aanpassen aan de specifieke casus):
> "Voor deze opdracht hanteren we een gereduceerd Social Finance NL tarief van €[x] per dag (op basis van 8 uur). Het standaardtarief van Social Finance NL bedraagt €1.480 per dag. Wij zijn van mening dat [kernmotivatie specifiek voor klant/interventie]. Social Finance NL wil hier graag aan bijdragen en om dit kracht bij te zetten hanteren wij voor deze opdracht een gereduceerd tarief."

### Randvoorwaarden (slide 12 — "Randvoorwaarden voor succes")

> ⚠️ **Slide mapping**: Randvoorwaarden gaan op **slide 12** ("RANDVOORWAARDEN VOOR SUCCES"), NIET op de akkoord-slide. De akkoord-slide (slide 17) bevat alleen handtekeningblokken — zie de "Akkoord" sectie hieronder.

Stel de volgende standaard randvoorwaarden altijd voor in stap 2c. De gebruiker kan items toevoegen of verwijderen.

**Standaard randvoorwaarden (altijd meenemen):**
1. Het tijdig aanleveren van relevante documentatie, (financiële) data en deelnemersgegevens
2. Het tijdig beschikbaar stellen van stakeholders voor interviews en het faciliteren van een warme introductie
3. De beschikbaarheid van deelnemersgegevens m.b.t. in- en uitstroomposities van deelnemers
4. Een vast aanspreekpunt binnen de organisatie gedurende het gehele traject
5. Data wordt aangeleverd in een gestructureerd, leesbaar formaat (bij voorkeur Excel); ruwe bestanden zonder toelichting worden niet geaccepteerd

Present them briefly — "Ik stel de volgende standaard randvoorwaarden voor, wil je er iets aan toevoegen of weglaten?" — then include the confirmed list in the config JSON under `randvoorwaarden`.

### ⬡ Akkoord / ondertekening (slide 17)

Slide 17 ("RANDVOORWAARDEN EN AKKOORD") bevat twee handtekeningblokken: één voor de klant (links) en één voor Social Finance NL (rechts). Vraag expliciet wie namens SFNL ondertekent:

> "Wie ondertekent de offerte namens Social Finance NL? (Naam + functie)"

Sla dit op als `sfnl_signatory` in de config. Standaard is dit de lead uit het team (doorgaans de director). Als de user niets opgeeft, gebruik dan de eerste persoon in de `team` array.

Het klant-ondertekeningsblok wordt gevuld met `contact_person` (naam) + `client_name` (organisatie).

### Budget calculation
Calculate: `total_days × day_rate = total_excl_btw`
BTW: 21% on top.
Propose payment schedule (choose based on project size):
- **Small (<20d)**: 50% bij aanvang, 50% bij oplevering
- **Medium (20-35d)**: 33% bij aanvang, 33% na fase 2, 34% bij oplevering eindrapport
- **Large (>35d)**: 33% bij start, 33% na fase 1, 34% bij oplevering

Show all numbers clearly so user can confirm.

---

## GENERATE — Build config & invoke the pptx-offerte skill

Once all 3 steps are confirmed:

### 1. Build the config file
Save to: `output/config_[klant_slug]_[YYYYMMDD].json`

```json
{
  "client_name": "...",
  "contact_person": "...",
  "project_title": "...",
  "proposal_date": "maand jaar",
  "day_rate": 1480,
  "factuuradres": null,
  "sfnl_signatory": {
    "name": "Laura Brouwer",
    "title": "Social Finance NL"
  },
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
        "number": 1, "name": "IMPACTNARRATIEF",
        "overview_description": "...", "doel": "...", "aanpak": "...",
        "acties_sfnl": ["..."], "acties_klant": ["..."],
        "deliverable": "...", "dagen": 8, "tijdlijn": "...",
        "outcomes_note": "Binnen het huidige budget werken we 9 outcomes financieel uit."
      },
      { "number": 2, "name": "MAATSCHAPPELIJKE BUSINESSCASE", ... },
      { "number": 3, "name": "ADVIES DUURZAME FINANCIERING EN COMMUNICATIE", ... }
    ]
  },
  "tijdslijn": { "maanden": 4, "header": "BINNEN VIER MAANDEN..." },
  "team": [
    { "name": "Laura Brouwer", "title_short": "ASSOCIATE DIRECTOR", "bio": "..." },
    { "name": "Dieuwertje Roos", "title_short": "MANAGER", "bio": "..." },
    { "name": "Dorine Klein Gunnewiek", "title_short": "ANALYST", "bio": "..." }
  ],
  "begroting": {
    "rows": [{ "fase": "Fase 1: Impactnarratief", "dagen": 8, "tarief": 1480, "totaal": 11840 }, ...],
    "total_excl_btw": 41440, "btw_percentage": 21, "btw": 8702, "total_incl_btw": 50142,
    "tarief_kanttekening": "Het tarief is een teamtarief gebaseerd op een team bestaande uit een director, manager en associate/analyst.",
    "tarief_motivatie": null,
    "betaaltermijnen": [{ "description": "Bij aanvang project (33%)", "amount": 13675 }, ...]
  },
  "randvoorwaarden": ["..."]
}
```

**Config field reference:**

| Field | Destination slide | Notes |
|---|---|---|
| `client_name` | Cover (1), Akkoord (17) | |
| `contact_person` | Akkoord (17) — client signing block | |
| `sfnl_signatory.name` | Akkoord (17) — SFNL signing block | Defaults to team[0].name |
| `sfnl_signatory.title` | Akkoord (17) — SFNL signing block | Defaults to "Social Finance NL" |
| `aanleiding.*` | Aanleiding (3) | |
| `aanpak.fases[]` | Aanpak overzicht (6), Fase detail slides (7–9+) | |
| `tijdslijn.*` | Tijdslijn (10) | |
| `team[]` | Team (13) | |
| `begroting.*` | Begroting (15) — table rows + notes box | |
| `randvoorwaarden[]` | Randvoorwaarden voor succes (12) | Bullet list, NOT the akkoord slide |

### 2. Confirm output path, then invoke the `pptx-offerte` skill

Suggest: `%USERPROFILE%\.projects SFNL\sfnl_offerte.schrijven\output\[YYYYMMDD] Offerte [Klant] SFNL.pptx`

Use the Skill tool to invoke the **`pptx-offerte`** skill (bundled in this plugin). Pass it the config JSON and the confirmed output path. The skill handles the full workflow: unpack → edit XML → clean → pack → visual QA → return file in chat.

---

## REVIEW

After generation, launch a **general-purpose sub-agent** to review the output. The sub-agent should:

### 1. Run the deterministic review script
```bash
py "%USERPROFILE%/.projects SFNL/sfnl_offerte.schrijven/scripts/review_offerte.py" \
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
The sub-agent should return a report in this format:

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
