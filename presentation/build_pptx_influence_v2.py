"""Build PPTX (v2) for 'Social Media Influence on People' — editorial style."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Inches, Pt

OUT = Path(__file__).parent / "social_media_influence_v2.pptx"

# Editorial / magazine palette — warm neutrals + bold coral accent
CREAM = RGBColor(0xF5, 0xEF, 0xE6)       # background
PAPER = RGBColor(0xFA, 0xF6, 0xF0)       # cards
INK = RGBColor(0x1B, 0x1B, 0x1B)         # main text
SUBINK = RGBColor(0x55, 0x55, 0x55)      # muted
CORAL = RGBColor(0xF2, 0x5F, 0x4C)       # accent
OLIVE = RGBColor(0x6B, 0x7A, 0x3A)       # secondary
TERRACOTTA = RGBColor(0xC9, 0x6F, 0x4A)  # support
NAVY = RGBColor(0x1C, 0x2A, 0x3A)        # dark accent
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

# Photo-placeholder palette (warm shades, look like Pexels muted photos)
PH1 = RGBColor(0xD9, 0xC4, 0xA6)
PH2 = RGBColor(0xB4, 0x99, 0x7A)
PH3 = RGBColor(0x88, 0x6C, 0x52)
PH4 = RGBColor(0xC9, 0x6F, 0x4A)
PH5 = RGBColor(0x6B, 0x7A, 0x3A)

HEAD_FONT = "DM Serif Display"   # serif, editorial feel
ALT_FONT = "Playfair Display"     # fallback serif
BODY_FONT = "Inter"
TAG_FONT = "Inter"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def add_slide(bg=CREAM):
    slide = prs.slides.add_slide(BLANK)
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg_shape.line.fill.background()
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = bg
    bg_shape.shadow.inherit = False
    return slide


def add_text(slide, left, top, width, height, text, *,
             font=BODY_FONT, size=18, color=INK, bold=False,
             italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             line_spacing=None, letter_spacing=None):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    tf.vertical_anchor = anchor
    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            p.line_spacing = line_spacing
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color
    return box


def add_rect(slide, left, top, width, height, fill, line=None, radius=0.0):
    if radius > 0:
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.adjustments[0] = radius
    else:
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    shape.shadow.inherit = False
    return shape


def add_circle(slide, cx, cy, r, fill, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - r, cy - r, r * 2, r * 2)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1.5)
    shape.shadow.inherit = False
    return shape


def add_line(slide, x1, y1, x2, y2, color=INK, weight=1.0):
    shape = slide.shapes.add_connector(1, x1, y1, x2, y2)
    shape.line.color.rgb = color
    shape.line.width = Pt(weight)
    return shape


def add_photo_placeholder(slide, left, top, width, height, color=PH2, label="PHOTO"):
    """A flat rectangle that visually marks where to drop a real photo in Canva/PPT."""
    add_rect(slide, left, top, width, height, color)
    # tiny image icon and label
    add_text(slide, left, top + height / 2 - Inches(0.3), width, Inches(0.4),
             "◳", font=BODY_FONT, size=28, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, left, top + height / 2 + Inches(0.1), width, Inches(0.3),
             label, font=TAG_FONT, size=10, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def add_chapter_tag(slide, top, num, label, color=CORAL):
    """Editorial chapter tag: 01 — LABEL with a horizontal rule."""
    add_text(slide, Inches(0.7), top, Inches(1.0), Inches(0.3),
             num, font=TAG_FONT, size=12, color=color, bold=True)
    add_line(slide, Inches(1.4), top + Inches(0.18), Inches(2.4), top + Inches(0.18),
             color=color, weight=1.0)
    add_text(slide, Inches(2.55), top, Inches(8), Inches(0.3),
             label, font=TAG_FONT, size=12, color=color, bold=True)


def add_footer(slide, page, total=10):
    add_line(slide, Inches(0.7), SH - Inches(0.55), SW - Inches(0.7), SH - Inches(0.55),
             color=SUBINK, weight=0.5)
    add_text(slide, Inches(0.7), SH - Inches(0.45), Inches(8), Inches(0.3),
             "Social Media Influence on People  ·  Anastasia Mogileva  ·  2026",
             size=10, color=SUBINK)
    add_text(slide, SW - Inches(2), SH - Inches(0.45), Inches(1.4), Inches(0.3),
             f"— {page:02d} —", size=10, color=SUBINK, align=PP_ALIGN.RIGHT)


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# =========================================================== SLIDE 1 — COVER
s = add_slide()
# Left half: photo placeholder
add_photo_placeholder(s, Inches(0), Inches(0), Inches(6.0), SH,
                      color=PH3, label="HERO PHOTO\n(suggest: hands holding phone)")
# Right half: editorial cover text
add_text(s, Inches(6.7), Inches(0.8), Inches(6), Inches(0.4),
         "FINAL PROJECT  ·  2026", font=TAG_FONT, size=12, color=CORAL, bold=True)
add_line(s, Inches(6.7), Inches(1.3), Inches(8.5), Inches(1.3), color=CORAL, weight=1.0)

add_text(s, Inches(6.7), Inches(1.6), Inches(6.3), Inches(3.8),
         "Social\nMedia\nInfluence\non People.",
         font=HEAD_FONT, size=64, color=INK, line_spacing=0.95)

add_text(s, Inches(6.7), Inches(5.6), Inches(6), Inches(0.5),
         "An essay in ten slides on\nlikes, lives, and limits.",
         font=BODY_FONT, size=14, color=SUBINK, italic=True)
add_text(s, Inches(6.7), Inches(6.4), Inches(6), Inches(0.4),
         "by Anastasia Mogileva",
         font=BODY_FONT, size=12, color=INK, bold=True)
add_text(s, Inches(6.7), Inches(6.7), Inches(6), Inches(0.4),
         "University · Faculty · Year",
         font=BODY_FONT, size=11, color=SUBINK)
add_notes(s, (
    "Hello everyone. My name is Anastasia. Today I will speak about social media and how it "
    "influences our life. Almost every person uses social media every day. In my presentation, "
    "I will show the good sides, the bad sides, and how to stay safe online."
))

# =========================================================== SLIDE 2 — WHAT IT IS
s = add_slide()
add_chapter_tag(s, Inches(0.6), "01", "WHAT IT IS")
add_text(s, Inches(0.7), Inches(1.2), Inches(11), Inches(1.4),
         "What is social media,\nreally?",
         font=HEAD_FONT, size=44, color=INK, line_spacing=1.0)

# Pull quote on the left
add_rect(s, Inches(0.7), Inches(3.4), Inches(6.5), Inches(3.2), PAPER, radius=0.02)
add_text(s, Inches(1.0), Inches(3.6), Inches(0.6), Inches(0.6),
         "“", font=HEAD_FONT, size=56, color=CORAL)
add_text(s, Inches(1.0), Inches(4.0), Inches(6.0), Inches(2.0),
         "Websites and apps that help\npeople share photos, videos\nand ideas online.",
         font=HEAD_FONT, size=22, color=INK, line_spacing=1.2)
add_text(s, Inches(1.0), Inches(6.0), Inches(6.0), Inches(0.4),
         "— short definition for everyone",
         font=BODY_FONT, size=11, color=SUBINK, italic=True)

# Stat block on the right
add_rect(s, Inches(7.5), Inches(3.4), Inches(5.2), Inches(3.2), NAVY)
add_text(s, Inches(7.5), Inches(3.6), Inches(5.2), Inches(0.4),
         "USERS WORLDWIDE",
         font=TAG_FONT, size=11, color=CORAL, bold=True, align=PP_ALIGN.CENTER)
add_text(s, Inches(7.5), Inches(4.1), Inches(5.2), Inches(2.0),
         "5.2 B",
         font=HEAD_FONT, size=110, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(7.5), Inches(6.1), Inches(5.2), Inches(0.4),
         "people online · Statista, 2024",
         font=BODY_FONT, size=12, color=PH1, align=PP_ALIGN.CENTER)

add_footer(s, 2)
add_notes(s, (
    "So, what is social media? Social media are websites and apps that help people talk to each "
    "other online. We share photos, videos, and ideas. Today, more than five billion people in "
    "the world use social media. It is the most popular activity on the phone."
))

# =========================================================== SLIDE 3 — PLATFORMS
s = add_slide()
add_chapter_tag(s, Inches(0.6), "02", "THE BIG FOUR")
add_text(s, Inches(0.7), Inches(1.2), Inches(11), Inches(1.4),
         "The four platforms\neveryone knows.",
         font=HEAD_FONT, size=40, color=INK, line_spacing=1.0)

# 4 long horizontal "magazine rows"
rows = [
    ("01", "TikTok",    "Short fun videos and dances.",           "1.5 B users", CORAL),
    ("02", "Instagram", "Photos, Stories and Reels.",             "2.0 B users", TERRACOTTA),
    ("03", "YouTube",   "Videos for every topic, big and small.", "2.5 B users", OLIVE),
    ("04", "Facebook",  "News, family and groups.",                "3.0 B users", NAVY),
]
row_h = Inches(0.78)
row_top = Inches(3.0)
for i, (num, name, desc, users, color) in enumerate(rows):
    y = row_top + (row_h + Inches(0.12)) * i
    add_line(s, Inches(0.7), y, Inches(12.6), y, color=SUBINK, weight=0.4)
    add_text(s, Inches(0.7), y + Inches(0.18), Inches(0.7), Inches(0.5),
             num, font=BODY_FONT, size=14, color=color, bold=True)
    add_text(s, Inches(1.5), y + Inches(0.13), Inches(2.5), Inches(0.6),
             name, font=HEAD_FONT, size=22, color=INK)
    add_text(s, Inches(4.5), y + Inches(0.22), Inches(6.0), Inches(0.5),
             desc, font=BODY_FONT, size=14, color=SUBINK)
    add_text(s, Inches(10.5), y + Inches(0.22), Inches(2.2), Inches(0.5),
             users, font=BODY_FONT, size=13, color=color, bold=True, align=PP_ALIGN.RIGHT)
# bottom line
add_line(s, Inches(0.7), row_top + (row_h + Inches(0.12)) * 4,
         Inches(12.6), row_top + (row_h + Inches(0.12)) * 4, color=SUBINK, weight=0.4)

add_footer(s, 3)
add_notes(s, (
    "There are many social media platforms, but four are the most popular. TikTok is famous for "
    "short fun videos. Instagram is about photos, stories, and Reels. YouTube has videos for "
    "every topic. Facebook is more popular with older people and family groups."
))

# =========================================================== SLIDE 4 — POSITIVE INFLUENCE
s = add_slide()
add_chapter_tag(s, Inches(0.6), "03", "THE BRIGHT SIDE", color=OLIVE)
add_text(s, Inches(0.7), Inches(1.2), Inches(11), Inches(1.4),
         "Why we love it.",
         font=HEAD_FONT, size=44, color=INK)

# Magazine: image left, list right
add_photo_placeholder(s, Inches(0.7), Inches(3.0), Inches(5.0), Inches(3.8),
                      color=PH5, label="PHOTO\n(friends laughing with phone)")
add_text(s, Inches(0.7), Inches(6.9), Inches(5.0), Inches(0.4),
         "Photo: friends connecting online.",
         font=BODY_FONT, size=10, color=SUBINK, italic=True)

items = [
    ("Family & friends", "Stay close from any country."),
    ("Free information",  "News and ideas in seconds."),
    ("Same hobbies",      "Find your community fast."),
    ("Support",            "Help in difficult moments."),
    ("Business",           "Jobs and new opportunities."),
]
ix = Inches(6.2)
iy = Inches(3.0)
for i, (h, sub) in enumerate(items):
    y = iy + Inches(0.78) * i
    # number
    add_text(s, ix, y, Inches(0.6), Inches(0.4),
             f"0{i+1}", font=BODY_FONT, size=12, color=OLIVE, bold=True)
    add_text(s, ix + Inches(0.7), y - Inches(0.05), Inches(3.0), Inches(0.5),
             h, font=HEAD_FONT, size=18, color=INK)
    add_text(s, ix + Inches(3.7), y, Inches(3.0), Inches(0.5),
             sub, font=BODY_FONT, size=13, color=SUBINK)

add_footer(s, 4)
add_notes(s, (
    "Social media has many positive sides. We can stay in touch with our family and friends in "
    "other countries — for free. We get news very fast. We can find people who love the same "
    "things. And many people use social media to find a new job or to start a small business."
))

# =========================================================== SLIDE 5 — COMMUNICATION & EDUCATION
s = add_slide()
add_chapter_tag(s, Inches(0.6), "04", "COMMUNICATION + EDUCATION", color=OLIVE)
add_text(s, Inches(0.7), Inches(1.2), Inches(11), Inches(1.4),
         "A free classroom\nin your pocket.",
         font=HEAD_FONT, size=40, color=INK, line_spacing=1.0)

# Big colored stat block — landscape
add_rect(s, Inches(0.7), Inches(3.2), Inches(7.5), Inches(3.6), OLIVE)
add_text(s, Inches(1.0), Inches(3.4), Inches(7), Inches(0.4),
         "TEENS WHO LEARN ON YOUTUBE EVERY WEEK",
         font=TAG_FONT, size=11, color=PH1, bold=True)
add_text(s, Inches(1.0), Inches(3.9), Inches(7.0), Inches(2.5),
         "83%",
         font=HEAD_FONT, size=160, color=WHITE,
         anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(1.0), Inches(6.3), Inches(7), Inches(0.4),
         "Pew Research, 2023",
         font=BODY_FONT, size=12, color=PH1, italic=True)

# Right column: bullets in editorial style
right_x = Inches(8.7)
add_text(s, right_x, Inches(3.2), Inches(4), Inches(0.5),
         "What changed",
         font=BODY_FONT, size=12, color=CORAL, bold=True)
add_line(s, right_x, Inches(3.55), right_x + Inches(2.0), Inches(3.55), color=CORAL, weight=1.0)

bullets = [
    "Free video calls with anyone, anywhere.",
    "Practice English with native speakers.",
    "Tutorials for almost every subject.",
    "Online study groups in Telegram and Reels.",
    "Quick help with homework from a community.",
]
for i, b in enumerate(bullets):
    y = Inches(3.75) + Inches(0.55) * i
    add_text(s, right_x, y, Inches(0.3), Inches(0.4),
             "—", font=BODY_FONT, size=14, color=OLIVE, bold=True)
    add_text(s, right_x + Inches(0.4), y, Inches(4.0), Inches(0.5),
             b, font=BODY_FONT, size=13, color=INK)

add_footer(s, 5)
add_notes(s, (
    "Social media also changed how we study. We can speak with people from another country in "
    "seconds. YouTube has free lessons about almost everything. Many students create study "
    "groups online. Learning is not only in the classroom anymore."
))

# =========================================================== SLIDE 6 — NEGATIVE INFLUENCE
s = add_slide()
add_chapter_tag(s, Inches(0.6), "05", "THE DARK SIDE", color=CORAL)
add_text(s, Inches(0.7), Inches(1.2), Inches(11), Inches(1.4),
         "But every coin\nhas two sides.",
         font=HEAD_FONT, size=42, color=INK, line_spacing=1.0)

# Five small editorial cards
items = [
    ("Too much screen time", "Hours every day, every week."),
    ("Fake news & rumors",   "Spread in minutes, not days."),
    ("Cyberbullying",         "Aggression in the comments."),
    ("Privacy",                "Our data is the product."),
    ("Pressure to be perfect", "Filtered lives, real anxiety."),
]
card_w = Inches(2.35)
card_h = Inches(3.2)
gap = Inches(0.18)
total_w = card_w * 5 + gap * 4
start = (SW - total_w) / 2
top = Inches(3.4)
for i, (h, sub) in enumerate(items):
    left = start + (card_w + gap) * i
    add_rect(s, left, top, card_w, card_h, PAPER, radius=0.04)
    add_rect(s, left, top, Inches(0.15), card_h, CORAL)
    add_text(s, left + Inches(0.3), top + Inches(0.5), card_w - Inches(0.4), Inches(0.5),
             f"0{i+1}", font=BODY_FONT, size=12, color=CORAL, bold=True)
    add_text(s, left + Inches(0.3), top + Inches(1.0), card_w - Inches(0.4), Inches(1.4),
             h, font=HEAD_FONT, size=18, color=INK, line_spacing=1.1)
    add_text(s, left + Inches(0.3), top + Inches(2.3), card_w - Inches(0.4), Inches(0.9),
             sub, font=BODY_FONT, size=12, color=SUBINK)

add_footer(s, 6)
add_notes(s, (
    "But social media also has serious negative sides. People spend too much time on the phone. "
    "We see a lot of fake news. In the comments, some users are aggressive — this is called "
    "cyberbullying. Social media also collects a lot of our personal data."
))

# =========================================================== SLIDE 7 — ADDICTION & SCREEN TIME
s = add_slide()
add_chapter_tag(s, Inches(0.6), "06", "SCREEN TIME", color=CORAL)
add_text(s, Inches(0.7), Inches(1.2), Inches(11), Inches(1.4),
         "The endless scroll.",
         font=HEAD_FONT, size=44, color=INK)

# Big stat on left
add_text(s, Inches(0.7), Inches(3.2), Inches(6.5), Inches(3.5),
         "2h\n30m",
         font=HEAD_FONT, size=180, color=CORAL,
         line_spacing=0.85, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.7), Inches(6.5), Inches(6.5), Inches(0.4),
         "average user · per day · GWI, 2024",
         font=BODY_FONT, size=13, color=SUBINK, italic=True)

# Right column: editorial facts
right_x = Inches(8.0)
add_text(s, right_x, Inches(3.0), Inches(4.5), Inches(0.5),
         "What's behind it",
         font=BODY_FONT, size=12, color=CORAL, bold=True)
add_line(s, right_x, Inches(3.35), right_x + Inches(2.0), Inches(3.35), color=CORAL, weight=1.0)

facts = [
    ("Teenagers", "up to 4–5 hours / day"),
    ("Dopamine loop", "endless scroll, small rewards"),
    ("Phone checks", "100+ times a day"),
    ("Most addictive", "TikTok & Instagram Reels"),
]
for i, (k, v) in enumerate(facts):
    y = Inches(3.7) + Inches(0.7) * i
    add_text(s, right_x, y, Inches(2.2), Inches(0.4),
             k, font=HEAD_FONT, size=18, color=INK)
    add_text(s, right_x + Inches(2.2), y + Inches(0.05), Inches(3.0), Inches(0.4),
             v, font=BODY_FONT, size=13, color=SUBINK)
    add_line(s, right_x, y + Inches(0.55), right_x + Inches(5.0), y + Inches(0.55),
             color=SUBINK, weight=0.3)

add_footer(s, 7)
add_notes(s, (
    "Many users spend more than two and a half hours on social media every day. For teenagers "
    "this number is higher — up to five hours. The endless scroll gives the brain small rewards, "
    "like a game. We check the phone more than one hundred times a day. This is a real form of "
    "digital addiction."
))

# =========================================================== SLIDE 8 — MENTAL HEALTH (dark slide)
s = add_slide(bg=NAVY)
# light chapter tag on dark
add_text(s, Inches(0.7), Inches(0.6), Inches(1.0), Inches(0.3),
         "07", font=TAG_FONT, size=12, color=CORAL, bold=True)
add_line(s, Inches(1.4), Inches(0.78), Inches(2.4), Inches(0.78), color=CORAL, weight=1.0)
add_text(s, Inches(2.55), Inches(0.6), Inches(8), Inches(0.3),
         "MENTAL HEALTH", font=TAG_FONT, size=12, color=CORAL, bold=True)

add_text(s, Inches(0.7), Inches(1.2), Inches(11), Inches(1.4),
         "Likes feel good.\nUntil they don't.",
         font=HEAD_FONT, size=42, color=WHITE, line_spacing=1.0)

# left: huge stat
add_text(s, Inches(0.7), Inches(3.4), Inches(6.5), Inches(3.0),
         "+27%",
         font=HEAD_FONT, size=200, color=CORAL,
         anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.7), Inches(6.5), Inches(6.5), Inches(0.4),
         "rise in teen depression, 2010–2020 · CDC, 2021",
         font=BODY_FONT, size=12, color=PH1, italic=True)

# right: bullets
right_x = Inches(8.0)
add_text(s, right_x, Inches(3.4), Inches(4.5), Inches(0.5),
         "Common effects",
         font=BODY_FONT, size=12, color=CORAL, bold=True)
add_line(s, right_x, Inches(3.75), right_x + Inches(2.0), Inches(3.75), color=CORAL, weight=1.0)
bullets = [
    "Higher risk of anxiety.",
    "More depression in teens.",
    "Low self-esteem from comparison.",
    "Sleep problems.",
    "FOMO — fear of missing out.",
]
for i, b in enumerate(bullets):
    y = Inches(4.0) + Inches(0.55) * i
    add_text(s, right_x, y, Inches(0.3), Inches(0.4),
             "—", font=BODY_FONT, size=14, color=CORAL, bold=True)
    add_text(s, right_x + Inches(0.4), y, Inches(4.5), Inches(0.5),
             b, font=BODY_FONT, size=14, color=WHITE)

# bottom rule + footer styled for dark
add_line(s, Inches(0.7), SH - Inches(0.55), SW - Inches(0.7), SH - Inches(0.55),
         color=PH1, weight=0.5)
add_text(s, Inches(0.7), SH - Inches(0.45), Inches(8), Inches(0.3),
         "Social Media Influence on People  ·  Anastasia Mogileva  ·  2026",
         size=10, color=PH1)
add_text(s, SW - Inches(2), SH - Inches(0.45), Inches(1.4), Inches(0.3),
         "— 08 —", size=10, color=PH1, align=PP_ALIGN.RIGHT)

add_notes(s, (
    "Many studies show that social media can harm our mental health. Teenagers who spend more "
    "than three hours a day on social media have a higher risk of depression and anxiety. We "
    "compare our real life to perfect photos and feel bad about ourselves. Many young people "
    "sleep less because they use the phone at night. This is called FOMO — fear of missing out."
))

# =========================================================== SLIDE 9 — SAFE USE
s = add_slide()
add_chapter_tag(s, Inches(0.6), "08", "TAKE CONTROL", color=OLIVE)
add_text(s, Inches(0.7), Inches(1.2), Inches(11), Inches(1.4),
         "Six small habits.",
         font=HEAD_FONT, size=44, color=INK)
add_text(s, Inches(0.7), Inches(2.5), Inches(11), Inches(0.4),
         "Tiny daily changes that bring back your attention.",
         font=BODY_FONT, size=14, color=SUBINK, italic=True)

# 2x3 editorial grid
tips = [
    ("01", "Set a daily time limit.",        "Every phone has this option."),
    ("02", "Turn off notifications.",        "They break your focus."),
    ("03", "Follow positive accounts.",      "Unfollow the rest."),
    ("04", "Protect your personal data.",    "Read what you share."),
    ("05", "Take a digital detox day.",      "One day a week, no phone."),
    ("06", "Don't scroll before sleep.",     "Use a book instead."),
]
card_w = Inches(4.0)
card_h = Inches(1.5)
gap_x = Inches(0.18)
gap_y = Inches(0.18)
start_left = Inches(0.7)
start_top = Inches(3.2)
for i, (num, h, sub) in enumerate(tips):
    col = i % 3
    row = i // 3
    left = start_left + (card_w + gap_x) * col
    top = start_top + (card_h + gap_y) * row
    add_rect(s, left, top, card_w, card_h, PAPER, radius=0.06)
    add_circle(s, left + Inches(0.45), top + Inches(0.45), Inches(0.25), OLIVE)
    add_text(s, left + Inches(0.2), top + Inches(0.2), Inches(0.6), Inches(0.5),
             num, font=BODY_FONT, size=11, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, left + Inches(0.9), top + Inches(0.2), card_w - Inches(1.0), Inches(0.5),
             h, font=HEAD_FONT, size=16, color=INK)
    add_text(s, left + Inches(0.9), top + Inches(0.75), card_w - Inches(1.0), Inches(0.7),
             sub, font=BODY_FONT, size=12, color=SUBINK)

add_footer(s, 9)
add_notes(s, (
    "The good news is that we can use social media in a smart way. Set a daily time limit, "
    "turn off notifications, follow accounts that inspire you. Don't share your personal data "
    "with everyone. Try one day per week without the phone — your mind will thank you."
))

# =========================================================== SLIDE 10 — CLOSING
s = add_slide()
# Left: huge serif "Thank you"
add_text(s, Inches(0.7), Inches(1.0), Inches(8.5), Inches(0.4),
         "CONCLUSION", font=TAG_FONT, size=12, color=CORAL, bold=True)
add_line(s, Inches(0.7), Inches(1.4), Inches(2.7), Inches(1.4), color=CORAL, weight=1.0)

add_text(s, Inches(0.7), Inches(1.8), Inches(8.5), Inches(3.0),
         "Thank you.",
         font=HEAD_FONT, size=110, color=INK)
add_text(s, Inches(0.7), Inches(4.6), Inches(8.5), Inches(2.0),
         ("Social media is a strong tool.\n"
          "It has good and bad sides.\n"
          "Balance is the answer."),
         font=HEAD_FONT, size=22, color=SUBINK, line_spacing=1.3)

add_text(s, Inches(0.7), Inches(6.5), Inches(8), Inches(0.4),
         "Anastasia Mogileva  ·  University · Faculty · 2026",
         font=BODY_FONT, size=11, color=SUBINK)

# Right: editorial sidebar
add_rect(s, Inches(9.5), Inches(0), Inches(3.833), SH, NAVY)
add_text(s, Inches(9.8), Inches(1.0), Inches(3.5), Inches(0.4),
         "QUESTIONS?", font=TAG_FONT, size=12, color=CORAL, bold=True)
add_line(s, Inches(9.8), Inches(1.4), Inches(11.0), Inches(1.4), color=CORAL, weight=1.0)
add_text(s, Inches(9.8), Inches(1.7), Inches(3.5), Inches(2.5),
         "I'm happy\nto answer.",
         font=HEAD_FONT, size=32, color=WHITE, line_spacing=1.0)
add_text(s, Inches(9.8), Inches(4.5), Inches(3.5), Inches(0.4),
         "PLATFORMS MENTIONED", font=TAG_FONT, size=10, color=CORAL, bold=True)
add_line(s, Inches(9.8), Inches(4.85), Inches(11.0), Inches(4.85), color=CORAL, weight=1.0)
add_text(s, Inches(9.8), Inches(5.0), Inches(3.5), Inches(1.5),
         "TikTok\nInstagram\nYouTube\nFacebook",
         font=BODY_FONT, size=14, color=WHITE, line_spacing=1.4)
add_notes(s, (
    "To conclude, social media is a very strong tool. It helps us learn, work, and stay "
    "connected, but it can also take our time and our energy. The most important thing is "
    "balance. If we use social media in a smart way, it gives more than it takes. Thank you for "
    "your attention. I will be happy to answer your questions."
))

prs.save(OUT)
print(f"Saved: {OUT}  ({OUT.stat().st_size // 1024} KB, {len(prs.slides)} slides)")
