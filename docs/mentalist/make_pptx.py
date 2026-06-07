# -*- coding: utf-8 -*-
"""Презентация ЛР9: схема преступления по сериалу «Менталист» (арка Red John)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

DARK  = RGBColor(0x1C, 0x25, 0x30)   # графитовый фон
RED    = RGBColor(0xC0, 0x39, 0x2B)  # красный Red John
GOLD   = RGBColor(0xC7, 0x9A, 0x1E)  # золото (Джейн)
INK    = RGBColor(0x1E, 0x2A, 0x24)
GREY   = RGBColor(0x5B, 0x63, 0x6B)
LIGHT  = RGBColor(0xF2, 0xF3, 0xF5)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GREEN2 = RGBColor(0x3E, 0x7A, 0x24)

prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
blank = prs.slide_layouts[6]

def add(): return prs.slides.add_slide(blank)
def fill(s, c): s.background.fill.solid(); s.background.fill.fore_color.rgb = c
def rect(s, l, t, w, h, color, line=None, rounded=False, line_w=None):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE, l, t, w, h)
    shp.shadow.inherit = False
    if color is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = color
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = line_w or Pt(1.2)
    return shp
def dashed(shp):
    ln = shp.line._get_or_add_ln(); d = ln.makeelement(qn('a:prstDash'), {'val': 'dash'}); ln.append(d)
def tb(s, l, t, w, h):
    b = s.shapes.add_textbox(l, t, w, h); b.text_frame.word_wrap = True; return b, b.text_frame
def run(p, text, size, color=INK, bold=False, italic=False):
    r = p.add_run(); r.text = text; r.font.size = Pt(size); r.font.color.rgb = color
    r.font.bold = bold; r.font.italic = italic; r.font.name = "Calibri"; return r
def img_fit(s, path, L, T, W, H, center=True):
    iw, ih = Image.open(path).size; k = min(W/iw, H/ih); w = int(iw*k); h = int(ih*k)
    l = int(L+(W-w)/2) if center else L; t = int(T+(H-h)/2) if center else T
    return s.shapes.add_picture(path, l, t, width=w, height=h)
def header(s, title, sub=None):
    rect(s, 0, 0, SW, Inches(1.12), DARK)
    rect(s, 0, 0, Inches(0.18), Inches(1.12), RED)
    img_fit(s, "smiley.png", Inches(12.25), Inches(0.16), Inches(0.82), Inches(0.82))
    b, tf = tb(s, Inches(0.45), Inches(0.1), Inches(11.4), Inches(0.95)); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    run(tf.paragraphs[0], title, 27, WHITE, bold=True)
    if sub: run(tf.add_paragraph(), sub, 13, GOLD)
def footer(s, n):
    rect(s, Inches(0.45), Inches(7.06), Inches(3.2), Pt(2.2), RED)
    b, tf = tb(s, Inches(10.8), Inches(6.95), Inches(2.4), Inches(0.4))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT; run(p, f"Менталист · ЛР №9 · {n}", 10, GREY)
def bullets(s, items, L=Inches(0.7), T=Inches(1.5), W=Inches(12.0), H=Inches(5.2), size=18, gap=11):
    b, tf = tb(s, L, T, W, H)
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            text = it[0]; lvl = it[1] if len(it) > 1 else 0
            bold = it[2] if len(it) > 2 else False; color = it[3] if len(it) > 3 else INK
        else: text, lvl, bold, color = it, 0, False, INK
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = lvl; p.space_after = Pt(gap)
        run(p, "●  " if lvl == 0 else "–  ", size-lvl*2, RED if lvl == 0 else GREY, bold=True)
        run(p, text, size-lvl*2, color, bold=bold)
def photo_ph(s, L, T, W, H, caption="Кадр из сериала\n(вставьте фото)"):
    box = rect(s, L, T, W, H, LIGHT, line=RED, rounded=True, line_w=Pt(1.6)); dashed(box)
    b, tf = tb(s, L, T, W, H); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, line in enumerate(caption.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = PP_ALIGN.CENTER
        run(p, line, 13, RED, bold=(i == 0))

# ---- СЛАЙД 1: ТИТУЛ ----
s = add(); fill(s, DARK)
rect(s, 0, 0, Inches(0.22), SH, RED)
img_fit(s, "smiley.png", Inches(0.7), Inches(0.7), Inches(1.7), Inches(1.7))
b, tf = tb(s, Inches(0.7), Inches(2.55), Inches(12.0), Inches(2.4))
run(tf.paragraphs[0], "Схема преступления", 46, WHITE, bold=True)
run(tf.add_paragraph(), "по сериалу «Менталист»", 40, RED, bold=True)
p = tf.add_paragraph(); p.space_before = Pt(10)
run(p, "Дело Red John: персонажи · события · доказательства", 18, GOLD, italic=True)
gallery = ["av_jane.png","av_lisbon.png","av_redjohn.png","av_mcallister.png","av_stiles.png","av_cho.png"]
x = Inches(0.7)
for a in gallery:
    img_fit(s, a, x, Inches(5.4), Inches(1.05), Inches(1.05), center=False); x += Inches(1.18)
b, tf = tb(s, Inches(0.7), Inches(6.7), Inches(12.0), Inches(0.7))
run(tf.paragraphs[0], "Лабораторное занятие №9  ·  IBM i2 Analyst's Notebook  ·  Выполнила: Могилёва Анастасия", 14, RGBColor(0xC9,0xD0,0xD6))

# ---- СЛАЙД 2: ЦЕЛЬ ----
s = add(); fill(s, WHITE); header(s, "Цель и задачи работы")
bullets(s, [
    ("Цель: построить схему преступления, отражающую связи между персонажами, событиями и доказательствами, средствами IBM i2 Analyst's Notebook.", 0, True, INK),
    ("Задачи:", 0, True, RED),
    ("выбрать произведение с детективной линией — сериал «Менталист»;", 1),
    ("сосредоточиться на сквозной арке поиска Red John;", 1),
    ("выделить персонажей, события и улики; построить связи;", 1),
    ("обозначить характер связей (прямые / косвенные);", 1),
    ("проанализировать схему и оформить отчёт и презентацию.", 1),
    ("Инструмент: IBM i2 Analyst's Notebook — импорт данных из CSV.", 0, True, GOLD),
], T=Inches(1.55), size=19, gap=11)
footer(s, 2)

# ---- СЛАЙД 3: ОБЗОР ----
s = add(); fill(s, WHITE); header(s, "Краткий обзор произведения", "«Менталист» (The Mentalist) · CBS · 2008–2015 · 7 сезонов")
bullets(s, [
    ("Патрик Джейн — бывший псевдо-экстрасенс с феноменальной наблюдательностью, консультирует Калифорнийское бюро расследований (CBI).", 0, True, INK),
    ("Когда-то в телеэфире он публично оскорбил серийного убийцу Red John — и тот убил его жену и дочь.", 0),
    ("Сквозная линия сериала — личная охота Джейна на Red John и его тайную сеть сообщников.", 0),
    ("Жанр: процедурный детектив с криминальной аркой. Метод Джейна — дедукция и психология.", 0),
    ("Удобно для схемы: чёткий убийца, список подозреваемых, узнаваемые улики и разветвлённая сеть.", 0, True, GREEN2),
], L=Inches(0.6), T=Inches(1.55), W=Inches(8.1), size=18, gap=13)
photo_ph(s, Inches(9.0), Inches(1.6), Inches(3.9), Inches(4.9))
footer(s, 3)

# ---- СЛАЙД 4: ГАЛЕРЕЯ ----
s = add(); fill(s, WHITE); header(s, "Действующие лица")
cards = [
    ("av_jane.png",  "Патрик Джейн", "консультант-менталист", GOLD),
    ("av_lisbon.png","Тереза Лисбон", "старший агент CBI", RGBColor(0x2C,0x6E,0x9E)),
    ("av_cho.png",   "Кимбелл Чо", "агент CBI", RGBColor(0x2F,0x8A,0x8A)),
    ("av_vanpelt.png","Грейс Ван Пелт", "агент CBI", RGBColor(0x4C,0x7A,0x34)),
    ("av_redjohn.png","Red John", "серийный убийца", RGBColor(0xA0,0x20,0x20)),
    ("av_mcallister.png","Т. Макаллистер", "шериф — это Red John", RED),
    ("av_stiles.png","Брет Стайлз", "лидер культа (подозреваемый)", RGBColor(0x7A,0x4F,0xA3)),
    ("av_rigsby.png","Уэйн Ригсби", "агент CBI", RGBColor(0x5A,0x6B,0x73)),
]
cw, ch = Inches(2.92), Inches(2.55); gx, gy = Inches(0.22), Inches(0.2)
x0, y0 = Inches(0.55), Inches(1.45)
for i, (av, name, role, col) in enumerate(cards):
    r, c = divmod(i, 4); L = x0 + c*(cw+gx); T = y0 + r*(ch+gy)
    rect(s, L, T, cw, ch, LIGHT, line=RGBColor(0xDD,0xDF,0xE3), rounded=True)
    rect(s, L, T, cw, Inches(0.12), col)
    img_fit(s, av, L, T+Inches(0.22), cw, Inches(1.35))
    b, tf = tb(s, L+Inches(0.1), T+Inches(1.62), cw-Inches(0.2), Inches(0.9))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; run(p, name, 15, INK, bold=True)
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER; run(p2, role, 12, GREY)
footer(s, 4)

# ---- СЛАЙД 5: СУЩНОСТИ ----
s = add(); fill(s, WHITE); header(s, "Ключевые сущности схемы")
cols = [
    ("ПЕРСОНАЖИ", RGBColor(0xBB,0xD7,0xF2), [
        "Патрик Джейн — детектив","Команда CBI: Лисбон, Чо, Ригсби, Ван Пелт",
        "Red John — убийца","«Список семи» подозреваемых","Семья Джейна — жертвы"]),
    ("СОБЫТИЯ", RGBColor(0xF8,0xB5,0xB0), [
        "Оскорбление Red John в эфире","Убийство семьи Джейна",
        "Крот Red John в CBI","Рукопожатие с убийцей","Развязка: гибель Макаллистера"]),
    ("ДОКАЗАТЕЛЬСТВА", RGBColor(0xBF,0xE3,0xB6), [
        "Кровавый смайлик (почерк)","Стих У. Блейка «Tyger»",
        "Список 7 подозреваемых","Метка «Ассоциации Блейка»","Запомнившаяся деталь встречи"]),
]
cw2, gp = Inches(4.0), Inches(0.27); x0, y0 = Inches(0.55), Inches(1.5)
for i, (head, color, its) in enumerate(cols):
    x = x0 + i*(cw2+gp)
    hd = rect(s, x, y0, cw2, Inches(0.62), color, line=RGBColor(0xAA,0xAA,0xAA), rounded=True)
    hd.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    run(hd.text_frame.paragraphs[0], head, 16, INK, bold=True)
    bx = rect(s, x, y0+Inches(0.7), cw2, Inches(4.6), LIGHT, line=RGBColor(0xDD,0xDF,0xE3), rounded=True)
    tf = bx.text_frame; tf.word_wrap = True; tf.margin_left = Inches(0.2); tf.margin_top = Inches(0.16)
    for j, it in enumerate(its):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph(); p.space_after = Pt(9)
        run(p, "•  ", 14, RED, bold=True); run(p, it, 13.5, INK)
footer(s, 5)

# ---- СЛАЙД 6: ХРОНОЛОГИЯ ----
s = add(); fill(s, WHITE); header(s, "Хронология ключевых событий")
img_fit(s, "timeline.png", Inches(0.4), Inches(1.45), Inches(12.5), Inches(5.5))
footer(s, 6)

# ---- СЛАЙД 7: СХЕМА ----
s = add(); fill(s, WHITE); header(s, "Схема преступления — круговой граф (IBM i2)")
img_fit(s, "scheme_circular.png", Inches(0.15), Inches(1.2), Inches(9.5), Inches(6.05))
img_fit(s, "legend.png", Inches(9.5), Inches(1.4), Inches(3.7), Inches(3.5))
b, tf = tb(s, Inches(9.5), Inches(5.05), Inches(3.7), Inches(2.0))
run(tf.paragraphs[0], "25 узлов и ~45 связей. Все сущности соединены в единую сеть; "
                      "узлы расположены по кругу, связи проходят внутри.", 12, INK)
footer(s, 7)

# ---- СЛАЙД 8: РАЗБОР ----
s = add(); fill(s, WHITE); header(s, "Разбор ключевых связей")
bullets(s, [
    ("Джейн ⇄ Red John — центральная ось схемы: личная вендетта длиною в сериал.", 0, True, RED),
    ("Триггер: Джейн оскорбил Red John в эфире → убийство жены и дочери (жертвы).", 0),
    ("Кровавый смайлик — фирменный почерк убийцы, связывает все эпизоды.", 0, True, RED),
    ("Стих Уильяма Блейка «Tyger» — ключ к личности Red John (линия дедукции Джейна).", 0, True, GOLD),
    ("«Список семи» подозреваемых связывает Джейна со всеми фигурантами.", 0),
    ("«Ассоциация Блейка» — тайная сеть сообщников (Бертрам, Киркланд, Хаффнер, Смит).", 0),
    ("Развязка: шериф Макаллистер оказался Red John — Джейн вычисляет и устраняет его.", 0, True, INK),
], T=Inches(1.5), size=17, gap=10)
footer(s, 8)

# ---- СЛАЙД 9: АНАЛИЗ ----
s = add(); fill(s, WHITE); header(s, "Анализ построенной схемы")
bullets(s, [
    ("Логика связей непротиворечива: у преступления есть мотив (месть убийцы), исполнитель и узнаваемая улика.", 0, True, GREEN2),
    ("Центральные узлы — Джейн и Red John: через них проходит большинство связей (подтверждается SNA-анализом центральности).", 0),
    ("Косвенные связи (пунктир) маскируют истину: членство в «Ассоциации Блейка» долго остаётся скрытым.", 0),
    ("«Список семи» сужает круг: схема наглядно показывает, как из множества подозреваемых выделяется Макаллистер.", 0),
    ("Двойные роли: Стайлз и Смит — одновременно «подозреваемые» и «помощники» Джейна.", 0),
], T=Inches(1.55), size=18, gap=13)
footer(s, 9)

# ---- СЛАЙД 10: ВЫВОДЫ ----
s = add(); fill(s, DARK)
rect(s, 0, 0, Inches(0.22), SH, RED)
img_fit(s, "smiley.png", Inches(11.7), Inches(0.6), Inches(1.2), Inches(1.2))
b, tf = tb(s, Inches(0.7), Inches(0.6), Inches(10.5), Inches(1.0))
run(tf.paragraphs[0], "Выводы", 40, WHITE, bold=True)
bullets(s, [
    ("Визуальный link-анализ в IBM i2 компактно представляет сложную детективную арку Red John.", 0, True, WHITE),
    ("Схема выявляет ключевые фигуры (Джейн, Red John), характер связей и роль каждой улики.", 0, False, RGBColor(0xDC,0xE0,0xE6)),
    ("Метод применим в реальной аналитике: расследования, OSINT, анализ преступных сетей.", 0, False, RGBColor(0xDC,0xE0,0xE6)),
    ("Результат работы: круговая схема преступления, отчёт и презентация.", 0, True, GOLD),
], T=Inches(2.0), size=20, gap=18)
b, tf = tb(s, Inches(0.7), Inches(6.5), Inches(11.5), Inches(0.7))
run(tf.paragraphs[0], "Спасибо за внимание!", 24, WHITE, bold=True, italic=True)

prs.save("Лабораторная_9_Менталист.pptx")
print("saved", len(prs.slides._sldIdLst), "slides")
