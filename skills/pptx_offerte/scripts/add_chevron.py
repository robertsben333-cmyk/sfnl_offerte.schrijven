"""Add or reflow chevrons on slide 6 of an unpacked SFNL offerte PPTX.

Usage:
    python add_chevron.py <unpacked_dir> --fases <N>

Example:
    python add_chevron.py unpacked/ --fases 4

What it does
------------
1. Reads slide6.xml from the unpacked directory.
2. Recalculates chevron width and x-positions for N fases so they fit the slide.
3. Updates the width + x-position of all existing chevron/homePlate shapes and their
   matching description boxes.
4. Adds new chevron(s) and description box(es) for any fases beyond 3, using accent4
   (and accent5, accent6 for 5 or 6 fases).
5. Repositions the timeline label text boxes to stay centred under each chevron.
6. Writes the updated XML back to slide6.xml.

After running this script, edit slide6.xml normally to fill in the text content
(chevron labels, description texts, timeline labels).

Slide geometry (EMUs)
---------------------
Slide width:  12192000
Left margin:  492935  (x of fase 1 chevron)
Overlap:       66935  (how much each chevron overlaps the next)
"""

import argparse
import re
import sys
from copy import deepcopy
from lxml import etree
from pathlib import Path


# ── Constants ────────────────────────────────────────────────────────────────

SLIDE_WIDTH  = 12192000
LEFT_MARGIN  = 492935
OVERLAP      = 66935

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'

# accent colours for fases 1-6 (index 0 = fase 1)
ACCENT_COLOURS = ['accent1', 'accent2', 'accent3', 'accent4', 'accent5', 'accent6']

# Description box height (EMU) — keep consistent with template
BOX_HEIGHT = 2321021
BOX_Y      = 2714121   # y-position of all description boxes

# Chevron height and y-position
CHEVRON_H  = 470523
CHEVRON_Y  = 2176240


# ── Geometry helpers ─────────────────────────────────────────────────────────

def chevron_width(n: int) -> int:
    """Width of each chevron for a layout of n fases."""
    usable = SLIDE_WIDTH - LEFT_MARGIN - (n - 1) * OVERLAP
    return usable // n


def chevron_x(i: int, w: int) -> int:
    """Left x-coordinate of chevron i (0-indexed) with width w."""
    return LEFT_MARGIN + i * (w - OVERLAP)


# ── XML helpers ──────────────────────────────────────────────────────────────

def get_xfrm(el):
    """Return the <a:xfrm> element inside el, or None."""
    return el.find('.//{%s}xfrm' % A)


def set_off_ext(xfrm, x=None, y=None, cx=None, cy=None):
    off = xfrm.find('{%s}off' % A)
    ext = xfrm.find('{%s}ext' % A)
    if x  is not None: off.set('x',  str(x))
    if y  is not None: off.set('y',  str(y))
    if cx is not None: ext.set('cx', str(cx))
    if cy is not None: ext.set('cy', str(cy))


def get_shape_x(sp):
    xfrm = get_xfrm(sp)
    if xfrm is None:
        return None
    off = xfrm.find('{%s}off' % A)
    return int(off.get('x')) if off is not None else None


def get_prst_geom(sp):
    return sp.find('.//{%s}prstGeom' % A)


def is_chevron_shape(sp):
    pg = get_prst_geom(sp)
    return pg is not None and pg.get('prst') in ('chevron', 'homePlate')


def is_description_box(sp):
    """Dashed rectangle below a chevron — identified by y-position."""
    xfrm = get_xfrm(sp)
    if xfrm is None:
        return False
    off = xfrm.find('{%s}off' % A)
    if off is None:
        return False
    y = int(off.get('y', 0))
    # Description boxes sit between y=2700000 and y=2730000
    return 2700000 < y < 2730000


def is_timeline_label(sp):
    """Small text box carrying a timeline label (Maand N)."""
    xfrm = get_xfrm(sp)
    if xfrm is None:
        return False
    off = xfrm.find('{%s}off' % A)
    if off is None:
        return False
    y = int(off.get('y', 0))
    # Timeline labels are in the lower portion of the slide
    return y > 5000000


def get_text_content(sp):
    texts = [t.text or '' for t in sp.findall('.//{%s}t' % A)]
    return ' '.join(texts).strip()


def make_chevron_sp(fase_index: int, x: int, w: int, label: str) -> etree._Element:
    """Create a new chevron <p:sp> element for a fase."""
    accent = ACCENT_COLOURS[min(fase_index, len(ACCENT_COLOURS) - 1)]
    sp = etree.Element('{%s}sp' % P)

    nvSpPr = etree.SubElement(sp, '{%s}nvSpPr' % P)
    cNvPr  = etree.SubElement(nvSpPr, '{%s}cNvPr' % P)
    cNvPr.set('id', str(100 + fase_index))
    cNvPr.set('name', f'Arrow: Chevron {100 + fase_index}')
    etree.SubElement(nvSpPr, '{%s}cNvSpPr' % P)
    etree.SubElement(nvSpPr, '{%s}nvPr' % P)

    spPr = etree.SubElement(sp, '{%s}spPr' % P)
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % A)
    off  = etree.SubElement(xfrm, '{%s}off' % A)
    off.set('x', str(x)); off.set('y', str(CHEVRON_Y))
    ext  = etree.SubElement(xfrm, '{%s}ext' % A)
    ext.set('cx', str(w)); ext.set('cy', str(CHEVRON_H))
    prst = etree.SubElement(spPr, '{%s}prstGeom' % A)
    prst.set('prst', 'chevron')
    etree.SubElement(prst, '{%s}avLst' % A)
    fill = etree.SubElement(spPr, '{%s}solidFill' % A)
    etree.SubElement(fill, '{%s}schemeClr' % A).set('val', accent)
    ln   = etree.SubElement(spPr, '{%s}ln' % A)
    etree.SubElement(ln, '{%s}noFill' % A)

    style = etree.SubElement(sp, '{%s}style' % P)
    for tag, idx_val in [('lnRef', '2'), ('fillRef', '1'), ('effectRef', '0'), ('fontRef', 'minor')]:
        ref = etree.SubElement(style, '{%s}%s' % (A, tag))
        ref.set('idx', idx_val)
        sc  = etree.SubElement(ref, '{%s}schemeClr' % A)
        if tag == 'fontRef':
            sc.set('val', 'lt1')
        else:
            sc.set('val', 'accent1')
            if tag == 'lnRef':
                etree.SubElement(sc, '{%s}shade' % A).set('val', '50000')

    txBody = etree.SubElement(sp, '{%s}txBody' % P)
    bodyPr = etree.SubElement(txBody, '{%s}bodyPr' % A)
    bodyPr.set('rtlCol', '0'); bodyPr.set('anchor', 'ctr')
    etree.SubElement(txBody, '{%s}lstStyle' % A)
    p_el = etree.SubElement(txBody, '{%s}p' % A)
    pPr  = etree.SubElement(p_el, '{%s}pPr' % A)
    for attr, val in [('marL','0'),('marR','0'),('lvl','0'),('indent','0'),
                      ('algn','ctr'),('rtl','0'),('eaLnBrk','1'),('latinLnBrk','0')]:
        pPr.set(attr, val)
    etree.SubElement(etree.SubElement(pPr, '{%s}lnSpc'  % A), '{%s}spcPct' % A).set('val', '100000')
    etree.SubElement(etree.SubElement(pPr, '{%s}spcBef' % A), '{%s}spcPts' % A).set('val', '0')
    etree.SubElement(etree.SubElement(pPr, '{%s}spcAft' % A), '{%s}spcPts' % A).set('val', '0')
    etree.SubElement(pPr, '{%s}buNone' % A)
    r_el = etree.SubElement(p_el, '{%s}r' % A)
    rPr  = etree.SubElement(r_el, '{%s}rPr' % A)
    for attr, val in [('kumimoji','0'),('lang','nl-NL'),('sz','1400'),('b','1'),
                      ('i','0'),('u','none'),('strike','noStrike'),('kern','1200'),
                      ('cap','none'),('spc','0'),('normalizeH','0'),('baseline','0'),('noProof','0')]:
        rPr.set(attr, val)
    ln2 = etree.SubElement(rPr, '{%s}ln' % A)
    etree.SubElement(ln2, '{%s}noFill' % A)
    sf2  = etree.SubElement(rPr, '{%s}solidFill' % A)
    etree.SubElement(sf2, '{%s}srgbClr' % A).set('val', 'FEFFFF')
    etree.SubElement(rPr, '{%s}effectLst' % A)
    lat2 = etree.SubElement(rPr, '{%s}latin' % A)
    lat2.set('typeface', 'Calibri'); lat2.set('panose', '020F0502020204030204')
    t_el = etree.SubElement(r_el, '{%s}t' % A)
    t_el.text = label

    return sp


def make_description_box(fase_index: int, x: int, w: int) -> etree._Element:
    """Create a dashed description box below a chevron."""
    accent = ACCENT_COLOURS[min(fase_index, len(ACCENT_COLOURS) - 1)]
    sp = etree.Element('{%s}sp' % P)

    nvSpPr = etree.SubElement(sp, '{%s}nvSpPr' % P)
    cNvPr  = etree.SubElement(nvSpPr, '{%s}cNvPr' % P)
    cNvPr.set('id', str(200 + fase_index))
    cNvPr.set('name', f'Rectangle {200 + fase_index}')
    etree.SubElement(nvSpPr, '{%s}cNvSpPr' % P)
    etree.SubElement(nvSpPr, '{%s}nvPr' % P)

    spPr = etree.SubElement(sp, '{%s}spPr' % P)
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % A)
    off  = etree.SubElement(xfrm, '{%s}off' % A)
    off.set('x', str(x)); off.set('y', str(BOX_Y))
    ext  = etree.SubElement(xfrm, '{%s}ext' % A)
    ext.set('cx', str(w)); ext.set('cy', str(BOX_HEIGHT))
    prst = etree.SubElement(spPr, '{%s}prstGeom' % A)
    prst.set('prst', 'rect')
    etree.SubElement(prst, '{%s}avLst' % A)
    etree.SubElement(spPr, '{%s}noFill' % A)
    ln   = etree.SubElement(spPr, '{%s}ln' % A)
    ln.set('w', '19050')
    sf   = etree.SubElement(ln, '{%s}solidFill' % A)
    etree.SubElement(sf, '{%s}schemeClr' % A).set('val', accent)
    etree.SubElement(ln, '{%s}prstDash' % A).set('val', 'sysDash')

    style = etree.SubElement(sp, '{%s}style' % P)
    for tag, idx_val in [('lnRef', '2'), ('fillRef', '1'), ('effectRef', '0'), ('fontRef', 'minor')]:
        ref = etree.SubElement(style, '{%s}%s' % (A, tag))
        ref.set('idx', idx_val)
        sc  = etree.SubElement(ref, '{%s}schemeClr' % A)
        sc.set('val', 'lt1' if tag == 'fontRef' else 'accent1')
        if tag == 'lnRef':
            etree.SubElement(sc, '{%s}shade' % A).set('val', '50000')

    txBody = etree.SubElement(sp, '{%s}txBody' % P)
    bodyPr = etree.SubElement(txBody, '{%s}bodyPr' % A)
    bodyPr.set('rtlCol', '0'); bodyPr.set('anchor', 't')
    bodyPr.set('anchorCtr', '0'); bodyPr.set('overflow', 'clip')
    etree.SubElement(txBody, '{%s}lstStyle' % A)
    p_el = etree.SubElement(txBody, '{%s}p' % A)
    pPr  = etree.SubElement(p_el, '{%s}pPr' % A)
    pPr.set('algn', 'just')
    r_el = etree.SubElement(p_el, '{%s}r' % A)
    rPr  = etree.SubElement(r_el, '{%s}rPr' % A)
    rPr.set('lang', 'nl-NL'); rPr.set('sz', '1200')
    sf2  = etree.SubElement(rPr, '{%s}solidFill' % A)
    etree.SubElement(sf2, '{%s}schemeClr' % A).set('val', 'tx1')
    lat  = etree.SubElement(rPr, '{%s}latin' % A)
    lat.set('typeface', 'Lato Light')
    lat.set('panose', '020F0502020204030203')
    lat.set('pitchFamily', '34'); lat.set('charset', '0')
    etree.SubElement(r_el, '{%s}t' % A).text = f'[Beschrijving fase {fase_index + 1}]'

    return sp


# ── Main ─────────────────────────────────────────────────────────────────────

def reflow_chevrons(unpacked_dir: Path, n_fases: int) -> None:
    slide_path = unpacked_dir / 'ppt' / 'slides' / 'slide6.xml'
    if not slide_path.exists():
        print(f'Error: {slide_path} not found', file=sys.stderr)
        sys.exit(1)

    tree = etree.parse(str(slide_path))
    root = tree.getroot()
    spTree = root.find('.//{%s}spTree' % P)

    w = chevron_width(n_fases)
    xs = [chevron_x(i, w) for i in range(n_fases)]

    # ── Collect existing chevrons and description boxes (sorted left to right) ──
    chevrons  = sorted(
        [sp for sp in spTree if is_chevron_shape(sp)],
        key=lambda sp: get_shape_x(sp) or 0,
    )
    desc_boxes = sorted(
        [sp for sp in spTree if is_description_box(sp)],
        key=lambda sp: get_shape_x(sp) or 0,
    )
    timeline_labels = [sp for sp in spTree if is_timeline_label(sp)]

    existing = len(chevrons)
    print(f'Found {existing} existing chevron(s), {len(desc_boxes)} description box(es).')
    print(f'Reflowing to {n_fases} fases — chevron width: {w} EMU')

    # ── Update existing chevrons ──
    for i, sp in enumerate(chevrons):
        xfrm = get_xfrm(sp)
        set_off_ext(xfrm, x=xs[i], cx=w)
        print(f'  Chevron {i+1}: x={xs[i]}, cx={w}')

    # ── Update existing description boxes ──
    for i, sp in enumerate(desc_boxes):
        xfrm = get_xfrm(sp)
        set_off_ext(xfrm, x=xs[i], cx=w)
        # Ensure overflow=clip on bodyPr
        bodyPr = sp.find('.//{%s}bodyPr' % A)
        if bodyPr is not None:
            bodyPr.set('overflow', 'clip')
        print(f'  Box {i+1}: x={xs[i]}, cx={w}')

    # ── Add missing chevrons and boxes ──
    for i in range(existing, n_fases):
        label = f'FASE {i+1}: [NAAM FASE]'
        new_chevron = make_chevron_sp(i, xs[i], w, label)
        new_box     = make_description_box(i, xs[i], w)
        spTree.append(new_chevron)
        spTree.append(new_box)
        print(f'  Added chevron {i+1} and description box at x={xs[i]}')

    # ── Reposition timeline labels ──
    # Timeline labels are sorted left to right; reassign to chevron centres
    centres = [xs[i] + w // 2 for i in range(n_fases)]
    for i, sp in enumerate(sorted(timeline_labels, key=lambda s: get_shape_x(s) or 0)):
        if i < n_fases:
            xfrm = get_xfrm(sp)
            if xfrm is not None:
                off = xfrm.find('{%s}off' % A)
                ext = xfrm.find('{%s}ext' % A)
                if off is not None and ext is not None:
                    label_w = int(ext.get('cx', 1376482))
                    off.set('x', str(centres[i] - label_w // 2))
                    print(f'  Timeline label {i+1}: centred at x={centres[i]}')

    tree.write(str(slide_path), xml_declaration=True, encoding='UTF-8', standalone=True)
    print(f'\nDone. slide6.xml updated for {n_fases} fases.')
    print('Next: edit slide6.xml to set the correct chevron labels, descriptions, and timeline text.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reflow chevrons on slide 6 of an SFNL offerte.')
    parser.add_argument('unpacked_dir', type=Path, help='Path to the unpacked PPTX directory')
    parser.add_argument('--fases', type=int, required=True, choices=[3, 4, 5, 6],
                        help='Number of fases to lay out')
    args = parser.parse_args()

    if not args.unpacked_dir.exists():
        print(f'Error: {args.unpacked_dir} not found', file=sys.stderr)
        sys.exit(1)

    reflow_chevrons(args.unpacked_dir, args.fases)
