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
3. Use the PPTX assembler for the presentation output.
4. Use the Word assembler for the document output when requested.
5. Run the relevant pytest tests or at minimum an end-to-end smoke generation before delivery.

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
