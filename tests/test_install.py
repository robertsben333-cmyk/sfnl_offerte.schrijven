"""Tests for install.py helpers."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_learnings_template_contains_required_sections():
    import install as install_module

    template = install_module.LEARNINGS_TEMPLATE
    assert "# SFNL Offerte Learnings" in template
    assert "## MBC" in template
    assert "### Kalibratie" in template
    assert "### Inhoudelijke patronen" in template
    assert "### Procesafwijkingen" in template
