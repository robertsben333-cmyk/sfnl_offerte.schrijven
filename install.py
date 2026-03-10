#!/usr/bin/env python3
"""
SFNL Offerte — Eenmalige installatie
Installeert de benodigde Python-dependency.

Gebruik (na git clone, vanuit de repo-map):
  py install.py
"""

import subprocess
import sys


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

    print("\nKlaar. Voeg de plugin toe via Claude Code → Manage Plugins.")


if __name__ == "__main__":
    install()
