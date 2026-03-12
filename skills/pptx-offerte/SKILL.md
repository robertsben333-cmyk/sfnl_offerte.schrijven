---
name: pptx-offerte
description: >
  Fill in the SFNL maatschappelijke businesscase (MBC) offerte PPTX template with proposal
  content from a config JSON. Use this skill when the sfnl-offerte skill reaches the GENERATE
  step and needs to produce the final .pptx file. Takes a config JSON + the house template and
  outputs a fully filled-in proposal presentation.
---

# PPTX Offerte — SFNL MBC Template Filler

Fills the SFNL offerte template (`offerte_mbc_template.pptx`) with content from a config JSON.
Uses an **unpack → Edit tool on XML → clean → pack** workflow that preserves all original
formatting: fonts, colors, sizes, and paragraph spacing are untouched because the Edit tool
does targeted string replacement inside existing `<a:t>` elements.

## Scripts (bundled)

All scripts are in the `scripts/` folder relative to this skill's base directory.

| Script | Purpose |
|--------|---------|
| `scripts/office/unpack.py` | Extract PPTX to pretty-printed XML |
| `scripts/add_slide.py` | Duplicate a slide (for extra fases) |
| `scripts/clean.py` | Remove orphaned files after edits |
| `scripts/office/pack.py` | Repack XML back to .pptx |
| `scripts/thumbnail.py` | Create visual grid for layout analysis |
| `scripts/office/soffice.py` | PDF conversion via LibreOffice |

---

## Workflow

```
1. Unpack template
2. Inspect slides (thumbnail + markitdown)
3. Edit slide XML files (use Edit tool — NOT sed or Python scripts)
4. Clean
5. Pack → output .pptx
6. Visual QA
7. Present file in chat
```

### Step 1 — Unpack

```bash
python scripts/office/unpack.py [TEMPLATE_PATH] unpacked/
```

The template is at:
`%USERPROFILE%\.projects SFNL\sfnl_offerte.schrijven\templates\offerte_mbc_template.pptx`
(resolve `%USERPROFILE%` to the actual home path)

### Step 2 — Inspect

```bash
python -m markitdown [TEMPLATE_PATH]
python scripts/thumbnail.py [TEMPLATE_PATH]
```

Review to confirm which XML file corresponds to which slide. Slide files are at
`unpacked/ppt/slides/slide{N}.xml`. Slide order is in `unpacked/ppt/presentation.xml`.

**Slides 17 and beyond are fixed SFNL boilerplate — never touch them.**

### Step 3 — Edit slide content

Use subagents to edit slides in parallel. Each slide is a separate XML file. Pass each
subagent: the slide file path, "Use the Edit tool for all changes", and the content below.

**Formatting rules (read before editing):**
- Only change `<a:t>` text content — never restructure `<a:p>` or `<a:r>` elements
- For multiple paragraphs: keep existing `<a:p>` elements, add new ones by copying the
  first paragraph's XML and changing the `<a:t>` text inside
- Use `b="1"` on `<a:rPr>` for headers (Doel, Aanpak, Acties, etc.)
- Smart quotes: use XML entities `&#x201C;` / `&#x201D;` / `&#x2018;` / `&#x2019;`
- Whitespace: add `xml:space="preserve"` on `<a:t>` with leading/trailing spaces

---

## Slide Content Map

### Slide 1 — Cover
Find and replace in the XML:
- `[naam klant]` → `{client_name}`
- `[naam project]` / `[NAAM PROJECT]` → `{client_name}`
- Date placeholder → `{proposal_date}`

### Slide 3 — Aanleiding
- `[SAMENVATTENDE ZIN]` → `{aanleiding.summary_line}`
- Shape with "Maatschappelijk vraagstuk": keep the bold header `<a:p>`, replace the body paragraph text with `{aanleiding.maatschappelijk_vraagstuk}`
- Shape with "Grootste uitdagingen": same pattern → `{aanleiding.grootste_uitdagingen}`
- Shape with "Behoefte van de klant": same pattern → `{aanleiding.behoefte_van_klant}`
- Any `<a:t>` starting with "LET OP" → empty string

### Slide 6 — Aanpak overzicht
- "IN DRIE FASES…" subtitle → `{aanpak.overview_subtitle}`
- Chevron "FASE 1:" → `FASE 1: {fases[0].name}`
- Chevron "FASE 2:" → `FASE 2: {fases[1].name}`
- Chevron "FASE 3:" → `FASE 3: {fases[2].name}`
- 3 rectangle description blocks → `{fases[0|1|2].overview_description}`
- Timeline date labels → `{fases[0|1|2].tijdlijn}`

### Slides 7, 8, 9 — Fase 1, 2, 3 detail
For each fase slide (slide 7 = fase 1, slide 8 = fase 2, slide 9 = fase 3):
- Title placeholder → `{fase.number}. {fase.name}`
- Left text box (contains "Doel"):
  ```
  Doel          ← bold header
  {fase.doel}
                ← blank paragraph
  Aanpak        ← bold header
  {fase.aanpak}
  ```
- Right text box (contains "Acties Social Finance NL"):
  ```
  Acties Social Finance NL:   ← bold
  • {acties_sfnl item 1}
  • {acties_sfnl item 2}
  ...
  {outcomes_note}              ← only if present
                               ← blank
  Acties {client_name}:        ← bold
  • {acties_klant item 1}
  ...
                               ← blank
  Deliverable fase {N}: {deliverable}
                               ← blank
  Duur: {fase.dagen} dagen
  ```
- Any `<a:t>` starting with "LET OP" → empty string

### Slide 10 — Tijdslijn
- "BINNEN … MAANDEN…" header → `{tijdslijn.header}`

### Slide 13 — Team
For each of the 3 team members:
- `[TEAMLID]` block → `{member.name}` (line 1) + `{member.title_short}` (line 2)
- `[Cv-omschrijving]` block → `{member.bio}`

### Slide 15 — Begroting
Find the budget text box and set its content to:
```
Social Finance NL voert de opdracht uit op basis van onze Algemene Voorwaarden.
Het tarief is exclusief BTW en op basis van 8 uur per dag.
Dit tarief is inclusief reiskosten binnen Nederland.

{fase 1 naam}: {dagen} dagen × €{tarief} = €{totaal}
{fase 2 naam}: {dagen} dagen × €{tarief} = €{totaal}
{fase 3 naam}: {dagen} dagen × €{tarief} = €{totaal}

Totaal (excl. BTW):  €{total_excl_btw}
BTW (21%):           €{btw}
Totaal (incl. BTW):  €{total_incl_btw}

{tarief_kanttekening}
{tarief_motivatie if present}
```

### Slide 16 — Randvoorwaarden en akkoord
- All `[naam klant]` → `{client_name}`
- Randvoorwaarden text box:
  ```
  Randvoorwaarden
  Zodra er akkoord is op de offerte wordt de definitieve teamsamenstelling vastgesteld.
  De planning is indicatief en wordt vastgesteld in overleg met {client_name} na akkoord.
  Zonder vooraf verkregen toestemming zal SFNL geen meerwerk in rekening brengen.

  Facturatieschema:
  €{amount} — {description}   ← one line per betaaltermijn
  ```

---

## Extra fases (4+)

If the config has more than 3 fases:
1. Duplicate slide 9 (fase 3): `python scripts/add_slide.py unpacked/ slide9.xml`
2. Insert the printed `<p:sldId>` into `presentation.xml` before the tijdslijn slide
3. Fill in the extra fase's content using the same pattern as slides 7–9
4. Tell the user to manually add a 4th chevron to slide 6 in PowerPoint

---

## Step 4 — Clean

```bash
python scripts/clean.py unpacked/
```

---

## Step 5 — Pack

```bash
python scripts/office/pack.py unpacked/ [OUTPUT_PATH] --original [TEMPLATE_PATH]
```

---

## Step 6 — Visual QA

Convert to images and inspect:

```bash
python scripts/office/soffice.py --headless --convert-to pdf [OUTPUT_PATH]
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

Use a subagent with fresh eyes. Prompt:

```
Visually inspect these SFNL offerte slides. Assume there are issues — find them.

Check for:
- Overlapping elements or text overflowing its box
- Missing or leftover placeholder text (anything in brackets like [naam klant])
- "LET OP" boxes that were not cleared
- Truncated text in the fase detail slides (right-hand box tends to overflow)
- Team slide: all 3 members present, no leftover [TEAMLID] placeholders
- Budget slide: all totals correct and legible
- Slide 6 chevrons: labels match the fase names in the config

Read these images — run `ls -1 "$PWD"/slide-*.jpg` and use the exact absolute paths:
[list the slide image paths]
```

Fix any issues, repack, and re-verify until a full pass is clean.

---

## Step 7 — Return file in chat

Use `present_files` if available. Otherwise post the full absolute output path:

> Offerte gegenereerd:
> `{OUTPUT_PATH}`
