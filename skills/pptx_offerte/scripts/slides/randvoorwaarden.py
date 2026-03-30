"""PPTX randvoorwaarden slide — bullet list."""
from pptx import Presentation
from skills.pptx_offerte.scripts.slides._utils import (
    ACCENT_MAP,
    clone_template_slide,
    find_placeholder,
    hex_color as _hex,
    set_paragraphs,
)


def add_slide(prs: Presentation, content: dict) -> None:
    """content: title, items (list[str]), proposition"""
    slide = clone_template_slide(prs, "randvoorwaarden")

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    muted = _hex("text_muted")

    set_paragraphs(
        find_placeholder(slide, 0),
        [{
            "text": content.get("title", "RANDVOORWAARDEN VOOR SUCCES"),
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
                "color": muted,
            }],
        )

    items = [
        {"text": f"• {item}", "role": "body", "size": 10, "color": primary}
        for item in content.get("items", [])
    ]
    set_paragraphs(find_placeholder(slide, 10), items)
