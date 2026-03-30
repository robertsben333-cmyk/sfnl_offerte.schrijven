"""Tests for Word aanleiding section component."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from docx import Document

BASE = "skills/pptx_offerte/assets/sfnl_base.docx"
CONTENT = {
    "vraagstuk": "Het vraagstuk is complex.",
    "uitdagingen": "De uitdagingen zijn divers.",
    "behoefte": "De klant heeft behoefte.",
}


def _full_text(doc) -> str:
    return "\n".join(p.text for p in doc.paragraphs)


def test_aanleiding_word_adds_three_blocks():
    from skills.pptx_offerte.scripts.word.aanleiding import add_section
    doc = Document(BASE)
    add_section(doc, CONTENT)
    text = _full_text(doc)
    assert "vraagstuk is complex" in text
    assert "uitdagingen zijn divers" in text
    assert "behoefte" in text
