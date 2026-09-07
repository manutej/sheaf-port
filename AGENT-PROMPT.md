# Paste this to an agent

You are looking at **sheaf-port** (`github.com/manutej/sheaf-port`).
Your job is to ingest a *different* target folder and emit four files.

## Prompt (copy everything in the box)

```
Read these files from the sheaf-port repo, in order:
1. AGENTS.md
2. skills/sheaf-ingest/SKILL.md
3. HANDOFF.md
4. docs/SHEAF.md   (only if you need the concept)

Target to ingest: TARGET_PATH_OR_CLONE

Do exactly this:
- Run: python scripts/ingest.py TARGET_PATH_OR_CLONE --out ./out
- If the script cannot run, walk the target with list/read/grep.
  A part is a module, function, class, or page with a locator you can open.
  A link exists only if the source shows an import or a markdown link.
  Do not invent links. Do not treat README paragraphs as parts.
- Write:
  out/STRUCTURE.md
  out/index.json
  out/lattice.json
  out/domain.package.yaml
- Quote STRUCTURE.md in your reply.
- Teal = the import or markdown link resolves inside the target folder.
  Terracotta = it does not. Colour is not permission to merge.
- Do not call the folder “ported.”
- Do not run pip install or python -m sheaf_port.
```

Replace `TARGET_PATH_OR_CLONE` with the path or `git clone` destination.

## After it runs

Open `out/STRUCTURE.md`. You should be able to name two files that import each other, and one terracotta edge if anything dangles.

Optional picture: copy `out/lattice.json` into `stalks-and-sections/docs/examples/` and restart that app.
