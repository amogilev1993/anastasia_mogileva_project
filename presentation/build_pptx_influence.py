"""Build the 10-slide PPTX for 'Social Media Influence on People'."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Inches, Pt

OUT = Path(__file__).parent / "social_media_influence.pptx"

# Brand palette
DARK = RGBColor(0x1E, 0x1E, 0x2E)
VIOLET = RGBColor(0x7C, 0x5C, 0xFF)
RED = RGBColor(0xFF, 0x6B, 0x6B)
GREEN = RGBColor(0x7B, 0xC4, 0x7F)
BG = RGBColor(0xF7, 0xF8, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x22, 0x28, 0x31)
MUTED = RGBColor(0x6B, 0x72, 0x80)

# Platform-ish colors (flat, not official)
TIKTOK = RGBColor(0x10, 0x10, 0x10)
TIKTOK_T = RGBColor(0x25, 0xF4, 0xEE)
INSTA = RGBColor(0xE1, 0x30, 0x6C)
YT = RGBColor(0xFF, 0x00, 0x33)
FB = RGBColor(0x18, 0x77, 0xF2)

HEAD_FONT = "Montserrat"
BODY_FONT = "Inter"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def add_slide(bg=BG):
    slide = prs.slides.add_slide(BLANK)
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg_shape.line.fill.background()
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = bg
    bg_shape.shadow.inherit = False
    return slide


def add_text(slide, left, top, width, height, text, *,
             font=BODY_FONT, size=18, color=TEXT, bold=False,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
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
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return box


def add_bullets(slide, left, top, width, height, items, *,
                size=20, color=TEXT, bullet_color=VIOLET, line_spacing=1.25):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(6)
        dot = p.add_run()
        dot.text = "•  "
        dot.font.name = BODY_FONT
        dot.font.size = Pt(size)
        dot.font.color.rgb = bullet_color
        dot.font.bold = True
        run = p.add_run()
        run.text = item
        run.font.name = BODY_FONT
        run.font.size = Pt(size)
        run.font.color.rgb = color
    return box


def add_rect(slide, left, top, width, height, fill, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.adjustments[0] = 0.12
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    shape.shadow.inherit = False
    return shape


def add_circle(slide, cx, cy, r, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - r, cy - r, r * 2, r * 2)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def add_accent_corner(slide, color=VIOLET):
    add_circle(slide, SW - Inches(0.5), Inches(0.5), Inches(1.6), color)


def add_footer(slide, page, total=10):
    add_text(slide, Inches(0.5), SH - Inches(0.4), Inches(6), Inches(0.3),
             "Social Media Influence on People",
             size=10, color=MUTED)
    add_text(slide, SW - Inches(2), SH - Inches(0.4), Inches(1.5), Inches(0.3),
             f"{page} / {total}", size=10, color=MUTED, align=PP_ALIGN.RIGHT)


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ---------------------------------------------------------------- SLIDE 1
s = add_slide(bg=WHITE)
add_circle(s, SW - Inches(0.2), SH - Inches(0.2), Inches(3.5), VIOLET)
add_circle(s, SW - Inches(0.2), SH - Inches(0.2), Inches(2.6), RGBColor(0xA9, 0x95, 0xFF))

add_text(s, Inches(0.7), Inches(1.2), Inches(8), Inches(0.5),
         "FINAL PROJECT  •  2026",
         font=BODY_FONT, size=14, color=VIOLET, bold=True)
add_text(s, Inches(0.7), Inches(1.8), Inches(11), Inches(2.7),
         "Social Media\nInfluence on People",
         font=HEAD_FONT, size=58, color=DARK, bold=True)
add_text(s, Inches(0.7), Inches(5.0), Inches(10), Inches(0.5),
         "Anastasia Mogileva  •  English Final Project",
         font=BODY_FONT, size=18, color=TEXT)
add_text(s, Inches(0.7), Inches(5.5), Inches(10), Inches(0.4),
         "TikTok  ·  Instagram  ·  YouTube  ·  Facebook",
         font=BODY_FONT, size=14, color=MUTED)
add_notes(s, (
    "Hello everyone. My name is Anastasia. Today I will speak about social media and how it "
    "influences our life. Almost every person uses social media every day. In my presentation, "
    "I will show the good sides, the bad sides, and how to stay safe online."
))

# ---------------------------------------------------------------- SLIDE 2
s = add_slide()
add_accent_corner(s)
add_text(s, Inches(0.7), Inches(0.6), Inches(10), Inches(0.4),
         "01  •  DEFINITION", size=12, color=VIOLET, bold=True)
add_text(s, Inches(0.7), Inches(1.0), Inches(12), Inches(1.0),
         "What Is Social Media?",
         font=HEAD_FONT, size=36, color=DARK, bold=True)

add_rect(s, Inches(0.7), Inches(2.4), Inches(6.5), Inches(4.0), WHITE)
add_text(s, Inches(1.0), Inches(2.7), Inches(6.0), Inches(1.4),
         "Websites and apps that help\npeople communicate online.",
         font=HEAD_FONT, size=22, color=DARK, bold=True)
add_bullets(s, Inches(1.0), Inches(4.2), Inches(6.0), Inches(2.0),
            ["People share photos, videos, ideas",
             "Free and easy to use",
             "The most popular activity on the phone"],
            size=16)

# Big stat card
add_rect(s, Inches(7.8), Inches(2.4), Inches(5.0), Inches(4.0), DARK)
add_text(s, Inches(7.8), Inches(2.7), Inches(5.0), Inches(0.6),
         "USERS WORLDWIDE",
         font=BODY_FONT, size=12, color=VIOLET, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(7.8), Inches(3.3), Inches(5.0), Inches(1.8),
         "5B+",
         font=HEAD_FONT, size=90, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(7.8), Inches(5.3), Inches(5.0), Inches(0.6),
         "people use social media (Statista, 2024)",
         font=BODY_FONT, size=13, color=MUTED,
         align=PP_ALIGN.CENTER)
add_footer(s, 2)
add_notes(s, (
    "So, what is social media? Social media are websites and apps that help people talk to each "
    "other online. We share photos, videos, and ideas with friends, and also with strangers. "
    "Today, more than five billion people in the world use social media. It is the most popular "
    "activity on the phone."
))

# ---------------------------------------------------------------- SLIDE 3
s = add_slide()
add_accent_corner(s)
add_text(s, Inches(0.7), Inches(0.6), Inches(10), Inches(0.4),
         "02  •  PLATFORMS", size=12, color=VIOLET, bold=True)
add_text(s, Inches(0.7), Inches(1.0), Inches(12), Inches(1.0),
         "Popular Social Media Platforms",
         font=HEAD_FONT, size=36, color=DARK, bold=True)

cards = [
    ("TikTok",    "Short fun videos",            "1.5B users",  TIKTOK, WHITE),
    ("Instagram", "Photos, Stories, Reels",      "2.0B users",  INSTA,  WHITE),
    ("YouTube",   "Videos for every topic",      "2.5B users",  YT,     WHITE),
    ("Facebook",  "News, family, groups",        "3.0B users",  FB,     WHITE),
]
card_w = Inches(2.8)
card_h = Inches(3.8)
gap = Inches(0.25)
top = Inches(2.5)
total_w = card_w * 4 + gap * 3
start_left = (SW - total_w) / 2
for i, (name, desc, users, color, text_color) in enumerate(cards):
    left = start_left + (card_w + gap) * i
    add_rect(s, left, top, card_w, card_h, color)
    # circular badge with first letter
    add_circle(s, left + Inches(0.7), top + Inches(0.7), Inches(0.4), WHITE)
    add_text(s, left + Inches(0.3), top + Inches(0.35), Inches(0.8), Inches(0.7),
             name[0], font=HEAD_FONT, size=22, color=color, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, left + Inches(0.3), top + Inches(1.4), card_w - Inches(0.6), Inches(0.6),
             name, font=HEAD_FONT, size=22, color=text_color, bold=True)
    add_text(s, left + Inches(0.3), top + Inches(2.0), card_w - Inches(0.6), Inches(1.2),
             desc, font=BODY_FONT, size=14, color=text_color)
    add_text(s, left + Inches(0.3), top + Inches(3.1), card_w - Inches(0.6), Inches(0.5),
             users, font=BODY_FONT, size=13, color=text_color, bold=True)
add_footer(s, 3)
add_notes(s, (
    "There are many social media platforms, but four are the most popular. TikTok is famous for "
    "short fun videos and dances. Instagram is about photos, stories, and Reels. YouTube has "
    "videos for every topic — from music to school lessons. Facebook is more popular with older "
    "people and family groups."
))

# ---------------------------------------------------------------- SLIDE 4
s = add_slide()
add_accent_corner(s, color=GREEN)
add_text(s, Inches(0.7), Inches(0.6), Inches(10), Inches(0.4),
         "03  •  THE GOOD SIDE", size=12, color=GREEN, bold=True)
add_text(s, Inches(0.7), Inches(1.0), Inches(12), Inches(1.0),
         "Positive Influence",
         font=HEAD_FONT, size=36, color=DARK, bold=True)

pos = [
    ("Family & friends", "Stay close from any country"),
    ("Free info", "News in seconds"),
    ("Same hobbies", "Find your community"),
    ("Support", "Help in difficult moments"),
    ("Business", "Jobs & new opportunities"),
]
card_w = Inches(2.4)
card_h = Inches(2.6)
gap = Inches(0.25)
top = Inches(2.5)
total_w = card_w * 5 + gap * 4
start_left = (SW - total_w) / 2
for i, (title, sub) in enumerate(pos):
    left = start_left + (card_w + gap) * i
    add_rect(s, left, top, card_w, card_h, WHITE)
    add_rect(s, left, top, card_w, Inches(0.15), GREEN)
    add_text(s, left + Inches(0.25), top + Inches(0.5), card_w - Inches(0.5), Inches(0.9),
             title, font=HEAD_FONT, size=16, color=DARK, bold=True)
    add_text(s, left + Inches(0.25), top + Inches(1.3), card_w - Inches(0.5), Inches(1.3),
             sub, font=BODY_FONT, size=12, color=MUTED)
add_text(s, Inches(0.7), Inches(5.7), Inches(12), Inches(0.6),
         "Example: many small businesses start on Instagram or TikTok.",
         font=BODY_FONT, size=16, color=TEXT)
add_footer(s, 4)
add_notes(s, (
    "Social media has many positive sides. First, we can stay in touch with our family and "
    "friends in other countries — for free. Second, we get news and information very fast. "
    "Third, we can find people who love the same things — music, sport, or art. And many people "
    "use social media to find a new job or to start a small business."
))

# ---------------------------------------------------------------- SLIDE 5
s = add_slide()
add_accent_corner(s, color=GREEN)
add_text(s, Inches(0.7), Inches(0.6), Inches(10), Inches(0.4),
         "04  •  COMMUNICATION & EDUCATION", size=12, color=GREEN, bold=True)
add_text(s, Inches(0.7), Inches(1.0), Inches(12), Inches(1.0),
         "Communication and Education",
         font=HEAD_FONT, size=36, color=DARK, bold=True)

add_bullets(s, Inches(0.7), Inches(2.5), Inches(7.0), Inches(4.0),
            [
                "Free video calls with anyone",
                "Practice foreign languages",
                "Learn from YouTube tutorials",
                "Online study groups & chats",
                "Quick help with homework",
            ],
            size=22, bullet_color=GREEN)

# Stat card on the right
add_rect(s, Inches(8.3), Inches(2.5), Inches(4.5), Inches(4.0), GREEN)
add_text(s, Inches(8.3), Inches(2.8), Inches(4.5), Inches(0.6),
         "TEENS WHO LEARN ON YOUTUBE",
         font=BODY_FONT, size=11, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(8.3), Inches(3.4), Inches(4.5), Inches(1.8),
         "83%",
         font=HEAD_FONT, size=110, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.3), Inches(5.4), Inches(4.5), Inches(0.8),
         "every week\n(Pew Research, 2023)",
         font=BODY_FONT, size=13, color=WHITE,
         align=PP_ALIGN.CENTER)
add_footer(s, 5)
add_notes(s, (
    "Social media also changed how we study. We can speak with people from another country in "
    "seconds and practice English or any other language. YouTube has free lessons about almost "
    "everything — math, programming, cooking. Many students create study groups on Telegram or "
    "Instagram. So, learning is not only in the classroom anymore."
))

# ---------------------------------------------------------------- SLIDE 6
s = add_slide()
add_accent_corner(s, color=RED)
add_text(s, Inches(0.7), Inches(0.6), Inches(10), Inches(0.4),
         "05  •  THE DARK SIDE", size=12, color=RED, bold=True)
add_text(s, Inches(0.7), Inches(1.0), Inches(12), Inches(1.0),
         "Negative Influence",
         font=HEAD_FONT, size=36, color=DARK, bold=True)

neg = [
    ("Too much screen time", "Hours every day"),
    ("Fake news & rumors", "Spreads very fast"),
    ("Cyberbullying", "Aggressive comments"),
    ("Privacy problems", "Personal data collected"),
    ("Perfect pictures", "Pressure to look great"),
]
card_w = Inches(2.4)
card_h = Inches(2.6)
gap = Inches(0.25)
top = Inches(2.5)
total_w = card_w * 5 + gap * 4
start_left = (SW - total_w) / 2
for i, (title, sub) in enumerate(neg):
    left = start_left + (card_w + gap) * i
    add_rect(s, left, top, card_w, card_h, WHITE)
    add_rect(s, left, top, card_w, Inches(0.15), RED)
    add_text(s, left + Inches(0.25), top + Inches(0.5), card_w - Inches(0.5), Inches(0.9),
             title, font=HEAD_FONT, size=15, color=DARK, bold=True)
    add_text(s, left + Inches(0.25), top + Inches(1.4), card_w - Inches(0.5), Inches(1.1),
             sub, font=BODY_FONT, size=12, color=MUTED)
add_footer(s, 6)
add_notes(s, (
    "But social media also has serious negative sides. Many people spend too much time on the "
    "phone every day. We see a lot of fake news and rumors. In the comments, some users are "
    "aggressive — this is called cyberbullying. Also, social media collects a lot of our "
    "personal data, and we often do not know how it is used."
))

# ---------------------------------------------------------------- SLIDE 7
s = add_slide()
add_accent_corner(s, color=RED)
add_text(s, Inches(0.7), Inches(0.6), Inches(10), Inches(0.4),
         "06  •  ADDICTION", size=12, color=RED, bold=True)
add_text(s, Inches(0.7), Inches(1.0), Inches(12), Inches(1.0),
         "Addiction and Screen Time",
         font=HEAD_FONT, size=36, color=DARK, bold=True)

add_bullets(s, Inches(0.7), Inches(2.5), Inches(7.0), Inches(4.0),
            [
                "Average user: 2h 30m / day",
                "Teenagers: up to 4–5 hours / day",
                "Endless scroll = dopamine loop",
                "Phone checked 100+ times a day",
                "TikTok & Reels — most addictive",
            ],
            size=20, bullet_color=RED)

# Big stat
add_rect(s, Inches(8.3), Inches(2.5), Inches(4.5), Inches(4.0), DARK)
add_text(s, Inches(8.3), Inches(2.8), Inches(4.5), Inches(0.6),
         "TIME ON SOCIAL MEDIA",
         font=BODY_FONT, size=11, color=VIOLET, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(8.3), Inches(3.4), Inches(4.5), Inches(1.8),
         "2h 30m",
         font=HEAD_FONT, size=70, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(8.3), Inches(5.4), Inches(4.5), Inches(0.8),
         "per day, global average\n(GWI, 2024)",
         font=BODY_FONT, size=13, color=WHITE,
         align=PP_ALIGN.CENTER)
add_footer(s, 7)
add_notes(s, (
    "Many users spend more than two and a half hours on social media every day. For teenagers, "
    "this number is even higher — up to five hours. The endless scroll gives the brain small "
    "rewards, like a game. We check the phone more than one hundred times every day, often "
    "without thinking. This is a real form of digital addiction."
))

# ---------------------------------------------------------------- SLIDE 8
s = add_slide(bg=DARK)
add_circle(s, SW - Inches(0.5), Inches(0.5), Inches(1.6), RED)
add_text(s, Inches(0.7), Inches(0.6), Inches(10), Inches(0.4),
         "07  •  WELL-BEING", size=12, color=RED, bold=True)
add_text(s, Inches(0.7), Inches(1.0), Inches(12), Inches(1.0),
         "Mental Health Problems",
         font=HEAD_FONT, size=36, color=WHITE, bold=True)

# Big stat on the left
add_text(s, Inches(0.7), Inches(2.5), Inches(6.0), Inches(3.0),
         "+27%",
         font=HEAD_FONT, size=160, color=RED, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_text(s, Inches(0.7), Inches(5.5), Inches(6.0), Inches(0.6),
         "depression in teens, 2010–2020 (CDC, 2021)",
         font=BODY_FONT, size=14, color=WHITE,
         align=PP_ALIGN.CENTER)

add_bullets(s, Inches(7.5), Inches(2.5), Inches(5.5), Inches(4.5),
            [
                "Higher risk of anxiety",
                "More depression in teens",
                "Low self-esteem (comparison)",
                "Sleep problems",
                "FOMO — fear of missing out",
            ],
            size=18, color=WHITE, bullet_color=RED)
add_footer(s, 8)
add_notes(s, (
    "Many studies show that social media can harm our mental health. Teenagers who spend more "
    "than three hours a day on social media have a higher risk of depression and anxiety. We "
    "compare our real life to perfect photos and feel bad about ourselves. Many young people "
    "also sleep less because they use the phone at night. This is called FOMO — fear of "
    "missing out."
))

# ---------------------------------------------------------------- SLIDE 9
s = add_slide()
add_accent_corner(s, color=GREEN)
add_text(s, Inches(0.7), Inches(0.6), Inches(10), Inches(0.4),
         "08  •  TAKE CONTROL", size=12, color=GREEN, bold=True)
add_text(s, Inches(0.7), Inches(1.0), Inches(12), Inches(1.0),
         "How to Use Social Media Safely",
         font=HEAD_FONT, size=36, color=DARK, bold=True)

tips = [
    "Set a daily TIME LIMIT",
    "Turn OFF push notifications",
    "Follow POSITIVE accounts",
    "Don't share personal data",
    "Take a DIGITAL DETOX day",
    "Don't scroll before sleep",
]
row_h = Inches(0.7)
top = Inches(2.4)
for i, tip in enumerate(tips):
    y = top + row_h * i + Inches(0.1) * i
    add_rect(s, Inches(0.7), y, Inches(8.5), row_h, WHITE)
    add_circle(s, Inches(1.1), y + Inches(0.35), Inches(0.22), GREEN)
    add_text(s, Inches(0.7), y, Inches(0.8), row_h, "✓",
             font=HEAD_FONT, size=18, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(1.6), y, Inches(7.5), row_h, tip,
             font=BODY_FONT, size=16, color=TEXT,
             anchor=MSO_ANCHOR.MIDDLE)

# Phone mock
add_rect(s, Inches(9.8), Inches(2.5), Inches(3.0), Inches(4.5), DARK)
add_rect(s, Inches(10.0), Inches(2.8), Inches(2.6), Inches(3.9), WHITE)
add_text(s, Inches(10.0), Inches(3.0), Inches(2.6), Inches(0.4),
         "SCREEN TIME", font=BODY_FONT, size=10, color=MUTED, bold=True,
         align=PP_ALIGN.CENTER)
add_text(s, Inches(10.0), Inches(3.6), Inches(2.6), Inches(1.4),
         "1 h", font=HEAD_FONT, size=60, color=DARK, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_rect(s, Inches(10.2), Inches(5.2), Inches(2.2), Inches(0.4), GREEN)
add_text(s, Inches(10.2), Inches(5.2), Inches(2.2), Inches(0.4),
         "Daily limit set",
         font=BODY_FONT, size=11, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
add_footer(s, 9)
add_notes(s, (
    "The good news is that we can use social media in a smart way. First, set a daily time "
    "limit — every phone has this option. Second, turn off notifications, because they break "
    "your focus. Third, follow accounts that inspire you, and unfollow the ones that make you "
    "feel bad. And try one day per week without the phone — your mind will thank you."
))

# ---------------------------------------------------------------- SLIDE 10
s = add_slide(bg=DARK)
add_circle(s, SW - Inches(0.2), SH - Inches(0.2), Inches(3.5), VIOLET)
add_circle(s, Inches(0.2), Inches(0.2), Inches(2.5), GREEN)

add_text(s, Inches(0.7), Inches(1.0), Inches(12), Inches(0.5),
         "CONCLUSION",
         font=BODY_FONT, size=14, color=VIOLET, bold=True)
add_text(s, Inches(0.7), Inches(1.6), Inches(12), Inches(1.5),
         "Thank you!",
         font=HEAD_FONT, size=72, color=WHITE, bold=True)
add_text(s, Inches(0.7), Inches(3.2), Inches(12), Inches(2.0),
         ("Social media is a strong tool.\n"
          "It has good and bad sides.\n"
          "Use it with balance — be a smart user."),
         font=BODY_FONT, size=22, color=WHITE)
add_text(s, Inches(0.7), Inches(5.6), Inches(12), Inches(0.5),
         "Questions?",
         font=HEAD_FONT, size=28, color=RED, bold=True)
add_text(s, Inches(0.7), Inches(6.5), Inches(12), Inches(0.4),
         "Anastasia Mogileva  •  TikTok · Instagram · YouTube · Facebook",
         font=BODY_FONT, size=12, color=MUTED)
add_notes(s, (
    "To conclude, social media is a very strong tool. It helps us learn, work, and stay "
    "connected, but it can also take our time and our energy. The most important thing is "
    "balance. If we use social media in a smart way, it gives more than it takes. Thank you "
    "for your attention. I will be happy to answer your questions."
))

prs.save(OUT)
print(f"Saved: {OUT}  ({OUT.stat().st_size // 1024} KB, {len(prs.slides)} slides)")
