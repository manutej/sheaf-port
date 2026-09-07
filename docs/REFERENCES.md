# References

Short list. Enough to go deeper without turning the README into a seminar.

## Sibling repos (use these)

| Repo | What it is |
|---|---|
| [manutej/sheaf-port](https://github.com/manutej/sheaf-port) | This repo. Folder → typed index + lattice + reusable package. |
| [manutej/stalks-and-sections](https://github.com/manutej/stalks-and-sections) | 3D lattice explorer. Drop `out/lattice.json` in `docs/examples/`. Richer TS ingest: `npm run sheaf:ingest`. |
| [manutej/meta-suite](https://github.com/manutej/meta-suite) | Pattern this package copies: reusable *structure*, not one instance. |
| [manutej/ceti-explainer](https://github.com/manutej/ceti-explainer) | Live `/sheaf-run` loop. Glue for CETI films, not arbitrary repos. |

Read next door if you want the picture: `docs/GENERATE.md` and `docs/INGEST.md` in stalks-and-sections.

## Concept (one step past this repo)

| Work | Why it is here |
|---|---|
| Glen Bredon, *Sheaf Theory* | Classical reference for “local data + restriction + glue.” Do not start here. |
| Allen Hatcher, *Algebraic Topology*, §2–3 | If you need homology as “obstructions to glue,” not as a product word. |
| Justin Curry, *Sheaves, Cosheaves and Applications* | Applied sheaves on cell complexes — closest math sibling to “parts + overlaps.” |
| Hansen & Ghrist, *Toward a spectral theory of cellular sheaves* | Why people draw sheaves as lattices / graphs with extra maps. |
| Riess, Hansen, Ghrist, *Sheaf-theoretic persistence* / related notes | Persistence of glue failures. Optional. |
| Forman, *A user's guide to discrete Morse theory* | Why we skip pairs that cannot disagree. Product word: cheap cover. |

## What we took / what we did not take

Took: parts, records that may differ in shape, restriction on observed overlaps, failed glue as an object.
Did not take into user-facing pages: cohomology groups as scores, sites and Grothendieck topologies, derived categories.

If a sentence needs a word from the “did not take” list to be true, it does not belong in START.md or GLOSSARY.md.
