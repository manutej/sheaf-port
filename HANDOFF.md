# Handoff — point this at a repo today

You are taking over sheaf-port. The job is not to re-explain sheaves.
The job is: **folder in, usable lattice out.**

## 90-second start

```bash
git clone https://github.com/manutej/sheaf-port
cd sheaf-port
python scripts/ingest.py . --out ./out
```

Open:

| File | Use it for |
|---|---|
| `out/STRUCTURE.md` | Human summary: parts, teal/terracotta, rebuild command |
| `out/lattice.json` | Drop into [stalks-and-sections](https://github.com/manutej/stalks-and-sections) `docs/examples/` and restart that app |
| `out/domain.package.yaml` | Reusable rule for the *next* folder of this kind |
| `out/index.json` | Counts an LLM can read without the lattice |

That command is stdlib only. No pip. No missing `bind.py`.

Then point it at the colleague's repo:

```bash
python scripts/ingest.py /path/to/their/repo --out ./out-their-repo
```

What works without extra setup: **Python**, **Markdown**, **JS/TS** (relative imports).  
What does not: compiled binaries, a 10k-file monorepo without `--cap`, treating `node_modules` as parts (skipped).

## What “usable” means

After one run you can:

1. Name two files that import each other (open the locators).
2. Point at a terracotta edge and say “this import or markdown link does not resolve in the folder.”
3. Re-run the same command on a sibling folder and get the same field names.

If every edge is terracotta, the walker failed to resolve imports (report it; do not call the folder “ported”).
If every edge is teal and the folder has known broken imports, the walker missed them.

## Read in this order

1. This file
2. [START.md](START.md) — the product sentence
3. [docs/SHEAF.md](docs/SHEAF.md) — what a sheaf is, 90 seconds
4. [docs/GLOSSARY.md](docs/GLOSSARY.md) — words
5. [AGENTS.md](AGENTS.md) — LLM-readable map of the repo
6. [docs/REFERENCES.md](docs/REFERENCES.md) — papers and sibling repos
7. [skills/sheaf-ingest/SKILL.md](skills/sheaf-ingest/SKILL.md) — if you are the model walking by hand

## Related surfaces (do not merge them)

| Repo | Use |
|---|---|
| this repo | folder → typed index + lattice + reusable package |
| [stalks-and-sections](https://github.com/manutej/stalks-and-sections) | 3D explorer + richer TS ingest (`npm run sheaf:ingest`) |
| [ceti-explainer](https://github.com/manutej/ceti-explainer) | live `/sheaf-run` loop for CETI films, not arbitrary repos |
| [meta-suite](https://github.com/manutej/meta-suite) | reusable *structure* pattern this package copies |

## Do not do on day one

- Do not treat teal as permission to merge.
- Do not run `pip install -e .` and expect `python -m sheaf_port` until `src/sheaf_port/ingest.py` exists on your clone. Use `scripts/ingest.py` first.
- Do not ingest `node_modules`.
- Do not rewrite the glossary into cohomology.
