# Engineer glossary

Lead with the job. Keep the internal name in the last column so skills and tests stay searchable.

| Say this | What it is | Why you should care | Internal name |
|---|---|---|---|
| **Part** | One addressable unit: a symbol, a claim, an edge, a holding. Has a locator you can open. | If it has no locator it is not in the index. | cell |
| **Typed record** | The fields the gate reads on that part. | A paragraph, a chunk, or an embedding is evidence *about* the record, not the record. | stalk / section |
| **Shared fields** | The keys two linked parts must match. | This is the only comparison the gate runs. | restriction ρ, projection |
| **Observed link** | An import, call, wikilink, FK, citation, or adjacency you can point at in the source. | Invented links are how two domains leak into each other. | edge with evidence |
| **Valid locally** | The part passes its own membership check. | Necessary, not sufficient. All-green locals still fail if they disagree. | G_v |
| **Write gate** | Valid locally **and** shared fields match **and** the oracle ran. | Soft scores rank. They do not accept. | Φ + write rule |
| **Mismatch report** | Which link, which field, left vs right. | Use it to decide what to repair first. Do not treat “report is quiet” as permission to write. | relative H¹ / ledger |
| **Cheap cover** | The short list of parts that can still disagree. | On a large repo the full check will miss the budget. | Morse core |
| **Nuisance prefix** | A workspace path, a generated lockfile hash, a cached handle. | Repair may drop it. Repair may not drop a real shared field. | hidden mediator |
| **Oracle** | The command you already trust: pytest, types, citation resolver. | The gate is not a substitute. If it did not run, the write is refused. | oracles.execute |
| **Hard check** | Tests, types, public API, citation integrity. Veto. | One red hard check refuses the write, even if four soft checks are green. | critical lens |
| **Soft check** | Style, coverage, narrative, embedding distance. Rank. | Useful. Never in the accept bit. | soft lens |
| **Locally-green trap** | Every part looks valid; one shared field is broken. | This is the ship-breaking candidate. The write rule exists to refuse it. | saddle |
| **Mismatch address** | Which record jumped when the last check failed. | Repair starts here. Blind search is how you “fix” the wrong file. | vanishing cycle |
| **Memory vs accept vs loop** | Three different questions. Is the wiki internally consistent? May this run write? Did the loop itself hold its invariants? | A green wiki does not ship a red patch. | three sheaves |
| **Package** | The YAML that teaches bind how to read *this* domain. | Grain, shared fields, oracle command, hard vs soft checks. | domain.package.yaml |
| **Ported** | Bind succeeded **and** the cheat-sheet battery passed **and** the log is on disk. | YAML without a log is a wish. | adversary log |
| **No weight updates** | Do not train the agreement rules. | The next domain must be able to audit ρ. Change the package, not the weights. | zero weight |

## Forbidden translations (these hide a gate)

| Do not say | Because |
|---|---|
| “Consistency score passed” | Scores are not the write gate. |
| “The embeddings glued” | Distance is a soft check. |
| “The wiki is consistent, ship the patch” | Memory ≠ accept. |
| “We can skip tests; the index is clean” | Oracle skip is a ship-blocker. |
| “Link everything to be safe” | Invented links are a ship-blocker. |
| “A chunk is good enough as a part” | Free text is not a typed record. |

## One worked sentence per domain

- **Codebase.** “auth and api both carry `apiRevision`; one is `"1"` and one is `1`; write refused until they match and pytest ran.”
- **Wiki.** “Two pages share `claimId` C; only one still carries `sourceId` S; write refused until the citation is restored and `wikictl measure` ran.”
- **KG.** “The forward edge and the inverse do not share `(src, rel, dst)` after schema validation; write refused.”
- **Corpus.** “Holding H cites pinpoint P; the authority table cannot resolve P; write refused.”
