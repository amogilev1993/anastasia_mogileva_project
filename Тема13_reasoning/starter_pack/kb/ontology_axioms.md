# Аксиомы онтологии

## TBox (классы и свойства)
- `Male ⊑ Person`
- `Female ⊑ Person`
- `Male ⊓ Female ⊑ ⊥` (попарно непересекающиеся)
- `hasAncestor`: TransitiveProperty
- `hasParent`: TransitiveProperty, `hasParent ⊑ hasAncestor`
- `hasChild`: `hasChild ≡ hasParent⁻¹`
- `hasSibling`: SymmetricProperty
- domain/range всех object properties: Person

## ABox (индивиды и факты)
- `Anna : Female`
- `Clara, Elena : Female`
- `Boris, Dmitry : Male`
- `Boris hasParent Anna`
- `Clara hasParent Anna`
- `Dmitry hasParent Boris`
- `Elena hasParent Clara`
- `Boris hasSibling Clara`

## Что должно вывестись reasoner'ом
1. `Anna hasChild Boris`, `Anna hasChild Clara` — из inverse_property.
2. `Boris hasChild Dmitry`, `Clara hasChild Elena` — из inverse_property.
3. `Clara hasSibling Boris` — из symmetric.
4. `Boris hasAncestor Anna`, `Clara hasAncestor Anna` — из subPropertyOf.
5. `Dmitry hasAncestor Boris`, `Elena hasAncestor Clara` — из subPropertyOf.
6. `Dmitry hasAncestor Anna`, `Elena hasAncestor Anna` — из transitive + subPropertyOf.
