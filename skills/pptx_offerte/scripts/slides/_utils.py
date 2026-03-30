"""Shared helpers for PPTX slide components."""
import json, os
from copy import deepcopy
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Pt

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

TEMPLATE_SLIDES = {
    "cover": 1,
    "aanleiding": 4,
    "aanpak_overview": 6,
    "fase_detail": 7,
    "tijdslijn": 8,
    "randvoorwaarden": 9,
    "budget_table": 13,
    "akkoord": 14,
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


def clone_template_slide(prs: Presentation, template_key: str):
    """Clone one of the boilerplate SFNL template slides into the active deck."""
    source = prs.slides[TEMPLATE_SLIDES[template_key] - 1]
    slide = prs.slides.add_slide(blank_layout(prs))

    src_bg = source._element.cSld.bg
    if src_bg is not None:
        cSld = slide._element.cSld
        if cSld.bg is not None:
            cSld.remove(cSld.bg)
        cSld.insert(0, deepcopy(src_bg))

    sp_tree = slide.shapes._spTree
    for shape in source.shapes:
        sp_tree.insert_element_before(deepcopy(shape.element), "p:extLst")
    return slide


def find_placeholder(slide, idx: int):
    for shape in slide.placeholders:
        try:
            if shape.placeholder_format.idx == idx:
                return shape
        except Exception:
            continue
    raise KeyError(f"Placeholder idx {idx} niet gevonden op slide")


def find_shape(slide, name: str, occurrence: int = 0):
    matches = [shape for shape in slide.shapes if shape.name == name]
    if occurrence >= len(matches):
        raise KeyError(f"Shape {name!r} occurrence {occurrence} niet gevonden")
    return matches[occurrence]


def remove_shape(shape) -> None:
    shape._element.getparent().remove(shape._element)


def _font_name(role: str) -> str:
    return STYLE["fonts"].get(role, STYLE["fonts"]["body"])


def apply_run_style(run, *, role="body", size=10, bold=False, italic=False, color=None) -> None:
    run.font.name = _font_name(role)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


def set_paragraphs(shape, paragraphs: list[dict], *, word_wrap=True) -> None:
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = word_wrap

    if not paragraphs:
        return

    for idx, spec in enumerate(paragraphs):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.level = spec.get("level", 0)
        if "alignment" in spec:
            p.alignment = spec["alignment"]
        run = p.add_run()
        run.text = spec.get("text", "")
        apply_run_style(
            run,
            role=spec.get("role", "body"),
            size=spec.get("size", 10),
            bold=spec.get("bold", False),
            italic=spec.get("italic", False),
            color=spec.get("color"),
        )


def set_text(shape, text: str, *, role="body", size=10, bold=False, italic=False, color=None) -> None:
    set_paragraphs(shape, [{
        "text": text,
        "role": role,
        "size": size,
        "bold": bold,
        "italic": italic,
        "color": color,
    }])
