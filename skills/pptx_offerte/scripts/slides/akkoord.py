"""PPTX akkoord slide — randvoorwaarden text + two signing boxes."""
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
    content: title, randvoorwaarden_tekst, termijnen (list[str]),
             sfnl_naam, klant_naam, klant_org, proposition
    """
    slide = clone_template_slide(prs, "akkoord")

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    muted = _hex("text_muted")

    set_paragraphs(
        find_placeholder(slide, 0),
        [{
            "text": content.get("title", "RANDVOORWAARDEN EN AKKOORD"),
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

    body = [
        {"text": "Randvoorwaarden", "role": "body", "size": 10, "bold": True, "color": primary},
        {"text": content.get("randvoorwaarden_tekst", ""), "role": "body", "size": 10, "color": primary},
    ]
    body.extend(
        {"text": f"• {termijn}", "role": "body", "size": 9, "color": muted}
        for termijn in content.get("termijnen", [])
    )
    set_paragraphs(find_placeholder(slide, 10), body)

    set_paragraphs(
        find_shape(slide, "TextBox 9"),
        [
            {"text": content.get("sfnl_naam", ""), "role": "body", "size": 10, "bold": True, "color": primary},
            {"text": "Social Finance NL", "role": "body", "size": 10, "color": muted},
        ],
    )
    set_paragraphs(
        find_shape(slide, "TextBox 8", 0),
        [
            {"text": content.get("klant_naam", ""), "role": "body", "size": 10, "bold": True, "color": primary},
            {"text": content.get("klant_org", ""), "role": "body", "size": 10, "color": muted},
        ],
    )
