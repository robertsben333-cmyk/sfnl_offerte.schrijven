"""Tests for Word cover section component."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from docx import Document

BASE = "skills/pptx_offerte/assets/sfnl_base.docx"
CONTENT = {"client": "Testorg", "title": "PROJECTTITEL", "date": "april 2026", "proposition": "mbc"}


def _full_text(doc) -> str:
    return "\n".join(p.text for p in doc.paragraphs)


def test_cover_word_adds_content():
    from skills.pptx_offerte.scripts.word.cover import add_section
    doc = Document(BASE)
    add_section(doc, CONTENT)
    text = _full_text(doc)
    assert "Testorg" in text
    assert "PROJECTTITEL" in text
    assert "april 2026" in text
