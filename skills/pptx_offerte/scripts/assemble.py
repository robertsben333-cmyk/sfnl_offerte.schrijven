"""Assemble a PPTX from a slide_plan list and the SFNL base template."""
import os
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pptx import Presentation

# Assets live alongside the consolidated skill package
_HERE = os.path.dirname(__file__)
ASSETS_DIR = os.path.normpath(os.path.join(_HERE, "../../pptx_offerte/assets"))
DEFAULT_BASE = os.path.join(ASSETS_DIR, "sfnl_base.pptx")

# Registry maps slide type → component add_slide function (loaded lazily)
_REGISTRY: dict | None = None

# Known types declared statically so we can validate without importing components
_KNOWN_TYPES = frozenset({
    "cover",
    "section_header",
    "aanleiding",
    "aanpak_overview",
    "fase_detail",
    "two_column",
    "tijdslijn",
    "team",
    "budget_table",
    "randvoorwaarden",
    "akkoord",
})


def _load_registry() -> dict:
    global _REGISTRY
    if _REGISTRY is not None:
        return _REGISTRY
    from skills.pptx_offerte.scripts.slides import (
        cover,
        section_header,
        aanleiding,
        aanpak_overview,
        fase_detail,
        two_column,
        tijdslijn,
        team,
        budget_table,
        randvoorwaarden,
        akkoord,
    )
    _REGISTRY = {
        "cover": cover.add_slide,
        "section_header": section_header.add_slide,
        "aanleiding": aanleiding.add_slide,
        "aanpak_overview": aanpak_overview.add_slide,
        "fase_detail": fase_detail.add_slide,
        "two_column": two_column.add_slide,
        "tijdslijn": tijdslijn.add_slide,
        "team": team.add_slide,
        "budget_table": budget_table.add_slide,
        "randvoorwaarden": randvoorwaarden.add_slide,
        "akkoord": akkoord.add_slide,
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

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    if not slide_plan:
        prs.save(output_path)
        return output_path

    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as tmp:
        temp_path = tmp.name

    try:
        prs.save(temp_path)
        _rewrite_slide_order(temp_path, output_path, boilerplate_count)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    return output_path


def _rewrite_slide_order(source_path: str, output_path: str, boilerplate_count: int) -> None:
    """Write a reordered copy of the pptx without mutating slide parts in-memory."""
    presentation_xml = "ppt/presentation.xml"
    ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}

    with zipfile.ZipFile(source_path, "r") as src:
        xml_bytes = src.read(presentation_xml)
        root = ET.fromstring(xml_bytes)
        sld_id_list = root.find("p:sldIdLst", ns)
        if sld_id_list is None:
            raise ValueError("presentation.xml mist p:sldIdLst")

        slide_ids = list(sld_id_list)
        generated_slide_ids = slide_ids[boilerplate_count:]
        sld_id_list[:] = generated_slide_ids
        updated_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                if item.filename == presentation_xml:
                    dst.writestr(item, updated_xml)
                else:
                    dst.writestr(item, src.read(item.filename))
