# -*- coding: utf-8 -*-
"""
Генератор данных для схемы преступления в IBM i2 Analyst's Notebook.
Сериал «Менталист» (The Mentalist), сквозная арка Red John.

Формирует:
  entities.csv — каталог сущностей (узлов);
  links.csv    — связи в формате «два конца в одной строке» для Import Design.
Кодировка UTF-8 с BOM, разделитель «;».
"""
import csv

ENTITIES = [
    # id            Подпись                                Тип             Иконка i2          Описание
    ("jane",   "Патрик Джейн",                  "Детектив",      "Male",            "Консультант-менталист CBI, ведёт охоту на Red John"),
    ("lisbon", "Тереза Лисбон",                 "Детектив",      "Female",          "Старший агент CBI"),
    ("cho",    "Кимбелл Чо",                    "Детектив",      "Male",            "Агент CBI"),
    ("rigsby", "Уэйн Ригсби",                   "Детектив",      "Male",            "Агент CBI"),
    ("vanpelt","Грейс Ван Пелт",                "Детектив",      "Female",          "Агент CBI"),
    ("redjohn","Red John (Кровавый Джон)",      "Преступник",    "Unknown Person",  "Серийный убийца, лидер тайной сети"),
    ("blake",  "«Ассоциация Блейка»",           "Организация",   "Organisation",    "Тайная сеть сообщников Red John"),
    ("mcallister","Томас Макаллистер (шериф)",  "Подозреваемый", "Male",            "Шериф — оказался Red John"),
    ("bertram","Гейл Бертрам",                  "Подозреваемый", "Male",            "Директор CBI"),
    ("kirkland","Боб Киркланд",                 "Подозреваемый", "Male",            "Агент Нацбезопасности"),
    ("stiles", "Брет Стайлз",                   "Подозреваемый", "Male",            "Лидер культа «Визуализируй»"),
    ("haffner","Рэймонд Хаффнер",               "Подозреваемый", "Male",            "Глава охранной фирмы"),
    ("smith",  "Рид Смит",                      "Подозреваемый", "Male",            "Агент ФБР"),
    ("partridge","Бретт Партридж",              "Подозреваемый", "Male",            "Криминалист CBI"),
    ("family", "Семья Джейна (Анджела и Шарлотта)", "Жертва",    "Group",           "Жена и дочь Джейна, убиты Red John"),
    # События
    ("e_provoke","Оскорбление Red John в эфире","Событие",       "Incident",        "Джейн публично унизил убийцу — спусковой крючок"),
    ("e_murder","Убийство семьи Джейна",        "Событие",       "Incident",        "Месть Red John"),
    ("e_mole", "Крот Red John в CBI",           "Событие",       "Incident",        "Внутренний агент сети в бюро"),
    ("e_handshake","Рукопожатие Джейна и убийцы","Событие",      "Incident",        "Личный контакт, ставший уликой памяти"),
    ("e_final","Разоблачение и гибель Макаллистера","Событие",   "Incident",        "Финальная развязка арки"),
    # Доказательства
    ("ev_smiley","Кровавый смайлик на стене",   "Доказательство","Symbol",          "Фирменный почерк убийцы"),
    ("ev_poem","Стих У. Блейка «Tyger»",        "Доказательство","Document",        "Литературный ключ к личности Red John"),
    ("ev_list","Список семи подозреваемых",     "Доказательство","Document",        "Перечень главных подозреваемых Джейна"),
    ("ev_mark","Метка членов Ассоциации Блейка","Доказательство","Symbol",          "Опознавательный знак сети"),
    ("ev_detail","Запомнившаяся деталь встречи","Доказательство","Note",            "Примета, которую Джейн вспомнил"),
]
EMAP = {e[0]: e for e in ENTITIES}

LINKS = [
    ("jane","lisbon","Партнёры, доверие","Both","Confirmed"),
    ("lisbon","cho","Руководит","Both","Confirmed"),
    ("lisbon","rigsby","Руководит","Both","Confirmed"),
    ("lisbon","vanpelt","Руководит","Both","Confirmed"),
    ("rigsby","vanpelt","Личные отношения","Both","Tentative"),
    ("jane","e_provoke","Спровоцировал","ToEnd2","Confirmed"),
    ("e_provoke","e_murder","Месть убийцы","ToEnd2","Confirmed"),
    ("redjohn","e_murder","Исполнитель","ToEnd2","Confirmed"),
    ("e_murder","family","Жертвы","ToEnd2","Confirmed"),
    ("jane","redjohn","Личная охота (вендетта)","Both","Confirmed"),
    ("e_murder","ev_smiley","Оставлен почерк","ToEnd2","Confirmed"),
    ("redjohn","ev_smiley","Фирменный знак","ToEnd2","Confirmed"),
    ("partridge","ev_smiley","Первым изучил","ToEnd2","Tentative"),
    ("jane","ev_poem","Разгадал отсылку","ToEnd2","Confirmed"),
    ("ev_poem","redjohn","Ключ к личности","ToEnd2","Confirmed"),
    ("e_handshake","jane","Запомнил деталь","ToEnd2","Confirmed"),
    ("redjohn","e_handshake","Контакт","ToEnd2","Tentative"),
    ("ev_detail","mcallister","Примета совпала","ToEnd2","Tentative"),
    ("jane","ev_detail","Вспомнил","ToEnd2","Confirmed"),
    ("jane","ev_list","Составил список","ToEnd2","Confirmed"),
    ("ev_list","mcallister","В списке","ToEnd2","Confirmed"),
    ("ev_list","bertram","В списке","ToEnd2","Confirmed"),
    ("ev_list","kirkland","В списке","ToEnd2","Confirmed"),
    ("ev_list","stiles","В списке","ToEnd2","Confirmed"),
    ("ev_list","haffner","В списке","ToEnd2","Confirmed"),
    ("ev_list","smith","В списке","ToEnd2","Confirmed"),
    ("ev_list","partridge","В списке","ToEnd2","Confirmed"),
    ("redjohn","blake","Покровитель / лидер","ToEnd2","Confirmed"),
    ("blake","bertram","Член сети","ToEnd2","Tentative"),
    ("blake","kirkland","Член сети","ToEnd2","Tentative"),
    ("blake","haffner","Член сети","ToEnd2","Tentative"),
    ("blake","smith","Член сети","ToEnd2","Tentative"),
    ("ev_mark","blake","Опознавательный знак","ToEnd2","Confirmed"),
    ("e_mole","blake","Связан с сетью","ToEnd2","Tentative"),
    ("e_mole","vanpelt","Крот — жених Ван Пелт","ToEnd2","Tentative"),
    ("mcallister","redjohn","ОКАЗАЛСЯ Red John","ToEnd2","Confirmed"),
    ("jane","e_final","Вычислил и устранил","ToEnd2","Confirmed"),
    ("e_final","mcallister","Разоблачён","ToEnd2","Confirmed"),
    ("stiles","jane","Манипуляции / помощь","ToEnd2","Tentative"),
    ("smith","jane","Курировал в ФБР","ToEnd2","Tentative"),
]

def write_entities(path="entities.csv"):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Идентификатор", "Подпись", "Тип сущности", "Иконка i2", "Описание"])
        for eid, label, etype, icon, desc in ENTITIES:
            w.writerow([eid, label, etype, icon, desc])

def write_links(path="links.csv"):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Конец 1 (подпись)", "Конец 1 тип", "Конец 1 иконка",
                    "Конец 2 (подпись)", "Конец 2 тип", "Конец 2 иконка",
                    "Связь", "Направление", "Достоверность"])
        for e1, e2, label, direction, strength in LINKS:
            a, b = EMAP[e1], EMAP[e2]
            w.writerow([a[1], a[2], a[3], b[1], b[2], b[3], label, direction, strength])

if __name__ == "__main__":
    write_entities(); write_links()
    print(f"Готово: {len(ENTITIES)} сущностей, {len(LINKS)} связей.")
