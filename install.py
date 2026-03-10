#!/usr/bin/env python3
"""
SFNL Offerte — Eenmalige installatie voor nieuwe gebruikers
Kopieert projectbestanden naar de juiste locaties en installeert dependencies.

Gebruik:
  py install.py
  py install.py --template "pad/naar/offerte_mbc_template.pptx"
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()

# Where Claude looks for skills
SKILL_DEST = Path.home() / ".claude" / "skills" / "sfnl-offerte"

# Where the project files land (scripts, data, templates, CLAUDE.md)
PROJECT_DEST = Path.home() / ".projects SFNL" / "sfnl_offerte.schrijven"

TEMPLATE_DEST = PROJECT_DEST / "templates" / "offerte_mbc_template.pptx"


def step(n, label):
    print(f"\n{n}. {label}")


def ok(msg=""):
    print(f"   ✓ {msg}" if msg else "   ✓")


def warn(msg):
    print(f"   ⚠  {msg}")


def install(template_path=None):
    print("=" * 55)
    print("  SFNL Offerte — Setup")
    print("=" * 55)

    # ── 1. python-pptx ────────────────────────────────────────
    step(1, "Afhankelijkheden controleren")
    try:
        import pptx  # noqa: F401
        ok("python-pptx al geïnstalleerd")
    except ImportError:
        print("   python-pptx installeren...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "python-pptx", "-q"],
            check=True,
        )
        ok("python-pptx geïnstalleerd")

    # ── 2. Claude skill ───────────────────────────────────────
    step(2, f"Claude skill installeren → {SKILL_DEST}")
    SKILL_DEST.mkdir(parents=True, exist_ok=True)
    skill_src = HERE / "SKILL.md"
    if skill_src.exists():
        shutil.copy2(skill_src, SKILL_DEST / "SKILL.md")
        ok("SKILL.md gekopieerd")
    else:
        warn("SKILL.md niet gevonden in de zip — sla deze stap over als je het al hebt")

    # ── 3. Projectbestanden ───────────────────────────────────
    step(3, f"Projectbestanden kopiëren → {PROJECT_DEST}")
    PROJECT_DEST.mkdir(parents=True, exist_ok=True)

    for subdir in ("scripts", "data"):
        src = HERE / subdir
        if src.exists():
            shutil.copytree(src, PROJECT_DEST / subdir, dirs_exist_ok=True)
            ok(f"{subdir}/ gekopieerd")

    claude_md = HERE / "CLAUDE.md"
    if claude_md.exists():
        shutil.copy2(claude_md, PROJECT_DEST / "CLAUDE.md")
        ok("CLAUDE.md gekopieerd")

    # Create output folder
    (PROJECT_DEST / "output").mkdir(exist_ok=True)
    ok("output/ map aangemaakt")

    # ── 4. Template ───────────────────────────────────────────
    step(4, "Proposaltemplate instellen")
    TEMPLATE_DEST.parent.mkdir(parents=True, exist_ok=True)

    if template_path:
        src = Path(template_path)
        if src.exists():
            shutil.copy2(src, TEMPLATE_DEST)
            ok(f"Template gekopieerd vanuit {src}")
        else:
            warn(f"Template niet gevonden op: {src}")
            _print_template_instructions()
    elif TEMPLATE_DEST.exists():
        ok("Template al aanwezig")
    else:
        # Check if it shipped alongside install.py
        bundled = HERE / "templates" / "offerte_mbc_template.pptx"
        if bundled.exists():
            shutil.copy2(bundled, TEMPLATE_DEST)
            ok("Template gekopieerd vanuit zip")
        else:
            warn("Template niet gevonden")
            _print_template_instructions()

    # ── 5. Klaar ──────────────────────────────────────────────
    print(f"\n{'=' * 55}")
    if TEMPLATE_DEST.exists():
        print("  Installatie voltooid ✓")
        print("  Typ /sfnl-offerte in Claude om te beginnen.")
    else:
        print("  Installatie bijna klaar — template ontbreekt nog (zie boven).")
    print("=" * 55)


def _print_template_instructions():
    print(f"""
   Vraag de template op via SharePoint of een collega en
   voer daarna het volgende uit:

     py install.py --template "pad/naar/offerte_mbc_template.pptx"

   Of kopieer het bestand handmatig naar:
     {TEMPLATE_DEST}
""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SFNL Offerte setup")
    parser.add_argument(
        "--template",
        metavar="PAD",
        help="Pad naar offerte_mbc_template.pptx",
    )
    args = parser.parse_args()
    install(args.template)
