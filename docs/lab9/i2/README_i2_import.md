# Построение схемы преступления в IBM i2 Analyst's Notebook

Тема: сериал **«Во все тяжкие» (Breaking Bad)**.

Этот каталог содержит «код для построения схемы» — генератор данных и сами данные,
готовые к импорту в IBM i2 Analyst's Notebook (ANB).

## Файлы

| Файл | Назначение |
|------|-----------|
| `generate_i2_csv.py` | Скрипт-генератор. Описывает сущности и связи и формирует CSV. |
| `entities.csv` | Каталог из 23 сущностей: персонажи, события, доказательства. |
| `links.csv` | 36 связей в формате «два конца в одной строке» (готово для Import Design). |

Перегенерировать данные: `python generate_i2_csv.py`

## Почему так строят схему в i2

В i2 Analyst's Notebook граф редко рисуют руками. Стандартный промышленный путь —
**импорт структурированных данных** (CSV / Excel / БД) через **Import Design**.
Каждая строка `links.csv` содержит обе сущности-конца, их типы, иконки и параметры
связи. При импорте i2 автоматически:
- создаёт узлы (entities) и склеивает одинаковые по подписи (identity);
- создаёт связи (links) с подписью, направлением и стилем линии;
- расставляет иконки по типам.

## Импорт `links.csv` в i2 ANB (пошагово)

1. **File → New Chart** — создать новую схему.
2. **Import → Import from File** (вкладка *Import*), выбрать `links.csv`.
   - Разделитель полей: **точка с запятой (`;`)**.
   - Кодировка: **UTF-8** (файлы сохранены с BOM, кириллица читается корректно).
3. На шаге **Import Design** выбрать тип строки: **Two entities and a link**
   (каждая строка = две сущности + связь между ними).
4. **Назначить столбцы (Column Actions):**
   - *Конец 1 (подпись)* → **End 1 → Entity → Label / Identity**;
   - *Конец 1 тип* → **End 1 → Entity Type**;
   - *Конец 1 иконка* → **End 1 → Icon** (или сопоставить вручную в Type Mapping);
   - *Конец 2 (подпись)* → **End 2 → Entity → Label / Identity**;
   - *Конец 2 тип* → **End 2 → Entity Type**;
   - *Конец 2 иконка* → **End 2 → Icon**;
   - *Связь* → **Link → Label**;
   - *Направление* → **Link → Direction** (значения `ToEnd2` / `ToEnd1` / `Both` / `None`);
   - *Достоверность* → **Link → Link Strength** (`Confirmed` = сплошная линия,
     `Tentative` = пунктир = косвенная связь).
5. (Опционально) Импортировать `entities.csv` отдельно как **Entities only**,
   чтобы подтянуть поле «Описание» в карточку каждого узла (вкладка *Cards*).
6. **Finish** — i2 построит граф.
7. Применить раскладку: **Arrange → Layout → Peacock / Circular / Hierarchical**
   для читаемого размещения.
8. **Analyze:** инструменты *Find Connecting Network*, *Social Network Analysis*
   (Betweenness) подсветят ключевую фигуру — узел **Уолтер Уайт**.

## Соответствие иконок (Type Mapping)

Если в палитре нет точного имени иконки — сопоставьте на шаге Import Design:

| Значение в CSV | Иконка i2 (рекомендация) |
|----------------|--------------------------|
| `Male` / `Female` | Person (Male / Female) |
| `Law Enforcement` | Law Enforcement Officer |
| `Group` | Group / Organisation |
| `Incident` | Incident / Event |
| `Explosion` | Explosion / Bomb |
| `Drugs` | Drugs |
| `Document` | Document |
| `Poison` | Poison / Biohazard |
| `Office Building` | Office Building |
| `Chemical` | Chemical / Flask |
| `Money` | Money |

## Что отразить в отчёте

- Скриншот импорта (Import Design с назначенными столбцами).
- Скриншот итогового графа (с разной раскладкой).
- Скриншот анализа SNA (выделенный центральный узел — Уолт).
- Пояснение характера связей: сплошные — прямые улики, пунктир — косвенные.
