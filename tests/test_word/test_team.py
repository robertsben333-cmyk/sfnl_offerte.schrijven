"""Tests for Word team section component."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from docx import Document

BASE = "skills/pptx_offerte/assets/sfnl_base.docx"
CONTENT = {
    "members": [
        {"name": "Laura Brouwer", "title": "ASSOCIATE DIRECTOR", "bio": "Laura heeft 10 jaar ervaring."},
        {"name": "Dieuwertje Roos", "title": "MANAGER", "bio": "Gespecialiseerd in MBC."},
    ]
}


def _full_text(doc) -> str:
    return "\n".join(p.text for p in doc.paragraphs)


def test_team_word_contains_names():
    from skills.pptx_offerte.scripts.word.team import add_section
    doc = Document(BASE)
    add_section(doc, CONTENT)
    text = _full_text(doc)
    assert "Laura Brouwer" in text
    assert "Dieuwertje Roos" in text
