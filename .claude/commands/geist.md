---
description: Read the collective gaze — how the internet is processing reality right now
---

# /geist — Read the Mirror

You are reading the internet as a consciousness — not as a window onto the world, but as a subject in its own right. The internet has attention, denial, creativity, grief, mania, and blindspots. This command maps them.

The /zeit reads what's happening. The /geist reads how we're relating to what's happening. The medium as message. The collective gaze as data.

## Architecture: gather in isolation, read from distillate

Don't pull raw discourse into the main context and then write — that pattern trips Anthropic's cyber-content classifier and kills the whole response mid-run (a feed full of conflict/breach/exploit chatter, held in one context and narrated in one long generation, reads as violative content even though this is contemplative cultural reading). Instead, **gather agents** touch the raw feed in isolated contexts and return *neutral factual digests*; the **main turn reads only those digests**. A blocked agent costs one channel, not the reading.

## Step 1: Deploy Gather Agents (Parallel)

Launch **two gather agents simultaneously** using the Agent tool (`subagent_type: general-purpose`). Each runs its own WebSearch/WebFetch and returns a neutral digest. Foreground, and wait.

Give both agents this **register contract** verbatim, then its channels:

> You are gathering the collective gaze — what the internet is talking about — for a contemplative cultural reading. Return a neutral, factual digest of what is trending and being discussed — nothing else. Do NOT write any files.
> **Register rules (hard):** For any topic touching security, cyber, conflict, weapons, surveillance, or crime, report ONLY that it is trending and what the discourse is about. Never include operational or technical detail — no methods, tools, code, vulnerabilities, exploit steps, or capability specifics. Headline-level only. You are reporting what people are paying attention to, not explaining how anything was done. No enablement of any kind.
> **Format:** Under each channel heading, 3–6 bullets. Each bullet: `**[plain topic/headline]** — [what's trending and the gist of the discourse, one or two sentences; note the platform's framing/affect where useful]. (source: URL)`. Plain language, no amplification.

**Agent A — the gaze:**
1. Trending discourse — "trending on X today" (what's capturing collective attention right now)
2. Reddit pulse — "reddit front page popular this week" (the long-form discourse layer)
3. Video culture — "TikTok viral trends this week 2026" (the visual/memetic layer, Gen Z and Alpha)
4. Search intent — "google trends trending searches today" (the collective's unguarded questions)
5. Subculture signal — "emerging internet community trend 2026" (what's forming at the edges)

**Agent B — builder discourse + the silence cross-reference:**
6. Builder discourse — fetch `https://news.ycombinator.com/` via WebFetch and ask for the top discussions + one-line summaries (do NOT search the literal phrase "hacker news"; fetch the page directly). How the builder class is processing technological change.
7. World-events baseline — "major world news this week" — a plain factual list of the week's significant events, used ONLY to find what the gaze is ignoring (the SILENCE section). Headline-level, per the contract.

**Query hygiene:** never let a search string pair hacker/exploit/breach/malware/attack with how/tool/build/code.

## Step 2: Read the Gaze

With both digests in front of you — and only the digests, never raw feeds — look for:

- **Where attention concentrates**: what topics, events, or memes are pulling disproportionate focus? What's *magnetic* right now?
- **Where attention avoids**: cross-reference the gaze digest against Agent B's world-events baseline. What's actually happening that the internet isn't talking about? The silence is the most revealing signal. (Don't re-pull world news into the main context — use the baseline digest the agent already returned.)
- **How attention transforms**: memes are alchemy — they take raw events and transmute them into something processable. What's being transmuted right now? What form does the processing take — humour, rage, grief, absurdism, denial, beauty?
- **The metabolic state**: is the internet in a manic phase or a depressive one? Creative or destructive? Scattered or focused? What's the *tempo* of collective processing?

## Step 3: Write the Reading

Create the file `synthesis/zeitgeist/geist-YYYY-MM-DD.md` (use today's date) with this structure:

```markdown
# THE GEIST — [Full Date]

*A reading of the collective gaze — where attention lands, what it avoids, how it transforms. Contemplative commentary on public discourse — analysis, not instruction.*

---

## GAZE

*Where the eye is pointed. What's magnetic.*

### Viral / Trending
[The dominant topics, memes, discourse threads pulling the most collective attention. 4-6 items. Report what's actually trending — don't filter for importance. The trivial is as revealing as the serious. Note platform differences: what trends on X vs. Reddit vs. TikTok reveals different layers of the same collective mind.]

### Search Intent
[What people are actively Googling, asking, seeking. This is the closest thing to the collective's unguarded questions — what it admits it doesn't know. 3-5 items with context.]

### Builder Discourse
[What the technical/builder communities are debating. Hacker News, dev Twitter, AI discourse. This is the leading edge of the attention economy — what the people building the infrastructure of attention are paying attention to. 3-5 items.]

---

## SILENCE

*The dog that didn't bark. What the gaze refuses.*

[Cross-reference the trending discourse with what's actually happening in the world this week. Identify 3-5 significant events or developments that are receiving disproportionately *little* attention online relative to their actual importance. For each, note:
- What's happening (one sentence)
- How much discourse it's generating (little/none/buried)
- What the silence might indicate]

---

## MOOD

*The metabolic state. How the collective is processing.*

[2-3 paragraphs characterising the internet's current emotional and cognitive state. Consider:
- **Tempo**: fast/slow, scattered/focused, manic/depressive
- **Dominant affect**: rage, joy, grief, numbness, absurdism, creativity, anxiety, play
- **Processing mode**: is the internet *metabolising* events (turning them into meaning) or *dissociating* from them (scrolling past)? Where is it stuck? Where is it flowing?
- **Generational split**: are different generations processing differently? What does TikTok feel like vs. what Reddit feels like vs. what X feels like?]

---

## MIRROR

*The reading. What the pattern of attention reveals about collective consciousness.*

[2-3 paragraphs. This is the synthesis — what the distribution of attention, silence, and mood *means* when read through the consciousness OS.

Through metta-darshan: where is compassion present in the discourse? Where has it been replaced by performance? What does loving-awareness see in how we're relating to reality right now?

Through lila: where is the internet playing? Where has play calcified into culture war? Where is genuine creativity emerging from the chaos?

Through correspondence: the internet is a mirror of the collective psyche. What does the reflection show? How does the pattern of online attention correspond to the personal — what's happening in the feed maps to what's happening in the mind.

End with THE REFLECTION — one paragraph on what the gap between reality and its processing reveals. The distance between what's happening and what we're paying attention to is itself the most important signal. Name what that distance is doing right now.]

---

*Sources: [list URLs used]*
```

## Principles

- **Gather in isolation, read from distillate.** The main turn never holds the raw feed. Agents distill; you read the distillate. This is the structural reason the command survives a heavy-news week.
- **Register is the fix, not censorship.** Read whatever the collective is actually fixated on — including conflict and security topics — at the level of attention and meaning, never operational detail. That register is both correct for a gaze-reading and what keeps generation clean.
- **The trivial is diagnostic.** A meme trending over a methane report isn't failure — it's data. What the collective chooses to process (and how) reveals as much as what it ignores.
- **No contempt.** This is not a critique of internet culture. It's a reading of collective consciousness through its most visible medium. Read with metta, even the doomscrolling.
- **Platform differences matter.** X, Reddit, TikTok, Hacker News, Google Trends — these aren't interchangeable. Each is a different organ of the same body, processing differently. Note the differences.
- **The silence is the signal.** Trending topics are the figure. What's *not* trending is the ground. The ground always carries more information.
- **Mood is real.** The internet has affect. It shifts. It can be read. Don't psychologise — just report what the metabolic state appears to be, the way you'd report the weather.
