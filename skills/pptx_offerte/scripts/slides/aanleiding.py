"""PPTX aanleiding slide — vraagstuk, uitdagingen, behoefte."""
from pptx import Presentation
from skills.pptx_offerte.scripts.slides._utils import (
    ACCENT_MAP,
    clone_template_slide,
    find_placeholder,
    find_shape,
    hex_color as _hex,
    set_paragraphs,
)


def add_slide(prs: Presentation, content: dict) -> None:
    """
    Add aanleiding slide with three text blocks.
    content: summary_line, vraagstuk, uitdagingen, behoefte, proposition
    """
    slide = clone_template_slide(prs, "aanleiding")

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    muted = _hex("text_muted")

    set_paragraphs(
        find_placeholder(slide, 0),
        [{
            "text": content.get("title", "AANLEIDING OFFERTE"),
            "role": "heading",
            "size": 20,
            "bold": True,
            "color": accent,
        }],
    )
    if content.get("summary_line"):
        set_paragraphs(
            find_placeholder(slide, 1),
            [{
                "text": content["summary_line"],
                "role": "subtitle",
                "size": 12,
                "color": muted,
            }],
        )

    def _fill_block(shape_name: str, heading: str, body: str) -> None:
        set_paragraphs(
            find_shape(slide, shape_name),
            [
                {"text": heading, "role": "body", "size": 11, "bold": True, "color": primary},
                {"text": "", "role": "body", "size": 6, "color": primary},
                {"text": body, "role": "body", "size": 10, "color": primary},
            ],
        )

    _fill_block("Rectangle 1", "Maatschappelijk vraagstuk", content.get("vraagstuk", ""))
    _fill_block("Rectangle 8", "Grootste uitdagingen", content.get("uitdagingen", ""))
    _fill_block("Rectangle 9", "Behoefte van de klant", content.get("behoefte", ""))
