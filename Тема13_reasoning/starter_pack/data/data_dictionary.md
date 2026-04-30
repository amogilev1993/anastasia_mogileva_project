# Data dictionary

## individuals.csv
| Поле | Тип | Описание |
|---|---|---|
| id | string | Идентификатор индивида (используется как имя в OWL) |
| class | enum {Male, Female} | Класс в иерархии Person |
| label | string | Человекочитаемая метка (rdfs:label) |
| note | string | Комментарий, не попадает в OWL |

## relationships.csv
| Поле | Тип | Описание |
|---|---|---|
| subject | string | id индивида-субъекта |
| predicate | enum {hasParent, hasChild, hasAncestor, hasSibling} | Свойство |
| object | string | id индивида-объекта |
| note | string | Комментарий |

В исходных данных намеренно записаны только `hasParent` и `hasSibling` — остальные
свойства должны вывестись reasoner'ом.
