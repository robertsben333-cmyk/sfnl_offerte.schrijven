"""Shared helpers for PPTX slide components."""
import json, os
from pptx import Presentation
from pptx.dml.color import RGBColor

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


def hex_color(key: str) -> RGBColor:
    h = STYLE["colors"][key].lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def blank_layout(prs: Presentation):
    """Return the blank slide layout by name, falling back to index 0."""
    name = STYLE.get("blank_layout_name", "Blank")
    for layout in prs.slide_master.slide_layouts:
        if layout.name == name:
            return layout
    return prs.slide_master.slide_layouts[0]
