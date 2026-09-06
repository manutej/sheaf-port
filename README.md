<div align="center">

**sheaf-port**

Port a coding agent onto a repo, a wiki, or any other connected dataset —
and only let it write when every part agrees on the fields they share.

![core](https://img.shields.io/badge/core-8_skills-E2B65A?style=flat-square&labelColor=0C0B0A)
![gate](https://img.shields.io/badge/write_gate-agree_%2B_valid-43C9BC?style=flat-square&labelColor=0C0B0A)
![oracle](https://img.shields.io/badge/tests-still_run-43C9BC?style=flat-square&labelColor=0C0B0A)
![clear](https://img.shields.io/badge/principle-clear_%3E_clever-E2B65A?style=flat-square&labelColor=0C0B0A)
![license](https://img.shields.io/badge/license-MIT-39C5BB?style=flat-square&labelColor=0C0B0A)

**[Why](#why-this-exists) · [What you get](#what-you-get) · [The write rule](#the-write-rule) · [Install](#install) · [See it](#see-it-the-aha-view) · [For engineers](docs/GLOSSARY.md)**

</div>

---

## Why this exists

Agents fail in a boring way. Each piece looks fine on its own — the test file is green, the wiki page reads well, the API stub type-checks — and the *combination* is wrong. A path is a string in one module and an int handle in another. A claim on page A cites a source that page B dropped. The agent averages the greens and ships.

**sheaf-port is a write gate for that failure.**

It indexes your project as typed records (not paragraphs, not embeddings). It only compares the fields two parts actually share. It writes if and only if every part is valid *and* those shared fields match *and* your real checks still ran (tests, types, citation resolver). A pretty consistency score is not enough.

That is the whole product. The rest of the plugin is how you attach this gate to a repo, a wiki, a knowledge graph, or a legal corpus without rewriting the agent.

## What you get

| You run | What happens |
|---|---|
| `/sheaf-port <package.yaml>` | Build a typed index of the domain. Refuse mystery chunks and invented links. |
| `/morse-reduce` | Drop checks that cannot disagree, so the gate stays cheap on a big repo. |
| `/phi-check` | Ask “does everything agree?” No repair. No write. |
| `/sheaf-run` | Propose → fix disagreements → write only if the gate passes → record a discrete lesson. |

Eight core skills do the work. Four of them already live in [ceti-explainer](https://github.com/manutej/ceti-explainer). Four are new in this repo: **bind**, **reduce**, **operator**, **adversary**.

The new ones, in engineer English:

| Skill | Invoke | What it emits |
|---|---|---|
| **bind** | `/sheaf-port` | A typed index: parts, shared fields, observed links only. |
| **reduce** | `/morse-reduce` | The short list of parts that can still disagree. |
| **harness** | `/sheaf-run` | The loop + the write rule. |
| **adversary** | (CI) | A log that says the domain is actually wired, not just described. |

## The write rule

```
write  ⇔  every part is valid
       ∧  shared fields match
       ∧  hard checks passed     (tests, types, public API, …)
       ∧  the real oracle ran    (pytest, wikictl, citation-resolve)
       ∧  the work moved forward
```

Soft scores (style, coverage, embedding distance) may *rank* candidates. They may not accept one.

The failure this rule exists to catch: four soft checks green, one shared field broken. That candidate looks like a local minimum and is a global contradiction. Refuse it.

## A domain is just a package

One YAML file tells bind how to read *your* source. Four profiles ship:

| Profile | A “part” is | Shared fields | The oracle |
|---|---|---|---|
| `profiles/codebase.yaml` | a symbol | path, symbol, apiRevision | `pytest -q` |
| `profiles/wiki.yaml` | a claim | claimId, sourceId | `wikictl measure` |
| `profiles/kg.yaml` | a typed edge | src, rel, dst | schema validator |
| `profiles/corpus.yaml` | a holding | holdingId, authority, pinpoint | citation resolver |

A bag of unrelated files is not a domain. Empty shared fields fail bind. Links bind did not observe in the source are refused.

## See it — the Aha view

Do not draw a second graph library. Export the bound index into [stalks-and-sections](https://github.com/manutej/stalks-and-sections) and read it on the lattice that already exists.

| You see | It means |
|---|---|
| A node | One part, with its own typed record |
| Node size | How many fields that record has |
| A teal edge | The two parts agree on every shared field |
| A terracotta edge | They disagree — this is the thing you fix |
| A ring | A fact the reducer is not allowed to drop |

`residualMeaning` is a sentence in *your* domain (“auth and api disagree on apiRevision type”), never “the residual of the coboundary.”

Export contract: [`docs/AHA-VIEW.md`](docs/AHA-VIEW.md).

## Install

```bash
git clone https://github.com/manutej/sheaf-port
cd sheaf-port
pip install -e ".[dev]"
PYTHONPATH=src python -m sheaf_port adversary
PYTHONPATH=src python -m pytest tests -q
```

Plugin install (Claude / Grok):

```bash
/plugin marketplace add manutej/sheaf-port
/plugin install sheaf-port@sheaf-port
```

Then `/sheaf-port profiles/codebase.yaml` on a repo, or `/sheaf-run` once an index exists.

## Design promises

Same four as [meta-suite](https://github.com/manutej/meta-suite):

- **Self-contained.** The write gate runs from this repo. The 3D lattice is optional and already built next door.
- **Never interrogates.** Bind infers what it can from the package; it states assumptions and proceeds.
- **Clear over clever.** User-facing pages use engineer words. The algebra lives in `skills/*/references/` and in [ceti-explainer](https://github.com/manutej/ceti-explainer).
- **It compounds.** A passed adversary log is how the next domain starts ahead of the last.

## What this is not

- Not a vector store with extra vocabulary.
- Not a replacement for your test runner.
- Not a claim that the model “understands sheaves.” The gate is a runtime check.
- Not a CETI film tool. CETI skills can sit *on* the loop after a domain is bound.

## Honesty

The accept bit is a contract we check at run time, not a theorem about the sampler. A related experiment on SWE-bench did not show a discovery advantage (118 vs 116, p = 0.75). We ship the invariance mechanism — typed records, shared-field checks, discrete repair — and we do not advertise a score lift we did not earn.

## Layout

```
sheaf-port/
├── skills/                 bind, reduce, harness, adversary (SKILL.md)
├── profiles/               codebase, wiki, kg, corpus
├── schemas/                domain.package.yaml
├── src/sheaf_port/         reference runtime + write rule
├── tests/                  ship-blocker battery
├── docs/                   WHY, glossary, Aha-view contract
├── eval/battery.yaml       what “ported” means
└── plugin.json
```

## License

MIT © 2026 Manu. See [LICENSE](LICENSE).
