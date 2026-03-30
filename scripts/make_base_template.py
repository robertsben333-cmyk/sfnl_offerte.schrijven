"""Strip SFNL template down to slide master + boilerplate slides (20+)."""
import os, sys
from pptx import Presentation

# Source: official SFNL branded template (28 slides; boilerplate starts at slide 20)
SRC = "SFNL template offerte.pptx"
DST = "skills/pptx-offerte/assets/sfnl_base.pptx"

# Number of content slides to strip (slides 1-19); only boilerplate (20-28) is kept
STRIP_COUNT = 19

if not os.path.exists(SRC):
    print(f"ERROR: source template not found: {SRC}", file=sys.stderr)
    print("Run this script from the project root directory.", file=sys.stderr)
    sys.exit(2)

prs = Presentation(SRC)

# python-pptx has no remove_slide; manipulate the XML sldIdLst directly.
# This leaves orphaned XML parts in the zip (known limitation) but produces a
# valid PPTX that PowerPoint handles correctly.
xml_slides = prs.slides._sldIdLst
slide_ids = list(xml_slides)

print(f"Total slides in source: {len(slide_ids)}")

for sldId in slide_ids[:STRIP_COUNT]:
    xml_slides.remove(sldId)

os.makedirs(os.path.dirname(DST), exist_ok=True)
prs.save(DST)
print(f"Base template saved to {DST}")
print(f"Slides remaining: {len(prs.slides)}")
