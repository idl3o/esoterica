# REFORMATION II — The Hygiene Pass

**For:** a future Claude Code session in VS Code, repo `idl3o/esoterica`
**From:** a full-corpus sweep (claude.ai), July 2026
**Companion files:** `RESTRUCTURE.md` + `HANDOFF.md` (Reformation I — the structural pass, now landed) + `OUTCOME.md` (its closeout)
**Authority:** *Proposed, not yet approved.* Reformation I was corpus-forward layout; that is materially complete. This pass is about what the layout can't fix: privacy, licence, provenance, and the debris the reorg left behind. Nothing here executes until Sam signs off — and the Priority 0 items are his call alone, because they concern a real third party and his own identifying data.

---

## Context in three sentences

The library now reads as a library; the structure reformation succeeded. But a public repo of a self-documenting human–AI practice accumulates a different kind of debt — identifying detail written for an audience of two, licence claims asserted only in prose, third-party material mirrored in bulk, and stale pointers from the move. This pass drains that debt without touching a single corpus argument.

## What this pass is NOT

- **Not a content edit.** No corpus document's ideas, prose, or voice change. The one exception is *removal* of files on privacy grounds (Priority 0), which is a publication decision, not an editorial one.
- **Not a restructure.** The `corpus/ | apparatus/ | docs/` layout stays. This is cleanup within it.
- **Not a quality pass.** Whether the metaphysics is formulaic is out of scope; `weed` and `negative-space` already own that.

---

## Findings, by severity

### Priority 0 — irreversible, on a public repo (Sam decides, then act same-session)

1. **Doxxing-grade PII about the owner.** `corpus/journey/sam-complete-astrological-consciousness-profile.md` contains exact birth date, birth *time*, city, and lat/long coordinates — the precise tuple used for identity verification. This should not sit in public.
2. **A named third party without consent.** Two `corpus/journey/jess-*.md` files identify a real person in full — surname included — with personal/romantic history and a call to contact them. They have no say in being hosted here. Highest-priority item in the sweep.
3. **Forward whereabouts.** `corpus/journey/*-pilgrimage.md` carry dated itineraries + budgets — travel-plan disclosure for a public reader.
4. **Byline confirm.** Full legal name appears as an author credit in `corpus/misc/SUBSURFACE_WHITEPAPER.md`. Likely intentional; confirm it is the desired public byline.

> Removing these from `HEAD` stops *new* readers; it does **not** remove them from git history or existing forks/caches. A true purge needs a history rewrite (`git filter-repo`) + force-push + Vercel cache invalidation — destructive and irreversible. That is a separate, explicitly-authorized step (see Phase A).

### Priority 1 — licence & provenance

5. **No `LICENSE` file.** CC BY 4.0 is asserted in `README.md` prose only; the README flags its own gap. Machine-unreadable licensing means no one can tell which parts are reusable.
6. **Third-party material under one roof, licence-ambiguous.** `corpus/extractions/` hosts verbatim (ASR) transcripts of others' talks — including a 46-file full-channel scrape of one creator (`extractions/benjamin-davies/`, per its own `channel-manifest.json`). Rights-retained-by-speaker is stated only in the root README, not per-file or in a LICENSE, so the CC-BY boundary is invisible from inside the tree.
7. **`film-slate/` raises the IP stakes.** It is pre-production for generating watchable *video* from Marvel / Riot / Netflix / Dune / Star Wars material — a derivative audiovisual product, a materially higher-risk category than written commentary. Worth an explicit decision before any wave is rendered or distributed.

### Priority 2 — repo weight & stale pointers

8. **~165 MB of audio in git.** `corpus/audio-transcripts/raw/*.m4a` (95.6 + 46.6 + 22.7 MB). Every clone pays this forever; the transcripts already capture the content.
9. **Stale reorg pointers.** `.mcp.json` (and `apparatus/mcp/README.md`) point at the pre-reorg `C:/Users/Sam/Documents/GitHub/esoterica/mcp/server.py`; `.env.example` describes a defunct Express server; `CAPSTONE.md` reports "210+ documents / 168 synthesis" against a live graph of 1,054 nodes.
10. **Constellation debris.** Three `.backup*.json` (80/101/113 nodes) sit beside the 1,054-node live graph looking like recovery files they are not; `constellation_weaving.json` is a stale one-shot output; 6 connections dangle to non-existent node ids.

### Priority 3 — apparatus correctness (code, not content)

11. **`apparatus/world-model` is unrun.** `src/store/vectors.py` uses the pre-0.4 ChromaDB API while `requirements.txt` pins `chromadb>=0.4.0` — it silently falls back to fake hash embeddings. Either fix the API call or mark the module `experimental` in its README so the pitch matches reality.
12. **Two graph-write paths.** Legacy Python scripts write `constellation.json` directly; the newer `.claude/workflows/register-the-harvest.js` writes via `mcp__esoterica__add_node`. Pick one canonical writer and document it, so the JSON stops needing three separate brace-repair hacks downstream.
13. **`apparatus/cli` search is a `# TODO` stub** advertised as a feature; either land it or drop the claim from its README.

---

## The plan

### Phase A — Privacy (branch `hygiene/privacy`, but do NOT self-merge; Sam merges)

Only after Sam rules on each Priority-0 item. Two tiers:

**A1 — Minimum (stops new exposure):**
```bash
git checkout -b hygiene/privacy
git rm corpus/journey/jess-*.md          # the two third-party recognition files
git rm corpus/journey/sam-complete-astrological-consciousness-profile.md
# For pilgrimage/whereabouts: Sam chooses redact-dates vs remove per file.
```
Grep the corpus for stray references so no dangling links remain, and check the constellation graph for nodes whose `document` points at a removed file:
```bash
grep -rlin "jess\|complete-astrological-consciousness" corpus/ constellation/
```
Remove/repoint any constellation node whose `document` field targets a deleted file (and any `connections` entry to it). Message: `chore(privacy): remove identifying journey files from HEAD`.

**A2 — Full purge (only with explicit "yes, rewrite history"):**
`git filter-repo --path-glob 'corpus/journey/jess-*.md' --path corpus/journey/sam-complete-astrological-consciousness-profile.md --invert-paths`, then force-push, then redeploy so Vercel drops the cached `/read/` and `/raw/` routes. Destructive, rewrites SHAs, breaks existing clones. Do not run without that sentence.

### Phase B — Licence & provenance (main, safe)

- Add a root `LICENSE` — **CC BY 4.0** for the project's own writing (matches the README's stated intent).
- Add `corpus/extractions/LICENSE` (or a `README.md` in that dir) stating the carve-out plainly: transcripts are third-party, rights retained by the original speakers, hosted with attribution, **not** relicensed under the project's CC BY. Note the double-derivative case (e.g. the Alan Watts clip already licensed from a third party) as attribution-only.
- Decide `film-slate/` disposition and record it: keep as private study, gate behind a "not for rendering/redistribution" note, or move out of the public tree. Whatever the call, write it down in `docs/` so it isn't re-litigated.
- Message: `docs(licence): add LICENSE + extractions provenance note`.

### Phase C — Weight & pointers (main, safe except C1)

- **C1 (audio):** move the three `.m4a` out of the repo. Preferred: delete from history (`git filter-repo --path corpus/audio-transcripts/raw/ --invert-paths`) since they're superseded by transcripts — same force-push caveat as A2, so batch it with A2 if Sam authorizes a single history rewrite. Minimum: `git rm` from HEAD + add `*.m4a` to `.gitignore` + a note in `audio-transcripts/README.md` on where the source audio now lives.
- **C2:** fix `.mcp.json` → `apparatus/mcp/server.py`; refresh `apparatus/mcp/README.md` setup path; rewrite `.env.example` to match the current static-Astro/no-env deploy (or delete it).
- **C3:** refresh `CAPSTONE.md` counts (or replace hard numbers with "see constellation graph" so it can't go stale again).
- Message(s): `chore: fix stale reorg paths; refresh capstone counts`.

### Phase D — Constellation & apparatus truth (main, safe)

- Delete the three stale `constellation/*.backup*.json` and `constellation_weaving.json` (they're history, not recovery; git already holds history). If a snapshot is wanted, add a single dated one and a one-line note on how it's regenerated.
- Resolve the 6 dangling connections: create the missing nodes or drop the edges.
- Pick the canonical graph writer (recommend the MCP `add_node` path, since the workflows already use it and it's single-writer-safe) and say so in `constellation/README.md`; mark the legacy Python scripts as archival.
- In `apparatus/world-model/README.md` mark status honestly (`experimental — vector layer needs a ChromaDB ≥0.4 rewrite before semantic search is real`), or fix `vectors.py`. In `apparatus/cli/README.md`, remove `tunnel`/search from the feature list until it exists.
- Prune the stale `DONE` array in `.claude/workflows/grow-the-harvest.js` (a mid-run checkpoint left committed) so the template isn't a landmine.
- Message(s): `chore(constellation): drop stale backups; fix dangling edges` / `docs(apparatus): mark true module status`.

---

## Sequencing

1. **Phase B + C2 + C3 + D** are safe, non-destructive, HEAD-only — do them first, on `main`, in small commits. They need no irreversible decision.
2. **Phase A1** (privacy, remove-from-HEAD) on a branch the moment Sam rules — merged by Sam.
3. **Phase A2 + C1** (history rewrite for PII *and* audio, batched into one `filter-repo` + force-push) only on an explicit, written "rewrite history" from Sam. One rewrite, everything at once, then redeploy.

## Constraints

- Never edit the *ideas* of a corpus document — structural/metadata/removal only.
- Preserve history with `git mv`/`git rm`; never delete-and-recreate.
- No force-push, ever, without the explicit sentence in Phase A2/C1.
- Anything Priority 0 is surfaced to Sam and left for Sam — do not decide on his behalf, and do not decide on the third party's behalf at all.
- If a verification step fails and the fix isn't obvious within this plan, stop and surface it.

## Loose ends for Sam to rule on

- Pilgrimage files: redact dates, or remove, or leave?
- `film-slate/`: private study / gated / out of public tree?
- History rewrite: authorize the single batched `filter-repo` (PII + audio), or keep to HEAD-only removals?
- Byline: is full legal name the intended public credit on the whitepaper?
