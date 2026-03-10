#!/usr/bin/env python3
"""
SFNL Offerte — Eenmalige installatie
Installeert python-pptx en registreert de Claude skill.

Gebruik (vanuit de gekloonde repo):
  py install.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
SKILL_DEST = Path.home() / ".claude" / "skills" / "sfnl-offerte"


def install():
    print("SFNL Offerte — Setup\n")

    # 1. python-pptx
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

    # 2. SKILL.md → ~/.claude/skills/sfnl-offerte/
    SKILL_DEST.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HERE / "SKILL.md", SKILL_DEST / "SKILL.md")
    print(f"✓ Skill geregistreerd → {SKILL_DEST}")

    print("\nKlaar. Typ /sfnl-offerte in Claude om te beginnen.")


if __name__ == "__main__":
    install()
