"""Tests for PPTX fase_detail slide component."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from pptx import Presentation

BASE = "skills/pptx_offerte/assets/sfnl_base.pptx"

CONTENT = {
    "number": 1,
    "naam": "Testfase",
    "klant": "Testklant",
    "doel": "Het doel is om X te bereiken.",
    "aanpak": "De aanpak bestaat uit Y stappen.",
    "acties_sfnl": ["Deskresearch", "Stakeholderinterviews"],
    "acties_klant": ["Beschikbaar stellen gegevens"],
    "deliverable": "Rapport en presentatie",
    "dagen": 8,
    "tijdlijn": "jan–feb 2026",
    "proposition": "mbc"
}


def _all_text(slide) -> str:
    return " ".join(s.text_frame.text for s in slide.shapes if s.has_text_frame)


def test_fase_detail_adds_one_slide():
    from skills.pptx_offerte.scripts.slides.fase_detail import add_slide
    prs = Presentation(BASE)
    before = len(prs.slides)
    add_slide(prs, CONTENT)
    assert len(prs.slides) == before + 1


def test_fase_detail_contains_phase_name():
    from skills.pptx_offerte.scripts.slides.fase_detail import add_slide
    prs = Presentation(BASE)
    add_slide(prs, CONTENT)
    assert "Testfase" in _all_text(prs.slides[-1])


def test_fase_detail_contains_doel_and_aanpak():
    from skills.pptx_offerte.scripts.slides.fase_detail import add_slide
    prs = Presentation(BASE)
    add_slide(prs, CONTENT)
    text = _all_text(prs.slides[-1])
    assert "doel is om X" in text
    assert "aanpak bestaat" in text


def test_fase_detail_contains_acties():
    from skills.pptx_offerte.scripts.slides.fase_detail import add_slide
    prs = Presentation(BASE)
    add_slide(prs, CONTENT)
    text = _all_text(prs.slides[-1])
    assert "Deskresearch" in text
    assert "Stakeholderinterviews" in text
    assert "TESTKLANT" in text


def test_fase_detail_contains_deliverable_and_days():
    from skills.pptx_offerte.scripts.slides.fase_detail import add_slide
    prs = Presentation(BASE)
    add_slide(prs, CONTENT)
    text = _all_text(prs.slides[-1])
    assert "Rapport en presentatie" in text
    assert "8" in text
