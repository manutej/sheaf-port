---
name: sheaf-morse
description: >
  Discrete Morse reduction of a bound sheaf. Pair cells along invertible,
  currently-agreeing restrictions; persist the unmatched critical core.
  Φ is evaluated on the core, not the unreduced cochain. Use when the cover
  is larger than INNER_BUDGET can glue, or when Tailor must know which cells
  can actually change Φ. Trigger on "sheaf morse", "morse-reduce", "critical
  cells", "reduce cochain", "Scythe", "/morse-reduce".
---

# sheaf-morse

The **calculator**. Not a decision skill. Not a write gate.

`sheaf-glue` decides. This skill makes the decision cheap and local by
replacing the full cochain with a smaller complex whose cohomology — and
whose Φ bit — are the same.

Conserves: `H•(reduced) ≅ H•(F)` and `Φ(core) == Φ(full)`.
Also conserves Tailor budget: coboundaries that cannot jump are not
recomputed inside INNER_BUDGET.

## Requires

`sheaf-bind` has emitted a `Sheaf` with typed cells, observed edges, and
stalks whose fields are records (not prose). If `morse_core` is already set
and `cover_generation` has not advanced, return it. Cover change (bind
hard rule 7) invalidates the core — recompute, do not patch.

Types: `src/sheaf_port/types.py`. Reducer: `src/sheaf_port/morse.py`.

## Legal pairing

A pair `(cell, edge)` is legal iff all of:

1. `edge.observed` is true (no invented incidence).
2. `shared_fields` is nonempty.
3. Both incident stalks contain every shared field.
4. Types of those fields match (`str` is not `int`).
5. The current restriction **holds** (`src[f] == dst[f]` for every shared `f`).
6. The matching stays acyclic (Forman: no directed cycle of paired faces).
7. After the pair is applied, `Φ(core) == Φ(full)` on the fixture check.

Conditions 3–4 are invertibility of the field-projection restriction.
Condition 5 is why a mismatching overlap **cannot** be paired: those two
cells carry the obstruction and stay critical.

Obstruction-adjacent cells stay unpaired even on a side-edge that happens
to agree. They still support the jump.

## Illegal pairing — raise `MorseError`, do not mutate

- Pair across a restriction failure.
- Pair when a shared field is missing or type-mismatched.
- Pair an unobserved / invented edge.
- Delete a cell and claim it was critical-paired.
- Reuse a Morse core after `cover_generation` advanced (new file, new page).

## Procedure

1. Mark every cell incident to a failing or non-invertible restriction as
   **critical**. These are the support of the jump.
2. On the subgraph of agreeing invertible edges, compute an acyclic matching
   (greedy tree pairing is enough at v0.1). Pair the child; keep one
   representative per agreeing component.
3. Persist `sheaf.morse_core = frozenset(unmatched cell ids)`.
4. Run the quasi-iso check: `Φ` on the full sheaf equals `Φ` on the core
   (restrictions among remaining cells, plus `G_v` of remaining stalks).
5. Hand the reduced sheaf to `sheaf-glue`. Do not glue yourself.

## Emits

```yaml
morse_core: [cell-id, ...]
paired: [{cell: id, edge: [src, dst], reason: invertible-and-agrees}]
refused: [{cell: id, edge: [src, dst], reason: mismatch|noninvertible|cycle|obstruction-adjacent}]
cover_generation: <int>
quasi_iso: true
```

`refused` is not a failure of this skill. It is the critical set.

## MUST NOT

- Delete a cell whose restriction is non-invertible.
- Recompute Φ on the unreduced cover inside INNER_BUDGET when `|X|` is large.
- Treat the Laplacian, a heat flow, or a soft residual as the Morse core.
- Change a stalk field. Morse pairs cells; it does not repair them.
- Accept, commit, or write. There is no Φ decision here.

## On failure

`MorseError` means the requested pairing was illegal. Leave `F` unchanged.
If the cover grew, drop the old core and recompute — do not patch it.

## Compose

```
bind → kernel → localize ∥ preserve → morse → glue ⇄ repair → (harness write rule)
```

`sheaf-cycles` (optional) reads the refused set as vanishing-cycle support.
`sheaf-support` (optional) uses the core as the only place `RΓ` can jump.

Fixtures: `fixtures/morse/legal-pair.json`, `illegal-mismatch.json`,
`illegal-noninvertible.json`. Tests: `tests/test_morse.py`.

## Honesty

Forman discrete Morse theory + Curry–Ghrist–Nanda reduction for sheaf
cohomology justify the pairing rule. This skill implements the **invariance
mechanism** (do not recompute coboundaries that cannot jump). It is not a
claim that Morse homology beats exact CSP on SWE-bench. Batruin’s discovery
gate failed; do not launder that failure through a smaller complex.
