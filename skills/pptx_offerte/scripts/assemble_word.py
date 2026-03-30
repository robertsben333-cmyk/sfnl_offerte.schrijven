"""Assemble a Word document from a slide_plan list and the SFNL base template."""
import os
from docx import Document

_HERE = os.path.dirname(__file__)
ASSETS_DIR = os.path.normpath(os.path.join(_HERE, "../../pptx-offerte/assets"))
DEFAULT_BASE = os.path.join(ASSETS_DIR, "sfnl_base.docx")

# Known section types for upfront validation
_KNOWN_TYPES: frozenset = frozenset({"cover", "aanleiding", "team"})

_REGISTRY: dict = {}


def _load_registry() -> None:
    global _REGISTRY
    if _REGISTRY:
        return
    from skills.pptx_offerte.scripts.word import cover, aanleiding, team
    _REGISTRY = {
        "cover": cover.add_section,
        "aanleiding": aanleiding.add_section,
        "team": team.add_section,
    }


def assemble_word(slide_plan: list, output_path: str, base: str = DEFAULT_BASE) -> str:
    """
    Build a .docx from slide_plan and save to output_path.

    slide_plan: [{"type": "cover", "content": {...}}, ...]
    Returns output_path.
    Raises ValueError for unknown section types.
    """
    # Validate all types upfront before loading registry or opening files
    for entry in slide_plan:
        section_type = entry.get("type")
        if section_type not in _KNOWN_TYPES:
            raise ValueError(
                f"Unknown section type: {section_type!r}. "
                f"Available: {sorted(_KNOWN_TYPES)}"
            )

    if slide_plan:
        _load_registry()

    doc = Document(base)

    for entry in slide_plan:
        _REGISTRY[entry["type"]](doc, entry.get("content", {}))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    return output_path
