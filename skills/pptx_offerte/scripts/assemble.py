"""Assemble a PPTX from a slide_plan list and the SFNL base template."""
import os
from pptx import Presentation

# Assets live in the hyphenated sibling directory (plugin convention)
_HERE = os.path.dirname(__file__)
ASSETS_DIR = os.path.normpath(os.path.join(_HERE, "../../pptx-offerte/assets"))
DEFAULT_BASE = os.path.join(ASSETS_DIR, "sfnl_base.pptx")

# Registry maps slide type → component add_slide function (loaded lazily)
_REGISTRY: dict | None = None

# Known types declared statically so we can validate without importing components
_KNOWN_TYPES = frozenset({"cover", "section_header", "aanleiding", "team"})


def _load_registry() -> dict:
    global _REGISTRY
    if _REGISTRY is not None:
        return _REGISTRY
    from skills.pptx_offerte.scripts.slides import (
        cover, section_header, aanleiding, team,
    )
    _REGISTRY = {
        "cover": cover.add_slide,
        "section_header": section_header.add_slide,
        "aanleiding": aanleiding.add_slide,
        "team": team.add_slide,
    }
    return _REGISTRY


def assemble(slide_plan: list, output_path: str, base: str = DEFAULT_BASE) -> str:
    """
    Build a .pptx from slide_plan and save to output_path.

    slide_plan: [{"type": "cover", "content": {...}}, ...]
    Returns output_path.
    Raises ValueError for unknown slide types.
    """
    # Validate all types upfront before doing any heavy work.
    # Use the static set so unknown-type raises without importing components.
    for entry in slide_plan:
        slide_type = entry.get("type")
        if slide_type not in _KNOWN_TYPES:
            raise ValueError(
                f"Unknown slide type: {slide_type!r}. "
                f"Available: {sorted(_KNOWN_TYPES)}"
            )

    prs = Presentation(base)
    boilerplate_count = len(prs.slides)

    if slide_plan:
        registry = _load_registry()
        for entry in slide_plan:
            registry[entry["type"]](prs, entry.get("content", {}))

    # New slides were appended after the boilerplate; move them to the front.
    _move_slides_to_front(prs, boilerplate_count)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    prs.save(output_path)
    return output_path


def _move_slides_to_front(prs: Presentation, boilerplate_count: int) -> None:
    """Reorder slide XML so new slides precede boilerplate slides."""
    sldIdLst = prs.slides._sldIdLst
    children = list(sldIdLst)
    # children[0:boilerplate_count] = boilerplate (added first via base template)
    # children[boilerplate_count:] = new slides (appended by component calls)
    reordered = children[boilerplate_count:] + children[:boilerplate_count]
    for child in children:
        sldIdLst.remove(child)
    for child in reordered:
        sldIdLst.append(child)
