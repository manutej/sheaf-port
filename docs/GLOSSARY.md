# Glossary

Two layers. **Concept** is what a sheaf is. **Product** is what this repo does with one.
You can use the left column in public. The right column keeps skills searchable.

Read [SHEAF.md](SHEAF.md) first if the idea is new. Papers and sibling repos: [REFERENCES.md](REFERENCES.md).

## Concept — the object

| Say this | Meaning, slowly | Why a weaker word is wrong | Paper name |
|---|---|---|---|
| **Part** | One piece with an address you can open: a function, a class, a page, a claim. | A paragraph with no address cannot be checked twice. | cell |
| **Record on a part** | The local data that piece carries. Different parts may have different fields. A module's API is not a wiki sentence. | Not “a node in one shared vector space.” | stalk / (local) section |
| **Overlap** | A place two parts both talk about, *and* you can point at the talk in the source (import, wikilink, citation). | “Same folder” is not an overlap. | edge on the cover |
| **Overlap rule / restriction** | How to read each record on that overlap. In this repo usually: keep the named fields, then compare them, including type. In `scripts/ingest.py` v0: does the named target resolve in the folder? | Not cosine similarity. Not “they mention the same topic.” | restriction map |
| **One picture / assembles** | Every part is locally fine *and* every observed overlap passes its rule. | Not “average score above a threshold.” | global section |
| **Fails to glue** | At least one overlap fails the rule. The failure has an address (two locators + a field or a dangling name). | Not “slightly inconsistent.” | obstruction |
| **Lattice** | A drawing of parts, overlaps, and failed glues. Teal = pass. Terracotta = fail. | A picture of a sheaf, not the sheaf. | explorer / SheafGraph |
| **Package** | The reusable recipe: what counts as a part, which fields are shared, how overlaps are found. | The structure for the *next* folder. The lattice is *this* folder. | domain.package.yaml / site + coefficients |

One sentence: a sheaf is local records, on addressable parts, with a named rule for each real overlap, so you can tell whether those locals form one whole — or name the overlap that failed.

## Product — this repo

| Say this | Meaning | Why you should care | Internal name |
|---|---|---|---|
| **Typed index** | The sheaf as files: parts, records, observed overlaps. | This is what “create a sheaf” emits. | bound sheaf |
| **Reusable structure** | The package. Same field names on a sibling folder. | Meta-suite half: structure for the category, instance for this run. | domain.package.yaml |
| **Ingest** | Walk a folder and write the index + lattice + package. | Out-of-box command: `python scripts/ingest.py <folder> --out ./out` | sheaf-ingest |
| **Write gate** | Optional later use: refuse a write unless the index assembles *and* tests ran. | Not the definition of sheaf. | Φ + write rule |
| **Valid locally** | This one part passes its own check. | Necessary, not sufficient. | G_v |
| **Mismatch report** | Which overlap, which field, left vs right. | Ranks what to fix. Does not approve a write. | relative H¹ |
| **Skip parts that already match** | Do not re-check pairs that cannot be the break. | Budget on a large folder. | Morse reduction |
| **Oracle** | The command you already trust (pytest, a citation checker). | The index is not a substitute. | oracles.execute |
| **Hard check** | Tests, types, public API. Veto. | One red veto refuses a write. | critical lens |
| **Soft check** | Style, coverage, embedding distance. Rank only. | Never the yes/no. | soft lens |
| **Locally-green trap** | Every part looks fine; one overlap is broken. | The case a score will miss. | saddle |
| **Ported** | Index built *and* a cheat-sheet battery passed *and* the log is on disk. | A YAML file is not a port. | adversary log |

## Colour on the lattice

| You see | v0 ingest means | Later write-gate means |
|---|---|---|
| Teal edge | The import or markdown link resolves inside the folder | Shared field values match, including type |
| Terracotta edge | The named target is missing | Those values do not match |
| Node | One part with a locator | Same |
| Ring / `known: true` | Pinned — do not “smooth” it away | Same |

Energy is a hint. It is never permission to write.

## Do not say these

| Phrase | What it hides |
|---|---|
| “It’s just a knowledge graph.” | Drops per-part records and the overlap rule. |
| “The embeddings glued.” | Replaces the overlap rule with a distance. |
| “The lattice *is* the sheaf.” | Confuses the picture with the structure. |
| “Consistency score passed.” | Replaces assemble / fail with an average. |
| “The wiki is consistent, so ship.” | Memory of the source is not a write decision. |
| “A chunk is a part.” | No locator, no record, no overlap rule. |
| “Link everything to be safe.” | Invented overlaps are not overlaps. |
| “It’s teal, merge it.” | Colour is not the write-gate. |

## Worked sentences

- **Code.** `api.py` says `from auth import login`. If `auth.login` is in the folder, that overlap is teal. If it is not, terracotta — and the edge names the missing target.
- **Wiki.** A page links to `sources.md`. If that file exists, teal. If the link is `sources.md` and the file was renamed, terracotta.
- **Later gate.** `auth` exports `apiRevision` as `"1"` and `api` reads it as `1`. Each file is locally fine. The overlap fails on type. Tests still have to run.
