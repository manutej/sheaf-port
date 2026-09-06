---
name: sheaf-bind
description: >
  Domain adapter for sheaf-port. Turn an interconnected source (repo, wiki,
  knowledge graph, corpus, sensor/dep graph) into a finite cellular sheaf:
  cells with locators, typed stalks, restriction as field projection, observed
  incidence only. The only domain-specific surface in the plugin. Use when the
  user says bind this repo, bind this wiki, instantiate a knowledge sheaf,
  port the harness onto a domain, or supplies a domain.package.yaml.
  Trigger on "sheaf-bind", "/sheaf-port", "domain package", "typed stalks",
  "free-text is not a stalk", "observed incidence".
---

# sheaf-bind

The **port**. Everything above this skill is domain-blind. Everything below it
is a product skin.

This skill does **not** glue, repair, Morse-reduce, or commit. It emits `F`
as a site + typed sheaf so `sheaf-kernel` can occupy the cover.

Types live in `src/sheaf_port/types.py`. Schema lives in
`schemas/domain.package.yaml`. Profiles live in `profiles/`.

## Conserved quantity

Cell identity and observed incidence. A cell without a locator is not a cell.
An edge that was not seen in the source is not an overlap. Free text is
evidence *about* a stalk, never the stalk.

## Input

A `domain.package.yaml` that fills `DomainPackage`:

```yaml
id: <domain-id>
cells_from: <locator rule>
cover_from: <incidence rule>
stalk_schema: [<typed field names>]
shared_fields: [<fields glue will compare>]
mediators: [<nuisance interiors repair may quotient>]
critical_lenses: [<deterministic oracles>]
soft_lenses: [<judges>]
oracle: <executable command>
grain: <symbol | claim | edge | holding | custom>
grain_min: 2
grain_max: 10000
min_observed_edges: 1
three_sheaves:
  knowledge: <what memory tracks>
  capability: <what Φ commits>
  conservation: <what the loop conserves>
forbidden:
  - train_restriction_maps
  - accept_on_H1
  - treat_embedding_as_stalk
  - invent_edges
```

`shared_fields` must be a non-empty subset of `stalk_schema`.
Embeddings, prose, and RAG chunks belong in `Stalk.evidence`, never in
`shared_fields`.

## Output

A `Sheaf`:

- `cells[id] = Cell(id, kind, locator)` — locator is a resolvable source address
- `stalks[id] = Stalk(cell_id, fields, g_v, evidence, sheaf_role)` — `fields`
  keys ⊆ `stalk_schema`
- `edges` — only `observed=True`; `shared_fields` copied from the package
- `schema` — the package `stalk_schema`
- `package_id`, `cover_generation = 0`, `morse_core = None`

Restriction on an edge `vw` is the field projection

```
ρ(s) = { k: s.fields[k] for k in edge.shared_fields }
```

Functoriality is required on the cover poset: composing two projections is
the projection onto the deeper shared fields. Bind must not invent a ρ that
is not a projection.

## Workflow

1. Load and validate the package (`load_package` / `validate_package`).
2. Walk the source with `cells_from`. Reject any candidate missing a locator.
3. Walk the source with `cover_from`. Keep an edge only with a cited incidence
   (import, call, wikilink, FK, citation, adjacency, shared declared field).
4. Allocate typed stalks. Put prose, summaries, embeddings in `evidence`.
5. Check grain: `grain_min ≤ |cells| ≤ grain_max` and `|edges| ≥ min_observed_edges`.
6. Emit `F`. Hand it to `sheaf-kernel`. Do not run Φ here.

## Hard rules

1. Free text is not a stalk. A README paragraph, docstring, RAG chunk, or
   tweet-length summary is evidence. BindError if it is placed in `fields`.
2. Do not invent edges. Complete-graph “to be safe” is domain leak (A4).
3. Empty `shared_fields` fails bind. Glue would have nothing exact to check.
4. Embeddings are a soft lens on the knowledge sheaf. They are never a
   shared field of the capability sheaf.
5. L-C-O-P-V is a CETI profile, not a kernel constant. A codebase profile
   uses `{path, symbol, apiRevision}` (and friends). A wiki profile uses
   `{claimId, sourceId}`. Do not force five CETI vertices onto a foreign site.
6. A port is a functor. Restriction after transport equals transport of
   restriction. If the adapter drops a shared field, Φ on the image is not
   Φ on the source — refuse the package.
7. Cover change increments `cover_generation` and invalidates `morse_core`.
8. Three sheaves stay apart. Knowledge-sheaf consistency is not capability Φ.
9. Bind does not run the oracle. Glue does. Bind only records `oracle`.

## MUST NOT

- Treat a vector store as a cover.
- Train ρ, or emit a learned map in place of a field projection.
- Reuse stalks from package A on package B without an explicit restriction
  (tell-apart / A12).
- Call the bind “ported” without a `sheaf-adversary` battery log.
- Special-case CETI inside this skill. CETI occupies the loop *after* a
  domain is bound.

## Worked profiles

| Package | Cells | Cover | Shared fields | Oracle |
|---|---|---|---|---|
| `profiles/codebase.yaml` | symbols | import + call graph | path, symbol, apiRevision | test runner |
| `profiles/wiki.yaml` | claims | wikilink + backlink | claimId, sourceId | link checker |
| `profiles/kg.yaml` | typed edges | incident schema edges | src, rel, dst | schema validator |
| `profiles/corpus.yaml` | holdings | citation / issue graph | holdingId, authority, pinpoint | citation resolver |

Grain failures:

- Too coarse: two independent contracts share one cell → false Φ failure.
- Too fine: every sentence is a cell → Morse core explodes.
  Bind records both as failed ports until grain is stable. That is attack L.

## Requires

A source the locator schema can address, and a `domain.package.yaml`.
A bag of unrelated blobs is not a domain.

## On failure

Raise `BindError` with the attack id when one applies (A1 false stalk, A4
invented edge, A12 identity collision, L grain). Do not emit a partial sheaf
and hope glue will catch it. Bind is the gate that keeps free-text out of Φ.

## Compose

```
/sheaf-port <domain.package.yaml>
        │
        ▼
   sheaf-bind          this skill
        │
        ▼
   sheaf-kernel        type the cover; confirm overlaps against the source
   sheaf-localize ∥ sheaf-preserve
        │
        ▼
   sheaf-morse         reduce before Tailor when |X| is large
   sheaf-glue ⇄ sheaf-repair
   noether-harness     dual-loop runtime
```

Eval: `sheaf-adversary`. A domain is ported only after the battery log.

## Honesty

Present bind as a **runtime-checked functor plus oracles**, not a theorem
that any dataset is a sheaf. Batruin’s discovery gate failed. Φ is a
contract on the bound sheaf, not a claim about the sampler. This skill
implements the adapter surface, not a cohomological lift of SWE-bench.
