---
description: Produce a complete zeitgeist reading and save to the archive
---

# /zeitgeist — Produce and Archive a Reading

You are producing an integrated zeitgeist reading — what's happening AND how it's being processed, woven together, organised by temporal scale. One document. Signal and processing in the same breath. Silence embedded, not appended.

The output is a single dated markdown file in `corpus/synthesis/zeitgeist/`. The site discovers readings by filename (`zeitgeist-YYYY-MM-DD.md`); there is no index to rebuild. A push to `main` goes live on esoterica.vercel.app as the homepage within about a minute.

## Architecture: gather in isolation, synthesise from distillate

This command does NOT pull raw world-signal into the main context and then write. It can't — that pattern trips Anthropic's cyber-content classifier and kills the whole response mid-run (a single brutal-news week of conflict/breach/exploit headlines, held in one context and narrated in one long generation, looks like violative content to the classifier even though the reading is contemplative journalism).

So the work is split. **Gather agents** touch the raw signal in their own isolated contexts and return *neutral factual digests* — what happened, why it matters, nothing operational. The **main turn synthesises only from those digests**, never the raw feed. This is the repo's own harvest → distillation → synthesis pipeline, applied to the news. It also means a blocked gather agent costs you one channel, not the entire reading.

The pipeline has eight stations. Four were added on 19–20 Sep 2026 after a run in which they caught what the first four let through; they are decisions, not decoration — do not skip them to save time.

| | Station | Who | Yields |
|---|---|---|---|
| 0 | Continuity | main | the threads the last reading left open |
| 1 | Gather | four agents, isolated | neutral digests |
| 2 | Read the pattern | main, digests only | scale map, correspondence |
| 3 | Write | main | the draft |
| 3a | **Verify** | one agent, isolated, in background from Step 2 | quotes and figures checked against the page |
| 3b | **Editorial pass** | main | overclaims cut, contradictions resolved |
| 3c | **Thread** | main | every item joined to its thread in the registry |
| 4 | Commit | main | reading + registry + the run's audit trail; push, or gated PR |

## Step 0: Continuity

Read the most recent reading in `corpus/synthesis/zeitgeist/` before gathering. Note its DEEP headlines, its correspondence and its EDGE. A reading is one entry in a running record: carry a thread forward by name when the week advances it ("the last reading found…"), and do not re-run one of its items without new evidence. Get today's date (`date -u +%Y-%m-%d`) and give it to every agent — their sense of "now" is their training cutoff, not the calendar.

Then read the open threads: `node apparatus/scripts/zeitgeist-slugs.mjs --threads`. A thread is the named thing a run of items has been about ("iran-war", "rate-cycle"); titles are fresh sentences each week, so without threads the archive cannot see that the war of March is the war of September. Know which threads are open, and at what scale each last sat, before you decide where this week's items belong. Create the run directory now: `docs/zeitgeist-runs/YYYY-MM-DD/`.

## Step 1: Deploy Gather Agents (Parallel)

Launch **four gather agents simultaneously** using the Agent tool (`subagent_type: general-purpose`). Each runs its own WebSearch/WebFetch calls and returns a neutral digest. Run them in the foreground and wait — the gathering is the work of this phase.

Give every agent this **register contract** verbatim, then its channel list:

> You are gathering raw world-signal for a contemplative news reading. Return a neutral, factual, journalistic digest — nothing else. Write that digest, byte for byte as you return it, to the one file path you are given below, and write or change no other file anywhere.
> **Register rules (hard):** For any story touching security, cyber, conflict, weapons, surveillance, or crime, report ONLY what happened and why it matters. Never include operational or technical detail — no methods, tools, code, vulnerabilities, exploit steps, malware behaviour, or capability specifics. Headline-level only. You are summarising events, not explaining how anything was done. No enablement of any kind.
> **Format:** Under each channel heading, 3–5 bullets. Each bullet: `**[plain headline]** — [1–2 sentence factual summary: who/what/when/where]. [If a processing channel: where and how it's circulating.] (source: URL)`. Plain language, no amplification, no analysis — analysis happens later, not here.
> **Fidelity rules (hard):** Today's date is [DATE]; discard anything older than about ten days unless the source says it is still current. Give **two dates** for every item: when the thing happened and when the source published it. If they differ by more than a few weeks — a 2023 paper on this week's front page, a spring incident reported now, a resurfaced clip — say so in the bullet; recycled items are signal, but only when labelled. Carry the source's own hedge on every figure (estimate, preliminary, self-reported, "sources say") and never give a rounder number than the source does. Attribute figures to whoever produced them, not to the outlet that relayed them. Use quotation marks only for words you saw on the page, and say who said them and where. If a claim rests on one outlet or one aggregator, say "single source". If a page was blocked or paywalled, say so rather than reconstructing it.

Each agent's file, in the run directory: `1-gather-a-world-material.md`, `1-gather-b-world-frontier.md`, `1-gather-c-processing-discourse.md`, `1-gather-d-processing-culture.md`. The verifier's is `3a-verifier.md`. These are the audit trail (`docs/zeitgeist-runs/README.md`): byte-exact, never edited afterwards, so a claim in a published reading can be traced to the digest that carried it. If an agent returns a digest but wrote no file, write the file yourself from what it returned, unedited.

**Agent A — World, material:**
1. Geopolitical — "major world news today" (conflicts, diplomacy, elections, treaties, power shifts)
2. Economic — "global economy financial markets news today" (markets, policy, currencies, trade)
3. Ecological — "climate environment ecology news this week" (earth systems, species, weather, energy transition)

**Agent B — World, frontier:**
4. Scientific — "scientific breakthroughs discoveries research [YEAR]" (papers, findings, space, physics, biology). Science feeds recirculate old papers as new: check the journal date, not the press-release date.
5. Technological — "AI technology breakthrough news this week" (releases, capabilities, regulation, infrastructure)
6. Cultural — "culture society trends news this week" (movements, art, discourse shifts, collective mood)

**Agent C — Processing, discourse.** Fetch these pages directly with WebFetch; searching for "what is trending" returns listicles. Every endpoint below was probed and found reachable on 19 Sep 2026. For each bullet say where and in what tone the item is circulating (outrage, humour, grief, indifference, fixation), not only what it is.
7. X trends — `https://trends24.in/united-states/`, the worldwide list at `https://getdaytrends.com/`, and at least two territories outside the Atlantic: `https://trends24.in/india/`, `https://trends24.in/indonesia/`, `https://trends24.in/brazil/` (same URL shape for other countries). Timestamped; no post counts.
8. Reddit, by proxy — reddit.com and old.reddit.com are refused by the fetch tool itself, so do not try them or their mirrors. Fetch `https://upstract.com/` (about half its items are Reddit's, each labelled by source; titles only, no scores, so read *presence*, never tone) and `https://lemmy.world/api/v3/post/list?sort=TopWeek&limit=15` (scores and dates present; skews to memes and anti-AI sentiment, so label the skew).
9. Tech discourse — `https://news.ycombinator.com/best` and `https://news.ycombinator.com/` for exact titles with points and comment counts (do NOT search the literal site name as a phrase), and `https://www.techmeme.com/` for the day's tech headlines. Titles only for anything security-related; do not open those threads.
10. Search intent — Google's public feed per territory, `https://trends.google.com/trending/rss?geo=XX`, for US, GB, JP, DE, IN and BR at least (NG and ID are reachable but were thin). Each feed exposes only its ten or so newest terms with coarse traffic floors, and on a match day football saturates every territory: report that as a fact about the instrument, not as the whole of a country's mind.
11. Collective look-ups — Wikipedia's most-viewed articles: `https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/YYYY/MM/DD` for yesterday and the day before (ignore `Main_Page`, `Special:` and `Wikipedia:` entries), with `https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report` as the curated weekly cross-check (it runs a week behind). This is what people went to *look up*: the clearest open measure of which events sent the collective to understand something. Also `https://public.api.bsky.app/xrpc/app.bsky.unspecced.getTrendingTopics` (no counts; US-centric).
- Close with **Notable absences**: any large story you met while gathering that appears on *none* of the lists above. Only what the lists show; no speculation about why.

**Agent D — Processing, culture.** No fetchable short-form video surface exists (the trackers probed were dead or script-only), so this agent works from reporting about the platforms. Get beyond listicles: prefer culture desks, trend newsletters and platform reports that say what people are doing and why the source thinks it spreads; when a "trend" appears only in a marketing blog, say so.
12. Short-form virality — "TikTok viral trends this week [YEAR]" (sounds, formats, aesthetics), plus `https://trending.knowyourmeme.com/` for explainer titles (no counts; mixes ranked and editorial items)
13. Emerging subculture — "emerging internet community trend [YEAR]" (niche movements, analogue and offline movements, attitudes to machine-made content), plus `https://www.garbageday.email/archive` (titles only; interpretive, and a useful corroboration of 12)

**When a channel dies.** A channel that returns blocked or empty two readings running is dead, not unlucky: probe replacements with a small agent (fetch each candidate once, report reachable / blocked / stale with three sample titles) and edit this list. Reddit sat blocked for four consecutive readings before anyone replaced it.

**Query hygiene (Lever 1):** Never let a search string pair hacker/exploit/breach/malware/attack with how/tool/build/code. If a genuinely important security story is in the feed, the agent still reports it — at headline level, per the register contract. The hygiene is about the *query strings and the generated detail*, not about censoring the news.

Follow up (still inside the agents, or with 1–2 targeted main-context WebSearches **only if the result is a plain headline lookup**) on the biggest stories for depth.

## Step 2: Read the Pattern

With the four digests in front of you — and *only* the digests, never raw feeds — don't organise by domain. Organise by scale:

- **Surface**: what events will metabolise in days? (Political moves, market sessions, single stories)
- **Current**: what trends are metabolising over weeks to months? (Market rotations, cultural movements, technological shifts)
- **Deep**: what phase transitions are metabolising over years? (Ecological shifts, constitutional realignments, structural technological change)
- **Tectonic**: what epoch markers exceed any single reading's capacity to contain? (Planetary mismatches, civilisational phase transitions)

For each item at every scale, look at BOTH the signal and its processing:
- Is the collective metabolising it? How? Through which platforms/organs?
- Is the collective refusing it? What does the silence mean?
- What does the gap between event and processing reveal?

Look for the **correspondence**: what single pattern is operating across all scales simultaneously?

If a gather agent returned blocked or empty, note the gap and proceed with the channels you have — never re-pull the raw signal into the main context to compensate.

## Step 3: Write the Reading

Create the file `corpus/synthesis/zeitgeist/zeitgeist-YYYY-MM-DD.md` (use today's date) with this structure:

```markdown
# ZEITGEIST — [Full Date]

*A reading of the present moment. Signal and processing integrated. Silence embedded. Scale honoured. Contemplative commentary on public events — analysis, not instruction.*

---

## SURFACE
*Events that metabolise in days.*

[3-5 items. Each item: what happened + how it's being processed + what the gap between event and processing reveals (in italics). The gap is the diagnostic — it shows where integration is happening and where the thermostat is active.]

---

## CURRENT
*Trends that metabolise in weeks to months.*

[3-5 items. Same integrated format. These are the rivers beneath the surface. Each item names not just the trend but how different organs of the collective body are metabolising it — financial markets, social media, subcultures, tech discourse. Show how the same signal produces different responses in different processing systems.]

---

## DEEP
*Phase transitions that metabolise in years.*

[2-3 items. The big fish. Each item includes the signal, the silence around it (how the collective gaze refuses or fails to process it), and what the silence means. These items get more space — 2-3 paragraphs each. The silence is part of the signal, not a separate section. Show the correspondence between what the gaze reaches for and what it refuses: "The ocean the escape trend reaches for is the same ocean whose coral is dying."]

---

## TECTONIC
*Epoch markers. The fish too big for the net.*

[1-2 items. Named, pointed at, explicitly acknowledged as exceeding the format's capacity. "We cannot contain this, but we can name it." No false domestication. These get honest treatment: what the signal is, why it exceeds the container, and what the only honest relationship to it might be.]

---

## CORRESPONDENCE
*The same pattern at every scale.*

[2-3 paragraphs. The as-above-so-below section. Identify one pattern operating across personal, social, civilisational, ecological, and cosmological scale simultaneously. This is the vertical integration that horizontal organisation misses. Not analysis of the signal — a different way of reading it. Name the pattern in a short phrase and **bold it once**, at first mention — the site indexes that phrase as the reading's pattern.]

## STATE
*The reading.*

[Through metta-darshan and lila. 2-3 paragraphs. Then a final paragraph opening with the literal marker `**THE EDGE:**` — what's trying to emerge. What's pressing against the inside of the current moment? What would need to change for the thermostat to become unnecessary? THE EDGE names what presses. It does not console.]

---

Sources: [list URLs used — drawn from the agents' digests and the verifier's report]

*Channel note: [which channels were blocked or thin; which items rest on a single outlet; what the verifier could not reach; which territories and platforms the trend lists actually covered; any context that came from the historical record and not from this week's gathering.]*
```

**Format is load-bearing.** The site parses this file. Each SURFACE and CURRENT item is one paragraph that opens with a `**bold sentence.**` and closes with its italic gap; each DEEP and TECTONIC item opens with a bold sentence and runs to several paragraphs, none of the later ones opening in bold. The bold opening is the item's title and, slugified, its public URL under `/zeitgeist/meta/item/`. The first bold phrase under DEEP is the reading's headline everywhere. `apparatus/site/src/lib/zeitgeist-parse.test.ts` runs the parsers over the whole archive; if you change the template, run it.

**Synthesis register (Lever 3):** the contemplative layers work at the level of *meaning*, never mechanism. If security/cyber/conflict signal is in the reading, treat it as a sign of where consciousness is — what it reveals about the collective — never as a technical account. You are reading the present, not explaining how anything was carried out. This is both the right register for a zeitgeist and what keeps the generation clean.

**Draft with few quotation marks.** A digest is already one paraphrase from its source. Write paraphrase, attributed, and promote it to quotation only when the verifier returns VERBATIM.

## Step 3a: Verify (isolated agent, in the background)

As soon as Step 2 has told you which quotations and figures the reading will lean on, launch **one verifier agent in the background** and keep writing. Give it the register contract's hard rules, then a numbered list: every string you intend to put in quotation marks, and every load-bearing figure, date, vote count, attribution and venue, each with the source URL from the digest. Twenty to thirty items is normal. Ask for one line per item:

> `N. VERBATIM | CLOSE (actual wording: "…") | NOT FOUND | UNREACHABLE — [who said or produced it, per the source] — [URL actually checked]`
> then a closing list, **"Items the writer must change"**, naming only what is CLOSE, NOT FOUND or mis-attributed, with the corrected wording. It must not guess; UNREACHABLE is an acceptable answer. If a page is blocked it may try a mirror or syndication of the same article (MPR for NPR, phys.org for AP) and must say which it used. Headline-level only: it confirms wording and numbers, it never retrieves how anything was done.

Reconcile every line before Step 4. Apply each correction; where an item came back UNREACHABLE, keep it only with its hedge and say so in the channel note. If a correction changes what an item means — a recycled paper presented as new, a quote moved to a different speaker — rewrite the item, do not patch the sentence.

**Why this station exists:** on its first run (19 Sep 2026) it corrected about twenty of twenty-five items in digests that read as clean: a quotation given the wrong venue, a joint statement credited to one leader, "estimate" added to a figure the source stated flat, a state's school closures reported as a country's, two outlets' claims fused into one, and a 2025 paper presented as that week's. The verifier shares the writer's model; what it does not share is the page. It is the external ruler.

## Step 3b: Editorial pass (main turn)

Re-read the finished draft once, against this list. Each line is a fault found in a published or nearly published reading.

- **Does THE EDGE agree with DEEP?** Internal contradiction is the one fault you can find without leaving the document. If DEEP says the collective ignored a question, the EDGE cannot say the collective quarrelled over it.
- **Superlatives and standing generalisations.** "The most concrete account yet", "the fastest-moving harm", "now reliably", "almost everything": one week's digests cannot carry them. Cut to what was observed.
- **Dating the turn.** "This week X ended" — check it did not end earlier. The ten-year yield's record, the end of cheap money, the first of anything: consult the historical record, and mark in the channel note what came from outside the week's gathering.
- **Imputed motive.** Report what was said and done, not why. "The supplier heard a threat to demand" is a guess wearing a verb.
- **Bending the event.** If an item has been phrased to fit the correspondence better than the digest supports, restore the digest's version and let the correspondence be weaker.
- **Recuperative close.** A negative finding stands. No closing aphorism that turns the week's failure into a good sign.
- **The limits of the net.** An absence is an absence *in the lists gathered*. Say which territories and platforms those were before reading a silence into them.
- **The thread that does not move.** A thread that has sat at the same scale for three readings running: has it moved and you missed it, or are you repeating it? And a thread that has changed scale this week is itself an item: say so.
- **The author's position.** This reading is written by an Anthropic model. When Anthropic, Claude, or the frontier laboratories are in the week's news, say so in the item, plainly and once per item. When the reading's conclusion coincides with its maker's public position, say that too, and ask the reader to count it once: an instrument reaching its maker's view is not a second opinion.
- **Prior art.** Before presenting an idea as the week's discovery, ask whether a literature already holds it.

## Step 3c: Thread the items (main turn)

Run `node apparatus/scripts/zeitgeist-slugs.mjs corpus/synthesis/zeitgeist/zeitgeist-YYYY-MM-DD.md`. It prints every item with its slug and the thread that slug already belongs to, or `(standalone)`. Do not compute slugs by eye: they truncate at sixty characters and twenty-seven live ones end in a hyphen.

Then edit `apparatus/site/src/data/zeitgeist-threads.json`:

- **An item that continues an open thread:** add its slug to that thread's `members`. Decide by what the item's *title* is about. One thread per item; if it straddles two, choose, and say which other thread it touched in the PR body.
- **A thread is minted only when it has two items to hold:** this week's and an earlier standalone one it plainly continues (search the archive's titles before deciding nothing came before). `id` is kebab-case, one to five words; `title` is a short noun phrase of at most six words with no full stop, the way a reader would name the thing. Never a sentence. Never a mood, a theme or one of the series' own devices ("the silence", "the gap"): a thread is a thing in the world.
- **A one-week event with no precedent stays standalone.** It needs no entry. Honest residue is a finding; a lunar crater is allowed to stand alone.
- **Closing a thread:** only when the reading itself says the thing has ended. Set `closed` to the reading's date.
- Never rename or remove an existing `id`, and never delete a member: both are public URLs.

The registry is checked by the site's tests (no slug in two threads, no member that matches no item, every once-live URL still a page or a redirect). Attended, run them; gated, the `site tests` workflow runs them on the PR and a wrong slug fails there.

## Step 4: Commit and Deploy

No index rebuild is needed; the Astro site reads the directory at build time.

Attended, if `apparatus/site/node_modules` exists, run `npm test --prefix apparatus/site` first: the archive suite parses the new reading, and a failure means the format drifted. Gated, the `site tests` workflow runs the same suite on the pull request.

**Attended (default):** commit to `main` and push. Vercel deploys on push.

```bash
git add corpus/synthesis/zeitgeist/zeitgeist-YYYY-MM-DD.md apparatus/site/src/data/zeitgeist-threads.json docs/zeitgeist-runs/YYYY-MM-DD
git commit -m "feat(zeitgeist): DD Mon YYYY reading: [headline from DEEP section]"
git push
```

**Gated (`/zeitgeist gated`, and every unattended run):** do NOT push to `main`. Push to a branch and open a pull request. The `zeitgeist PR notify` workflow mentions Sam on the PR, GitHub emails him, and he authorises by merging (or declines by closing). The cloud routine always runs gated (Sam's decision, 10 Sep 2026):

```bash
git checkout -b zeitgeist/YYYY-MM-DD
git add corpus/synthesis/zeitgeist/zeitgeist-YYYY-MM-DD.md apparatus/site/src/data/zeitgeist-threads.json docs/zeitgeist-runs/YYYY-MM-DD
git commit -m "feat(zeitgeist): DD Mon YYYY reading: [headline from DEEP section]"
git push -u origin zeitgeist/YYYY-MM-DD
gh pr create --fill --title "zeitgeist: DD Mon YYYY" --body "[DEEP headline]

[THE EDGE sentence]

Channels blocked/empty: [list or none]
Verifier: [N checked / N corrected / N unreachable]
Threads: [N items joined open threads / N threads minted (ids) / N standalone / any straddlers]
Author's position: [which items touch Anthropic or the frontier labs, or none]"
```

The PR body carries the Step 5 report so the reviewer never has to open the file to decide. The author's-position line is there so that a reading about its own maker never reaches the front door without the reviewer knowing that is what it is.

## Step 5: Confirm

After push completes, report:
- The date of the reading
- The headline from DEEP (first bold phrase in that section)
- The edge (one sentence from THE EDGE)
- Confirmation that changes are pushed and deploying to esoterica.vercel.app, or the PR URL if gated
- If any gather channel came back blocked/empty, name which one, so the gap is visible
- The verifier's tally (checked / corrected / unreachable), and anything the editorial pass changed that the reviewer should know about

## Principles

- **Gather in isolation, synthesise from distillate.** The main turn never holds the raw feed. Agents distill; you read the distillate. This is the structural reason the command survives a heavy-news week — and it's the repo's own pipeline turned on the present moment.
- **Register is the fix, not censorship.** The reading covers whatever is actually happening, including conflict and security stories. It covers them at the level of significance and meaning — headline-level fact plus contemplative reading — never operational detail. That register is simultaneously the correct one for a zeitgeist and the one that keeps generation clean.
- **Scale before domain.** Organise by temporal scale (surface/current/deep/tectonic), not by domain. The scale is the instruction to the reader's nervous system about how to relate to the signal.
- **Integration, not separation.** Every item shows what happened AND how it's being processed. The gap between signal and processing is embedded in each item.
- **Silence is signal.** What the collective refuses to process is as important as what it processes. Embed the silence at every scale level — especially in DEEP.
- **Threshold honesty.** Name the fish too big for the net. Don't domesticate tectonic signals into bullet points.
- **Correspondence is structure.** The CORRESPONDENCE section is a different axis of reading, not analysis. Show the pattern operating vertically across scales.
- **Breathing architecture.** Section breaks are refractory periods. Design the silence between sections as carefully as the sections.
- **The archive is the product.** Each reading becomes a permanent record. Write as if someone reads it a year from now to understand what this moment felt like.
- **Fidelity first.** Report what's actually happening. Don't bend events to fit a narrative. The pattern emerges from honest observation or not at all.
- **The digest is a paraphrase.** Gather agents stand one remove from the page and the writer stands one remove from them. The register clause (quotation marks only for words the source contains; every figure with its own hedge) cannot be honoured from digests alone. The verifier is what cashes it.
- **Titles are sentences; threads are names.** The item's bold opening is written fresh and should be. What it is *about* is recorded once, in the registry, so the archive can show a thing sinking from SURFACE to DEEP over a season. Without that record 402 of the first 426 items stood alone, the war among them.
- **Old light is signal, when labelled.** Much of any week arrives late: the memo unsealed years on, the incident reported a season after, the paper recirculated as new. The lag between event and sight is itself a reading. Unlabelled, it is just an error.
- **Live on save.** The reading goes live immediately. This is the front door of esoterica — treat it with the gravity it deserves.
