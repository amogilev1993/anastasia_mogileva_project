# Competency Questions (CQ)

Вопросы, на которые онтология должна уметь отвечать после reasoning.

| ID | Вопрос | Покрытие свойствами | В ноутбуке |
|---|---|---|---|
| CQ1 | Кто из индивидов является мужчиной? | rdf:type | Q1 |
| CQ2 | Кто все предки Дмитрия (любого поколения)? | hasAncestor (transitive) | Q2 |
| CQ3 | У кого Анна — родитель (т.е. кто её дети)? | hasChild (inverse) | Q3 |
| CQ4 | Кто сиблинги Клары? | hasSibling (symmetric) | Q4 |
| CQ5 | Кто внуки Анны? | hasChild ∘ hasChild (chain) | Q5 |
| CQ6 | Является ли Дмитрий потомком Анны? | hasAncestor через цепочку | косвенно через Q2 |
| CQ7 | Все ли женщины являются Person? | subClassOf | вне SPARQL, проверка иерархии |
| CQ8 | Существует ли в графе несогласованность? | consistency check | через sync_reasoner |
