# Start here

Say this to a frontier LLM (or run it yourself):

> Take `<this folder>` and build a typed index, a lattice knowledge base, and a reusable structure I can run on the next folder.

That is the product. Everything else is optional.

## Do it

```bash
git clone https://github.com/manutej/sheaf-port
cd sheaf-port
PYTHONPATH=src python -m sheaf_port ingest path/to/folder --out ./out
```

You get:

| File | What it is |
|---|---|
| `out/lattice.json` | Lattice knowledge base. Drop into [stalks-and-sections](https://github.com/manutej/stalks-and-sections) `docs/examples/` |
| `out/domain.package.yaml` | Reusable structure: what a part is, which fields are shared, how links are observed |
| `out/STRUCTURE.md` | How to rebuild the same index on a sibling folder |

A part is a file:line (a function, a class, a page). A link exists only if an `import` or a markdown link was in the source. Paragraphs are notes, not parts.

## What works in the walker today

- Python folders (functions, classes, imports)
- Markdown folders (pages, `[links]`, `[[wikilinks]]`)
- Mixed folders of those two

TypeScript monorepos: use stalks-and-sections `npm run sheaf:ingest` for the lattice, and still keep `domain.package.yaml` from this repo so the structure is reusable.

## What this is not

Not a write-gate. Not “the folder is ported.” Not permission to merge because the lattice is teal.

The skill that matches the sentence: `skills/sheaf-ingest/SKILL.md`.
