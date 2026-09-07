# Start here

Say this to a frontier LLM, or run it yourself:

> Take `<this folder>` and build a typed index, a lattice knowledge base,
> and a reusable structure I can run on the next folder.

[Handoff](HANDOFF.md) · [Agent prompt](AGENT-PROMPT.md) · [What a sheaf is](docs/SHEAF.md) · [Glossary](docs/GLOSSARY.md) · [For agents](AGENTS.md)

## Copy this

```bash
git clone https://github.com/manutej/sheaf-port
cd sheaf-port
python scripts/ingest.py path/to/folder --out ./out
cat out/STRUCTURE.md
```

No pip. Stdlib only.

| File | What it is |
|---|---|
| `out/lattice.json` | Picture of the sheaf. Drop into [stalks-and-sections](https://github.com/manutej/stalks-and-sections) `docs/examples/` |
| `out/domain.package.yaml` | Reusable structure for the next folder |
| `out/STRUCTURE.md` | Rebuild command + what was skipped |
| `out/index.json` | Counts an LLM can read |

A part is a module, function, class, or page you can open. An overlap exists only if an `import` or a markdown link was in the source. Teal = that target is in the folder. Terracotta = it is not.

## What the walker covers today

Python, Markdown, JS/TS relative imports, mixed folders of those.

TypeScript monorepos that need pooling: [stalks-and-sections](https://github.com/manutej/stalks-and-sections) `npm run sheaf:ingest`, and still keep `domain.package.yaml` from this run.

## What this is not

Not a write-gate. Not “the folder is ported.” Not permission to merge because the lattice is teal. Not a knowledge graph with extra words.
