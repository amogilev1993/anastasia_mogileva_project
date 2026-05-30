# -*- coding: utf-8 -*-
"""Сборка презентации ЛР9: схема преступления по сериалу «Во все тяжкие»."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

NAVY   = RGBColor(0x1A, 0x3C, 0x5E)
ACCENT = RGBColor(0xC0, 0x1C, 0x28)
GREEN  = RGBColor(0x2E, 0x7D, 0x32)
DARK   = RGBColor(0x22, 0x22, 0x22)
GREY   = RGBColor(0x55, 0x55, 0x55)
LIGHT  = RGBColor(0xF2, 0xF4, 0xF7)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
blank = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(blank)


def fill(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def band(slide, height=Inches(1.15), color=NAVY):
    sh = slide.shapes.add_shape(1, 0, 0, SW, height)
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def textbox(slide, l, t, w, h):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    return tb, tf


def set_run(r, size, color=DARK, bold=False, italic=False, font="Calibri"):
    r.font.size = Pt(size); r.font.color.rgb = color
    r.font.bold = bold; r.font.italic = italic; r.font.name = font


def title_band(slide, text, sub=None):
    band(slide)
    tb, tf = textbox(slide, Inches(0.5), Inches(0.12), Inches(12.3), Inches(0.95))
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = text; set_run(r, 30, WHITE, bold=True)
    if sub:
        p2 = tf.add_paragraph()
        r2 = p2.add_run(); r2.text = sub; set_run(r2, 14, RGBColor(0xCF, 0xDD, 0xEC))


def bullets(slide, items, left=Inches(0.7), top=Inches(1.55),
            width=Inches(12.0), height=Inches(5.4), size=18, gap=10):
    tb, tf = textbox(slide, left, top, width, height)
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            text, lvl, bold, color = (it + (0, False, DARK))[:4]
        else:
            text, lvl, bold, color = it, 0, False, DARK
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = lvl
        p.space_after = Pt(gap)
        bullet = "• " if lvl == 0 else "– "
        r = p.add_run(); r.text = (bullet + text) if text else ""
        set_run(r, size - lvl * 2, color, bold=bold)
    return tb


def add_image_fit(slide, path, max_l, max_t, max_w, max_h):
    iw, ih = Image.open(path).size
    ratio = min(max_w / iw, max_h / ih)
    w = int(iw * ratio); h = int(ih * ratio)
    l = int(max_l + (max_w - w) / 2)
    t = int(max_t + (max_h - h) / 2)
    return slide.shapes.add_picture(path, l, t, width=w, height=h)


def footer(slide, n):
    tb, tf = textbox(slide, Inches(11.3), Inches(7.05), Inches(1.9), Inches(0.4))
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
    r = p.add_run(); r.text = f"ЛР №9  •  {n}"; set_run(r, 11, GREY)


# ---------------- Слайд 1: Титульный ----------------
s = add_slide(); fill(s, NAVY)
sh = s.shapes.add_shape(1, 0, Inches(2.55), SW, Inches(2.4))
sh.fill.solid(); sh.fill.fore_color.rgb = WHITE; sh.line.fill.background(); sh.shadow.inherit = False
tb, tf = textbox(s, Inches(0.8), Inches(2.7), Inches(11.7), Inches(2.1))
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Схема преступления по сериалу «Во все тяжкие»"; set_run(r, 34, NAVY, bold=True)
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
r = p2.add_run(); r.text = "Визуальный анализ связей: персонажи • события • доказательства"
set_run(r, 18, ACCENT, italic=True)
tb, tf = textbox(s, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.7))
for txt, sz in [("Лабораторное занятие №9", 18), ("Создание схемы преступления в визуальной аналитической среде", 15),
                ("Выполнила: Могилёва Анастасия", 15)]:
    p = tf.paragraphs[0] if txt.startswith("Лаб") else tf.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = txt; set_run(r, sz, WHITE, bold=txt.startswith("Лаб"))

# ---------------- Слайд 2: Цель и задачи ----------------
s = add_slide(); fill(s, WHITE)
title_band(s, "Цель и задачи работы")
bullets(s, [
    ("Цель: построить схему преступления, отображающую связи между персонажами, событиями и доказательствами, средствами визуальной аналитической среды.", 0, True, NAVY),
    ("Задачи:", 0, True, DARK),
    ("выбрать произведение с детективной/криминальной линией;", 1, False, DARK),
    ("выделить ключевые сущности: персонажей, события, улики;", 1, False, DARK),
    ("построить связи и обозначить их характер (прямые/косвенные);", 1, False, DARK),
    ("проанализировать схему, выявить логику и пробелы;", 1, False, DARK),
    ("оформить отчёт и презентацию.", 1, False, DARK),
    ("Инструмент: IBM i2 Analyst's Notebook (link-анализ), импорт данных из CSV.", 0, False, GREY),
], top=Inches(1.6), size=19, gap=12)
footer(s, 2)

# ---------------- Слайд 3: Обзор произведения ----------------
s = add_slide(); fill(s, WHITE)
title_band(s, "Краткий обзор произведения", "«Во все тяжкие» (Breaking Bad), AMC, 2008–2013, 5 сезонов")
bullets(s, [
    ("Уолтер Уайт — школьный учитель химии, узнаёт о смертельном диагнозе (рак лёгких).", 0, False, DARK),
    ("Чтобы обеспечить семью, он начинает подпольно производить метамфетамин вместе с бывшим учеником Джесси Пинкманом.", 0, False, DARK),
    ("Под псевдонимом «Хайзенберг» Уолт превращается из жертвы обстоятельств в безжалостного главу наркоимперии.", 0, False, DARK),
    ("Жанр: криминальная драма. Центральная линия — производство и сбыт наркотиков и расследование DEA.", 0, False, DARK),
    ("Почему удобно для схемы: множество персонажей, чёткая преступная сеть, узнаваемые улики и причинно-следственные связи.", 0, True, GREEN),
], top=Inches(1.75), size=19, gap=14)
footer(s, 3)

# ---------------- Слайд 4: Методология / сущности ----------------
s = add_slide(); fill(s, WHITE)
title_band(s, "Методология: ключевые сущности")
# три колонки
cols = [
    ("ПЕРСОНАЖИ", RGBColor(0xBB,0xD7,0xF2), [
        "Уолт «Хайзенберг» — организатор",
        "Джесси Пинкман — сообщник",
        "Густаво Фринг — дистрибьютор",
        "Майк, Сол, Лидия — инфраструктура",
        "Хэнк (DEA) — детектив",
        "Гейл, Брок — жертвы",
    ]),
    ("СОБЫТИЯ", RGBColor(0xF8,0xB5,0xB0), [
        "Производство «голубого мета»",
        "Убийство Гейла",
        "Отравление Брока (рицин)",
        "Взрыв — гибель Гуса",
        "Гибель Хэнка",
    ]),
    ("ДОКАЗАТЕЛЬСТВА", RGBColor(0xBF,0xE3,0xB6), [
        "Голубой метамфетамин",
        "Книга «Leaves of Grass» («G.B.»)",
        "Рицин (яд)",
        "Суперлаборатория / RV",
        "Метиламин (сырьё)",
        "Деньги / автомойка A1",
    ]),
]
cw = Inches(4.0); gap = Inches(0.27); x0 = Inches(0.55); y0 = Inches(1.6)
for i, (head, color, items) in enumerate(cols):
    x = x0 + i * (cw + gap)
    hd = s.shapes.add_shape(1, x, y0, cw, Inches(0.6))
    hd.fill.solid(); hd.fill.fore_color.rgb = color; hd.line.color.rgb = GREY; hd.shadow.inherit = False
    tf = hd.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = head; set_run(r, 16, DARK, bold=True)
    bx = s.shapes.add_shape(1, x, y0 + Inches(0.6), cw, Inches(4.7))
    bx.fill.solid(); bx.fill.fore_color.rgb = LIGHT; bx.line.color.rgb = GREY; bx.shadow.inherit = False
    tf = bx.text_frame; tf.word_wrap = True; tf.margin_left = Inches(0.18); tf.margin_top = Inches(0.15)
    for j, it in enumerate(items):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        r = p.add_run(); r.text = "• " + it; set_run(r, 14, DARK)
footer(s, 4)

# ---------------- Слайд 5: Хронология ----------------
s = add_slide(); fill(s, WHITE)
title_band(s, "Хронология ключевых событий")
add_image_fit(s, "timeline.png", Inches(0.4), Inches(1.5), Inches(12.5), Inches(5.6))
footer(s, 5)

# ---------------- Слайд 6: Схема преступления ----------------
s = add_slide(); fill(s, WHITE)
title_band(s, "Схема преступления в IBM i2 (link-граф связей)")
add_image_fit(s, "scheme.png", Inches(0.2), Inches(1.25), Inches(9.4), Inches(6.0))
add_image_fit(s, "legend.png", Inches(9.55), Inches(1.6), Inches(3.6), Inches(3.2))
tb, tf = textbox(s, Inches(9.55), Inches(4.9), Inches(3.6), Inches(2.3))
p = tf.paragraphs[0]
r = p.add_run(); r.text = "Граф построен в IBM i2 Analyst's Notebook импортом из CSV (23 узла, 36 связей). "
set_run(r, 12, DARK)
r = p.add_run(); r.text = "Узлы — сущности, рёбра — связи с подписью характера отношения."
set_run(r, 12, DARK)
footer(s, 6)

# ---------------- Слайд 7: Разбор связей ч.1 ----------------
s = add_slide(); fill(s, WHITE)
title_band(s, "Разбор ключевых связей · ядро группы")
bullets(s, [
    ("Уолт ⇄ Джесси — партнёры по производству; центральная связь всей сети.", 0, True, NAVY),
    ("Уолт ⇄ Скайлер — брак; жена легализует доходы через автомойку A1.", 0, False, DARK),
    ("Уолт ⇄ Сол Гудман — адвокат-«прикрытие», связывает Уолта с Майком и теневой логистикой.", 0, False, DARK),
    ("Уолт ⇄ Гус Фринг — Уолт нанят как повар; Гус обеспечивает сбыт через сеть Los Pollos Hermanos.", 0, False, DARK),
    ("Гус → Майк, Лидия — охрана и поставки метиламина (сырьё → производство).", 0, False, DARK),
    ("Вывод: преступление держится не на одном человеке, а на устойчивой сети ролей.", 0, True, GREEN),
], top=Inches(1.6), size=19, gap=13)
footer(s, 7)

# ---------------- Слайд 8: Разбор связей ч.2 ----------------
s = add_slide(); fill(s, WHITE)
title_band(s, "Разбор ключевых связей · улики и расследование")
bullets(s, [
    ("«Голубой метамфетамин» — фирменная улика: именно она выводит DEA на след «Хайзенберга».", 0, True, ACCENT),
    ("Книга «Leaves of Grass» с надписью «G.B.» (Гейл Боттикер) — ключевое доказательство: по ней Хэнк понимает, что Уолт и есть Хайзенберг.", 0, True, ACCENT),
    ("Рицин — орудие отравления Брока; инструмент манипуляции Джесси (Уолт подставляет Гуса).", 0, False, DARK),
    ("Линия DEA (золотая): Хэнк ⇄ Уолт — родство (зять) + расследование; косвенные связи долго маскируют истину.", 0, False, DARK),
    ("Красные связи ведут к насилию: убийство Гейла, взрыв (гибель Гуса), гибель Хэнка.", 0, False, DARK),
], top=Inches(1.6), size=18, gap=13)
footer(s, 8)

# ---------------- Слайд 9: Анализ схемы ----------------
s = add_slide(); fill(s, WHITE)
title_band(s, "Анализ построенной схемы")
bullets(s, [
    ("Логика связей замкнута и непротиворечива: каждое преступление имеет мотив, исполнителя и улику.", 0, True, NAVY),
    ("Косвенные связи (пунктир) — самые опасные для следствия: родство Хэнк↔Уолт маскирует подозреваемого.", 0, False, DARK),
    ("Уязвимая точка сети — Уолт: он связан со всеми кластерами, его устранение разрушает всю империю.", 0, False, DARK),
    ("Потенциально «пропущенные» связи в реальном следствии: финансовый след денег и поставки метиламина (Лидия) — их раскрытие ускорило бы дело.", 0, False, DARK),
    ("Уточнение ролей: Гус — одновременно «дистрибьютор» и «жертва»; Джесси — «сообщник» и «жертва манипуляций».", 0, False, DARK),
    ("Значимость: схема наглядно показывает, как бытовая мотивация перерастает в организованную преступность.", 0, True, GREEN),
], top=Inches(1.55), size=18, gap=11)
footer(s, 9)

# ---------------- Слайд 10: Выводы ----------------
s = add_slide(); fill(s, NAVY)
tb, tf = textbox(s, Inches(0.9), Inches(0.7), Inches(11.5), Inches(1.0))
p = tf.paragraphs[0]; r = p.add_run(); r.text = "Выводы"; set_run(r, 34, WHITE, bold=True)
bullets(s, [
    ("Визуальная аналитическая среда (link-анализ) позволяет компактно представить сложную криминальную сеть.", 0, True, WHITE),
    ("Схема выявляет ключевую фигуру, характер связей и роль каждой улики в раскрытии преступления.", 0, False, RGBColor(0xE8,0xEE,0xF6)),
    ("Метод применим в реальной аналитике: расследования, OSINT, анализ организованных групп.", 0, False, RGBColor(0xE8,0xEE,0xF6)),
    ("Результат работы: схема преступления, отчёт и презентация на 10 слайдов.", 0, True, RGBColor(0xFF,0xE0,0x8A)),
], top=Inches(2.0), size=20, gap=18)
tb, tf = textbox(s, Inches(0.9), Inches(6.4), Inches(11.5), Inches(0.7))
p = tf.paragraphs[0]
r = p.add_run(); r.text = "Спасибо за внимание!"; set_run(r, 22, WHITE, bold=True, italic=True)

prs.save("Лабораторная_9_Во_все_тяжкие.pptx")
print("pptx saved:", len(prs.slides._sldIdLst), "slides")
