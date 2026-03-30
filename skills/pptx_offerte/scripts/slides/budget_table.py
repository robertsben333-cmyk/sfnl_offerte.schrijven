"""PPTX budget_table slide — template-anchored begroting slide."""
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from lxml import etree
from skills.pptx_offerte.scripts.slides._utils import (
    ACCENT_MAP,
    clone_template_slide,
    find_placeholder,
    hex_color as _hex,
    remove_shape,
    set_paragraphs,
)


def _set_cell(cell, text, font_size=10, bold=False, fg=None, bg=None):
    cell.text = text
    set_paragraphs(cell, [{
        "text": text,
        "role": "body",
        "size": font_size,
        "bold": bold,
        "color": fg,
    }])

    if bg:
        tcPr = cell._tc.get_or_add_tcPr()
        # Remove any existing solidFill to avoid duplicates
        for old in tcPr.findall(qn("a:solidFill")):
            tcPr.remove(old)
        solidFill = etree.SubElement(tcPr, qn("a:solidFill"))
        srgbClr = etree.SubElement(solidFill, qn("a:srgbClr"))
        srgbClr.set("val", "".join(f"{channel:02X}" for channel in bg))


def add_slide(prs: Presentation, content: dict) -> None:
    """
    content: rows (list of {fase, dagen, kosten}), day_rate, tarief_note,
             social_rate_disclaimer, termijnen, proposition
    """
    slide = clone_template_slide(prs, "budget_table")

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    white = _hex("white")
    muted = _hex("text_muted")

    set_paragraphs(
        find_placeholder(slide, 0),
        [{
            "text": content.get("title", "BEGROTING"),
            "role": "heading",
            "size": 20,
            "bold": True,
            "color": accent,
        }],
    )
    if content.get("subtitle"):
        set_paragraphs(
            find_placeholder(slide, 1),
            [{
                "text": content["subtitle"],
                "role": "subtitle",
                "size": 11,
                "color": primary,
            }],
        )

    rows = content.get("rows", [])
    table_shape = next(shape for shape in slide.shapes if shape.has_table)
    table_left, table_top = table_shape.left, table_shape.top
    table_w, table_h = table_shape.width, table_shape.height
    remove_shape(table_shape)

    if rows:
        table = slide.shapes.add_table(len(rows) + 1, 4, table_left, table_top, table_w, table_h).table
        table.columns[0].width = int(table_w * 0.56)
        table.columns[1].width = int(table_w * 0.14)
        table.columns[2].width = int(table_w * 0.15)
        table.columns[3].width = int(table_w * 0.15)

        for col_idx, header in enumerate(["", "# dagen", "Dagtarief ex. btw", "Kosten"]):
            _set_cell(table.cell(0, col_idx), header, font_size=10, bold=True, fg=accent)

        light_grey = RGBColor(0xF2, 0xF2, 0xF2)
        default_day_rate = content.get("day_rate", "")
        for r_idx, row in enumerate(rows, start=1):
            is_last = r_idx == len(rows)
            bg = accent if is_last else (light_grey if r_idx % 2 == 0 else white)
            fg_color = white if is_last else primary
            bold = is_last
            day_rate = row.get("dagtarief", default_day_rate)
            day_rate_text = f"\u20ac {day_rate:,.0f}".replace(",", ".") if isinstance(day_rate, (int, float)) else str(day_rate)
            kosten = row.get("kosten", "")
            kosten_text = f"\u20ac {kosten:,.0f}".replace(",", ".") if isinstance(kosten, (int, float)) else str(kosten)
            values = [row.get("fase", ""), str(row.get("dagen", "")), day_rate_text, kosten_text]
            for col_idx, value in enumerate(values):
                _set_cell(table.cell(r_idx, col_idx), value, font_size=10, bold=bold, fg=fg_color, bg=bg)

    tarief_note = content.get("tarief_note", "")
    social_rate_disclaimer = content.get("social_rate_disclaimer", "")
    termijnen = content.get("termijnen", [])
    notes = [
        {"text": "Social Finance NL voert de opdracht uit op basis van onze Algemene Voorwaarden.", "role": "body", "size": 10, "color": primary},
        {"text": "Het tarief is exclusief BTW en op basis van 8 uur per dag.", "role": "body", "size": 10, "color": primary},
        {"text": "Het tarief is een teamtarief gebaseerd op een team bestaande uit een director, manager en associate/analyst.", "role": "body", "size": 10, "color": primary},
    ]
    if tarief_note:
        notes.append({"text": tarief_note, "role": "body", "size": 10, "color": muted})
    if social_rate_disclaimer:
        notes.append({"text": social_rate_disclaimer, "role": "body", "size": 10, "color": muted})
    if termijnen:
        notes.append({
            "text": f"Facturatie geschiedt volgens het volgende schema: {'; '.join(termijnen)}.",
            "role": "body",
            "size": 10,
            "color": primary,
        })
    set_paragraphs(find_placeholder(slide, 10), notes)
