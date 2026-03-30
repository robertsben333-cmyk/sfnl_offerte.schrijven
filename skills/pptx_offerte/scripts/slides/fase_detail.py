"""PPTX fase_detail slide — two-column layout with actions left, doel/aanpak right."""
from pptx import Presentation
from skills.pptx_offerte.scripts.slides._utils import (
    ACCENT_MAP,
    clone_template_slide,
    find_placeholder,
    hex_color as _hex,
    set_paragraphs,
)


def add_slide(prs: Presentation, content: dict) -> None:
    """
    Add a fase detail slide.

    content keys:
      number (int): Phase number
      naam (str): Phase name
      klant (str): Client name for "Acties [klant]" label
      doel (str): Phase goal
      aanpak (str): Approach description
      acties_sfnl (list[str]): SFNL actions
      acties_klant (list[str]): Client actions
      deliverable (str): Deliverable description
      dagen (int): Number of days
      tijdlijn (str): Timeline string
      proposition (str): Proposition id
    """
    slide = clone_template_slide(prs, "fase_detail")

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")

    number = content.get("number", "")
    naam = content.get("naam", "")
    set_paragraphs(
        find_placeholder(slide, 0),
        [{
            "text": f"{number}. {naam}" if number != "" else naam,
            "role": "heading",
            "size": 18,
            "bold": True,
            "color": primary,
        }],
    )
    set_paragraphs(
        find_placeholder(slide, 1),
        [{
            "text": content.get("subtitle", f"AANPAK FASE {number}" if number != "" else "AANPAK"),
            "role": "subtitle",
            "size": 11,
            "color": accent,
        }],
    )

    right_paragraphs = [
        {"text": "DOEL", "role": "body", "size": 11, "bold": True, "color": accent},
        {"text": content.get("doel", ""), "role": "body", "size": 10, "color": primary},
        {"text": "", "role": "body", "size": 6, "color": primary},
        {"text": "AANPAK", "role": "body", "size": 11, "bold": True, "color": accent},
        {"text": content.get("aanpak", ""), "role": "body", "size": 10, "color": primary},
    ]
    set_paragraphs(find_placeholder(slide, 11), right_paragraphs)

    klant = content.get("klant", "Klant").upper()
    left_paragraphs = [{"text": "ACTIES SOCIAL FINANCE NL", "role": "body", "size": 9, "bold": True, "color": accent}]
    left_paragraphs.extend(
        {"text": f"• {item}", "role": "body", "size": 9, "color": primary}
        for item in content.get("acties_sfnl", [])
    )
    left_paragraphs.append({"text": "", "role": "body", "size": 6, "color": primary})
    left_paragraphs.append({"text": f"ACTIES {klant}", "role": "body", "size": 9, "bold": True, "color": accent})
    left_paragraphs.extend(
        {"text": f"• {item}", "role": "body", "size": 9, "color": primary}
        for item in content.get("acties_klant", [])
    )
    left_paragraphs.extend([
        {"text": "", "role": "body", "size": 6, "color": primary},
        {"text": "DELIVERABLE", "role": "body", "size": 9, "bold": True, "color": accent},
        {"text": content.get("deliverable", ""), "role": "body", "size": 9, "color": primary},
        {"text": "", "role": "body", "size": 6, "color": primary},
        {"text": "TIJDLIJN", "role": "body", "size": 9, "bold": True, "color": accent},
        {"text": str(content.get("tijdlijn", "")), "role": "body", "size": 9, "color": primary},
        {"text": "", "role": "body", "size": 6, "color": primary},
        {"text": "DAGDELEN", "role": "body", "size": 9, "bold": True, "color": accent},
        {"text": str(content.get("dagen", "")), "role": "body", "size": 9, "color": primary},
    ])
    set_paragraphs(find_placeholder(slide, 12), left_paragraphs)
