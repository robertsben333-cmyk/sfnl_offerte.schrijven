"""Tests for Word akkoord section component."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from docx import Document

BASE = "skills/pptx_offerte/assets/sfnl_base.docx"
CONTENT = {
    "randvoorwaarden_tekst": "De teamsamenstelling is indicatief.",
    "termijnen": ["50% bij opdrachtverlening", "50% bij oplevering"],
    "sfnl_naam": "Ruben Koekoek",
    "klant_naam": "Jan de Vries",
    "klant_org": "Testorganisatie",
}


def _full_text(doc) -> str:
    return "\n".join(p.text for p in doc.paragraphs)


def test_akkoord_word_contains_names_and_terms():
    from skills.pptx_offerte.scripts.word.akkoord import add_section
    doc = Document(BASE)
    add_section(doc, CONTENT)
    text = _full_text(doc)
    assert "Ruben Koekoek" in text
    assert "Jan de Vries" in text
    assert "opdrachtverlening" in text
