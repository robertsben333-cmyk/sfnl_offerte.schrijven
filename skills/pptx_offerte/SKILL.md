---
name: pptx_offerte
description: >
  Assemble SFNL offerte deliverables from a content-only slide_plan JSON. Use this skill when
  the sfnl-offerte skill reaches GENERATE and needs a PowerPoint and optionally a Word version.
  The template is a visual reference for geometry and branding; proposal text must come from
  the slide_plan content, never from hardcoded component copy.
---

# PPTX Offerte — Component-Based Assembler

This skill builds SFNL offerte deliverables with reusable components in
`skills/pptx_offerte/scripts/`.

## Core rule

All copy is content-driven:
- Every text fragment comes from `slide_plan[*].content`
- The house templates are used for base assets and visual proportions
- Do not hardcode proposition-specific body copy in slide or Word components
- Respect SFNL template typography: `Gotham Bold` for titles, `Montserrat Light` for subtitles, `Lato Light` for body copy

## Assemblers

- PPTX: `skills/pptx_offerte/scripts/assemble.py`
- Word: `skills/pptx_offerte/scripts/assemble_word.py`
- Base assets: `skills/pptx_offerte/assets/sfnl_base.pptx` and `skills/pptx_offerte/assets/sfnl_base.docx`

## Supported PPTX slide types

- `cover`
- `section_header`
- `aanleiding`
- `aanpak_overview`
- `fase_detail`
- `tijdslijn`
- `team`
- `budget_table`
- `randvoorwaarden`
- `akkoord`

## PowerPoint sequence

Default deckvolgorde voor offertes:

`cover → aanleiding → aanpak_overview → fase_detail × n → tijdslijn → randvoorwaarden → budget_table → akkoord`

When a fase has substeps, `fase_detail × n` expands to one `fase_detail` per substep (e.g. `fase_detail` "2.1" + `fase_detail` "2.2" instead of one `fase_detail` "2"). All substep slides share the same deck-wide typography scale.

Gebruik `section_header` alleen waar het deck daar echt sterker van wordt. Gebruik `team` alleen als de teamsamenstelling commercieel iets toevoegt.

## Supported Word section types

- `cover`
- `aanleiding`
- `aanpak_section`
- `team`
- `budget_table`
- `akkoord`

## Workflow

1. Build a `slide_plan` JSON with explicit `type` and `content` objects.
2. Keep all narrative text in the JSON payload, not in the components.
3. Read `references/copy_length_reference.md` before writing dense slides such as `aanleiding`, `aanpak_overview`, `fase_detail`, `tijdslijn`, `budget_table` and `akkoord`.
4. Add a non-rendering `copy_reference` block to the relevant `content` objects so the config itself shows the intended copy density and target ranges.
5. Write the `slide_plan` to the template, not against it: reuse existing template artwork and text boxes whenever the slide type exists in the SFNL base deck.
6. Use one deck-wide typography scale per slide group. Font size may shrink for denser decks, but do not manually shrink only one outlier slide.
5. Use the PPTX assembler for the presentation output.
6. Use the Word assembler for the document output when requested.
7. Run the relevant pytest tests or at minimum an end-to-end smoke generation before delivery.

## Example slide_plan

```json
[
  {
    "type": "cover",
    "content": {
      "client": "Voorbeeldorganisatie",
      "title": "VOORBEELDPROJECT",
      "date": "maart 2026",
      "proposition": "mbc"
    }
  },
  {
    "type": "aanpak_overview",
    "content": {
      "title": "ONZE AANPAK",
      "subtitle": "In drie fases werken we naar een businesscase toe.",
      "phases": [
        {
          "naam": "Fase 1",
          "beschrijving": "Korte omschrijving",
          "tijdlijn": "jan-feb"
        }
      ],
      "proposition": "mbc"
    }
  }
]
```

## Geometry and styling rules

- Use `blank_layout(prs)` from `skills.pptx_offerte.scripts.slides._utils`
- Use `prs.slide_width` and `prs.slide_height` for positioning
- Reuse colors and fonts from `STYLE` / `ACCENT_MAP`
- Use the official SFNL base deck as the source for template-anchored slide cloning where fidelity matters
- If a template slide already contains the needed visual elements, duplicate that slide and edit the existing text boxes or table cells instead of redrawing the slide
- Keep body-size decisions consistent across comparable slides. For example: all `fase_detail` slides in one deck should share one typography scale

## Slide review lens

Check every generated deck slide-by-slide:

- `cover`: title must stay in the orange field; client/date metadata must sit cleanly in the pink block without overlapping `OFFERTE`
- `aanleiding`: panel headings stay centered and white; body text sits inside the coloured panels, not on top of them or above them
- `aanpak_overview`: max 4 overview chevrons in the template variant; per phase use full explanatory sentences and keep the slide around the density of the example offers
- `fase_detail`: left column is compact operational info; right column carries the substantive explanation; labels are bold; all phase slides (including substep slides) share one body-size scale. Substep slides use dotted numbers (`"2.1"`) and set `subtitle` to the parent fase name for context.
- `tijdslijn`: keep month labels short, use the existing template table/fills instead of rebuilding the slide, and fill the detail rows with concrete betweenstappen where possible
- `randvoorwaarden`: prefer 3-4 strong bullets; if more is needed, move nuance to another slide or the akkoordtekst
- `budget_table`: keep the note block short enough to preserve whitespace below the table and explicitly style table text in SFNL body typography
- `akkoord`: no placeholders, warning highlights, or unresolved signer names

## Validation

Preferred checks:

```bash
py -m pytest tests/test_slides -v
py -m pytest tests/test_word -v
py -m pytest tests/test_assemble.py tests/test_assemble_word.py tests/test_integration.py -v
```

If you add new component types, update:
- `skills/pptx_offerte/scripts/assemble.py`
- `skills/pptx_offerte/scripts/assemble_word.py`
- tests that prove the new types are accepted
