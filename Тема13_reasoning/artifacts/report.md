# Тема 13 — Reasoning отчёт

**Использован reasoner:** `HermiT`
**Запросов:** 5
**Inferred facts:** 11

## KPI

| kpi | target | actual | passed | notes |
| --- | --- | --- | --- | --- |
| reasoner_started | >=1 OK in log | HermiT | True | Pellet/HermiT приоритетнее ручного замыкания |
| queries_count | ==5 | 5 | True | 5 SPARQL разной сложности |
| queries_nonempty_after | >=3 | 5 | True | после reasoning |
| inferred_facts | >=3 | 11 | True | новые ABox-тройки между индивидами |
| ontology_consistent | no inconsistent classes | OK | True | ни один класс не выведен в owl:Nothing |

## Запросы (до/после reasoning)

### Q1 — простой: Все индивиды класса Male

```sparql
PREFIX : <http://example.org/family.owl#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>

SELECT ?x WHERE { ?x rdf:type :Male }
```

- **до reasoning:**  `[Boris, Dmitry]`
- **после reasoning:** `[Boris, Dmitry]`
- **новое после reasoning:** `[]`
- **интерпретация:** rdf:type не требует reasoning — Male указан явно у Boris и Dmitry.

### Q2 — транзитивность: Все предки Дмитрия

```sparql
PREFIX : <http://example.org/family.owl#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>

SELECT ?x WHERE { :Dmitry :hasAncestor ?x }
```

- **до reasoning:**  `[]`
- **после reasoning:** `[Anna, Boris]`
- **новое после reasoning:** `[Anna, Boris]`
- **интерпретация:** До reasoning hasAncestor у Dmitry пуст. После — добавляются Boris (по subPropertyOf hasParent⊑hasAncestor) и Anna (по транзитивности).

### Q3 — инверсия: Дети Анны (через hasChild = hasParent⁻¹)

```sparql
PREFIX : <http://example.org/family.owl#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>

SELECT ?x WHERE { :Anna :hasChild ?x }
```

- **до reasoning:**  `[]`
- **после reasoning:** `[Boris, Clara]`
- **новое после reasoning:** `[Boris, Clara]`
- **интерпретация:** До reasoning hasChild не задан явно. После — материализуется как inverse_property от hasParent.

### Q4 — симметрия: Сиблинги Клары

```sparql
PREFIX : <http://example.org/family.owl#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>

SELECT ?x WHERE { :Clara :hasSibling ?x }
```

- **до reasoning:**  `[]`
- **после reasoning:** `[Boris]`
- **новое после reasoning:** `[Boris]`
- **интерпретация:** До reasoning только Boris→Clara. После — symmetric делает обратное Clara→Boris.

### Q5 — цепочка / смешанный: Внуки Анны

```sparql
PREFIX : <http://example.org/family.owl#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>

SELECT ?x WHERE { :Anna :hasChild ?y . ?y :hasChild ?x }
```

- **до reasoning:**  `[]`
- **после reasoning:** `[Dmitry, Elena]`
- **новое после reasoning:** `[Dmitry, Elena]`
- **интерпретация:** Цепочка hasChild∘hasChild требует, чтобы оба hasChild были выведены reasoner'ом из inverse hasParent. Внуки Анны: Dmitry, Elena.

## Inferred facts (с указанием правила)

### inverse_property  (4)
- `Anna hasChild Boris`
- `Anna hasChild Clara`
- `Boris hasChild Dmitry`
- `Clara hasChild Elena`

### subPropertyOf+transitive  (6)
- `Boris hasAncestor Anna`
- `Clara hasAncestor Anna`
- `Dmitry hasAncestor Anna`
- `Dmitry hasAncestor Boris`
- `Elena hasAncestor Anna`
- `Elena hasAncestor Clara`

### symmetric  (1)
- `Clara hasSibling Boris`

## Ограничения

- ABox мал (5 индивидов) — для иллюстративных целей.
- `hasSibling` задан явно, не выводится через property chain.
- Атрибуты (имя/дата/место) сознательно вне скоупа.
- При отсутствии Java reasoning делается ручным замыканием.