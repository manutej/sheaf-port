---
name: sheaf-ingest
description: >-
  Take a folder, repo, wiki, or knowledge base and build a typed index of its
  parts, a lattice you can open, and a reusable package so the next folder
  uses the same structure. Use when the user says "take this codebase and
  create a sheaf", "build a lattice knowledge base", "ingest this folder",
  "make a reusable structure from this repo", or "index this wiki." Do not
  use for a one-file edit or a chat Q&A. Do not treat paragraphs or
  embeddings as parts. Do not invent links.
---

# sheaf-ingest

The product sentence:

> Take this folder / repo / knowledge base. Build a typed index. Draw it as a lattice. Leave a structure you can run on the next folder.

That is this skill. A later write-gate is optional.

## What you emit (always these four)

| User said | File | What it is |
|---|---|---|
| create a sheaf | `index` / bound parts | parts with locators + typed fields + observed links only |
| lattice knowledge base | `lattice.json` | drop into [stalks-and-sections](https://github.com/manutej/stalks-and-sections) `docs/examples/` |
| reusable structure | `domain.package.yaml` | what a part is, shared fields, how links are observed |
| repeatable | `STRUCTURE.md` | rebuild command + what was skipped |

## Procedure

1. Look at the folder. Infer kind: Python code, Markdown wiki, TypeScript monorepo, or mixed. State the assumption in one line.
2. Walk parts with locators you can open (`path:symbol` or `page#heading`). Skip `node_modules`, `dist`, `.git`, binaries.
3. Walk overlaps only with evidence: `import` / `from X import`, `[text](path)`, `[[page]]`, a citation key. No complete graph.
4. Shared fields default to `{path, symbol}` for code and `{page, title}` for markdown. Prose goes in evidence, never in those fields.
5. Write the four files. `residualMeaning` on the lattice is one sentence in the domain ("these two symbols disagree on path").
6. Tell the user how to rebuild on a sibling folder using the same `domain.package.yaml`.

### Speedups if the tooling is present

- Python / Markdown folder in this repo:
  `PYTHONPATH=src python -m sheaf_port ingest <folder> --out <out-dir>`
- TypeScript monorepo in [stalks-and-sections](https://github.com/manutej/stalks-and-sections):
  `npm run sheaf:ingest -- --job job.json`
  Still write `domain.package.yaml` here so the *structure* is reusable.

If those commands are missing, do the walk with list/read/grep. Do not block the skill on a walker covering Go or Rust.

## MUST NOT

- Treat a paragraph, README blob, or embedding as a part
- Invent links so the graph looks connected
- Fill lattice sections with random numbers
- Call the folder "ported"
- Treat teal / energy as permission to write
- Ask the user questions — infer grain and proceed

## Done when

- Someone can open two locators and see why an edge exists
- Someone can point `domain.package.yaml` at a sibling folder and get the same field names
- `lattice.json` has a one-sentence `residualMeaning` in domain English
- `STRUCTURE.md` lists what was skipped

## Honesty

This skill builds the index, the lattice, and the reusable package. It does not refuse writes. That is a later check if they ask for a write gate.
