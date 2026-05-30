# -*- coding: utf-8 -*-
"""
Генератор данных для построения схемы преступления в IBM i2 Analyst's Notebook.
Тема: сериал «Во все тяжкие» (Breaking Bad).

Скрипт формирует два CSV-файла в кодировке UTF-8 с BOM (i2 корректно читает кириллицу):
  1) entities.csv — каталог сущностей (узлов): персонажи, события, доказательства;
  2) links.csv    — связи (рёбра) в формате «два конца в одной строке»,
                    пригодном для импорта через Import Design в i2 ANB.

Запуск:  python generate_i2_csv.py
"""
import csv

# ---------------------------------------------------------------------------
# 1. СУЩНОСТИ (узлы графа).
#    Поле "Icon" — имя стандартной иконки палитры i2 Analyst's Notebook.
#    Поле "Type" — пользовательский тип сущности (Entity Type) для группировки.
# ---------------------------------------------------------------------------
ENTITIES = [
    # id                     Label (подпись)                         Type            i2 Icon              Описание
    ("walt",   "Уолтер Уайт «Хайзенберг»",  "Персонаж",      "Male",              "Учитель химии, организатор наркопроизводства"),
    ("jesse",  "Джесси Пинкман",            "Персонаж",      "Male",              "Сообщник, «повар» метамфетамина"),
    ("skyler", "Скайлер Уайт",              "Персонаж",      "Female",            "Жена Уолта, отмывание денег"),
    ("saul",   "Сол Гудман",                "Персонаж",      "Male",              "Адвокат, юридическое прикрытие"),
    ("gus",    "Густаво Фринг",             "Персонаж",      "Male",              "Дистрибьютор, владелец Los Pollos Hermanos"),
    ("mike",   "Майк Эрмантраут",           "Персонаж",      "Male",              "Охрана и «решала» Гуса"),
    ("lydia",  "Лидия Родарт-Кантильо",     "Персонаж",      "Female",            "Поставщик метиламина (Madrigal)"),
    ("jack",   "Банда Джека",               "Организация",   "Group",             "Наёмники-неонацисты"),
    ("hector", "Гектор Саламанка",          "Персонаж",      "Male",              "Картель, враг Гуса"),
    ("hank",   "Хэнк Шрейдер",              "Детектив",      "Law Enforcement",   "Агент DEA, зять Уолта"),
    ("gale",   "Гейл Боттикер",             "Жертва",        "Male",              "Химик-ассистент, убит"),
    ("brock",  "Брок Кантильо",             "Жертва",        "Male",              "Ребёнок, отравлен"),
    # События
    ("e_cook",  "Производство «голубого мета»", "Событие",   "Incident",          "Подпольное производство метамфетамина"),
    ("e_gale",  "Убийство Гейла",            "Событие",      "Incident",          "Устранение свидетеля-химика"),
    ("e_brock", "Отравление Брока",          "Событие",      "Incident",          "Отравление рицином (манипуляция)"),
    ("e_blast", "Взрыв — гибель Гуса",       "Событие",      "Explosion",         "Бомба в доме престарелых"),
    ("e_hank",  "Гибель Хэнка",              "Событие",      "Incident",          "Перестрелка с бандой Джека"),
    # Доказательства / улики
    ("ev_meth", "Голубой метамфетамин",      "Доказательство","Drugs",            "Фирменная улика, выводит DEA на след"),
    ("ev_book", "Книга «Leaves of Grass» («G.B.»)", "Доказательство","Document",  "Ключевая улика: разоблачение Хайзенберга"),
    ("ev_ricin","Рицин (капсула-яд)",        "Доказательство","Poison",           "Орудие отравления Брока"),
    ("ev_lab",  "Суперлаборатория / фургон RV", "Доказательство","Office Building","Место преступления"),
    ("ev_methyl","Метиламин (сырьё)",        "Доказательство","Chemical",          "Сырьё для синтеза"),
    ("ev_money","Деньги / автомойка A1",     "Доказательство","Money",             "Легализация доходов"),
]

# Быстрый доступ по id -> (label, type, icon)
EMAP = {e[0]: e for e in ENTITIES}

# ---------------------------------------------------------------------------
# 2. СВЯЗИ (рёбра графа).
#    direction: ToEnd2 | ToEnd1 | Both | None
#    strength : Confirmed (сплошная линия) | Tentative (пунктир — косвенная связь)
# ---------------------------------------------------------------------------
LINKS = [
    # end1     end2        label (характер связи)                 direction  strength
    ("walt",   "jesse",   "Партнёры по производству",            "Both",    "Confirmed"),
    ("walt",   "skyler",  "Муж / жена, отмывание денег",          "Both",    "Confirmed"),
    ("walt",   "saul",    "Клиент — адвокат",                     "Both",    "Confirmed"),
    ("saul",   "mike",    "Связал с «решалой»",                   "ToEnd2",  "Tentative"),
    ("walt",   "gus",     "Нанят как повар",                      "Both",    "Confirmed"),
    ("gus",    "mike",    "Работодатель",                         "Both",    "Confirmed"),
    ("gus",    "lydia",   "Канал поставок",                       "Both",    "Confirmed"),
    ("lydia",  "ev_methyl","Поставляет сырьё",                    "ToEnd2",  "Confirmed"),
    ("ev_methyl","e_cook","Используется в производстве",          "ToEnd2",  "Tentative"),
    ("walt",   "e_cook",  "Организует",                           "ToEnd2",  "Confirmed"),
    ("jesse",  "e_cook",  "Варит",                                "ToEnd2",  "Confirmed"),
    ("e_cook", "ev_meth", "Продукт",                              "ToEnd2",  "Confirmed"),
    ("e_cook", "ev_lab",  "Место преступления",                   "ToEnd2",  "Confirmed"),
    ("gus",    "ev_meth", "Сбыт",                                 "ToEnd1",  "Tentative"),
    ("skyler", "ev_money","Легализует",                           "ToEnd2",  "Confirmed"),
    ("walt",   "ev_money","Доход от продаж",                      "ToEnd2",  "Confirmed"),
    ("gus",    "gale",    "Нанял химиком",                        "ToEnd2",  "Confirmed"),
    ("walt",   "e_gale",  "Заказал устранение",                   "ToEnd2",  "Confirmed"),
    ("jesse",  "e_gale",  "Исполнитель",                          "ToEnd2",  "Confirmed"),
    ("e_gale", "gale",    "Жертва",                               "ToEnd2",  "Confirmed"),
    ("walt",   "e_brock", "Организовал",                          "ToEnd2",  "Confirmed"),
    ("e_brock","ev_ricin","Орудие",                               "ToEnd2",  "Confirmed"),
    ("e_brock","brock",   "Жертва",                               "ToEnd2",  "Confirmed"),
    ("e_brock","jesse",   "Манипуляция (подставил Гуса)",         "ToEnd2",  "Tentative"),
    ("walt",   "e_blast", "Спланировал",                          "ToEnd2",  "Confirmed"),
    ("hector", "e_blast", "Привёл в действие бомбу",              "ToEnd2",  "Confirmed"),
    ("e_blast","gus",     "Гибель",                               "ToEnd2",  "Confirmed"),
    ("hank",   "walt",    "Родство (зять)",                       "Both",    "Tentative"),
    ("hank",   "ev_meth", "Расследует источник",                  "ToEnd2",  "Confirmed"),
    ("hank",   "gus",     "Подозревал",                           "ToEnd2",  "Tentative"),
    ("ev_book","hank",    "Улика: разоблачение Хайзенберга",      "ToEnd2",  "Confirmed"),
    ("walt",   "ev_book", "Оставил книгу дома",                   "ToEnd2",  "Confirmed"),
    ("gale",   "ev_book", "Дарственная надпись «G.B.»",           "ToEnd2",  "Tentative"),
    ("hank",   "jack",    "Перестрелка",                          "Both",    "Tentative"),
    ("jack",   "e_hank",  "Исполнитель",                          "ToEnd2",  "Confirmed"),
    ("e_hank", "hank",    "Жертва",                               "ToEnd2",  "Confirmed"),
]

# ---------------------------------------------------------------------------
# 3. ЗАПИСЬ ФАЙЛОВ
# ---------------------------------------------------------------------------
def write_entities(path="entities.csv"):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Идентификатор", "Подпись", "Тип сущности", "Иконка i2", "Описание"])
        for eid, label, etype, icon, desc in ENTITIES:
            w.writerow([eid, label, etype, icon, desc])

def write_links(path="links.csv"):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow([
            "Конец 1 (подпись)", "Конец 1 тип", "Конец 1 иконка",
            "Конец 2 (подпись)", "Конец 2 тип", "Конец 2 иконка",
            "Связь", "Направление", "Достоверность",
        ])
        for e1, e2, label, direction, strength in LINKS:
            l1, t1, i1 = EMAP[e1][1], EMAP[e1][2], EMAP[e1][3]
            l2, t2, i2_ = EMAP[e2][1], EMAP[e2][2], EMAP[e2][3]
            w.writerow([l1, t1, i1, l2, t2, i2_, label, direction, strength])

if __name__ == "__main__":
    write_entities()
    write_links()
    print(f"Готово: {len(ENTITIES)} сущностей, {len(LINKS)} связей.")
    print("Файлы: entities.csv, links.csv (UTF-8 с BOM, разделитель ';').")
