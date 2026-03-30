"""Tests for assemble.py PPTX pipeline."""
import os, sys, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

ASSETS_DIR = "skills/pptx-offerte/assets"
BASE_PPTX = os.path.join(ASSETS_DIR, "sfnl_base.pptx")


def test_assemble_empty_plan_preserves_boilerplate(tmp_path):
    """Assembling an empty slide_plan returns only boilerplate slides."""
    from skills.pptx_offerte.scripts.assemble import assemble
    from pptx import Presentation

    output = str(tmp_path / "out.pptx")
    assemble([], output, base=BASE_PPTX)

    prs = Presentation(output)
    base_prs = Presentation(BASE_PPTX)
    assert len(prs.slides) == len(base_prs.slides)


def test_assemble_unknown_type_raises(tmp_path):
    """Unknown slide type raises ValueError."""
    from skills.pptx_offerte.scripts.assemble import assemble

    output = str(tmp_path / "out.pptx")
    with pytest.raises(ValueError, match="Unknown slide type"):
        assemble([{"type": "nonexistent", "content": {}}], output, base=BASE_PPTX)
