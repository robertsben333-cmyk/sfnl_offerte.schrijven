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
| `scripts/add_chevron.py` | Add a 4th (or Nth) chevron to slide 6 programmatically |
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
4. Strip yellow highlights
5. Clean
6. Pack → output .pptx
7. Visual QA
8. Present file in chat
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

**Always resolve the slide map first** — run the presentation.xml rId lookup to know which
slideN.xml corresponds to which presentation slide number. The mapping is NOT always 1:1
(e.g. after a fase-4 slide is inserted, slide 10 in the deck may be slide26.xml on disk).

**Slides 18 and beyond are fixed SFNL boilerplate — never touch them.**

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

### Step 4 — Strip yellow highlights

Template runs carry `<a:highlight><a:srgbClr val="FFFF00"/></a:highlight>` that survive
editing and show up as visible yellow in the output. After editing each slide, strip them
with Python:

```python
import re

def strip_yellow_highlights(xml: str) -> str:
    return re.sub(
        r'<a:highlight>\s*<a:srgbClr val="FFFF00"/>\s*</a:highlight>',
        '',
        xml,
        flags=re.DOTALL,
    )
```

Apply this to every edited slide file before packing. Read the file, call the function,
write it back.

**Exception:** Do NOT strip highlights from the timeline label text boxes on slide 6
(Maand 1, Maand 2, etc.) — those yellow labels are intentional design elements.

---

## Slide Content Map

**Slide numbering note:** The table below uses *presentation slide numbers* (as seen in
PowerPoint). Always confirm the mapping to disk files via `presentation.xml` before
editing — after inserting extra fase slides the disk file numbers diverge from the
presentation order.

### Slide 1 — Cover
Find and replace in the XML:
- `[naam klant]` → `{client_name}`
- `[naam project]` / `[NAAM PROJECT]` → `{client_name}`
- Date placeholder → `{proposal_date}`

### Slide 3 — Aanleiding
- `[SAMENVATTENDE ZIN]` → `{aanleiding.summary_line}`
- Shape with "Maatschappelijk vraagstuk": keep the bold header `<a:p>`, replace the body
  paragraph text with `{aanleiding.maatschappelijk_vraagstuk}`
- Shape with "Grootste uitdagingen": same pattern → `{aanleiding.grootste_uitdagingen}`
- Shape with "Behoefte van de klant": same pattern → `{aanleiding.behoefte_van_klant}`
- Any `<a:t>` starting with "LET OP" → empty string

### Slide 6 — Aanpak overzicht

**Standard 3-fase layout (default):**
- "IN DRIE FASES…" subtitle → `{aanpak.overview_subtitle}`
- Chevron "FASE 1:" → `FASE 1: {fases[0].name}`
- Chevron "FASE 2:" → `FASE 2: {fases[1].name}`
- Chevron "FASE 3:" → `FASE 3: {fases[2].name}`
- 3 rectangle description blocks → `{fases[0|1|2].overview_description}`
- Timeline date labels → `{fases[0|1|2].tijdlijn}`

**4-fase layout — run add_chevron.py BEFORE editing text:**

```bash
python scripts/add_chevron.py unpacked/ --fases 4
```

This repositions all existing chevrons and description boxes, adds the 4th chevron in
accent4 colour, and updates timeline label positions. After running, edit text as normal:
- Description texts: keep these SHORT (max 25 words each) to prevent box overflow
- `overflow="clip"` is already set on all description `<a:bodyPr>` by the script

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
  {outcomes_note}              ← only if present in config
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

### Extra fase slides (fase 4+)
Duplicate slide 9 for each extra fase:
```bash
python scripts/add_slide.py unpacked/ slide9.xml
```
Insert the printed `<p:sldId>` into `presentation.xml` directly after the rId for slide 9
(before the tijdslijn slide). Fill in using the same pattern as slides 7–9.

### Slide 10 — Tijdslijn
- "BINNEN … MAANDEN…" header → `{tijdslijn.header}`

### Slide 12 — Randvoorwaarden voor succes  *(disk file: slide11.xml)*

Fill placeholder `idx="10"` with bullet paragraphs. Each item in `config.randvoorwaarden`
becomes one bullet. Use this paragraph pattern for every bullet:

```xml
<a:p>
  <a:pPr marL="228600" indent="-228600">
    <a:buFont typeface="Arial" panose="020B0604020202020204" pitchFamily="34" charset="0"/>
    <a:buChar char="•"/>
  </a:pPr>
  <a:r>
    <a:rPr lang="nl-NL" sz="1600">
      <a:solidFill><a:srgbClr val="233348"/></a:solidFill>
      <a:latin typeface="Lato Light" panose="020F0302020204030203"
               pitchFamily="34" charset="0"/>
    </a:rPr>
    <a:t>{randvoorwaarde text}</a:t>
  </a:r>
</a:p>
```

Use Python + lxml (not the Edit tool) for this slide because it requires adding a variable
number of paragraphs. Find the placeholder via `nvPr > ph[@idx="10"]`, get its `txBody`
(in the `p:` namespace), clear all existing `<a:p>` children, and append one bullet per
randvoorwaarde.

**Do NOT add a "Randvoorwaarden" heading** — the slide title already says it.
**Do NOT put the facturatieschema here** — that belongs on slide 17 (akkoord).

### Slide 13 — Team (cover)
No content to fill. Boilerplate slide only.

### Slide 14 — Team detail  *(disk file: slide13.xml)*
For each of the 3 team members:
- `[TEAMLID]` block → `{member.name}` (line 1) + `{member.title_short}` (line 2)
- `[Cv-omschrijving]` block → `{member.bio}`

### Slide 15 — Begroting  *(disk file: slide15.xml)*

This slide has **two separate elements** — fill them both.

**A. The budget table (`<a:tbl>` inside `<p:graphicFrame>`)**

The table has 4 columns: fase/onderdeel | # dagen | Dagtarief ex. btw | Kosten.
Structure: 1 header row + one data row per fase + 1 totaal row (accent1 background).

Empty cells only have `<a:endParaRPr>` — replace with a real `<a:r>` run.
Use Python + lxml (not the Edit tool) for reliable cell access:

```python
from lxml import etree

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'

def fill_cell(cell, text, left=False, bold=False, white=False):
    txBody = cell.find('{%s}txBody' % A)
    for p in list(txBody.findall('{%s}p' % A)):
        txBody.remove(p)
    p   = etree.SubElement(txBody, '{%s}p' % A)
    pPr = etree.SubElement(p, '{%s}pPr' % A)
    pPr.set('algn', 'l' if left else 'ctr')
    if left: pPr.set('fontAlgn', 'ctr')
    r   = etree.SubElement(p, '{%s}r' % A)
    rPr = etree.SubElement(r, '{%s}rPr' % A)
    rPr.set('lang', 'nl-NL'); rPr.set('sz', '1400')
    rPr.set('b', '1' if bold else '0')
    fill = etree.SubElement(rPr, '{%s}solidFill' % A)
    clr  = etree.SubElement(fill, '{%s}srgbClr' % A)
    clr.set('val', 'FFFFFF' if (bold or white) else '233348')
    etree.SubElement(rPr, '{%s}effectLst' % A)
    lat = etree.SubElement(rPr, '{%s}latin' % A)
    lat.set('typeface', 'Lato Light')
    lat.set('panose', '020F0502020204030203')
    lat.set('pitchFamily', '34'); lat.set('charset', '0')
    etree.SubElement(r, '{%s}t' % A).text = text

tree = etree.parse('unpacked/ppt/slides/slide15.xml')
tbl  = tree.getroot().find('.//{%s}tbl' % A)
rows = tbl.findall('{%s}tr' % A)
# rows[0] = header (skip), rows[1..N-1] = data, rows[-1] = totaal

for i, fase in enumerate(config['begroting']['rows'], 1):
    cells = rows[i].findall('{%s}tc' % A)
    fill_cell(cells[0], fase['fase'],                    left=True)
    fill_cell(cells[1], str(fase['dagen']))
    fill_cell(cells[2], f"€ {fase['tarief']:,.0f}".replace(',', '.'))
    fill_cell(cells[3], f"€ {fase['totaal']:,.0f}".replace(',', '.'))

totaal_cells = rows[-1].findall('{%s}tc' % A)
fill_cell(totaal_cells[0], 'Totaal (ex. btw)',           left=True, bold=True, white=True)
fill_cell(totaal_cells[1], str(total_dagen),                         bold=True, white=True)
fill_cell(totaal_cells[2], f"€ {day_rate:,.0f}".replace(',', '.'),  bold=True, white=True)
fill_cell(totaal_cells[3], f"€ {total_excl_btw:,.0f}".replace(',', '.'), bold=True, white=True)

tree.write('unpacked/ppt/slides/slide15.xml', xml_declaration=True,
           encoding='UTF-8', standalone=True)
```

Do NOT touch row heights, tcPr borders, or the solidFill on the totaal row.

**B. The notes text box (placeholder `idx="10"`, below the table)**

This text box is in the **`p:` namespace** (not `a:`). Find it via
`nvPr > ph[@idx="10"]` and get its `txBody` as `sp.find('{P}txBody')`.

Set content to 3–4 short lines only:
```
Social Finance NL voert de opdracht uit op basis van onze Algemene Voorwaarden.
Het tarief is exclusief BTW en op basis van 8 uur per dag.
Dit tarief is inclusief reiskosten binnen Nederland.
{tarief_motivatie}   ← NGO/reduced rate motivation paragraph; omit if null
```

Use font size sz="1100", color 233348, Lato Light.
Do NOT put per-fase cost breakdown lines here — those are in the table above.

### Slide 17 — Akkoord  *(disk file: slide16.xml)*

This slide contains **only** the signing section and facturatieschema.
**Do NOT put randvoorwaarden bullets here** — those belong on slide 12.

**Placeholder `idx="10"` (main content area):**

Note: the txBody of this placeholder is in the **`p:` namespace**. Find via
`sp.find('{P}nvPr') > ph[@idx="10"]`, then `sp.find('{P}txBody')`.

Set content to:
```
Facturatieschema:
• € {amount} — {description}
• € {amount} — {description}
• € {amount} — {description}

De planning is indicatief en wordt vastgesteld in overleg met {client_name} na akkoord.
Zonder vooraf verkregen toestemming zal SFNL geen meerwerk in rekening brengen.
```

**Signing boxes (inside `<p:grpSp>`):**

Two signature text boxes, identified by x-position in `<a:off>`:
- Left box (x ≈ 1.224.545 EMU) → SFNL side
- Right box (x ≈ 6.103.180 EMU) → client side

Replace the entire txBody content of each box. Pattern: blank line → name → organisation.

```python
# Left box: SFNL
# Right box: client (replace the yellow [ ] placeholder runs entirely)

def set_signing_box(sp, name, organisation):
    txBody = sp.find('{%s}txBody' % P)   # txBody is in P namespace
    for p in list(txBody.findall('{%s}p' % A)):
        txBody.remove(p)
    for text in ['', name, organisation]:
        p   = etree.SubElement(txBody, '{%s}p' % A)
        r   = etree.SubElement(p, '{%s}r' % A)
        rPr = etree.SubElement(r, '{%s}rPr' % A)
        rPr.set('lang', 'nl-NL'); rPr.set('sz', '1400')
        fill = etree.SubElement(rPr, '{%s}solidFill' % A)
        etree.SubElement(fill, '{%s}srgbClr' % A).set('val', '233348')
        lat = etree.SubElement(rPr, '{%s}latin' % A)
        lat.set('typeface', 'Lato Light')
        lat.set('panose', '020F0302020204030203')
        lat.set('pitchFamily', '34'); lat.set('charset', '0')
        etree.SubElement(r, '{%s}t' % A).text = text
```

`sfnl_signatory` defaults to `team[0].name` if not set in config.

---

## Step 5 — Clean

```bash
python scripts/clean.py unpacked/
```

---

## Step 6 — Pack

Pack **from inside** the unpacked directory so paths inside the zip are correct:

```bash
cd unpacked && zip -r ../output.pptx . -x "*.DS_Store" && cd ..
```

Or use the pack script:
```bash
python scripts/office/pack.py unpacked/ [OUTPUT_PATH] --original [TEMPLATE_PATH]
```

---

## Step 7 — Visual QA

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
- Yellow highlighted text that was not stripped
- Truncated text in the fase detail slides (right-hand box tends to overflow)
- Team slide: all 3 members present, no leftover [TEAMLID] placeholders
- Slide 6: chevron labels match fase names; description boxes do not overlap;
  if 4 fases, confirm 4 chevrons are visible and descriptions are not clipped
- Slide 12 (Randvoorwaarden): bullets present, no duplicate "Randvoorwaarden" heading
- Slide 15 (Begroting): per-fase rows filled in the TABLE (not in the text box below);
  totaal row shows correct sum; notes text box has max 4 short lines only
- Slide 17 (Akkoord): NO randvoorwaarden bullets here; both signing boxes filled (SFNL
  left, client right); facturatieschema present with correct amounts

Read these images — run `ls -1 "$PWD"/slide-*.jpg` and use the exact absolute paths:
[list the slide image paths]
```

Fix any issues, repack, and re-verify until a full pass is clean.

---

## Step 8 — Return file in chat

Use `present_files` if available. Otherwise post the full absolute output path:

> Offerte gegenereerd:
> `{OUTPUT_PATH}`
