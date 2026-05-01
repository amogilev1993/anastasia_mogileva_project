# Data dictionary

## individuals.csv

| Колонка | Тип | Описание |
|---|---|---|
| id | string | Идентификатор индивида (используется как имя в OWL). |
| class | string | Класс из иерархии онтологии (Student, Professor, Course, …). |
| name | string | Человеко-читаемое имя/название (rdfs:label). |
| email | string \| empty | Email (только для Person). |
| age | int \| empty | Возраст (только для Person). |
| extra | string | Доп. атрибуты в формате `key=value`, напр. `credits=6`, `year=2024`. |

## relationships.csv

| Колонка | Тип | Описание |
|---|---|---|
| subject | string | id индивида (subject триплета). |
| property | string | имя ObjectProperty онтологии. |
| object | string | id индивида (object триплета). |

## Замечание
DataProperties (hasName, hasEmail, hasAge, hasCredits, hasYear) хранятся
**в `individuals.csv`** (колонки name/email/age/extra).
ObjectProperties — **в `relationships.csv`**.
