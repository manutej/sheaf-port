# sheaf-bind package contract

Source of types: `src/sheaf_port/types.py`.

## DomainPackage → Sheaf

`bind(package, source) -> Sheaf | BindError`

`source` is a walker the profile understands (repo tree, wiki dump, edge list,
corpus index). Bind does not crawl an undocumented blob.

## Validation order

1. `id` set.
2. `stalk_schema` non-empty; every name is an identifier, not a sentence.
3. `shared_fields` non-empty and ⊆ `stalk_schema`.
4. `oracle` is a non-empty command string.
5. Every `forbidden` token from the schema is present or inherited.
6. Walk cells. Each `Cell.locator` must be non-empty and unique.
7. Walk edges. `observed` must be True. Cite the incidence.
8. Grain window. `|cells|` in `[grain_min, grain_max]`. `|edges| >= min_observed_edges`.
9. No `fields` key outside `stalk_schema`. No embedding / prose key in `shared_fields`.
10. `three_sheaves` has knowledge, capability, conservation as distinct strings.

## Functor law

Let T be the transport encoded by the package. For every observed overlap U → V:

```
ρ_{T(U) ← T(V)} ∘ T = T ∘ ρ_{U ← V}
```

Operationally: shared fields on the image are exactly the transported shared
fields of the source. Dropping a field to “fit the film” or “fit the tweet”
breaks the law. That content goes in `evidence[]`.

## Cover generation

Adding or deleting a cell increments `cover_generation` and sets
`morse_core = None`. Φ on a stale core is not Φ on the enlarged sheaf.
