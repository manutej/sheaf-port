# Adversarial evaluation of the simplified copy

These attacks are aimed at the README / WHY / glossary, not at the runtime. Runtime ship-blockers stay in `eval/battery.yaml`.

A simplification is rejected if it hides a gate or invents a permission the runtime does not give.

## Round 1 — did we lie?

| Id | Attack | What sloppy copy would say | Required reading |
|---|---|---|---|
| C1 | Score-as-accept | “Consistency score passed, you can write.” | Write rule has no score in the accept bit. |
| C2 | Embeddings glued | “Nearby vectors mean the parts agree.” | Distance is a soft check. |
| C3 | Wiki ships the patch | “The knowledge base is consistent, deploy.” | Memory ≠ accept. |
| C4 | Skip the oracle | “The index is clean, no need for pytest.” | Oracle skip is a ship-blocker. |
| C5 | Chunks are parts | “Drop your documents in; we will index them.” | No locator, no part. |
| C6 | Complete graph | “We link everything so nothing is missed.” | Invented links are a ship-blocker. |
| C7 | Reduce is optional polish | “Skip reduce on a large repo, it is just faster.” | Unreduced check blows the budget and invites C1. |
| C8 | Theorem claim | “The agent now understands sheaves.” | Runtime contract only. Honesty paragraph required. |

## Round 2 — did we hide a gate inside a friendly word?

| Id | Friendly word | Hidden failure |
|---|---|---|
| C9 | “Index” | Must still refuse free text. |
| C10 | “Agree” | Must still be exact field match, including type. `"1"` vs `1` is terracotta. |
| C11 | “Fix” | Repair is discrete (canonical representative or drop a nuisance prefix). Not a learned map. |
| C12 | “Cheap” | Reduce may not drop a part whose shared fields still disagree. |
| C13 | “Ported” | Requires the adversary log, not a parsed YAML. |

## Round 3 — did the Aha view become decoration?

| Id | Attack | Refuse |
|---|---|---|
| C14 | Rainbow residuals | Lattice contract is teal ↔ terracotta only. |
| C15 | Gaussian-filled sections | Unknown is zero. |
| C16 | Energy → 0 drawn as write | Energy is a reading aid. Discrete gate still decides. |
| C17 | No domain sentence on terracotta | `residualMeaning` missing → export is not done. |
| C18 | Force-graph-only layout sold as the product | Positions may be readable strata; colour must still encode the shared-field mismatch. |

## Pass condition

Copy passes when:

1. A grep over `README.md`, `docs/WHY.md`, `docs/GLOSSARY.md` for `functor|morphism|colimit|yoneda|adjunction|coboundary|microlocal` is empty.
2. Every C1–C13 sentence above is *refused* by a quoted line in those files.
3. `docs/AHA-VIEW.md` still names the five conjuncts of the write rule.
4. Runtime battery is unchanged.

Theory names may appear in `docs/WHY.md` appendix and in `skills/*/references/`.
