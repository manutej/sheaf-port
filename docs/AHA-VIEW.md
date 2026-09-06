# Aha view — reuse the lattice, do not redraw it

The 3D explorer already lives in [manutej/stalks-and-sections](https://github.com/manutej/stalks-and-sections). sheaf-port **exports** a bound index into that app’s JSON. It does not grow a second WebGL stack.

Quality bar for a loaded graph: a stranger can point at a terracotta edge and say, in domain words, which shared field broke. If they cannot, the export is decoration.

## What the lattice must show for a ported domain

| Lattice object | sheaf-port object | Engineer reading |
|---|---|---|
| Node | part / cell | One symbol, claim, edge, or holding |
| `dim` | `len(typed record)` | How many fields the gate reads |
| `section` | numeric encoding of those fields | Never Gaussian-filled. Unknown = zero. |
| Edge | observed link | Import, wikilink, citation, … |
| `restrictKind: projection` | shared-field copy | The only comparison the write gate runs |
| Teal edge | shared fields match (and types match) | Safe overlap |
| Terracotta edge | shared fields disagree | The ticket |
| Ring (`known: true`) | pinned / critical part | Reducer may not drop this |
| Hierarchy plane | optional grain / package layer | Code vs tests vs CI; page vs claim vs source |

`residualMeaning` is required and is a domain sentence:

```
"terracotta means two linked symbols disagree on path, symbol, or apiRevision — including type."
```

## Export shape

Target schema: [`stalks-and-sections/docs/examples/sheaf.schema.json`](https://github.com/manutej/stalks-and-sections/blob/main/docs/examples/sheaf.schema.json).

```json
{
  "id": "sheaf-port-codebase-fixture",
  "title": "Tiny auth/api pair",
  "kicker": "Write gate on shared apiRevision",
  "residualMeaning": "Terracotta means auth and api disagree on path, symbol, or apiRevision (value or type).",
  "levels": [
    { "id": 0, "label": "Implementation", "kicker": "symbols the gate reads" },
    { "id": 1, "label": "Checks", "kicker": "tests and oracles" }
  ],
  "nodes": [
    {
      "id": "auth.session",
      "title": "auth.session",
      "kind": "symbol",
      "level": 0,
      "dim": 3,
      "known": true,
      "section": [1, 0, 1],
      "summary": "fields: path, symbol, apiRevision",
      "sources": ["src/auth.py"]
    }
  ],
  "edges": [
    {
      "source": "auth.session",
      "target": "api.handler",
      "relation": "imports",
      "restrictKind": "projection",
      "note": "shared: path, symbol, apiRevision"
    }
  ]
}
```

Rules carried over from the lattice handoff:

- Do not Gaussian-fill missing records. Zero means unknown.
- Every coordinate has a meaning in `summary`.
- Ship at least one designed teal edge and one designed terracotta edge so the scale is readable.
- Validator in stalks-and-sections must exit 0 before we call the view done.

## Dashboard grammar (2D glance, next to the lattice)

meta-mvp section order, bound to the same export:

1. **Hero** — write allowed or refused, in one line.
2. **Glance** — parts, observed links, teal count, terracotta count, oracle ran yes/no.
3. **Map** — the lattice, or a 2D slice of one plane.
4. **Ticket list** — each terracotta edge as `left.field ≠ right.field (string vs int)`.
5. **Accept bit** — the five conjuncts, each a pass/fail. Soft score visible, not in the bit.

No second colour system. Teal / terracotta from the lattice is the only residual scale.

## Commands

```bash
# from sheaf-port, once the exporter lands
PYTHONPATH=src python -m sheaf_port export-lattice \
  --package profiles/codebase.yaml \
  --out /tmp/codebase-lattice.json

# from stalks-and-sections
npm run sheaf:validate -- /tmp/codebase-lattice.json
# drop the file in docs/examples/ and restart the app
```

## What the Aha view is not

- Not a force graph with sheaf words on the tooltip.
- Not a proof that the sampler understands the index.
- Not allowed to treat energy→0 as “write.” Energy is a reading aid. The write gate is discrete.
