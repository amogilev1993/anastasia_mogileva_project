# -*- coding: utf-8 -*-
"""Формирование отчёта ЛР9 (.docx): схема преступления по сериалу «Во все тяжкие»."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image

GREEN = RGBColor(0x3E, 0x7A, 0x24)
DARK  = RGBColor(0x1E, 0x2A, 0x24)
GREY  = RGBColor(0x5B, 0x6B, 0x63)

doc = Document()

# базовый шрифт
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(13)
st._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
for sec in doc.sections:
    sec.top_margin = Cm(2); sec.bottom_margin = Cm(2)
    sec.left_margin = Cm(3); sec.right_margin = Cm(1.5)


def para(text="", size=13, bold=False, italic=False, color=None, align=None,
         space_after=6, space_before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.4
    if align: p.alignment = align
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size); r.bold = bold; r.italic = italic
        if color: r.font.color.rgb = color
    return p


def h(text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(15 if level == 1 else 13.5)
    r.font.color.rgb = GREEN
    return p


def bullet(text, bold_part=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.35
    if bold_part:
        r = p.add_run(bold_part + " "); r.bold = True; r.font.size = Pt(13)
    r = p.add_run(text); r.font.size = Pt(13)
    return p


def picture(path, width_cm, caption):
    iw, ih = Image.open(path).size
    doc.add_picture(path, width=Cm(width_cm))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = para(caption, size=11, italic=True, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER,
               space_after=10, space_before=2)


def placeholder(text):
    """Серая рамка-плейсхолдер под скриншот из i2."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Cm(15)
    # граница
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "dashed"); e.set(qn("w:sz"), "12")
        e.set(qn("w:color"), "5AA634")
        borders.append(e)
    tcPr.append(borders)
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(26); p.paragraph_format.space_after = Pt(26)
    r = p.add_run("📷  " + text); r.font.size = Pt(12); r.bold = True
    r.font.color.rgb = GREEN
    para("", space_after=8)


# ======================= ТИТУЛЬНЫЙ ЛИСТ =======================
for _ in range(3):
    para("", space_after=2)
para("ОТЧЁТ", size=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=DARK, space_after=4)
para("по лабораторной работе №9", size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
para("Тема: Создание схемы преступления на основе выбранного фильма, книги или сериала "
     "с использованием визуальной аналитической среды",
     size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
para("Произведение: сериал «Во все тяжкие» (Breaking Bad)",
     size=14, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=GREEN, space_after=4)
para("Инструмент: IBM i2 Analyst's Notebook",
     size=13, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=GREY, space_after=40)
for _ in range(4):
    para("", space_after=2)
para("Выполнила: Могилёва Анастасия", size=13, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=2)
para("Проверил: _______________________", size=13, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=40)
para("2026 г.", size=13, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ======================= 1. ЦЕЛЬ И ЗАДАЧИ =======================
h("1. Цель и задачи работы")
para("Цель работы — построить схему преступления, отображающую связи между персонажами, "
     "событиями и доказательствами, с использованием визуальной аналитической среды "
     "IBM i2 Analyst's Notebook, а также проанализировать выявленные связи.")
para("Задачи:", bold=True, space_after=3)
bullet("выбрать произведение с детективной (криминальной) сюжетной линией;")
bullet("выделить ключевые сущности: персонажей, события и доказательства;")
bullet("построить связи между ними и обозначить их характер (прямые / косвенные);")
bullet("проанализировать схему, выявить логику и возможные пробелы;")
bullet("оформить отчёт и подготовить презентацию.")

# ======================= 2. ОБЗОР ПРОИЗВЕДЕНИЯ =======================
h("2. Краткий обзор выбранного произведения")
para("«Во все тяжкие» (Breaking Bad) — американский криминальный драматический сериал "
     "(канал AMC, 2008–2013, 5 сезонов). Главный герой — Уолтер Уайт, школьный учитель химии, "
     "который узнаёт о смертельном диагнозе. Чтобы обеспечить семью, он начинает подпольно "
     "производить метамфетамин вместе с бывшим учеником Джесси Пинкманом.")
para("Под псевдонимом «Хайзенберг» Уолтер постепенно превращается из жертвы обстоятельств "
     "в безжалостного главу наркоимперии. Центральная линия сюжета — производство и сбыт "
     "наркотиков и параллельное расследование, которое ведёт агент DEA Хэнк Шрейдер, "
     "приходящийся Уолту родственником (зятем).")
para("Произведение удобно для построения схемы преступления: в нём действует разветвлённая "
     "преступная сеть, присутствуют узнаваемые вещественные улики и чёткие "
     "причинно-следственные связи между событиями.")

# ======================= 3. ПРОЦЕСС ПОСТРОЕНИЯ =======================
h("3. Описание процесса построения схемы")
para("На основе сюжета были выделены ключевые сущности трёх типов — персонажи, события и "
     "доказательства. Ниже приведён их перечень.")

h("3.1. Персонажи", level=2)
chars = [
    ("Уолтер Уайт «Хайзенберг»", "организатор наркопроизводства (учитель химии)."),
    ("Джесси Пинкман", "сообщник, «повар» метамфетамина."),
    ("Скайлер Уайт", "жена Уолта, отмывание денег через автомойку."),
    ("Густаво Фринг", "дистрибьютор, владелец сети Los Pollos Hermanos."),
    ("Майк Эрмантраут", "охрана и «решала» Гуса."),
    ("Сол Гудман", "адвокат, юридическое прикрытие."),
    ("Лидия", "поставщик сырья (метиламина)."),
    ("Гектор Саламанка", "представитель картеля, враг Гуса."),
    ("Банда Джека", "наёмники."),
    ("Хэнк Шрейдер", "агент DEA, ведёт расследование (детектив)."),
    ("Гейл Боттикер", "химик-ассистент — жертва."),
    ("Брок", "ребёнок — жертва отравления."),
]
for n, d in chars:
    bullet(d, bold_part=n + " —")

h("3.2. События", level=2)
for n, d in [
    ("Производство «голубого мета»", "подпольный синтез метамфетамина."),
    ("Убийство Гейла", "устранение свидетеля-химика."),
    ("Отравление Брока", "отравление рицином как инструмент манипуляции."),
    ("Взрыв в доме престарелых", "гибель Густаво Фринга."),
    ("Гибель Хэнка", "перестрелка с бандой Джека."),
]:
    bullet(d, bold_part=n + " —")

h("3.3. Доказательства (улики)", level=2)
for n, d in [
    ("Голубой метамфетамин", "фирменная улика, выводит DEA на след «Хайзенберга»."),
    ("Книга «Leaves of Grass» с надписью «G.B.»", "ключевая улика, разоблачающая Уолта."),
    ("Рицин", "орудие отравления Брока."),
    ("Суперлаборатория / фургон RV", "место преступления."),
    ("Метиламин", "сырьё для синтеза."),
    ("Деньги / автомойка A1", "средство легализации доходов."),
]:
    bullet(d, bold_part=n + " —")

h("3.4. Построение схемы в IBM i2 Analyst's Notebook", level=2)
para("Схема строилась импортом структурированных данных в IBM i2 Analyst's Notebook через "
     "механизм Import Design. Данные подготовлены в виде CSV-файла, где каждая строка "
     "описывает связь и обе её сущности-конца. Порядок работы:")
bullet("создание новой схемы (File → New Chart);", )
bullet("импорт CSV-файла связей (Import → Import from File), разделитель «;», кодировка UTF-8;")
bullet("выбор типа строки «две сущности и связь» (этап Select Design);")
bullet("назначение столбцов (этап Assign Columns): подпись → Identity/Label, тип → Entity Type, "
       "иконка → Icon; для связи — Label, Direction и Link Strength;")
bullet("слияние одинаковых узлов по Identity (этап Import Details);")
bullet("применение круговой раскладки (Arrange → Layout) и анализ (Social Network Analysis).")
para("Характер связей кодируется стилем линии: сплошная линия — прямая связь / прямые улики, "
     "пунктирная — косвенная связь. Направление стрелок отражает направленность отношения "
     "(например, «исполнитель → жертва»).", space_after=10)
placeholder("Скриншот 1. Окно импорта данных в IBM i2 (этап Assign Columns)")
placeholder("Скриншот 2. Построенная схема в IBM i2 (рабочее окно)")

# ======================= 4. СХЕМА =======================
doc.add_page_break()
h("4. Схема преступления")
para("Итоговая схема представляет собой круговой граф: 23 сущности (узла) и 36 связей. "
     "Все элементы соединены в единую сеть.")
picture("scheme_circular.png", 16.5, "Рисунок 1 — Круговая схема преступления (граф связей)")
picture("legend.png", 13.5, "Рисунок 2 — Условные обозначения схемы")
para("Для наглядности хронологической последовательности событий построена временная линия.",
     space_before=6)
picture("timeline.png", 16.5, "Рисунок 3 — Хронология ключевых событий")

# ======================= 5. АНАЛИЗ =======================
doc.add_page_break()
h("5. Анализ выявленных связей")
para("Анализ построенной схемы позволяет сделать следующие выводы.")
bullet("Логика связей непротиворечива: у каждого преступления прослеживается мотив, "
       "исполнитель и связанная с ним улика.")
bullet("Ядро преступной сети — связка Уолт ⇄ Джесси (партнёры по производству), вокруг которой "
       "формируется инфраструктура: Гус (сбыт), Майк (охрана), Лидия (сырьё), Сол (прикрытие).")
bullet("Уязвимая точка сети — Уолтер Уайт: он связан со всеми кластерами, поэтому его "
       "устранение разрушает всю систему. Это подтверждается анализом центральности "
       "(Betweenness) в Social Network Analysis.")
bullet("Косвенные связи (пунктир) наиболее опасны для следствия: родственная связь "
       "Хэнк ↔ Уолт долго маскирует подозреваемого от расследования.")
bullet("Некоторые персонажи имеют двойные роли: Густаво Фринг — одновременно «дистрибьютор» "
       "и «жертва»; Джесси — «сообщник» и «жертва манипуляций».")

h("6. Значимость ключевых элементов схемы")
para("Отдельные элементы схемы играют решающую роль в развитии сюжета:")
bullet("выводит расследование DEA на след «Хайзенберга» по уникальному составу и цвету.",
       bold_part="Голубой метамфетамин —")
bullet("является переломной уликой: именно по дарственной надписи «G.B.» (Гейл Боттикер) "
       "Хэнк понимает, что его родственник Уолт и есть разыскиваемый «Хайзенберг».",
       bold_part="Книга «Leaves of Grass» —")
bullet("связывает преступление и манипуляцию: отравление Брока используется, чтобы настроить "
       "Джесси против Гуса.", bold_part="Рицин —")
bullet("показывает, как бытовой мотив (обеспечить семью) перерастает в "
       "организованную преступность.", bold_part="Связь Уолт → деньги / автомойка —")

# ======================= 7. ВЫВОДЫ =======================
h("7. Выводы")
para("В ходе лабораторной работы построена схема преступления по сериалу «Во все тяжкие» "
     "средствами визуальной аналитической среды IBM i2 Analyst's Notebook. Схема в форме "
     "кругового графа наглядно отображает связи между персонажами, событиями и "
     "доказательствами.")
para("Визуальный link-анализ позволяет компактно представить сложную криминальную сеть, "
     "выявить ключевую фигуру, определить характер связей и оценить роль каждой улики в "
     "раскрытии преступления. Подобный метод применяется в реальной аналитической работе: "
     "при расследованиях, OSINT-анализе и изучении организованных групп.")

doc.save("Отчёт_ЛР9_Во_все_тяжкие.docx")
print("docx saved")
