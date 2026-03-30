"""PPTX tijdslijn slide — template-anchored planning table."""
from pptx import Presentation
from skills.pptx_offerte.scripts.slides._utils import (
    ACCENT_MAP,
    clone_template_slide,
    find_placeholder,
    hex_color as _hex,
    remove_shape,
    set_paragraphs,
)


def add_slide(prs: Presentation, content: dict) -> None:
    """content: title, intro, phases (list of {naam, periode, activiteiten}), disclaimer, proposition"""
    slide = clone_template_slide(prs, "tijdslijn")

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    muted = _hex("text_muted")

    set_paragraphs(
        find_placeholder(slide, 0),
        [{
            "text": content.get("title", "TIJDSLIJN"),
            "role": "heading",
            "size": 20,
            "bold": True,
            "color": accent,
        }],
    )
    intro_parts = []
    if content.get("intro"):
        intro_parts.append({"text": content["intro"], "role": "subtitle", "size": 11, "color": primary})
    if content.get("disclaimer"):
        intro_parts.append({"text": f"* {content['disclaimer']}", "role": "body", "size": 8, "color": muted})
    if intro_parts:
        set_paragraphs(find_placeholder(slide, 1), intro_parts)

    table_shape = next(shape for shape in slide.shapes if shape.has_table)
    left, top, width, height = table_shape.left, table_shape.top, table_shape.width, table_shape.height
    remove_shape(table_shape)

    phases = content.get("phases", [])
    table = slide.shapes.add_table(len(phases) + 1, 3, left, top, width, height).table
    for col_idx, header in enumerate(["Fase", "Periode", "Activiteiten"]):
        cell = table.cell(0, col_idx)
        cell.text = header
        set_paragraphs(cell, [{"text": header, "role": "body", "size": 10, "bold": True, "color": accent}])

    for row_idx, phase in enumerate(phases, start=1):
        values = [phase.get("naam", ""), phase.get("periode", ""), phase.get("activiteiten", "")]
        for col_idx, value in enumerate(values):
            cell = table.cell(row_idx, col_idx)
            cell.text = value
            set_paragraphs(cell, [{"text": value, "role": "body", "size": 9, "color": primary}])
