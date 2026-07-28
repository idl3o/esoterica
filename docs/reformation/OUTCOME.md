# OUTCOME — Esoterica Restructure

*The record of what the [HANDOFF](HANDOFF.md) produced. The plan is closed.*

Executed on branch `restructure/corpus-apparatus`, landed in commit `28e34a6`,
merged to `main` as PR #1. The commit body is the authoritative changelog; this
file is the plan-to-reality reconciliation and the list of what remains.

---

## What the plan called for, and what happened

**Commit 1 — artifacts out of VCS.** Done, and then some. The three index
JSONs, `__pycache__/`, and `generated_seeds/` are gitignored. The build script
that produced them (`build-synthesis-index.js`) was itself deleted as dead — the
Astro site generates its own data via `apparatus/site/scripts/sync-public-data.mjs`.

**Commit 2 — deployment ephemera → docs/.** Executed with a better disposition
than the plan specified. Rather than collapse the seven process records into
four rewritten files (and lose Sam's originals), the originals were preserved
verbatim under `docs/history/`, and a single fresh `docs/deployment.md` documents
the *current* build. No prose was rewritten. `grok-imagine-context.md` also landed
in `docs/history/`.

**Commit 3 — corpus / apparatus split.** Done. Nineteen content directories under
`corpus/`; site, mcp, cli, generation, notebooks, world-model, scripts under
`apparatus/`. The path layer was rebuilt so the site finds the repo root by
climbing for the `corpus/ + constellation/` pair rather than counting `../` hops —
it survives living at `apparatus/site`. Public URLs unchanged.

**Commit 4 — README + INDEX.** README replaced with the absent-narrator draft
([README-draft.md](README-draft.md), now `../../README.md`). INDEX regenerated.

## The one deliberate deviation

`constellation/` stayed a **top-level peer** of `corpus/` rather than dissolving
into it. Its Python curation tools are hardcoded to sit beside `constellation.json`
(`Path(__file__).parent / "constellation.json"`); splitting the graph from its only
maintenance tools was judged a net loss. The site reads it as a distinct source.
This was flagged in the commit for review and stands as the accepted layout —
CLAUDE.md now documents four top-level units, not three.

## Triage decisions (plan §Commit 3)

- `client/`, `server/`, `api/` — **deleted** (dead since the 2026-03-18 Astro
  switch; the Express platform pointed at nothing live). Recoverable in history.
- `oracle.{html,ts}`, `synthesis-library{,-v1}.html`, the three
  `constellation_explorer*.html` — **deleted** as superseded (explorer v3 was
  byte-identical to the site's `public/explorer.html`).
- Root `package.json` — **deleted** (Express manifest; Vercel builds from
  `apparatus/site` via explicit install/build commands in `vercel.json`).
- `CAPSTONE.md`, `ENGRAMS.md` — **kept at root** as threshold documents.
- `misc/` — moved to `corpus/misc/` intact; SEED.md's citations reprefixed and
  verified to resolve.

## Residue fixed at closeout (2026-07-23)

- `INIT.md` still linked `./misc/internal/CLAUDE_INITIALIZATION.md` — a threshold
  link the commit-4 reprefix missed. Corrected to `./corpus/misc/internal/...`.
  A sweep of all eight root threshold docs now shows zero broken relative links.

## Still open (out of the restructure's scope)

1. **Functional runs of the repathed Python.** The MCP server and CLI tools were
   verified to *compile* and every computed path anchor was checked to resolve, but
   not exercised against a live host — they need an MCP host, args, and network.
2. **The two-checkout reconciliation.** Two clones of `idl3o/esoterica` exist; per
   `.mcp.json` the live MCP still writes to the checkout that was *not* restructured.
   Until that is repointed or the two are reconciled, constellation writes from the
   running MCP land in the old tree. Tracked in session memory as
   `two-checkout-divergence`.

---

*Corpus forward, apparatus recessed, artifacts out of the index, the doorway
cleared. The library reads as a library.*
