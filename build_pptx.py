"""Generate epstein_files_presentation.pptx from the talk content."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

BG       = RGBColor(0x0E, 0x0F, 0x13)
BG_CARD  = RGBColor(0x14, 0x16, 0x1D)
FG       = RGBColor(0xEE, 0xF0, 0xF5)
MUTED    = RGBColor(0x9A, 0xA3, 0xB2)
ACCENT   = RGBColor(0xE6, 0x39, 0x46)
ACCENT_2 = RGBColor(0xF1, 0xC4, 0x0F)
LINE     = RGBColor(0x2A, 0x2E, 0x39)
MYTH_BG  = RGBColor(0x2A, 0x14, 0x18)
TRUTH_BG = RGBColor(0x10, 0x24, 0x1B)
GREEN    = RGBColor(0x2E, 0xCC, 0x71)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
blank = prs.slide_layouts[6]


def paint_bg(slide, color=BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.line.fill.background()
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.shadow.inherit = False
    return bg


def add_text(slide, left, top, width, height, text, *,
             size=18, bold=False, color=FG, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, font="Calibri"):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        f = r.font
        f.name = font
        f.size = Pt(size)
        f.bold = bold
        f.color.rgb = color
    return tb


def add_eyebrow(slide, text):
    add_text(slide, Inches(0.7), Inches(0.6), Inches(12), Inches(0.4),
             text.upper(), size=14, bold=True, color=ACCENT)


def add_title(slide, text, size=44):
    add_text(slide, Inches(0.7), Inches(1.1), Inches(12), Inches(1.6),
             text, size=size, bold=True, color=FG)


def add_card(slide, left, top, width, height, fill=BG_CARD, border=LINE):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shp.adjustments[0] = 0.08
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    shp.line.color.rgb = border
    shp.line.width = Pt(0.75)
    shp.shadow.inherit = False
    return shp


def add_progress(slide, idx, total):
    bar_h = Emu(38100)
    slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, bar_h)\
        .fill.solid()
    full = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, int(SLIDE_W * idx / total), bar_h)
    full.line.fill.background()
    full.fill.solid()
    full.fill.fore_color.rgb = ACCENT


def add_counter(slide, idx, total):
    add_text(slide, Inches(11.5), Inches(7.05), Inches(1.5), Inches(0.35),
             f"{idx} / {total}", size=11, color=MUTED, align=PP_ALIGN.RIGHT)


SLIDES = []


def slide(fn):
    SLIDES.append(fn)
    return fn


@slide
def s_title(s):
    paint_bg(s)
    add_eyebrow(s, "Presentation")
    add_text(s, Inches(0.7), Inches(2.4), Inches(12), Inches(2),
             "The Epstein Files", size=72, bold=True, color=FG)
    add_text(s, Inches(0.7), Inches(4.6), Inches(12), Inches(1),
             "Documents, names, myths, and memes — what's actually inside.",
             size=22, color=MUTED)


@slide
def s_intro(s):
    paint_bg(s)
    add_eyebrow(s, "Introduction")
    add_title(s, "What are the Epstein Files?")
    add_text(s, Inches(0.7), Inches(3.0), Inches(12), Inches(1),
             "The \"Epstein Files\" are documents about the rich and notorious man Jeffrey Epstein.",
             size=22, color=FG)
    add_text(s, Inches(0.7), Inches(3.9), Inches(12), Inches(1),
             "The police released them to the public.",
             size=22, color=FG)


@slide
def s_part1(s):
    paint_bg(s)
    add_eyebrow(s, "Part 1")
    add_title(s, "What is it?")
    bullets = [
        "•  Epstein owned an island and a private plane.",
        "•  He did terrible things to women.",
        "•  He was arrested in 2019.",
        "•  He later died in prison.",
        "•  In 2026, the US government released 3.5 million pages: names, photos, phone numbers.",
    ]
    add_text(s, Inches(0.9), Inches(2.7), Inches(11.5), Inches(4),
             "\n".join(bullets), size=22, color=FG)


def celebrity_card(s, left, top, name, body):
    w, h = Inches(5.7), Inches(2.0)
    add_card(s, left, top, w, h)
    add_text(s, left + Inches(0.3), top + Inches(0.2), w - Inches(0.6), Inches(0.5),
             name, size=22, bold=True, color=ACCENT_2)
    add_text(s, left + Inches(0.3), top + Inches(0.8), w - Inches(0.6), h - Inches(1.0),
             body, size=16, color=FG)


@slide
def s_part2a(s):
    paint_bg(s)
    add_eyebrow(s, "Part 2 · Celebrities")
    add_title(s, "Which names appear in the files?")
    quote = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                               Inches(0.7), Inches(2.5), Inches(0.08), Inches(0.5))
    quote.line.fill.background()
    quote.fill.solid()
    quote.fill.fore_color.rgb = ACCENT
    add_text(s, Inches(0.95), Inches(2.5), Inches(11.5), Inches(0.5),
             "A name in the files ≠ a bad person. Maybe they just hung out.",
             size=16, color=MUTED)

    top1, top2 = Inches(3.2), Inches(5.3)
    celebrity_card(s, Inches(0.7), top1, "Trump",
                   "The name appears many times. He says: \"I didn't know about the bad stuff.\"")
    celebrity_card(s, Inches(6.9), top1, "Prince Andrew",
                   "A woman accused him. He lost his royal duties.")
    celebrity_card(s, Inches(0.7), top2, "Bill Clinton",
                   "Flew on Epstein's plane.")
    celebrity_card(s, Inches(6.9), top2, "Elon Musk",
                   "Asked about a party. Denies anything bad.")


@slide
def s_part2b(s):
    paint_bg(s)
    add_eyebrow(s, "Part 2 · Celebrities")
    add_title(s, "More names")
    celebrity_card(s, Inches(0.7), Inches(2.7), "Bill Gates",
                   "Epstein talked about him. Gates denies any wrongdoing.")
    celebrity_card(s, Inches(6.9), Inches(2.7), "Karina — a dentist from Belarus",
                   "Received a large sum of money after Epstein's death. Strange.")
    add_text(s, Inches(0.7), Inches(5.4), Inches(12), Inches(1),
             "Being mentioned doesn't equal being guilty — but it raises questions.",
             size=18, color=MUTED)


def myth_truth_pair(s, top, myth, truth):
    w = Inches(5.9)
    h = Inches(1.25)
    add_card(s, Inches(0.7), top, w, h, fill=MYTH_BG, border=ACCENT)
    add_text(s, Inches(0.9), top + Inches(0.12), w - Inches(0.4), Inches(0.32),
             "MYTH", size=11, bold=True, color=ACCENT)
    add_text(s, Inches(0.9), top + Inches(0.45), w - Inches(0.4), h - Inches(0.55),
             myth, size=15, color=FG)

    add_card(s, Inches(6.8), top, w, h, fill=TRUTH_BG, border=GREEN)
    add_text(s, Inches(7.0), top + Inches(0.12), w - Inches(0.4), Inches(0.32),
             "TRUTH", size=11, bold=True, color=GREEN)
    add_text(s, Inches(7.0), top + Inches(0.45), w - Inches(0.4), h - Inches(0.55),
             truth, size=15, color=FG)


@slide
def s_part3(s):
    paint_bg(s)
    add_eyebrow(s, "Part 3")
    add_title(s, "Myths and Truth")
    myth_truth_pair(s, Inches(2.6),
                    "There's a secret list of bad people.",
                    "No. The FBI hasn't found such a list.")
    myth_truth_pair(s, Inches(4.0),
                    "Epstein was murdered.",
                    "The police said it was suicide. But not everyone believes it.")
    myth_truth_pair(s, Inches(5.4),
                    "There's a secret \"pizza\" code in the files (an old rumor).",
                    "It's not true.")


def meme_card(s, top, title, body):
    h = Inches(1.3)
    add_card(s, Inches(0.7), top, Inches(12), h)
    add_text(s, Inches(0.95), top + Inches(0.15), Inches(11.5), Inches(0.4),
             title, size=18, bold=True, color=ACCENT_2)
    add_text(s, Inches(0.95), top + Inches(0.55), Inches(11.5), h - Inches(0.65),
             body, size=15, color=FG)


@slide
def s_part4a(s):
    paint_bg(s)
    add_eyebrow(s, "Part 4 · Internet Culture")
    add_title(s, "Epstein Memes")
    meme_card(s, Inches(2.6),
              "1. \"Epstein didn't kill himself\"",
              "The official version was \"suicide,\" but no one believes it. The meme implies he was killed to keep him quiet.")
    meme_card(s, Inches(4.0),
              "2. Epstein Island",
              "There were weird parties there. The joke: \"Let's go to the island?\" means \"Are you trying to get into trouble?\"")
    meme_card(s, Inches(5.4),
              "3. The Client List",
              "Everyone expected a list of the biggest names. But there was nothing. Meme: \"The rich hid the truth, as always.\"")


@slide
def s_part4b(s):
    paint_bg(s)
    add_eyebrow(s, "Part 4 · Internet Culture")
    add_title(s, "Why do people joke about this?")
    add_text(s, Inches(0.7), Inches(2.9), Inches(12), Inches(0.8),
             "It's dark humor. People are angry at the rich and powerful.",
             size=22, color=FG)

    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                             Inches(0.7), Inches(4.0), Inches(0.08), Inches(1.2))
    bar.line.fill.background()
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    add_text(s, Inches(0.95), Inches(4.0), Inches(11.5), Inches(1.2),
             "Memes are a way of saying: \"We remember everything\nand haven't forgiven anything.\"",
             size=20, color=MUTED)

    add_text(s, Inches(0.7), Inches(5.7), Inches(12), Inches(1),
             "Humor becomes the language of distrust toward institutions.",
             size=16, color=MUTED)


@slide
def s_conclusion(s):
    paint_bg(s)
    add_eyebrow(s, "Conclusion")
    add_title(s, "What does it all mean?")
    bullets = [
        "•  The \"Epstein Files\" aren't just one secret list — they're many old documents.",
        "•  They show that rich people helped each other.",
        "•  Some knew about the bad stuff but stayed silent.",
        "•  And memes about \"Epstein didn't kill himself\" will stay on the internet forever.",
    ]
    add_text(s, Inches(0.9), Inches(2.8), Inches(11.5), Inches(4),
             "\n".join(bullets), size=22, color=FG)


@slide
def s_end(s):
    paint_bg(s)
    add_eyebrow(s, "The End")
    add_text(s, Inches(0.7), Inches(2.6), Inches(12), Inches(2),
             "Thank you.", size=72, bold=True, color=FG)
    add_text(s, Inches(0.7), Inches(4.7), Inches(12), Inches(1),
             "Questions?", size=24, color=MUTED)


total = len(SLIDES)
for i, fn in enumerate(SLIDES, start=1):
    s = prs.slides.add_slide(blank)
    fn(s)
    add_progress(s, i, total)
    add_counter(s, i, total)

out = "/home/user/anastasia_mogileva_project/epstein_files_presentation.pptx"
prs.save(out)
print(f"saved: {out}")
