"""Tests for review_offerte budget compatibility."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_check_budget_accepts_slide_plan_budget_table():
    from scripts.review_offerte import check_budget

    slide_plan = [
        {"type": "budget_table", "content": {
            "rows": [
                {"fase": "Fase 1", "kosten": 1000},
                {"fase": "Fase 2", "kosten": 2000},
                {"fase": "Totaal", "kosten": 3000},
            ]
        }}
    ]

    assert check_budget(slide_plan) == []


def test_check_budget_flags_mismatched_total_in_slide_plan():
    from scripts.review_offerte import check_budget

    slide_plan = [
        {"type": "budget_table", "content": {
            "rows": [
                {"fase": "Fase 1", "kosten": 1000},
                {"fase": "Totaal", "kosten": 1200},
            ]
        }}
    ]

    issues = check_budget(slide_plan)
    assert any("Totaalrij" in issue for issue in issues)
