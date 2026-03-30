"""PPTX cover slide component."""
import json, os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

STYLE_PATH = os.path.join(os.path.dirname(__file__), "../../../../data/style.json")
with open(STYLE_PATH) as f:
    STYLE = json.load(f)

ACCENT_MAP = {
    "mbc": "accent_mbc",
    "impact_meten": "accent_impact_meten",
    "advies_innovatieve_financiering": "accent_advies_innovatief",
    "intermediair": "accent_intermediair",
    "fondsmanagement": "accent_fondsmanagement",
    "partnerschappen": "accent_partnerschappen",
}

def _hex(key: str) -> RGBColor:
    h = STYLE["colors"][key].lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def add_slide(prs: Presentation, content: dict) -> None:
    """
    Add a cover slide.
    content: client, title, date, proposition
    """
    W = prs.slide_width
    H = prs.slide_height
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    white = _hex("white")

    # White background
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = white

    # Left accent bar (~8% width)
    bar_w = int(W * 0.08)
    bar = slide.shapes.add_shape(1, 0, 0, bar_w, H)
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()

    left = bar_w + Inches(0.3)

    # Client name
    tf = slide.shapes.add_textbox(left, int(H * 0.15), W - left - Inches(0.3), Inches(0.6))
    p = tf.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = content.get("client", "")
    run.font.name = STYLE["fonts"]["body"]
    run.font.size = Pt(14)
    run.font.color.rgb = _hex("text_muted")

    # Project title
    tf = slide.shapes.add_textbox(left, int(H * 0.30), W - left - Inches(0.3), Inches(1.5))
    tf.text_frame.word_wrap = True
    p = tf.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = content.get("title", "")
    run.font.name = STYLE["fonts"]["heading"]
    run.font.size = Pt(32)
    run.font.bold = True
    run.font.color.rgb = primary

    # "OFFERTE" label
    tf = slide.shapes.add_textbox(left, int(H * 0.58), W - left - Inches(0.3), Inches(0.4))
    p = tf.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = "OFFERTE"
    run.font.name = STYLE["fonts"]["body"]
    run.font.size = Pt(11)
    run.font.color.rgb = accent
    run.font.bold = True

    # Date
    tf = slide.shapes.add_textbox(left, int(H * 0.68), W - left - Inches(0.3), Inches(0.4))
    p = tf.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = content.get("date", "")
    run.font.name = STYLE["fonts"]["body"]
    run.font.size = Pt(12)
    run.font.color.rgb = _hex("text_muted")
