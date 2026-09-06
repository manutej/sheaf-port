# What a sheaf is

Ninety seconds, then one level deeper. Paper names at the end.
This page is the concept. The product sentence is in [START.md](../START.md).

## Ninety seconds

You have something made of pieces that overlap — map sheets, files, wiki pages.

A **graph** only says which pieces are linked.
A **sheaf** also says:

1. what data lives on each piece (its own record — pieces need not share one shape),
2. how to read that data on an overlap (usually: keep the fields the overlap names),
3. whether two linked pieces are compatible: those shared fields match, including type.

If every *observed* overlap is compatible, the local data forms one picture.
If an import or a wikilink carries `"1"` on one side and `1` on the other, you do not have one picture. You have a named disagreement.

A knowledge graph and an embedding store do not give you that last sentence.
The lattice is a drawing of this. Teal = compatible. Terracotta = the named disagreement.
Building the sheaf is not permission to write.

## One level deeper

You already have local truths: a file that type-checks, a page that cites a
source, a sensor that reports its patch. A sheaf is the extra rule for
*when two local truths talk about the same overlap*.

Each part keeps its own record. On an overlap there is a specified
comparison — not “are they similar,” but “do these named fields match
under this map.” If every comparison succeeds, the local truths form one
picture. If one fails, you do not have one knowledge base. You have
pieces that will not sit on the same map.

A graph can still be drawn when the comparison fails. A sheaf *records
the failure* as a first-class fact.

### Three pieces, no more

1. **Parts you can open** — a file, a page, a claim. No locator → not a part.
2. **A record on each part** — the fields that live there. Records need not
   be the same shape. A module’s API is not a paragraph.
3. **A comparison rule only on overlaps you can point at** — an import, a
   wikilink, a citation. No evidence → not an overlap.

Parts may carry different fields. You only compare what the overlap names.

### The atlas, then the repo

Each map sheet has its own coordinates. Where two sheets cover the same
ridge, there is a translation between those coordinates. If the
translations disagree, you do not have one atlas. You have two maps of
“the same” place that are not the same place.

Same fact in a codebase:

- `auth.py` exports `apiRevision` as the string `"1"`.
- `api.py` imports it as the integer `1`.
- Each file is locally fine.
- The overlap (the import) does not agree.
- No single interface exists yet.

The string-versus-int detail matters. That is a failed comparison, not a
small distance.

### What “build a sheaf from this folder” means

Name the parts, fill the records, keep only observed overlaps. That
object *is* the sheaf.

- The **lattice** is how you look at it. Teal = this comparison holds.
  Terracotta = it does not.
- The **package** is the reusable rule for what a part and an overlap
  *are*, so the next folder is indexed the same way.
- A **write-gate** is one thing you can *do* with a glued assignment.
  Building the sheaf does not, by itself, refuse writes.

A single picture is an assignment that survives every comparison.
“Almost glued” is not glued.

## Not this

| Easy reading | Why it is wrong |
|---|---|
| “So it’s a knowledge graph.” | A KG relates entities. A sheaf assigns data to parts and compares through a specified map. “A related-to B” is not a restriction. |
| “So it’s embeddings.” | Near vectors can still fail the named-field comparison. |
| “So it’s just types.” | Types check one file. The sheaf checks the overlap. |
| “So it’s the write-gate.” | The sheaf is the index plus comparison rules. The gate is a later use. |
| “So the lattice *is* the sheaf.” | The lattice is a drawing. Colour is the comparison result. |
| “Everything is a sheaf.” | A bag of files with no observed overlaps is not worth building. Empty shared fields fail. |

## If you want the paper names

| Paper name | On this page |
|---|---|
| sheaf | parts + records + comparison-on-overlaps |
| restriction | the comparison map on an overlap |
| (local) section | a record chosen on one part |
| global section | one picture: every comparison succeeded |
| stalk | the record living at one part |

Stay off this page: coboundary, site, descent, presheaf, cohomology.
Those belong in references, not in the first explanation.

Attacks that this page is written to survive: [EXPLAIN-ATTACKS.md](EXPLAIN-ATTACKS.md).
