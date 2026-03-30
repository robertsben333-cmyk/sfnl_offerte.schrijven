"""PPTX aanpak_overview slide — chevron phases with descriptions."""
from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from skills.pptx_offerte.scripts.slides._utils import (
    ACCENT_MAP,
    clone_template_slide,
    find_placeholder,
    find_shape,
    hex_color as _hex,
    remove_shape,
    set_paragraphs,
)

_PENTAGON = 56
_CHEVRON = 55


def add_slide(prs: Presentation, content: dict) -> None:
    """
    Add aanpak overview slide with 2-5 phase chevrons.

    content keys:
      title (str): Slide title e.g. "ONZE AANPAK"
      subtitle (str): One-line summary
      phases (list): Each has naam, beschrijving, tijdlijn
      proposition (str): Proposition id for accent color
    """
    W = prs.slide_width
    H = prs.slide_height
    slide = clone_template_slide(prs, "aanpak_overview")

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    white = _hex("white")
    muted = _hex("text_muted")

    set_paragraphs(
        find_placeholder(slide, 0),
        [{
            "text": content.get("title", "PLAN VAN AANPAK"),
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

    phases = content.get("phases", [])[:5]
    if not phases:
        return

    n = len(phases)
    for shape_name in [
        "Straight Arrow Connector 13",
        "TextBox 14",
        "TextBox 16",
        "TextBox 17",
        "Tekstvak 1",
    ]:
        try:
            while True:
                remove_shape(find_shape(slide, shape_name))
        except KeyError:
            pass

    base_shapes = [
        find_shape(slide, "Arrow: Pentagon 5"),
        find_shape(slide, "Arrow: Chevron 6"),
        find_shape(slide, "Arrow: Chevron 7"),
        find_shape(slide, "Arrow: Chevron 8"),
    ]
    desc_boxes = [
        find_shape(slide, "Tijdelijke aanduiding voor inhoud 19"),
        find_shape(slide, "Tijdelijke aanduiding voor inhoud 20"),
        find_shape(slide, "Tijdelijke aanduiding voor inhoud 23"),
        find_shape(slide, "Tijdelijke aanduiding voor inhoud 26"),
    ]
    intro_box = find_shape(slide, "Tijdelijke aanduiding voor inhoud 18")
    if content.get("intro"):
        set_paragraphs(
            intro_box,
            [{
                "text": content["intro"],
                "role": "body",
                "size": 10,
                "color": primary,
            }],
        )
    else:
        remove_shape(intro_box)

    first_left = base_shapes[0].left
    last_right = base_shapes[-1].left + base_shapes[-1].width
    total_span = last_right - first_left
    step = total_span / n
    chev_w = int(step * 1.06)
    chev_top = base_shapes[0].top
    chev_h = base_shapes[0].height
    box_top = desc_boxes[0].top
    box_h = desc_boxes[0].height
    tl_top = int(H * 0.785)

    shapes = []
    boxes = []
    for i in range(n):
        if i < len(base_shapes):
            shape = base_shapes[i]
            box = desc_boxes[i]
        else:
            left = int(first_left + i * step)
            shape = slide.shapes.add_shape(_CHEVRON, left, chev_top, chev_w, chev_h)
            box = slide.shapes.add_textbox(left, box_top, int(step * 0.92), box_h)
        shapes.append(shape)
        boxes.append(box)

    for i in range(n, len(base_shapes)):
        remove_shape(base_shapes[i])
        remove_shape(desc_boxes[i])

    for i, phase in enumerate(phases):
        left = int(first_left + i * step)
        shape = shapes[i]
        box = boxes[i]
        shape.left = left
        shape.top = chev_top
        shape.width = chev_w
        shape.height = chev_h
        shape.fill.solid()
        shape.fill.fore_color.rgb = accent
        shape.line.fill.background()
        set_paragraphs(
            shape,
            [{
                "text": phase.get("naam", ""),
                "role": "body",
                "size": 10,
                "bold": True,
                "color": white,
                "alignment": PP_ALIGN.CENTER,
            }],
        )

        box.left = left
        box.top = box_top
        box.width = int(step * 0.92)
        box.height = box_h
        set_paragraphs(
            box,
            [{
                "text": phase.get("beschrijving", ""),
                "role": "body",
                "size": 9,
                "color": primary,
            }],
        )

        timeline_box = slide.shapes.add_textbox(left, tl_top, int(step * 0.92), int(H * 0.05))
        set_paragraphs(
            timeline_box,
            [{
                "text": phase.get("tijdlijn", ""),
                "role": "body",
                "size": 8,
                "color": muted,
            }],
        )
