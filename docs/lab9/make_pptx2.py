# -*- coding: utf-8 -*-
"""Красивая презентация ЛР9: схема преступления по сериалу «Во все тяжкие».
   Стиль: фирменный зелёный, плитки-элементы Br/Ba, аватары персонажей."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

# ---- палитра ----
DARKG  = RGBColor(0x14, 0x21, 0x1A)   # тёмно-зелёный фон
GREEN  = RGBColor(0x5A, 0xA6, 0x34)   # фирменный зелёный
GREEN2 = RGBColor(0x3E, 0x7A, 0x24)
YELLOW = RGBColor(0xC7, 0xD9, 0x2D)
INK    = RGBColor(0x1E, 0x2A, 0x24)
GREY   = RGBColor(0x5B, 0x6B, 0x63)
LIGHT  = RGBColor(0xF1, 0xF5, 0xF0)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
RED    = RGBColor(0xC0, 0x39, 0x2B)
GOLD   = RGBColor(0xB8, 0x86, 0x0B)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
blank = prs.slide_layouts[6]


def add():            return prs.slides.add_slide(blank)
def fill(s, c):
    s.background.fill.solid(); s.background.fill.fore_color.rgb = c

def rect(s, l, t, w, h, color, line=None, rounded=False, line_w=None):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                             l, t, w, h)
    shp.shadow.inherit = False
    if color is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = color
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = line_w or Pt(1.2)
    return shp

def dashed(shp):
    ln = shp.line._get_or_add_ln()
    d = ln.makeelement(qn('a:prstDash'), {'val': 'dash'}); ln.append(d)

def tb(s, l, t, w, h):
    b = s.shapes.add_textbox(l, t, w, h); b.text_frame.word_wrap = True
    return b, b.text_frame

def run(p, text, size, color=INK, bold=False, italic=False):
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.color.rgb = color
    r.font.bold = bold; r.font.italic = italic; r.font.name = "Calibri"
    return r

def img_fit(s, path, L, T, W, H, center=True):
    iw, ih = Image.open(path).size
    k = min(W / iw, H / ih); w = int(iw * k); h = int(ih * k)
    l = int(L + (W - w) / 2) if center else L
    t = int(T + (H - h) / 2) if center else T
    return s.shapes.add_picture(path, l, t, width=w, height=h)

def header(s, title, sub=None):
    rect(s, 0, 0, SW, Inches(1.12), DARKG)
    rect(s, 0, 0, Inches(0.18), Inches(1.12), GREEN)        # акцентная полоса
    img_fit(s, "tile_br.png", Inches(11.95), Inches(0.16), Inches(0.8), Inches(0.8))
    img_fit(s, "tile_ba.png", Inches(12.5),  Inches(0.16), Inches(0.8), Inches(0.8))
    b, tf = tb(s, Inches(0.45), Inches(0.1), Inches(11.2), Inches(0.95))
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    run(tf.paragraphs[0], title, 28, WHITE, bold=True)
    if sub:
        run(tf.add_paragraph(), sub, 13, YELLOW)

def footer(s, n):
    rect(s, Inches(0.45), Inches(7.06), Inches(3.2), Pt(2.2), GREEN)
    b, tf = tb(s, Inches(10.8), Inches(6.95), Inches(2.4), Inches(0.4))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
    run(p, f"Во все тяжкие · ЛР №9 · {n}", 10, GREY)

def bullets(s, items, L=Inches(0.7), T=Inches(1.5), W=Inches(12.0), H=Inches(5.2),
            size=18, gap=11):
    b, tf = tb(s, L, T, W, H)
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            text  = it[0]
            lvl   = it[1] if len(it) > 1 else 0
            bold  = it[2] if len(it) > 2 else False
            color = it[3] if len(it) > 3 else INK
        else:
            text, lvl, bold, color = it, 0, False, INK
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = lvl; p.space_after = Pt(gap)
        mark = "●  " if lvl == 0 else "–  "
        rr = run(p, mark, size - lvl * 2, GREEN if lvl == 0 else GREY, bold=True)
        run(p, text, size - lvl * 2, color, bold=bold)

def photo_ph(s, L, T, W, H, caption="Кадр из сериала\n(вставьте фото)"):
    box = rect(s, L, T, W, H, LIGHT, line=GREEN, rounded=True, line_w=Pt(1.6)); dashed(box)
    b, tf = tb(s, L, T, W, H); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, line in enumerate(caption.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        run(p, line, 13, GREEN, bold=(i == 0))

# =====================================================================
# СЛАЙД 1 — ТИТУЛ
# =====================================================================
s = add(); fill(s, DARKG)
rect(s, 0, 0, Inches(0.22), SH, GREEN)
img_fit(s, "tile_br.png", Inches(0.7), Inches(0.7), Inches(1.5), Inches(1.5))
img_fit(s, "tile_ba.png", Inches(2.25), Inches(0.7), Inches(1.5), Inches(1.5))
b, tf = tb(s, Inches(0.7), Inches(2.5), Inches(12.0), Inches(2.4))
run(tf.paragraphs[0], "Схема преступления", 46, WHITE, bold=True)
run(tf.add_paragraph(), "по сериалу «Во все тяжкие»", 40, GREEN, bold=True)
p = tf.add_paragraph(); p.space_before = Pt(10)
run(p, "Визуальный анализ связей: персонажи · события · доказательства", 18, YELLOW, italic=True)
# полоса аватаров
gallery = ["av_walt.png","av_jesse.png","av_gus.png","av_hank.png","av_skyler.png","av_saul.png"]
x = Inches(0.7)
for a in gallery:
    img_fit(s, a, x, Inches(5.35), Inches(1.05), Inches(1.05), center=False)
    x += Inches(1.18)
b, tf = tb(s, Inches(0.7), Inches(6.7), Inches(12.0), Inches(0.7))
run(tf.paragraphs[0], "Лабораторное занятие №9  ·  IBM i2 Analyst's Notebook  ·  Выполнила: Могилёва Анастасия",
    14, RGBColor(0xC9,0xD6,0xCC))

# =====================================================================
# СЛАЙД 2 — ЦЕЛЬ И ЗАДАЧИ
# =====================================================================
s = add(); fill(s, WHITE); header(s, "Цель и задачи работы")
bullets(s, [
    ("Цель: построить схему преступления, отражающую связи между персонажами, событиями и доказательствами, средствами визуальной аналитической среды.", 0, True, INK),
    ("Задачи:", 0, True, GREEN2),
    ("выбрать произведение с криминальной линией — сериал «Во все тяжкие»;", 1),
    ("выделить ключевые сущности: персонажей, события, улики;", 1),
    ("построить связи и обозначить их характер (прямые / косвенные);", 1),
    ("проанализировать схему, выявить логику и пробелы;", 1),
    ("оформить отчёт и презентацию.", 1),
    ("Инструмент: IBM i2 Analyst's Notebook — импорт данных из CSV (Import Design).", 0, True, GOLD),
], T=Inches(1.55), size=19, gap=12)
footer(s, 2)

# =====================================================================
# СЛАЙД 3 — ОБЗОР СЕРИАЛА (+ плейсхолдер фото)
# =====================================================================
s = add(); fill(s, WHITE)
header(s, "Краткий обзор произведения", "«Во все тяжкие» (Breaking Bad) · AMC · 2008–2013 · 5 сезонов")
bullets(s, [
    ("Уолтер Уайт — школьный учитель химии, узнаёт о смертельном диагнозе.", 0, True, INK),
    ("Чтобы обеспечить семью, начинает подпольно производить метамфетамин вместе с бывшим учеником Джесси Пинкманом.", 0),
    ("Под псевдонимом «Хайзенберг» превращается из жертвы обстоятельств в главу наркоимперии.", 0),
    ("Жанр: криминальная драма; центральная линия — производство, сбыт и расследование DEA.", 0),
    ("Удобно для схемы: большая преступная сеть, узнаваемые улики, чёткие причинно-следственные связи.", 0, True, GREEN2),
], L=Inches(0.6), T=Inches(1.55), W=Inches(8.1), size=18, gap=14)
photo_ph(s, Inches(9.0), Inches(1.6), Inches(3.9), Inches(4.9))
footer(s, 3)

# =====================================================================
# СЛАЙД 4 — ГАЛЕРЕЯ ПЕРСОНАЖЕЙ
# =====================================================================
s = add(); fill(s, WHITE); header(s, "Действующие лица")
cards = [
    ("av_walt.png",  "Уолтер Уайт", "«Хайзенберг» — организатор", GREEN2),
    ("av_jesse.png", "Джесси Пинкман", "сообщник, «повар»", RGBColor(0x2C,0x6E,0x9E)),
    ("av_gus.png",   "Густаво Фринг", "дистрибьютор", RGBColor(0x7A,0x4F,0xA3)),
    ("av_hank.png",  "Хэнк Шрейдер", "агент DEA (детектив)", GOLD),
    ("av_skyler.png","Скайлер Уайт", "жена, отмывание денег", RGBColor(0xB0,0x45,0x7A)),
    ("av_saul.png",  "Сол Гудман", "адвокат, прикрытие", RGBColor(0xD2,0x69,0x1E)),
    ("av_mike.png",  "Майк Эрмантраут", "охрана, «решала»", RGBColor(0x5A,0x6B,0x73)),
    ("av_gale.png",  "Гейл Боттикер", "химик — жертва", RGBColor(0x6E,0x7B,0x47)),
]
cw, ch = Inches(2.92), Inches(2.55)
gx, gy = Inches(0.22), Inches(0.2)
x0 = Inches(0.55); y0 = Inches(1.45)
for i, (av, name, role, col) in enumerate(cards):
    r, c = divmod(i, 4)
    L = x0 + c * (cw + gx); T = y0 + r * (ch + gy)
    rect(s, L, T, cw, ch, LIGHT, line=RGBColor(0xDD,0xE5,0xDC), rounded=True)
    rect(s, L, T, cw, Inches(0.12), col, rounded=False)
    img_fit(s, av, L, T + Inches(0.22), cw, Inches(1.35))
    b, tf = tb(s, L + Inches(0.1), T + Inches(1.62), cw - Inches(0.2), Inches(0.9))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, name, 15, INK, bold=True)
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
    run(p2, role, 12, GREY)
footer(s, 4)

# =====================================================================
# СЛАЙД 5 — КЛЮЧЕВЫЕ СУЩНОСТИ (3 колонки)
# =====================================================================
s = add(); fill(s, WHITE); header(s, "Ключевые сущности схемы")
cols = [
    ("ПЕРСОНАЖИ", RGBColor(0xBB,0xD7,0xF2), [
        "Уолт «Хайзенберг» — организатор","Джесси Пинкман — сообщник",
        "Густаво Фринг — дистрибьютор","Майк · Сол · Лидия — инфраструктура",
        "Хэнк (DEA) — детектив","Гейл, Брок — жертвы"]),
    ("СОБЫТИЯ", RGBColor(0xF8,0xB5,0xB0), [
        "Производство «голубого мета»","Убийство Гейла",
        "Отравление Брока (рицин)","Взрыв — гибель Гуса","Гибель Хэнка"]),
    ("ДОКАЗАТЕЛЬСТВА", RGBColor(0xBF,0xE3,0xB6), [
        "Голубой метамфетамин","Книга «Leaves of Grass» («G.B.»)",
        "Рицин (яд)","Суперлаборатория / RV","Метиламин (сырьё)","Деньги / автомойка A1"]),
]
cw2 = Inches(4.0); gp = Inches(0.27); x0 = Inches(0.55); y0 = Inches(1.5)
for i, (head, color, items) in enumerate(cols):
    x = x0 + i * (cw2 + gp)
    hd = rect(s, x, y0, cw2, Inches(0.62), color, line=RGBColor(0xAA,0xAA,0xAA), rounded=True)
    tf = hd.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run(tf.paragraphs[0], head, 16, INK, bold=True)
    bx = rect(s, x, y0 + Inches(0.7), cw2, Inches(4.6), LIGHT, line=RGBColor(0xDD,0xE5,0xDC), rounded=True)
    tf = bx.text_frame; tf.word_wrap = True
    tf.margin_left = Inches(0.2); tf.margin_top = Inches(0.16)
    for j, it in enumerate(items):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.space_after = Pt(9)
        run(p, "•  ", 14, GREEN, bold=True); run(p, it, 14, INK)
footer(s, 5)

# =====================================================================
# СЛАЙД 6 — ХРОНОЛОГИЯ
# =====================================================================
s = add(); fill(s, WHITE); header(s, "Хронология ключевых событий")
img_fit(s, "timeline.png", Inches(0.4), Inches(1.45), Inches(12.5), Inches(5.5))
footer(s, 6)

# =====================================================================
# СЛАЙД 7 — КРУГОВАЯ СХЕМА
# =====================================================================
s = add(); fill(s, WHITE); header(s, "Схема преступления — круговой граф (IBM i2)")
img_fit(s, "scheme_circular.png", Inches(0.15), Inches(1.2), Inches(9.5), Inches(6.05))
img_fit(s, "legend.png", Inches(9.5), Inches(1.45), Inches(3.7), Inches(3.2))
b, tf = tb(s, Inches(9.5), Inches(4.8), Inches(3.7), Inches(2.3))
run(tf.paragraphs[0], "23 узла и 36 связей. Все сущности соединены в единую сеть; "
                      "узлы расположены по кругу, связи проходят внутри.", 12, INK)
footer(s, 7)

# =====================================================================
# СЛАЙД 8 — РАЗБОР СВЯЗЕЙ
# =====================================================================
s = add(); fill(s, WHITE); header(s, "Разбор ключевых связей")
bullets(s, [
    ("Уолт ⇄ Джесси — ядро сети: партнёры по производству.", 0, True, GREEN2),
    ("Уолт ⇄ Гус Фринг — наём «повара» и канал сбыта (Los Pollos Hermanos); Майк и Лидия обеспечивают охрану и сырьё.", 0),
    ("«Голубой мет» — фирменная улика, выводит DEA на след «Хайзенберга».", 0, True, RED),
    ("Книга «Leaves of Grass» с надписью «G.B.» — ключевое доказательство: Хэнк понимает, кто такой Хайзенберг.", 0, True, RED),
    ("Рицин — орудие отравления Брока и инструмент манипуляции Джесси.", 0),
    ("Красные связи ведут к насилию: убийство Гейла, взрыв (гибель Гуса), гибель Хэнка.", 0),
], T=Inches(1.55), size=18, gap=13)
footer(s, 8)

# =====================================================================
# СЛАЙД 9 — АНАЛИЗ
# =====================================================================
s = add(); fill(s, WHITE); header(s, "Анализ построенной схемы")
bullets(s, [
    ("Логика связей непротиворечива: у каждого преступления есть мотив, исполнитель и улика.", 0, True, GREEN2),
    ("Косвенные связи (пунктир) — самые опасные для следствия: родство Хэнк↔Уолт долго маскирует подозреваемого.", 0),
    ("Уязвимая точка сети — Уолт: связан со всеми кластерами; его устранение разрушает всю империю (подтверждается SNA-анализом).", 0),
    ("Потенциально «пропущенные» связи: финансовый след денег и поставки метиламина (Лидия) — их раскрытие ускорило бы дело.", 0),
    ("Двойные роли: Гус — «дистрибьютор» и «жертва»; Джесси — «сообщник» и «жертва манипуляций».", 0),
], T=Inches(1.55), size=18, gap=13)
footer(s, 9)

# =====================================================================
# СЛАЙД 10 — ВЫВОДЫ
# =====================================================================
s = add(); fill(s, DARKG)
rect(s, 0, 0, Inches(0.22), SH, GREEN)
img_fit(s, "tile_br.png", Inches(11.6), Inches(0.6), Inches(1.1), Inches(1.1))
img_fit(s, "tile_ba.png", Inches(11.6), Inches(1.85), Inches(1.1), Inches(1.1))
b, tf = tb(s, Inches(0.7), Inches(0.6), Inches(10.5), Inches(1.0))
run(tf.paragraphs[0], "Выводы", 40, WHITE, bold=True)
bullets(s, [
    ("Визуальная аналитическая среда (link-анализ в IBM i2) компактно представляет сложную криминальную сеть.", 0, True, WHITE),
    ("Схема выявляет ключевую фигуру, характер связей и роль каждой улики в раскрытии преступления.", 0, False, RGBColor(0xDC,0xE6,0xDD)),
    ("Метод применим в реальной аналитике: расследования, OSINT, анализ организованных групп.", 0, False, RGBColor(0xDC,0xE6,0xDD)),
    ("Результат работы: круговая схема преступления, отчёт и презентация.", 0, True, YELLOW),
], T=Inches(2.0), size=20, gap=18)
b, tf = tb(s, Inches(0.7), Inches(6.5), Inches(11.5), Inches(0.7))
run(tf.paragraphs[0], "Спасибо за внимание!", 24, WHITE, bold=True, italic=True)

prs.save("Лабораторная_9_Во_все_тяжкие.pptx")
print("saved", len(prs.slides._sldIdLst), "slides")
