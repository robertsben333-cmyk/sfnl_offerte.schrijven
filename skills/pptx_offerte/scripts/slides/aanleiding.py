"""PPTX aanleiding slide — vraagstuk, uitdagingen, behoefte."""
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

BLOCK_LABELS = [
    ("vraagstuk", "MAATSCHAPPELIJK VRAAGSTUK"),
    ("uitdagingen", "GROOTSTE UITDAGINGEN"),
    ("behoefte", "BEHOEFTE VAN DE KLANT"),
]

def _hex(key: str) -> RGBColor:
    h = STYLE["colors"][key].lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def add_slide(prs: Presentation, content: dict) -> None:
    """
    Add aanleiding slide with three text blocks.
    content: summary_line, vraagstuk, uitdagingen, behoefte, proposition
    """
    W = prs.slide_width
    H = prs.slide_height
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    white = _hex("white")

    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = white

    # Slide header
    tf = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), W - Inches(1.0), Inches(0.5))
    p = tf.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = "AANLEIDING"
    run.font.name = STYLE["fonts"]["heading"]
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.color.rgb = accent

    # Summary line
    summary = content.get("summary_line", "")
    if summary:
        tf = slide.shapes.add_textbox(Inches(0.5), Inches(0.9), W - Inches(1.0), Inches(0.4))
        p = tf.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = summary
        run.font.name = STYLE["fonts"]["body"]
        run.font.size = Pt(12)
        run.font.italic = True
        run.font.color.rgb = _hex("text_muted")

    # Three columns
    block_w = int((W - Inches(1.0)) / 3)
    block_h = int(H * 0.60)
    top = int(H * 0.28)

    for i, (key, label) in enumerate(BLOCK_LABELS):
        left = int(Inches(0.5) + i * (block_w + Inches(0.1)))

        tf = slide.shapes.add_textbox(left, top, block_w, Inches(0.35))
        p = tf.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = label
        run.font.name = STYLE["fonts"]["body"]
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.color.rgb = accent

        tf = slide.shapes.add_textbox(left, int(top + Inches(0.38)), block_w, int(block_h - Inches(0.38)))
        tf.text_frame.word_wrap = True
        p = tf.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = content.get(key, "")
        run.font.name = STYLE["fonts"]["body"]
        run.font.size = Pt(10)
        run.font.color.rgb = primary
