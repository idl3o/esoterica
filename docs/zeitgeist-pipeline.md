# Zeitgeist pipeline — working checklist

Started 19 Sep 2026 (evening run). Tick as it lands; strike what is declined. Decisions are Sam's, marked **D**. Gotchas are already-paid-for; do not regress.

## Where things stand

- [x] 19 Sep reading live (#4). Parsers fixed and tested, command gained continuity / verify / editorial stations, site tests in CI (#5). Notify workflow on `main` (#2).
- [x] Routine on `claude-opus-5` (Fable needs cloud usage credits). Prompt reports verifier tally and author's position.
- [ ] **Mon 21 Sep 07:03 UTC — first real cloud run.** Read its log (`RemoteTrigger list_runs` → `get_run_log`). Pass = PR opened from `zeitgeist/2026-09-21`, body carries verifier tally + author's-position line, `notify` job fires and the email arrives, `site tests` green. Anything less, fix the command file, not the prompt.

## The finding that sets tonight's agenda

Measured over 35 readings: **426 item appearances, 402 distinct ids, 9 recurring (2.2%)** — and all nine recur only because of nine hand merges last touched 17 July. Meanwhile 29 distinct ids are about Iran/Hormuz/the war, 46 about AI, 27 about money and oil, 17 about climate. Titles moved from noun phrases ("The Social Exit") to declarative sentences (median seven words, longest thirty-three), so slugs can never match again.

Consequence: the meta index's whole premise, persistence across scales, is inoperative. It labels ~98% of items "metabolised" (single appearance, now gone), which is false of the war, the rate cycle and the mind being built. The archive has a longitudinal record and no way to read it.

## Phase 0 — decisions before code

- [x] **D1. Provenance.** *Ruled 20 Sep: yes, `docs/zeitgeist-runs/<date>/`. 19 Sep recovered byte-exact from the session transcript (six files). Still owed: the command writes them each run (Phase 4).* Original question: Today's four digests, the verifier report and the channel probe exist only in this session's context and die with it. Save them (they are the audit trail `/weed` would want, and the natural input for threading)? If yes, where: `docs/zeitgeist-runs/2026-09-19/` (process memory, my lean) vs beside the readings in the corpus vs nowhere. If yes, do it **first**, before context compacts. Going forward it means the command writes them each run, and the routine may touch more than one file.
- [x] **D2. Where the thread registry lives.** *Ruled: site data, as `apparatus/site/src/data/zeitgeist-threads.json` (the v1 curation file, migrated and renamed).* Extend `apparatus/site/src/data/zeitgeist-items-curation.json` (exists, site already reads it; my lean, least machinery) vs a registry in the corpus beside the readings (the writer reads it at Step 0 either way).
- [x] **D3. How an item gets its thread.** *Ruled: sidecar mapping keyed by item slug; readings stay pure.* Sidecar mapping in the registry, keyed by item slug (readings stay pure markdown; backfill touches no reading; my lean) vs an inline `<!-- thread: x -->` marker in each item (self-describing, but tooling residue in the library).
- [x] **D4. Partition or graph.** *Ruled: partition; schema tolerates unknown keys so `also` can arrive later.* One thread per item (simple, matches the current id model) vs primary + `also[]` ("the price of time… a strait is setting it" is rates *and* Hormuz). Lean: partition now, leave room for `also`.
- [ ] **D5. Who names the threads.** *Ruled: one mind drafts, Sam reviews the names before assignment. Gate still ahead.* The taxonomy is an act of naming over your archive. Proposal: one mind drafts it (no fan-out; delegated agents clump at whatever shape the prompt names), you review the list of ~40–60 names before a single item is assigned.

## Phase 1 — registry, pure and tested (no UI)

- [x] Schema for the registry with zod (new dependency; first schema in the site). Type derived from schema, not hand-written.
- [x] `zeitgeist-threads.ts`: pure resolver `(itemSlug) → threadId`, replacing the fuzzy `findCanonicalId` (which substring-matches titles against variants: any title containing "oil shock" is captured, silently).
- [x] Tests against the archive: every variant slug in the registry exists in some reading (no dangling); no slug in two threads; every item resolves to exactly one id; resolution is deterministic.
- [x] Status semantics rewritten around threads: `active` / `dormant` / `closed`, with "metabolised" reserved for a thread a reading explicitly closes.

**Phase 1 findings (20 Sep).** Migration reproduced every live item id exactly (0 mismatches over 426 items; build emits the same 402 item pages as the snapshot). Of the 29 variants hand-typed in July, 16 matched no reading at all (`civilisations-floor` for the real `civilisation-s-floor`); the fuzzy matcher had been doing the work silently, capturing 16 items. 27 live slugs end in a hyphen (truncate-after-trim), so `slugify` must never be tidied. `src/data/zeitgeist-item-ids.snapshot.json` is now the permanent no-404 contract.

## Phase 2 — backfill the archive

- [x] Export the 402 items (date, scale, title, gap) to one table.
- [x] Single-mind clustering pass → draft taxonomy: **57 threads over 330 of 426 items; recurring ids 2.2% → 38.4%.** Independently validated and dry-run (194 tests, build green, registry restored).
- [ ] **D5 review gate — waiting on Sam.** Read `docs/zeitgeist-threads-draft.md` (ten editor's flags on top). On approval: apply renames, move the gas-prices item, copy the JSON into the registry, delete both draft files.
- [ ] Report the residue honestly: how many items are genuine singletons (a lunar crater is allowed to be one).
- [ ] Acceptance: recurring share rises from 2.2% to whatever is true; a named thread exists for the war, the rate cycle, AI pacing, the exit, the haze/heat line; spot-check twenty assignments by hand.

## Phase 3 — site

- [x] **Gotcha: merging a singleton into a thread deletes its public URL.** *Done: the item route emits a redirect page per retired id; the snapshot test enforces it.* `/zeitgeist/meta/item/<slug>` pages vanish when their slug becomes a variant. Emit a redirect page for every variant slug. Test: no item URL that exists on the live site today 404s after the change (snapshot the list before starting).
- [x] Thread page: appearances in date order with their scale, so migration reads at a glance (SURFACE → CURRENT → DEEP is the series' own thesis made visible), gaps in sequence beneath.
- [x] "Moved between scales" on the meta index, most recently seen first. *Still open: a full threads index sorted by persistence.*
- [ ] Reading page: each item links to its thread; archive cards show the correspondence pattern now that all 35 parse.
- [ ] `astro build` green; page count sane (2,747 today).

## Phase 4 — the writer learns the threads

- [x] Command Step 0 reads the registry: open threads, last scale, last seen. Step 3 assigns every item to a thread or mints one (kebab-case noun phrase, not a sentence). Step 4 commits the registry with the reading.
- [x] Editorial-pass line: "a thread that has appeared three readings running at the same scale — has it moved, or are you repeating it?"
- [x] Gather agents and the verifier write their own files into `docs/zeitgeist-runs/<date>/` (D1 going forward). `apparatus/scripts/zeitgeist-slugs.mjs` lists a reading's slugs and threads on a bare clone; a test pins it to the site's parser.
- [ ] **After this branch merges:** routine prompt step 4 must allow the registry and the run directory (it still says "do not touch any other file"), and its PR-body order gains the Threads line.
- [ ] Routine prompt: allow the registry as a second touched file. CI: registry tests run on zeitgeist PRs (already covered by the path filter if D2 = site data; extend the filter if it lives in the corpus).

## Phase 5 — stretch

- [ ] Atom feed at `/zeitgeist/feed.xml` (headline, pattern, edge, summary, link). None exists; distribution phase; an hour, fully testable.
- [ ] `/zeitgeist-probe` as its own command: the 27-endpoint probe prompt, so replacing a dead channel is one invocation.
- [ ] Opportunistic, only in files touched: remove the `!` and `as string` in `zeitgeist.ts` / `zeitgeist-index.ts`.

## Gotchas already resolved — do not regress

- Item titles are public URLs. `zeitgeist-parse.test.ts` pins every title the shipped regex found.
- Section content must lose its trailing `---` before item parsing, or every section's last gap is lost.
- `RemoteTrigger update` rejects a partial `job_config`: resend the whole `ccr` block with the one field changed.
- reddit.com is refused by the fetch tool itself. Do not retry it or its mirrors.
- Git Bash mangles `rev:path` arguments (`git show origin/x:file`); use `gh` or PowerShell.
- Fetch tools pass pages through a summarising model: "verbatim" is at one remove. Say so in the channel note.

## What is declined

- Rewriting past readings to one format, or adding thread markers to them. The parser bends; the archive stands as written.
- Embedding-based or build-time automatic clustering. Vercel has no local model, and a silent clusterer is the fuzzy matcher again at scale. Threads are named, committed and reviewable.
- Changing pattern precedence in CORRESPONDENCE, so past labels do not move.
- Flipping tsconfig or lint flags in the site unasked.
