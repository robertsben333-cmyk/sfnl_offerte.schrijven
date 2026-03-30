"""Tests for assemble_word.py pipeline."""
import os, sys, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

BASE_DOCX = "skills/pptx-offerte/assets/sfnl_base.docx"


def test_assemble_word_empty_plan(tmp_path):
    """Assembling an empty plan produces a valid docx."""
    from skills.pptx_offerte.scripts.assemble_word import assemble_word
    from docx import Document

    output = str(tmp_path / "out.docx")
    assemble_word([], output, base=BASE_DOCX)
    doc = Document(output)
    assert doc is not None


def test_assemble_word_unknown_type_raises(tmp_path):
    """Unknown section type raises ValueError."""
    from skills.pptx_offerte.scripts.assemble_word import assemble_word

    output = str(tmp_path / "out.docx")
    with pytest.raises(ValueError, match="Unknown section type"):
        assemble_word([{"type": "nonexistent", "content": {}}], output, base=BASE_DOCX)
