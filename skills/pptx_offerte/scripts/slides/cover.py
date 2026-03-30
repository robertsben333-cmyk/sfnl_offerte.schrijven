"""PPTX cover slide component."""
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
    Add a cover slide.
    content: client, title, date, proposition
    """
    slide = clone_template_slide(prs, "cover")

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    muted = _hex("text_muted")

    set_paragraphs(
        find_shape(slide, "Text Placeholder 4"),
        [{
            "text": content.get("title", ""),
            "role": "heading",
            "size": 30,
            "bold": True,
            "color": primary,
        }],
    )
    meta = []
    if content.get("client"):
        meta.append({
            "text": content["client"],
            "role": "subtitle",
            "size": 14,
            "color": accent,
        })
    if content.get("date"):
        meta.append({
            "text": content["date"],
            "role": "body",
            "size": 11,
            "color": muted,
        })
    if meta:
        set_paragraphs(find_placeholder(slide, 14), meta)
