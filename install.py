#!/usr/bin/env python3
"""
SFNL Offerte — Eenmalige installatie
Installeert de benodigde Python-dependency.

Gebruik (na git clone, vanuit de repo-map):
  py install.py
"""

import subprocess
import sys
from pathlib import Path

LEARNINGS_TEMPLATE = """# SFNL Offerte Learnings

## MBC

### Kalibratie
<!-- dag-schattingen, tarieven, betalingstermijnen -->

### Inhoudelijke patronen
<!-- sector-inzichten, terugkerende aandachtspunten, effectieve formuleringen -->

### Procesafwijkingen
<!-- hoe fases of structuur werd aangepast t.o.v. de standaard -->
"""


def install():
    print("SFNL Offerte — Setup\n")
    try:
        import pptx  # noqa: F401
        print("✓ python-pptx al geïnstalleerd")
    except ImportError:
        print("  python-pptx installeren...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "python-pptx", "-q"],
            check=True,
        )
        print("✓ python-pptx geïnstalleerd")

    learnings_path = Path(__file__).parent / "data" / "learnings.md"
    if learnings_path.exists():
        print("✓ data/learnings.md al aanwezig")
    else:
        learnings_path.write_text(LEARNINGS_TEMPLATE, encoding="utf-8")
        print("✓ data/learnings.md aangemaakt")

    old_skill_path = Path.home() / ".claude" / "skills" / "sfnl-offerte"
    if old_skill_path.exists():
        print(f"! Verwijder handmatig de oude skill: {old_skill_path}")

    print("\nKlaar. Voeg de plugin toe via Claude Code → Manage Plugins.")


if __name__ == "__main__":
    install()
