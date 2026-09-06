# Why this plugin exists

Audience: an engineer wiring an agent to a repo, a wiki, or a connected dataset.
Theory names stay in the appendix. This page is the utility argument.

## The failure

You already have checks. Tests. Types. Linters. A wiki that cites sources. The agent still ships a change that is locally fine and globally wrong.

Typical shape:

- `auth.py` exports `apiRevision` as the string `"1"`.
- `api.py` imports it as the integer `1`.
- Each file type-checks in isolation. The test that would have caught the pair did not run, or the agent treated a green style score as permission.
- A reviewer reading one file sees nothing.

The same shape appears outside code:

- Wiki page A asserts claim C and cites source S. Page B repeats claim C and dropped S.
- A knowledge-graph edge and its inverse do not carry the same typed endpoints.
- A legal holding on one memo cites a pinpoint the authority table cannot resolve.

Embeddings do not catch this. Two paragraphs can be near in vector space and disagree on the one field that matters.

## The mechanism (three rules)

1. **Index parts, not paragraphs.** A part has an id, a locator you can open, and a typed record. A README sentence is evidence *about* a part. It is not the part.
2. **Compare only shared fields.** If two parts are linked by an import, a wikilink, or a citation, check the keys that link actually shares. Do not invent extra links “to be safe.” Do not compare embeddings as if they were those keys.
3. **Write only when the parts are valid *and* the shared keys match *and* the real oracle ran.** A mismatch report can rank what to fix first. It cannot accept the write.

That is the write gate. Everything else is plumbing so the gate stays cheap and honest.

## Why the extra pieces earn their keep

| Piece | Plain job | What breaks if you drop it |
|---|---|---|
| **Bind** | Build the typed index from a package file | The agent treats a RAG chunk as a part. The gate has nothing exact to check. |
| **Reduce** | Skip pairs that cannot disagree | The gate times out on a 10k-file repo and someone “simplifies” it into a score. |
| **Repair** | Fix a representative or drop a nuisance prefix, then re-check | The agent either aborts or patches in prose. |
| **Harness** | Propose → fix → write → record a discrete lesson | Skills become a library with no runtime. |
| **Adversary** | Replay the known cheats against this domain | You call the domain “ported” because the YAML parsed. |

Reduce is not optional on a large cover. That is a budget fact, not a taste.

## Why not “just embed and cluster”

Because the bug is discrete. `"1"` versus `1` is a type mismatch, not a distance. A linearized “everything almost agrees” report will stay quiet while the write is still wrong. The gate keeps the discrete check, and keeps your test runner in the accept bit.

## Why not fine-tune the agreement rules

If the next domain is a wiki instead of a repo, a learned agreement map is not auditable. Shared-field projection is. Adaptation is a new package file and a new adversary log, not a weight update.

## What “ported” means

A domain is ported when:

1. Bind built an index with locators and observed links.
2. The write rule refused the known cheats (false part, score-as-accept, invented links, skipped tests).
3. The adversary log sits next to the package file.

Until that log exists, the YAML is a wish.

## The Aha

Open the bound index in [stalks-and-sections](https://github.com/manutej/stalks-and-sections). Teal edges agree. Terracotta edges are the ticket. Point at one terracotta edge and say, in your domain’s words, which shared field broke. If you cannot say it, the index is not done.

## Appendix — names used internally

Only if you asked. The runtime still uses these slugs. User-facing copy should not lead with them.

| Internal | User-facing |
|---|---|
| sheaf | typed consistency graph / index |
| stalk, section | typed record on one part |
| restriction ρ | shared-field projection |
| Φ | the write-gate predicate (valid ∧ agree) |
| relative H¹ | mismatch report (ranks; never accepts) |
| Morse reduction | drop checks that cannot disagree |
| vanishing cycle | address of the last mismatch |
| saddle | locally-green, globally-broken candidate |
| three sheaves | memory vs run-accept vs loop invariants |
| zero weight | no fine-tuning the agreement rules |
