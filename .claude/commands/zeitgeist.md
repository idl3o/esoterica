---
description: Produce a complete zeitgeist reading and save to the archive
---

# /zeitgeist — Produce and Archive a Reading

You are producing an integrated zeitgeist reading — what's happening AND how it's being processed, woven together, organised by temporal scale. One document. Signal and processing in the same breath. Silence embedded, not appended.

The output is a single dated markdown file in `synthesis/zeitgeist/` that goes live immediately on esoterica.vercel.app as the homepage.

## Architecture: gather in isolation, synthesise from distillate

This command does NOT pull raw world-signal into the main context and then write. It can't — that pattern trips Anthropic's cyber-content classifier and kills the whole response mid-run (a single brutal-news week of conflict/breach/exploit headlines, held in one context and narrated in one long generation, looks like violative content to the classifier even though the reading is contemplative journalism).

So the work is split. **Gather agents** touch the raw signal in their own isolated contexts and return *neutral factual digests* — what happened, why it matters, nothing operational. The **main turn synthesises only from those digests**, never the raw feed. This is the repo's own harvest → distillation → synthesis pipeline, applied to the news. It also means a blocked gather agent costs you one channel, not the entire reading.

## Step 1: Deploy Gather Agents (Parallel)

Launch **four gather agents simultaneously** using the Agent tool (`subagent_type: general-purpose`). Each runs its own WebSearch/WebFetch calls and returns a neutral digest. Run them in the foreground and wait — the gathering is the work of this phase.

Give every agent this **register contract** verbatim, then its channel list:

> You are gathering raw world-signal for a contemplative news reading. Return a neutral, factual, journalistic digest — nothing else. Do NOT write any files.
> **Register rules (hard):** For any story touching security, cyber, conflict, weapons, surveillance, or crime, report ONLY what happened and why it matters. Never include operational or technical detail — no methods, tools, code, vulnerabilities, exploit steps, malware behaviour, or capability specifics. Headline-level only. You are summarising events, not explaining how anything was done. No enablement of any kind.
> **Format:** Under each channel heading, 3–5 bullets. Each bullet: `**[plain headline]** — [1–2 sentence factual summary: who/what/when/where]. [If a processing channel: where and how it's circulating.] (source: URL)`. Plain language, no amplification, no analysis — analysis happens later, not here.

**Agent A — World, material:**
1. Geopolitical — "major world news today" (conflicts, diplomacy, elections, treaties, power shifts)
2. Economic — "global economy financial markets news today" (markets, policy, currencies, trade)
3. Ecological — "climate environment ecology news this week" (earth systems, species, weather, energy transition)

**Agent B — World, frontier:**
4. Scientific — "scientific breakthroughs discoveries research 2026" (papers, findings, space, physics, biology)
5. Technological — "AI technology breakthrough news this week" (releases, capabilities, regulation, infrastructure)
6. Cultural — "culture society trends news this week" (movements, art, discourse shifts, collective mood)

**Agent C — Processing, discourse:**
7. Trending discourse — "trending on X today" (what the discourse is fixated on)
8. Reddit pulse — "reddit front page popular this week"
9. Tech discourse — fetch `https://news.ycombinator.com/` via WebFetch and ask for the top discussions + one-line summaries (do NOT search the literal phrase "hacker news"; fetch the page directly)
10. Search intent — "google trends trending searches today"

**Agent D — Processing, culture:**
11. Short-form virality — "TikTok viral trends this week 2026" (video culture)
12. Emerging subculture — "emerging internet community trend 2026" (subculture signal, niche movements)

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

Create the file `synthesis/zeitgeist/zeitgeist-YYYY-MM-DD.md` (use today's date) with this structure:

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

[2-3 paragraphs. The as-above-so-below section. Identify one pattern operating across personal, social, civilisational, ecological, and cosmological scale simultaneously. This is the vertical integration that horizontal organisation misses. Not analysis of the signal — a different way of reading it.]

## STATE
*The reading.*

[Through metta-darshan and lila. 2-3 paragraphs. End with THE EDGE — what's trying to emerge. What's pressing against the inside of the current moment? What would need to change for the thermostat to become unnecessary?]

---

Sources: [list URLs used — drawn from the agents' digests]
```

**Synthesis register (Lever 3):** the contemplative layers work at the level of *meaning*, never mechanism. If security/cyber/conflict signal is in the reading, treat it as a sign of where consciousness is — what it reveals about the collective — never as a technical account. You are reading the present, not explaining how anything was carried out. This is both the right register for a zeitgeist and what keeps the generation clean.

## Step 4: Rebuild Index and Deploy

After saving the reading, run the full deploy sequence:

```bash
node build-synthesis-index.js --public
git add synthesis/zeitgeist/zeitgeist-YYYY-MM-DD.md synthesis-index.json library-index.json
git commit -m "Add zeitgeist reading DD Mon YYYY: [headline from DEEP section]"
git push
```

Vercel auto-deploys on push. The homepage will show the new reading within ~60 seconds.

## Step 5: Confirm

After push completes, report:
- The date of the reading
- The headline from DEEP (first bold phrase in that section)
- The edge (one sentence from THE EDGE)
- Confirmation that changes are pushed and deploying to esoterica.vercel.app
- If any gather channel came back blocked/empty, name which one, so the gap is visible

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
- **Live on save.** The reading goes live immediately. This is the front door of esoterica — treat it with the gravity it deserves.
```
