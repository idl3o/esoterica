---
description: Produce a complete zeitgeist reading and save to the archive
---

# /zeitgeist — Produce and Archive a Reading

You are producing an integrated zeitgeist reading — what's happening AND how it's being processed, woven together, organised by temporal scale. One document. Signal and processing in the same breath. Silence embedded, not appended.

The output is a single dated markdown file in `synthesis/zeitgeist/` that goes live immediately on esoterica.vercel.app as the homepage.

## Step 1: Gather Signal (Parallel)

Run **all twelve searches simultaneously** using WebSearch — six for what's happening, six for how it's being processed:

**World signal:**
1. "major world news today" (geopolitical)
2. "global economy financial markets news today" (economic)
3. "scientific breakthroughs discoveries research 2026" (scientific)
4. "AI technology breakthrough news this week" (technological)
5. "culture society trends news this week" (cultural)
6. "climate environment ecology news this week" (ecological)

**Processing signal:**
7. "trending on Twitter X today" (trending discourse)
8. "reddit front page popular trending this week" (Reddit pulse)
9. "TikTok viral trends this week 2026" (video culture)
10. "Google Trends trending searches today" (search intent)
11. "Hacker News trending AI tech discussion this week" (tech discourse)
12. "subculture internet community emerging trend 2026" (subculture signal)

Follow up with 2-3 targeted searches on the biggest stories for depth.

## Step 2: Read the Pattern

With all twelve channels in front of you, don't organise by domain. Organise by scale:

- **Surface**: what events will metabolise in days? (Political moves, market sessions, single stories)
- **Current**: what trends are metabolising over weeks to months? (Market rotations, cultural movements, technological shifts)
- **Deep**: what phase transitions are metabolising over years? (Ecological shifts, constitutional realignments, structural technological change)
- **Tectonic**: what epoch markers exceed any single reading's capacity to contain? (Planetary mismatches, civilisational phase transitions)

For each item at every scale, look at BOTH the signal and its processing:
- Is the collective metabolising it? How? Through which platforms/organs?
- Is the collective refusing it? What does the silence mean?
- What does the gap between event and processing reveal?

Look for the **correspondence**: what single pattern is operating across all scales simultaneously?

## Step 3: Write the Reading

Create the file `synthesis/zeitgeist/zeitgeist-YYYY-MM-DD.md` (use today's date) with this structure:

```markdown
# ZEITGEIST — [Full Date]

*A reading of the present moment. Signal and processing integrated. Silence embedded. Scale honoured.*

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

Sources: [list URLs used]
```

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

## Principles

- **Scale before domain.** Organise by temporal scale (surface/current/deep/tectonic), not by domain (geopolitical/economic/etc.). The scale is the instruction to the reader's nervous system about how to relate to the signal.
- **Integration, not separation.** Every item shows what happened AND how it's being processed. The gap between signal and processing is embedded in each item, not relegated to a separate document.
- **Silence is signal.** What the collective refuses to process is as important as what it processes. Embed the silence at every scale level — especially in DEEP, where the biggest signals often receive the smallest processing.
- **Threshold honesty.** Name the fish too big for the net. Don't domesticate tectonic signals into bullet points. Acknowledge what the format cannot contain.
- **Correspondence is structure.** The CORRESPONDENCE section is not analysis — it's a different axis of reading. Show the pattern operating vertically (across scales) after showing it horizontally (within each scale).
- **Breathing architecture.** The section breaks are refractory periods. The italic subheadings are invitations to breathe. Design the silence between sections as carefully as the sections themselves.
- **The archive is the product.** Each reading becomes a permanent record. Write as if someone will read this a year from now to understand what this moment felt like — not just what happened, but how consciousness was relating to what happened.
- **Fidelity first.** Report what's actually happening. Don't bend events to fit a narrative. The pattern will emerge from honest observation or it won't emerge at all.
- **Live on save.** The reading goes live immediately. This is the front door of esoterica — treat it with the gravity it deserves.
