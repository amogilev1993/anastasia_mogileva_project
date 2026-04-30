# Предметная область: Семейные связи (учебная онтология)

## Зачем
Семейные связи — каноничный пример для демонстрации возможностей OWL DL reasoning,
потому что отношения «родитель», «ребёнок», «предок», «сиблинг» естественно ложатся
на четыре характеристики свойств:

- **TransitiveProperty** — `hasAncestor`, `hasParent` (предок предка — тоже предок).
- **InverseObjectProperty** — `hasChild ≡ hasParent⁻¹`.
- **SymmetricProperty** — `hasSibling` (если A — сиблинг B, то B — сиблинг A).
- **rdfs:subPropertyOf** — `hasParent ⊑ hasAncestor`.

## Термины
| Термин | Смысл |
|---|---|
| Person | Базовый класс, любой человек |
| Male / Female | Подклассы, попарно непересекающиеся |
| hasParent | A — потомок B |
| hasChild | A — родитель B |
| hasAncestor | A — потомок B (любого поколения) |
| hasSibling | A и B имеют общего родителя (упрощение) |

## Допущения
1. Моногенетическое моделирование: пол индивида фиксирован, без социальных ролей.
2. Граф семейных связей — DAG (нет циклов «потомок самого себя»).
3. Сиблинги задаются вручную, не выводятся через общего родителя
   (это могло бы потребовать `hasSibling` через property chain, что усложняет ризонинг).
4. Время и место рождения, имена, даты — за пределами скоупа.

## Что считать правильным ответом
- После запуска reasoner должна выполниться непротиворечивость (no inconsistencies).
- Транзитивность `hasAncestor` материализована: для Дмитрия предками выводятся Boris и Anna.
- Инверсия `hasChild` материализована: для Анны выводятся дети Boris и Clara.
- Симметрия `hasSibling` материализована: если задано `Boris hasSibling Clara`,
  то после reasoning есть и обратное.

## Источники
- W3C OWL 2 Primer — <https://www.w3.org/TR/owl2-primer/>
- Owlready2 docs — <https://owlready2.readthedocs.io/>
- Horridge & Bechhofer (2011), *The OWL API: A Java API for OWL ontologies*.
- Lamy J.-B. (2017), *Owlready: Ontology-oriented programming in Python*, AI in Medicine 80.
