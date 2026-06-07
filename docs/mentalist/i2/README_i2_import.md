# Построение схемы преступления в IBM i2 Analyst's Notebook

Сериал **«Менталист»** (The Mentalist), сквозная арка **Red John**.

## Файлы
| Файл | Назначение |
|------|-----------|
| `generate_i2_csv.py` | Скрипт-генератор данных. |
| `entities.csv` | Каталог из 25 сущностей: детективы, подозреваемые, события, улики. |
| `links.csv` | 40 связей в формате «два конца в одной строке» (для Import Design). |

Перегенерировать: `python generate_i2_csv.py`

## Импорт `links.csv` (по этапам мастера импорта i2)
1. **File → New Chart**.
2. **Import → Import from File**, выбрать `links.csv`.
3. **Define Columns**: разделитель — **Semicolon (`;`)**, кодировка — **UTF-8**, текст-квалификатор — `"`. Должно получиться **9 столбцов**.
4. **Select Rows**: отметить «первая строка — заголовки» (останется 40 строк).
5. **Column Actions**: ничего менять не нужно (все столбцы — Text).
6. **Select Design**: тип строки — **Two entities and a link** (две сущности + связь).
7. **Assign Columns** — назначить столбцы:
   - `Конец 1 (подпись)` → End 1 **Identity / Label**
   - `Конец 1 тип` → End 1 **Entity Type**
   - `Конец 1 иконка` → End 1 **Icon**
   - `Конец 2 (подпись)` → End 2 **Identity / Label**
   - `Конец 2 тип` → End 2 **Entity Type**
   - `Конец 2 иконка` → End 2 **Icon**
   - `Связь` → Link **Label**
   - `Направление` → Link **Direction** (`ToEnd2` / `ToEnd1` / `Both` / `None`)
   - `Достоверность` → Link **Link Strength** (`Confirmed` = сплошная, `Tentative` = пунктир)
8. **Import Details**: слияние одинаковых узлов **по Identity**, добавить в новую схему. **Finish**.
9. **Arrange → Layout → Circular** — круговая раскладка.
10. **Analyze → Social Network Analysis → Betweenness** — подсветит центральные узлы: **Патрик Джейн** и **Red John**.

## Маппинг иконок (Type Mapping)
| Значение в CSV | Иконка i2 |
|----------------|-----------|
| `Male` / `Female` | Person (Male / Female) |
| `Unknown Person` | Unknown / Anonymous Person |
| `Organisation` | Organisation |
| `Group` | Group |
| `Incident` | Incident / Event |
| `Symbol` | Symbol / Sign |
| `Document` | Document |
| `Note` | Note / Text Block |

## Для отчёта
Сделай скриншоты: окно **Assign Columns**, готовый граф (круговая раскладка), результат **SNA** (выделенные центральные узлы Джейн и Red John).
