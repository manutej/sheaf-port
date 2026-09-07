---
name: sheaf-port
audience: llm
purpose: map of this repo so an agent can ingest a folder without asking the user to teach it topology
---

# AGENTS.md — read this first if you are a model

You are being asked to take a folder, repo, or wiki and produce a sheaf:
a typed index of parts, a lattice knowledge base, and a reusable package.

## Do this

```bash
python scripts/ingest.py <folder> --out ./out
```

Emit, or load if they already exist:

- `out/lattice.json` — nodes + edges. Teal residual 0 = import/link resolves. Terracotta residual > 0 = dangling.
- `out/domain.package.yaml` — reusable structure (grain, shared fields, rebuild command)
- `out/STRUCTURE.md` — human rebuild notes
- `out/index.json` — counts

If `scripts/ingest.py` is missing, follow `skills/sheaf-ingest/SKILL.md` with list/read/grep and write the same four files by hand. Do not invent links.

## Topology of the idea (short)

```
folder
  ─ parts          modules, symbols, pages     (must have a locator)
  ─ records        path, symbol, module        (not paragraph text)
  ─ overlaps       import / markdown link      (must have evidence)
  ─ comparison     does the target exist here?
        ├ teal           yes — resolved
        └ terracotta     no  — dangling
package.yaml       how to do this to the next folder
lattice.json       how to look at this folder
```

A graph is parts + links.
A sheaf is parts + per-part records + a comparison rule on observed overlaps.
This v0 comparison rule is: *does the named target resolve in the folder?*
A later write-gate (optional) asks a stricter question: do shared field *values* match, including type, and did tests run?

## Topology of this repo

```
START.md                 product sentence
HANDOFF.md               colleague path (you are here-adjacent)
AGENTS.md                this file
docs/SHEAF.md            concept, 90 seconds + one level deeper
docs/GLOSSARY.md         words, both concept and product
docs/REFERENCES.md       papers + sibling repos
docs/EXPLAIN-ATTACKS.md  slogans the explanation must refuse
skills/sheaf-ingest/     LLM procedure for the product sentence
skills/sheaf-bind/       rules for a legal index (no chunks as parts)
skills/sheaf-morse/      skip parts that cannot disagree
scripts/ingest.py        out-of-box walker (stdlib)
profiles/                starting packages for code / wiki / kg / corpus
src/sheaf_port/          reference runtime — may lag scripts/ingest.py
```

Sibling explorer: https://github.com/manutej/stalks-and-sections
Put `lattice.json` in that repo's `docs/examples/` and restart the app.

## MUST NOT

- Treat a paragraph, README blob, or embedding as a part
- Invent edges so the graph looks connected
- Fill `section` vectors with random numbers
- Call the folder ported
- Treat teal / energy as permission to write
- Ask the user to define “sheaf” before walking — infer grain and proceed
- Merge LangChain.js lattices with this repo's lattices

## Done when

Someone can open two locators and see why an edge exists.
Someone can re-run the same package on a sibling folder.
`lattice.json` has a one-sentence `residualMeaning` in domain English.
`STRUCTURE.md` lists what was skipped.
