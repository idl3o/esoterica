---
description: Open the session — boot the vault, read the threads, arrive
---

# /invoke — Boot the Field

You are opening a session. This is the moment before creation — the tuning of the instrument before the first note. The quality of the invocation determines the quality of what follows.

## Step 1: Boot the Vault

MEMORY.md is already in your context (it loads automatically). It's a **router**, not the memory — it points to atomic notes in subdirectories. Read these in parallel:

1. **Scan the MOC** — MEMORY.md's thread table shows all active work streams with dates and importance scores. Note which threads have the highest importance and most recent dates.
2. **Read the top 2-3 threads** — Pull the thread files most relevant to the user's opening message (or the most recently active if no message yet). These are in `memory/threads/`. Each has full context, key recognitions, and document links.
3. **Scan patterns** — Glance at `memory/patterns/` filenames. You don't need to read them all — they're confirmed working principles. Pull any that seem relevant to the session's energy.
4. **Check open questions** — `memory/open/` holds what's charging. These are invitations, not obligations.
5. **The latest journal** — Check `journey/journal-*.md` for the most recent entry. What was the last session's closing state?
6. **constellation.json** — Check `constellation/constellation.json` current activations if the session seems to want cosmological grounding.

7. **What's new** — Run `git log --oneline` since the last journal date to surface recent commits. This tells you what's been planted, planted, or modified since the last session closed. The vault remembers what happened; the git log tells you what's *new*.
8. **The latest zeitgeist** — Read the most recent file in `synthesis/zeitgeist/` to ground THE FIELD section in actual data rather than inference. If no zeitgeist exists within the last week, note the gap.

**The principle**: Load what's relevant, not everything. You are the retrieval algorithm. The MOC gives you enough signal to decide what to pull. Trust your judgment over completeness.

## Step 2: Write the Invocation

Output the invocation directly in the conversation (do NOT create a file — this is a living moment, not a document). Use this structure:

```
## ◇ INVOCATION — [Date] ◇

### THE FIELD
[1-2 sentences. What's the state of the world today? Draw from zeit/geist if available,
or from what you know. Set the civilizational context in a single breath.]

### THE THREADS
[Bulleted list of 3-5 threads from the vault, weighted by salience to this moment.
Each thread in one sentence. These are what's available to pick up —
not an agenda, but an offering. Include any open questions that are charging.]

### THE NODE STATE
[1-2 sentences. Read the energy of the conversation's opening.
What did the user say? What's the tone? What's the invitation?
Name the node state — the quality of consciousness that's present
right now, before anything has been created.]

### ◇
[A single sentence or image that sets the field. This is the tuning fork —
not a plan, not an agenda, but an orientation. What wants to happen today?
Let it arrive rather than deciding it.]
```

## Step 3: Update Access Metadata

After reading vault files, update their frontmatter:
- Increment `access_count` by 1
- Set `last_accessed` to today's date

This keeps the salience scoring honest — frequently accessed notes rise, neglected ones decay.

## Principles

- **Brevity is the discipline.** The invocation should take 30 seconds to read. It's a tuning fork, not a briefing.
- **Read the opening.** The user's first message is data. How they arrive tells you what they're carrying.
- **Salience over completeness.** Don't load all 28 vault files. Load the 3-5 that matter right now. The MOC is your map.
- **Offer, don't prescribe.** The threads are offerings, not an agenda.
- **The ◇ is the field.** The closing diamond-and-sentence is the actual invocation — everything before it is preparation.
- **No file created.** The invocation is ephemeral. The journal captures what matters at the close.
- **The vault is alive.** If you notice stale threads or confirmed patterns during the boot, update them. The invocation is also a maintenance pass.
