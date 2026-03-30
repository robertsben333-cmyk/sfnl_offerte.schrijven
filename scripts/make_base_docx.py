"""Create SFNL branded Word base template."""
import json, os, sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

STYLE_PATH = "data/style.json"
DST = "skills/pptx-offerte/assets/sfnl_base.docx"

if not os.path.exists(STYLE_PATH):
    print(f"ERROR: {STYLE_PATH} not found. Run from project root.", file=sys.stderr)
    sys.exit(2)

with open(STYLE_PATH) as f:
    style = json.load(f)


def hex_to_rgb(hex_color: str) -> RGBColor:
    h = hex_color.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


doc = Document()

# Page margins
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.5)

# Heading 1
h1 = doc.styles["Heading 1"]
h1.font.name = style["fonts"]["heading"]
h1.font.size = Pt(24)
h1.font.bold = True
h1.font.color.rgb = hex_to_rgb(style["colors"]["primary"])

# Heading 2
h2 = doc.styles["Heading 2"]
h2.font.name = style["fonts"]["heading"]
h2.font.size = Pt(16)
h2.font.bold = True
h2.font.color.rgb = hex_to_rgb(style["colors"]["primary"])

# Heading 3
h3 = doc.styles["Heading 3"]
h3.font.name = style["fonts"]["heading"]
h3.font.size = Pt(13)
h3.font.bold = True
h3.font.color.rgb = hex_to_rgb(style["colors"]["accent_mbc"])

# Normal
normal = doc.styles["Normal"]
normal.font.name = style["fonts"]["body"]
normal.font.size = Pt(11)
normal.font.color.rgb = hex_to_rgb(style["colors"]["text_dark"])

os.makedirs(os.path.dirname(DST), exist_ok=True)
doc.save(DST)
print(f"Word base template saved to {DST}")
