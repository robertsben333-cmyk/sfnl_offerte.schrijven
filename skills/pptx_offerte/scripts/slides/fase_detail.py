"""PPTX fase_detail slide — two-column layout with actions left, doel/aanpak right."""
from pptx import Presentation
from pptx.util import Pt
from skills.pptx_offerte.scripts.slides._utils import STYLE, ACCENT_MAP, hex_color as _hex, blank_layout


def add_slide(prs: Presentation, content: dict) -> None:
    """
    Add a fase detail slide.

    content keys:
      number (int): Phase number
      naam (str): Phase name
      klant (str): Client name for "Acties [klant]" label
      doel (str): Phase goal
      aanpak (str): Approach description
      acties_sfnl (list[str]): SFNL actions
      acties_klant (list[str]): Client actions
      deliverable (str): Deliverable description
      dagen (int): Number of days
      tijdlijn (str): Timeline string
      proposition (str): Proposition id
    """
    W = prs.slide_width
    H = prs.slide_height
    slide = prs.slides.add_slide(blank_layout(prs))

    proposition = content.get("proposition", "mbc")
    accent = _hex(ACCENT_MAP.get(proposition, "accent_mbc"))
    primary = _hex("primary")
    white = _hex("white")

    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = white

    number = content.get("number", "")
    naam = content.get("naam", "")

    # Title
    tf = slide.shapes.add_textbox(int(W * 0.036), int(H * 0.08), int(W * 0.939), int(H * 0.049))
    p = tf.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = f"{number}. {naam}" if number else naam
    run.font.name = STYLE["fonts"]["heading"]
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = primary

    # Subtitle: "AANPAK FASE N"
    tf = slide.shapes.add_textbox(int(W * 0.036), int(H * 0.138), int(W * 0.939), int(H * 0.083))
    p = tf.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = f"AANPAK FASE {number}" if number else "AANPAK"
    run.font.name = STYLE["fonts"]["body"]
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = accent

    # Column layout
    col_top = int(H * 0.26)
    left_w = int(W * 0.32)
    right_left = int(W * 0.37)
    right_w = int(W * 0.60)
    left_left = int(W * 0.036)
    row_h = int(H * 0.04)  # label height
    body_h = int(H * 0.08)  # body text height

    # --- LEFT COLUMN ---
    cursor = col_top

    def add_label_and_body(label_text, body_text, is_list=False):
        nonlocal cursor
        # Label
        tf = slide.shapes.add_textbox(left_left, cursor, left_w, row_h)
        p = tf.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = label_text
        run.font.name = STYLE["fonts"]["body"]
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.color.rgb = accent
        cursor += row_h

        # Body
        items = body_text if is_list else [body_text]
        h = max(row_h, row_h * len(items)) if is_list else body_h
        tf = slide.shapes.add_textbox(left_left, cursor, left_w, h)
        tf.text_frame.word_wrap = True
        for j, item in enumerate(items):
            if j == 0:
                p = tf.text_frame.paragraphs[0]
            else:
                p = tf.text_frame.add_paragraph()
            run = p.add_run()
            run.text = f"• {item}" if is_list else item
            run.font.name = STYLE["fonts"]["body"]
            run.font.size = Pt(9)
            run.font.color.rgb = primary
        cursor += h + int(H * 0.01)

    acties_sfnl = content.get("acties_sfnl", [])
    add_label_and_body("ACTIES SOCIAL FINANCE NL", acties_sfnl, is_list=True)

    klant = content.get("klant", "KLANT")
    acties_klant = content.get("acties_klant", [])
    add_label_and_body(f"ACTIES {klant.upper()}", acties_klant, is_list=True)

    deliverable = content.get("deliverable", "")
    add_label_and_body("DELIVERABLE", deliverable)

    tijdlijn = content.get("tijdlijn", "")
    add_label_and_body("TIJDLIJN", str(tijdlijn))

    dagen = content.get("dagen", "")
    add_label_and_body("DAGDELEN", str(dagen))

    # --- RIGHT COLUMN ---
    right_cursor = col_top

    def add_right_section(label_text, body_text):
        nonlocal right_cursor
        tf = slide.shapes.add_textbox(right_left, right_cursor, right_w, row_h)
        p = tf.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = label_text
        run.font.name = STYLE["fonts"]["heading"]
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = accent
        right_cursor += row_h

        content_h = int(H * 0.22)
        tf = slide.shapes.add_textbox(right_left, right_cursor, right_w, content_h)
        tf.text_frame.word_wrap = True
        p = tf.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = body_text
        run.font.name = STYLE["fonts"]["body"]
        run.font.size = Pt(10)
        run.font.color.rgb = primary
        right_cursor += content_h + int(H * 0.02)

    add_right_section("DOEL", content.get("doel", ""))
    add_right_section("AANPAK", content.get("aanpak", ""))
