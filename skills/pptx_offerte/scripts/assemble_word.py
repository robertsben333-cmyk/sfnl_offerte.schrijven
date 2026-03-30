"""Assemble a Word document from a slide_plan list and the SFNL base template."""
import os
from docx import Document

_HERE = os.path.dirname(__file__)
ASSETS_DIR = os.path.normpath(os.path.join(_HERE, "../../pptx_offerte/assets"))
DEFAULT_BASE = os.path.join(ASSETS_DIR, "sfnl_base.docx")

# Known section types for upfront validation
_KNOWN_TYPES: frozenset = frozenset({
    "cover",
    "section_header",
    "aanleiding",
    "aanpak_section",
    "aanpak_overview",
    "fase_detail",
    "tijdslijn",
    "team",
    "budget_table",
    "randvoorwaarden",
    "akkoord",
})

_REGISTRY: dict | None = None


def _load_registry() -> None:
    global _REGISTRY
    if _REGISTRY is not None:
        return
    from skills.pptx_offerte.scripts.word import (
        cover,
        aanleiding,
        aanpak_section,
        team,
        budget_table,
        akkoord,
    )
    _REGISTRY = {
        "cover": cover.add_section,
        "aanleiding": aanleiding.add_section,
        "aanpak_section": aanpak_section.add_section,
        "team": team.add_section,
        "budget_table": budget_table.add_section,
        "akkoord": akkoord.add_section,
    }


def _normalize_word_plan(slide_plan: list) -> list:
    """Collapse PPTX-native slide types into Word-native sections."""
    normalized = []
    aanpak_section_content = None
    randvoorwaarden_items = []

    for entry in slide_plan:
        section_type = entry.get("type")
        content = dict(entry.get("content", {}))

        if section_type == "section_header":
            continue

        if section_type == "aanpak_section":
            if aanpak_section_content is not None:
                normalized.append({"type": "aanpak_section", "content": aanpak_section_content})
            aanpak_section_content = {
                "title": content.get("title", "Plan van aanpak"),
                "subtitle": content.get("subtitle", ""),
                "phases": list(content.get("phases", [])),
            }
            continue

        if section_type == "aanpak_overview":
            if aanpak_section_content is None:
                aanpak_section_content = {
                    "title": content.get("title", "Plan van aanpak"),
                    "subtitle": content.get("subtitle", ""),
                    "phases": [],
                }
            else:
                aanpak_section_content["title"] = content.get("title", aanpak_section_content.get("title", "Plan van aanpak"))
                aanpak_section_content["subtitle"] = content.get("subtitle", aanpak_section_content.get("subtitle", ""))
            for index, phase in enumerate(content.get("phases", []), start=1):
                merged = dict(phase)
                merged.setdefault("number", index)
                aanpak_section_content["phases"].append(merged)
            continue

        if section_type == "fase_detail":
            if aanpak_section_content is None:
                aanpak_section_content = {"title": "Plan van aanpak", "subtitle": "", "phases": []}
            phase = dict(content)
            phase_number = phase.get("number")
            existing = None
            if phase_number is not None:
                existing = next(
                    (item for item in aanpak_section_content["phases"] if item.get("number") == phase_number),
                    None,
                )
            if existing is None:
                aanpak_section_content["phases"].append(phase)
            else:
                existing.update({k: v for k, v in phase.items() if v not in ("", [], None)})
            continue

        if section_type == "tijdslijn":
            if aanpak_section_content is None:
                aanpak_section_content = {"title": "Plan van aanpak", "subtitle": "", "phases": []}
            if content.get("intro") and not aanpak_section_content.get("subtitle"):
                aanpak_section_content["subtitle"] = content["intro"]
            if content.get("disclaimer"):
                aanpak_section_content["timeline_note"] = content["disclaimer"]
            for index, phase in enumerate(content.get("phases", []), start=1):
                existing = next(
                    (item for item in aanpak_section_content["phases"] if item.get("number", index) == index),
                    None,
                )
                if existing is None:
                    merged = {"number": index, "naam": phase.get("naam", ""), "tijdlijn": phase.get("periode", "")}
                    if phase.get("activiteiten"):
                        merged["beschrijving"] = phase["activiteiten"]
                    aanpak_section_content["phases"].append(merged)
                else:
                    existing.setdefault("tijdlijn", phase.get("periode", ""))
                    existing.setdefault("beschrijving", phase.get("activiteiten", ""))
            continue

        if section_type == "randvoorwaarden":
            randvoorwaarden_items.extend(content.get("items", []))
            continue

        if aanpak_section_content is not None and section_type not in {"aanpak_overview", "fase_detail", "tijdslijn"}:
            normalized.append({"type": "aanpak_section", "content": aanpak_section_content})
            aanpak_section_content = None

        if section_type == "akkoord" and randvoorwaarden_items:
            content.setdefault("randvoorwaarden_items", []).extend(randvoorwaarden_items)
            randvoorwaarden_items = []

        normalized.append({"type": section_type, "content": content})

    if aanpak_section_content is not None:
        normalized.append({"type": "aanpak_section", "content": aanpak_section_content})
    if randvoorwaarden_items:
        normalized.append({"type": "akkoord", "content": {"randvoorwaarden_items": randvoorwaarden_items}})
    return normalized


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

    normalized_plan = _normalize_word_plan(slide_plan)

    if normalized_plan:
        _load_registry()
        assert _REGISTRY is not None

    doc = Document(base)

    for entry in normalized_plan:
        _REGISTRY[entry["type"]](doc, entry.get("content", {}))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    return output_path
