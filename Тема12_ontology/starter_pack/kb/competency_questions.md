# Competency Questions (CQ)

CQ — это вопросы, на которые онтология должна давать ответ. Каждый вопрос проверяется
запросом / итерацией по индивидам в ноутбуке.

| ID | Вопрос | Что покрывает |
|---|---|---|
| CQ1 | Какие курсы изучает студент Alice? | enrolledIn, Student, Course |
| CQ2 | Кто преподаёт курс ML101? | teaches / taughtBy (инверсное), Course |
| CQ3 | На какой кафедре числится профессор Smith? | memberOf, Professor → Department |
| CQ4 | Какие аспиранты у профессора Smith? | supervises, PhDStudent |
| CQ5 | Какие кафедры входят в факультет инженерии? | partOf, Department → Faculty |
| CQ6 | Какие публикации у профессора Smith? | hasAuthor (inverse), Publication |
| CQ7 | В каких аудиториях проходит курс DB201? | heldIn, Course → Room |
| CQ8 | Какие курсы предлагает кафедра CS? | offeredBy (inverse), Course → Department |
| CQ9 | Сколько кредитов даёт курс ML101? | hasCredits (DataProperty) |
| CQ10 | Кто работает над проектом AIProject? | worksOnProject |

## Покрытие по моделям представления знаний

- Иерархия классов (is-a) проверяется CQ1, CQ2, CQ3 (через типы).
- Объектные свойства проверяются CQ1, CQ2, CQ4, CQ5, CQ6, CQ7, CQ8, CQ10.
- Data-свойства проверяются CQ9.
- Инверсные свойства проверяются CQ2 (taughtBy инверсен teaches), CQ6 (hasAuthor inverse).
