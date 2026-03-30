"""PPTX section header (divider) slide component."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from skills.pptx_offerte.scripts.slides._utils import STYLE, ACCENT_MAP, hex_color as _hex, blank_layout


def add_slide(prs: Presentation, content: dict) -> None:
    """
    Add a section divider slide with colored background.
    content: title, proposition
    """
    W = prs.slide_width
    H = prs.slide_height
    slide = prs.slides.add_slide(blank_layout(prs))

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    white = _hex("white")

    # Full colored background
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = accent

    # Section title
    tf = slide.shapes.add_textbox(Inches(1), int(H * 0.35), W - Inches(2), Inches(1.2))
    tf.text_frame.word_wrap = True
    p = tf.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = content.get("title", "")
    run.font.name = STYLE["fonts"]["heading"]
    run.font.size = Pt(36)
    run.font.bold = True
    run.font.color.rgb = white
