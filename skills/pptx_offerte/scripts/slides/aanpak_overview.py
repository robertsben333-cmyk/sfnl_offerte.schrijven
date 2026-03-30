"""PPTX aanpak_overview slide — chevron phases with descriptions."""
from pptx import Presentation
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN
from skills.pptx_offerte.scripts.slides._utils import STYLE, ACCENT_MAP, hex_color as _hex, blank_layout

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
    slide = prs.slides.add_slide(blank_layout(prs))

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    white = _hex("white")
    muted = _hex("text_muted")

    # White background
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = white

    # Slide title
    tf = slide.shapes.add_textbox(int(W * 0.036), int(H * 0.08), int(W * 0.939), int(H * 0.049))
    p = tf.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = content.get("title", "ONZE AANPAK")
    run.font.name = STYLE["fonts"]["heading"]
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = accent

    # Subtitle
    subtitle = content.get("subtitle", "")
    if subtitle:
        tf = slide.shapes.add_textbox(int(W * 0.036), int(H * 0.138), int(W * 0.939), int(H * 0.083))
        tf.text_frame.word_wrap = True
        p = tf.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = subtitle
        run.font.name = STYLE["fonts"]["body"]
        run.font.size = Pt(11)
        run.font.color.rgb = primary

    phases = content.get("phases", [])[:5]
    if not phases:
        return

    n = len(phases)
    total_w = int(W * 0.937)
    start_left = int(W * 0.036)
    gap = int(W * 0.005) if n > 1 else 0
    chev_w = (total_w - gap * (n - 1)) // n
    chev_top = int(H * 0.42)
    chev_h = int(H * 0.08)
    box_top = int(H * 0.52)
    box_h = int(H * 0.22)
    tl_top = int(H * 0.77)

    for i, phase in enumerate(phases):
        left = start_left + i * (chev_w + gap)
        shape_type = _PENTAGON if i == 0 else _CHEVRON
        shape = slide.shapes.add_shape(shape_type, left, chev_top, chev_w, chev_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = accent
        shape.line.fill.background()
        tf = shape.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = phase.get("naam", "")
        run.font.name = STYLE["fonts"]["body"]
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = white

        # Description box
        tf = slide.shapes.add_textbox(left, box_top, chev_w, box_h)
        tf.text_frame.word_wrap = True
        p = tf.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = phase.get("beschrijving", "")
        run.font.name = STYLE["fonts"]["body"]
        run.font.size = Pt(9)
        run.font.color.rgb = primary

        # Timeline label
        tijdlijn = phase.get("tijdlijn", "")
        if tijdlijn:
            tf = slide.shapes.add_textbox(left, tl_top, chev_w, int(H * 0.05))
            p = tf.text_frame.paragraphs[0]
            run = p.add_run()
            run.text = tijdlijn
            run.font.name = STYLE["fonts"]["body"]
            run.font.size = Pt(8)
            run.font.color.rgb = muted
