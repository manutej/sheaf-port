# Start here

Say this to a frontier LLM that has `sheaf-ingest` loaded:

> Take `<this folder>` and build a typed index, a lattice knowledge base,
> and a reusable structure I can run on the next folder.

That is the product. [What a sheaf is](docs/SHEAF.md) · [Glossary](docs/GLOSSARY.md)

## What you should get back

| File | What it is |
|---|---|
| a typed index | parts with locators, records, and only the links you can point at in the source |
| `lattice.json` | picture of that index — drop into [stalks-and-sections](https://github.com/manutej/stalks-and-sections) `docs/examples/` |
| `domain.package.yaml` | reusable structure: what a part is, which fields are shared, how links are found |
| `STRUCTURE.md` | how to rebuild the same index on a sibling folder |

A part is something you can open (a function, a class, a page). A paragraph
is a note about a part, not a part. A link exists only if an `import` or a
markdown link was in the source.

## How the model should do it

Follow [`skills/sheaf-ingest/SKILL.md`](skills/sheaf-ingest/SKILL.md).
It can walk with list / read / grep today. Do not block on a language the
walker does not cover.

If this repo has a working ingest command on your clone:

```bash
PYTHONPATH=src python -m sheaf_port ingest path/to/folder --out ./out
```

If that command is missing, the skill is still the procedure. A fresh clone
as of this writing has the skill and the explanation; the Python walker may
still be landing.

TypeScript monorepos: use stalks-and-sections `npm run sheaf:ingest` for the
lattice, and still write `domain.package.yaml` here so the *structure*
reuses.

## What this is not

- Not “the lattice is teal, so merge.”
- Not “the folder is ported.”
- Not a write-gate. That is a later check, if you ask for one.
- Not a claim that a bag of unrelated files is already a sheaf.
