"""Tests for Word aanpak section component."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from docx import Document

BASE = "skills/pptx_offerte/assets/sfnl_base.docx"
CONTENT = {
    "title": "Plan van aanpak",
    "subtitle": "In twee fases werken we naar een businesscase toe.",
    "phases": [
        {
            "number": 1,
            "naam": "Impactverkenning",
            "klant": "Testklant",
            "doel": "Begrijpen welke impact centraal staat.",
            "aanpak": "Interviews en deskresearch.",
            "acties_sfnl": ["Deskresearch", "Interviews"],
            "acties_klant": ["Documenten delen"],
            "deliverable": "Notitie met eerste inzichten",
            "dagen": 6,
            "tijdlijn": "jan-feb 2026",
        }
    ],
}


def _full_text(doc) -> str:
    return "\n".join(p.text for p in doc.paragraphs)


def test_aanpak_section_contains_phase_content():
    from skills.pptx_offerte.scripts.word.aanpak_section import add_section
    doc = Document(BASE)
    add_section(doc, CONTENT)
    text = _full_text(doc)
    assert "Impactverkenning" in text
    assert "Interviews en deskresearch" in text
    assert "Notitie met eerste inzichten" in text
