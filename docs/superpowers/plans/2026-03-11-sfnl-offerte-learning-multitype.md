# SFNL Offerte Learning-mechanisme & Multi-projecttype Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hernoem de `sfnl-offerte` skill naar `sfnl-offerte-mbc` en voeg een learning-mechanisme toe dat gegeneraliseerde inzichten wegschrijft na akkoord en inleest bij volgende offertes.

**Architecture:** Drie losse wijzigingen die sequentieel worden doorgevoerd: (1) hernoemen van de skill-map + plugin-manifesten, (2) aanmaken van `data/learnings.md` met lege sectiestructuur + install.py uitbreiding, (3) leerlogica in `SKILL.md`. Elke taak eindigt met een commit.

**Tech Stack:** Markdown (skill), Python (install.py + pathlib), JSON (plugin manifests), Git (history-behoud via git mv)

**Spec:** `docs/superpowers/specs/2026-03-11-sfnl-offerte-learning-multitype-design.md`

---

## Chunk 1: Hernoeming en plugin-manifesten

### Task 1: Hernoem skill-map en update plugin-manifesten

**Files:**
- Rename: `skills/sfnl-offerte/` → `skills/sfnl-offerte-mbc/` (via git mv)
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Stap 1: Hernoem de skill-map met git mv (bewaart history)**

```bash
git mv skills/sfnl-offerte skills/sfnl-offerte-mbc
```

Verwacht: geen output, geen fout.

- [ ] **Stap 2: Controleer dat de map hernoemd is**

```bash
ls skills/
```

Verwacht: `sfnl-offerte-mbc/` zichtbaar, geen `sfnl-offerte/` meer.

- [ ] **Stap 3: Update `.claude-plugin/plugin.json`**

Vervang de volledige inhoud van `.claude-plugin/plugin.json` met:

```json
{
  "name": "sfnl-offerte-mbc",
  "version": "1.1.0",
  "description": "Schrijft SFNL MBC-offertes voor maatschappelijke businesscases en duurzame financiering",
  "author": {
    "name": "Social Finance NL"
  },
  "repository": "https://github.com/robertsben333-cmyk/sfnl_offerte.schrijven",
  "keywords": ["sfnl", "offerte", "mbc", "businesscase", "impact", "financiering"]
}
```

- [ ] **Stap 4: Update `.claude-plugin/marketplace.json`**

Vervang de volledige inhoud van `.claude-plugin/marketplace.json` met:

```json
{
  "name": "sfnl-plugins",
  "description": "Claude plugins voor Social Finance NL",
  "owner": {
    "name": "Social Finance NL",
    "email": "info@socialfinancenl.nl"
  },
  "plugins": [
    {
      "name": "sfnl-offerte-mbc",
      "description": "Schrijft SFNL MBC-offertes voor maatschappelijke businesscases en duurzame financiering",
      "version": "1.1.0",
      "source": "./",
      "author": {
        "name": "Social Finance NL"
      }
    }
  ]
}
```

- [ ] **Stap 5: Commit**

```bash
git add skills/sfnl-offerte-mbc .claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "refactor: hernoem sfnl-offerte skill naar sfnl-offerte-mbc"
```

---

## Chunk 2: learnings.md en install.py

### Task 2: Maak `data/learnings.md` aan

**Files:**
- Create: `data/learnings.md`

- [ ] **Stap 1: Maak `data/learnings.md` aan met lege sectiestructuur**

Inhoud van `data/learnings.md`:

```markdown
# SFNL Offerte Learnings

## MBC

### Kalibratie
<!-- dag-schattingen, tarieven, betalingstermijnen -->
<!-- Format: - [YYYY-MM-DD] [label]: [inzicht] -->

### Inhoudelijke patronen
<!-- sector-inzichten, terugkerende aandachtspunten, effectieve formuleringen -->
<!-- Format: - [YYYY-MM-DD] [label]: [inzicht] -->

### Procesafwijkingen
<!-- hoe fases of structuur werd aangepast t.o.v. de standaard -->
<!-- Format: - [YYYY-MM-DD] [label]: [inzicht] -->
```

- [ ] **Stap 2: Commit**

```bash
git add data/learnings.md
git commit -m "feat: voeg lege data/learnings.md toe"
```

---

### Task 3: Breid `install.py` uit

**Files:**
- Modify: `install.py`

De huidige `install.py` heeft alleen python-pptx installatie. We voegen twee dingen toe:
1. Aanmaken van `data/learnings.md` als die niet bestaat
2. Waarschuwing als de oude `~/.claude/skills/sfnl-offerte/` nog bestaat

- [ ] **Stap 1: Pas `install.py` aan**

Vervang de volledige inhoud van `install.py` met:

```python
#!/usr/bin/env python3
"""
SFNL Offerte — Eenmalige installatie
Installeert de benodigde Python-dependency en bereidt projectbestanden voor.

Gebruik (na git clone, vanuit de repo-map):
  py install.py
"""

import subprocess
import sys
from pathlib import Path

LEARNINGS_TEMPLATE = """\
# SFNL Offerte Learnings

## MBC

### Kalibratie
<!-- dag-schattingen, tarieven, betalingstermijnen -->
<!-- Format: - [YYYY-MM-DD] [label]: [inzicht] -->

### Inhoudelijke patronen
<!-- sector-inzichten, terugkerende aandachtspunten, effectieve formuleringen -->
<!-- Format: - [YYYY-MM-DD] [label]: [inzicht] -->

### Procesafwijkingen
<!-- hoe fases of structuur werd aangepast t.o.v. de standaard -->
<!-- Format: - [YYYY-MM-DD] [label]: [inzicht] -->
"""


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

    # 2. data/learnings.md aanmaken als die niet bestaat
    learnings_path = Path(__file__).parent / "data" / "learnings.md"
    if not learnings_path.exists():
        learnings_path.write_text(LEARNINGS_TEMPLATE, encoding="utf-8")
        print("✓ data/learnings.md aangemaakt")
    else:
        print("✓ data/learnings.md al aanwezig")

    # 3. Waarschuw als oude skill-map nog bestaat
    old_skill_path = Path.home() / ".claude" / "skills" / "sfnl-offerte"
    if old_skill_path.exists():
        print(
            f"\n⚠  Oude skill gevonden: {old_skill_path}\n"
            f"   Verwijder handmatig: rm -rf \"{old_skill_path}\""
        )

    print("\nKlaar. Voeg de plugin toe via Claude Code → Manage Plugins.")


if __name__ == "__main__":
    install()
```

- [ ] **Stap 2: Verifieer dat install.py syntactisch correct is**

```bash
py -m py_compile install.py && echo "OK"
```

Verwacht: `OK`

- [ ] **Stap 3: Voer install.py uit en controleer output**

```bash
py install.py
```

Verwacht output (exact):
```
SFNL Offerte — Setup

✓ python-pptx al geïnstalleerd
✓ data/learnings.md al aanwezig

Klaar. Voeg de plugin toe via Claude Code → Manage Plugins.
```

(De `learnings.md` bestaat al uit Task 2, dus "al aanwezig" is correct.)

- [ ] **Stap 4: Commit**

```bash
git add install.py
git commit -m "feat: install.py maakt learnings.md aan en waarschuwt voor oude skill"
```

---

## Chunk 3: Leerlogica in SKILL.md

> **Vereiste**: Chunk 1 (Task 1) moet volledig gecommit zijn voordat je hier begint — Task 4 werkt op het hernoemde pad `skills/sfnl-offerte-mbc/SKILL.md`.

### Task 4: Voeg leerlogica toe aan `skills/sfnl-offerte-mbc/SKILL.md`

**Files:**
- Modify: `skills/sfnl-offerte-mbc/SKILL.md`

De SKILL.md heeft twee aanvullingen nodig:
1. Een **"Learnings laden"** sectie — na de STEP 1 (intake) header, vóór STEP 2a
2. Een **"Learnings schrijven"** sectie — na STEP 2c, vóór het GENERATE blok

#### Stap 1: Voeg "Learnings laden" sectie in

- [ ] **Stap 1: Voeg de volgende sectie in direct vóór `## STEP 2a`**

Voeg in tussen het einde van de `## STEP 1` sectie en het begin van `## STEP 2a`:

```markdown
---

## LEARNINGS — Laden (na stap 1, vóór stap 2a)

Lees `${CLAUDE_PLUGIN_ROOT}/data/learnings.md` ná de intake maar vóór het opstellen van voorstellen. Learnings beïnvloeden de intakevragen **niet**.

Als het bestand niet bestaat of leeg is: sla dit blok over en ga door met de defaults.

### Kalibraties (stilzwijgend toepassen in stap 2b)

Kalibraties worden toegepast op het moment dat dag-schattingen worden opgesteld in stap 2b — pas dan is de tier bekend.

**Basislijn per tier:**

| Tier | Fase 1 | Fase 2 | Fase 3 |
|------|--------|--------|--------|
| Basic | 6d | 9d | 4d |
| Standaard | 8d | 14d | 6d |
| Complex | 10d | 19d | 8d |

**Regels:**
- Kalibraties uit onafhankelijke dimensies worden opgeteld: "+1d zorgsector" + "+1d beperkte data" = +2d.
- Als twee entries in dezelfde dimensie conflicteren: gebruik de meest recente entry.
- Toon het gecorrigeerde getal als default, alsof het de oorspronkelijke schatting is — noem de correctie niet.

Voorbeeld: learnings zeggen "+1d fase 2 voor zorgsector" en "+1d fase 2 voor beperkte data". Stel voor: "Fase 2: 16 dagen" (basiswaarde 14d + 2d) zonder vermelding.

### Inhoudelijke patronen (expliciet benoemen in stap 2a)

Alle matchende patronen worden expliciet benoemd. Als twee patronen tegenstrijdig zijn, toon ze beide zodat de gebruiker kan oordelen.

Voorbeeld: "Op basis van eerdere offertes voor zorginstellingen: intern draagvlak is bijna altijd een kernbehoefte — ik heb dit als eerste aandachtspunt opgenomen."

```

#### Stap 2: Voeg "Learnings schrijven" sectie in

- [ ] **Stap 2: Voeg de volgende sectie in direct ná `## STEP 2c` en vóór `## GENERATE`**

Voeg in tussen het einde van `## STEP 2c` en het begin van `## GENERATE`:

```markdown
---

## LEARNINGS — Schrijven (na akkoord stap 2c, vóór generatie)

Analyseer de bevestigde keuzes en vergelijk met de defaults. Schrijf naar `${CLAUDE_PLUGIN_ROOT}/data/learnings.md` (append, nooit overschrijven) als aan één of meer drempelcriteria is voldaan.

**Drempelcriteria:**

| Categorie | Drempel | Sectie in learnings.md |
|-----------|---------|------------------------|
| Kalibratie dag-schatting | Afwijking ≥ 2 dagen t.o.v. basislijn per fase | `### Kalibratie` |
| Kalibratie tarief | NGO-tarief bij non-profit klant — alleen als geen entry met label `tarief:ngo-non-profit` bestaat | `### Kalibratie` |
| Inhoudelijk patroon | Aandachtspunt direct voortkomend uit klanttype/sector, niet projectspecifiek | `### Inhoudelijke patronen` |
| Procesafwijking | Fase-structuur wijkt af van standaard 3-fasen opzet | `### Procesafwijkingen` |

**Format per entry:** `- [YYYY-MM-DD] label: inzicht`

**Regels:**
- Geen klantnamen, geen specifieke bedragen.
- Beknopt (één regel per inzicht).
- Als niets aan de drempel voldoet: schrijf niets.
- Foutafhandeling: als schrijven mislukt, toon waarschuwing ("Kon learnings niet opslaan: [reden]") en ga door met generatie.

**Voorbeeldentries:**
```markdown
- [2026-03-11] zorgsector fase2: +2d t.o.v. standaard baseline door beperkte databeschikbaarheid
- [2026-03-11] tarief:ngo-non-profit: NGO-tarief gekozen bij non-profit klant
- [2026-03-11] zorgsector aandachtspunt: intern draagvlak is bijna altijd een kernbehoefte
- [2026-03-11] procesafwijking: fase 4 toegevoegd voor financieel businessplan (+10d)
```

```

- [ ] **Stap 3: Verifieer de sectievolgorde in SKILL.md**

Open `skills/sfnl-offerte-mbc/SKILL.md` en controleer dat de volgorde klopt:
```
## STEP 1 — Intake
## LEARNINGS — Laden
## STEP 2a — Propose: Doel & Doelgroep
## STEP 2b — Propose: Fases & Tijdlijn
## STEP 2c — Propose: Outcomes, Team, Tarief & Budget
## LEARNINGS — Schrijven
## GENERATE — Build config & run script
## REVIEW
```

- [ ] **Stap 4: Commit**

```bash
git add skills/sfnl-offerte-mbc/SKILL.md
git commit -m "feat: voeg learning-mechanisme toe aan sfnl-offerte-mbc skill"
```

---

## Chunk 4: CLAUDE.md update en handmatige verificatie

### Task 5: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

`CLAUDE.md` bevat verwijzingen naar de skill-naam en directorystructuur. Deze moeten worden bijgewerkt.

- [ ] **Stap 1: Update de directorystructuur in CLAUDE.md**

Voeg `data/learnings.md` toe aan de directory-tree in CLAUDE.md:

Zoek de sectie:
```
data/
  team.json                    — All SFNL team members with bios and contact info
```

Vervang door:
```
data/
  team.json                    — All SFNL team members with bios and contact info
  learnings.md                 — Accumulated insights across proposals (auto-updated by skill)
skills/
  sfnl-offerte-mbc/SKILL.md   — MBC proposal skill (trigger: /sfnl-offerte-mbc)
```

- [ ] **Stap 2: Voeg een notitie toe aan CLAUDE.md over de skill-naam**

Voeg onderaan de bestaande inhoud toe (vóór eventuele footer):

```markdown
## Skill naam

De skill heet `sfnl-offerte-mbc` (getriggerd via `/sfnl-offerte-mbc`). Toekomstige projecttypes krijgen eigen skills in `skills/sfnl-offerte-[type]/SKILL.md`.
```

- [ ] **Stap 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md met learnings.md en nieuwe skill naam"
```

---

### Task 6: Handmatige verificatie

Geen geautomatiseerde tests mogelijk voor markdown-skills. Voer de volgende verificatiestappen handmatig uit.

- [ ] **Stap 1: Verwijder en herlaad de plugin in Claude Code**

1. Open Claude Code → Settings → Plugins
2. Verwijder de `sfnl-offerte` (of `sfnl-plugins`) plugin
3. Voeg de plugin opnieuw toe via de repo-map
4. Controleer dat `sfnl-offerte-mbc` zichtbaar is in de plugin-lijst

- [ ] **Stap 2: Verifieer skill-trigger**

Typ in Claude Code: `/sfnl-offerte-mbc`
Verwacht: de skill wordt geladen en stelt de intakevragen van stap 1.

- [ ] **Stap 3: Verifieer learnings-lading**

Voeg een testentry toe aan `data/learnings.md`:
```markdown
- [2026-03-11] zorgsector fase2: +2d t.o.v. standaard baseline (testentry)
```

Start een nieuwe offerte via `/sfnl-offerte-mbc`. Voer de intake in met een zorginstelling als klant.
Verwacht bij stap 2b: de dag-schatting voor fase 2 is 2 dagen hoger dan de standaard baseline zonder vermelding.

- [ ] **Stap 4: Verifieer learnings-schrijven**

Rond de offerte af t/m stap 2c. Accepteer alle defaults zodat niets de drempel haalt.
Verwacht: `data/learnings.md` is ongewijzigd (geen nieuwe entries).

Pas een dag-schatting aan met ≥2 dagen afwijking en bevestig opnieuw.
Verwacht: `data/learnings.md` bevat een nieuwe kalibratie-entry.

- [ ] **Stap 5: Verwijder testentry uit learnings.md**

Verwijder de in stap 3 toegevoegde testentry handmatig uit `data/learnings.md`.

- [ ] **Stap 6: Final commit (als stap 4/5 wijzigingen hebben achtergelaten)**

```bash
git add data/learnings.md
git commit -m "chore: verwijder testentry uit learnings.md"
```

---

## Samenvatting gewijzigde bestanden

| Bestand | Wijziging |
|---------|-----------|
| `skills/sfnl-offerte-mbc/SKILL.md` | Hernoemd (git mv) + leerlogica toegevoegd |
| `.claude-plugin/plugin.json` | Naam + versie bijgewerkt |
| `.claude-plugin/marketplace.json` | Plugin-naam bijgewerkt |
| `data/learnings.md` | Nieuw bestand (lege sectiestructuur) |
| `install.py` | learnings.md aanmaken + oude skill waarschuwing |
| `CLAUDE.md` | Directorystructuur + skill-naam bijgewerkt |
