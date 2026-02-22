---
description: Pull a thread — trace connections across the repository's net of gems
---

# /threads — Walk the Net

You are tracing connections. This is Indra's Net made operational — pick up one jewel and see what every other jewel reflects. Pull one thread and feel the entire web vibrate.

/threads is not /research. Research gathers new material. Threads reveals the hidden structure of what's already here. The repository is a lattice of connections — explicit cross-references, thematic resonances, structural parallels, shared archetypes, unnoticed contradictions — and most of those connections have never been named. /threads names them.

The user will provide a seed. This might be:
- A concept ("ouroboros," "the pharmakon," "as above so below")
- A document ("the prima materia synthesis," "the Dragon Ball bridge")
- A question ("what connects the serpent to the OS?")
- A theme ("dissolution," "boundaries," "the fast")
- A pattern ("every fiction bridge contains a shedding moment")
- Nothing — in which case, pick a thread that's been vibrating in the session and follow it

## Step 1: Plant the Seed

Name the seed clearly in the conversation. If the user's input is ambiguous, don't ask — pick the most interesting interpretation and run with it. The threads will correct course if you chose wrong.

## Step 2: Deploy the Cartographer

Launch a single explorer agent (subagent_type: Explore, thoroughness: very thorough) with these specific instructions:

**Starting from the seed concept, trace connections across the entire esoterica repository.** Search all directories: `synthesis/`, `traditions/`, `fiction-bridges/`, `protocols/`, `seeds/`, `distillations/`, `extractions/`, `correspondences/`, `translated/`, `garden/`, `journey/`, `constellation/`.

For each connection found, classify its nature:
- **Explicit**: the document directly references or cross-links to the seed
- **Thematic**: the document explores the same theme through different material
- **Structural**: the document exhibits the same deep pattern or architecture
- **Resonant**: the document vibrates with the seed in a way that's felt rather than argued — shared tone, shared recognition, shared energy
- **Contradictory**: the document challenges, complicates, or inverts the seed — tension that generates insight
- **Latent**: the document contains material that *could* connect but the connection hasn't been made yet — the thread exists but hasn't been pulled

For each connection, provide:
- File path
- Nature of connection (from the list above)
- The specific point of contact — not just "this file is related" but WHERE and HOW it connects
- A key quote or passage that makes the connection visible

**Cast wide, not deep.** The cartographer's job is to find as many connections as possible, not to analyse them in depth. Breadth over depth. Surprise over confirmation. The unexpected connection matters more than the obvious one.

## Step 3: While the Agent Works

While the cartographer explores, do your own thread-tracing in the main context:
- Check MEMORY.md for open threads related to the seed
- Check constellation.json (if accessible) for existing cluster connections
- Read 1-2 documents you expect to be central — not to duplicate the agent's work but to have key material loaded when you compile

## Step 4: Weave the Map

When the agent returns, compile the connections into a thread map. Output this directly in the conversation (no file — the map is alive, not archived):

```
## THREADS FROM: [Seed]

### THE WEB
[Visual or structured representation of the connection network.
Group by connection type. Show the seed at the centre and the
threads radiating outward. For a rich seed, this might be
20-40 connections across the full repository.]

### THE BRIGHT THREADS
[3-5 strongest connections — the ones where the resonance is
loudest, the structural parallel most precise, the contact point
most illuminating. For each, name the connection and quote the
passage that makes it visible. These are the threads that want
to be followed.]

### THE DARK THREADS
[2-3 connections that surprised — documents you wouldn't expect
to connect to the seed, but do. Contradictions, inversions,
tensions. These are often the most generative because they
reveal structure you didn't know was there.]

### THE LATENT THREADS
[2-3 connections that don't yet exist but want to. Gaps in the
lattice. Documents that SHOULD connect but don't reference each
other. Themes that rhyme but haven't been woven. These are
seeds for future /synthesise or /bridge work.]

### THE PATTERN
[1-3 sentences. What does the thread map reveal about the
repository's deep structure? Every thread-trace teaches
something about the whole. Name what you learned about
the lattice by walking this particular path through it.]
```

## Step 5: Optional — Update the Constellation

If the thread map reveals connections that should be reflected in `constellation.json`, note them. Don't update automatically — name what wants updating and let the session decide whether to act on it.

## Principles

- **Map, don't create.** /threads reveals existing structure. It does not generate new synthesis, new bridges, new documents. If the map reveals something that wants to be created, name it — that's a seed for /synthesise or /bridge. The map itself is the product.
- **Breadth over depth.** The cartographer should find 20-40 connections, not 5 deeply-analysed ones. The power of /threads is in revealing the *density* of the lattice — showing how richly interconnected the repository has become. Depth comes later, when a specific thread is followed.
- **Surprise over confirmation.** The obvious connections (serpent → ouroboros, alchemy → nigredo) are useful for completeness but not for insight. The command earns its keep with the *dark threads* — the connections you didn't expect, the resonances that cross domains, the structural parallels between a fiction bridge and a protocol, between a cosmological synthesis and a personal journal entry.
- **The pattern is the prize.** The closing section — "what does this map reveal about the deep structure?" — is where /threads delivers its real value. Each thread-trace is a cross-section of the lattice, and every cross-section teaches something about the whole. Over time, repeated /threads invocations build a picture of the repository's emergent architecture that no single document can provide.
- **Ephemeral by design.** Like /reflect and /invoke, the thread map lives in the conversation. If it produces insights that want to persist, they go into /journal or MEMORY.md. The map itself is a moment of seeing, not a document to maintain.
- **One seed at a time.** If the user provides multiple seeds, pick the one with the most energy. Multiple seeds produce multiple maps — run them sequentially, not merged. Each seed reveals a different cross-section of the lattice.
- **The net is alive.** Indra's Net has no fixed structure — each jewel reflects every other, and the reflections change as new jewels are added. The thread map from today will be different from the thread map a week from now, because new documents, new bridges, new recognitions change the reflections. /threads is a snapshot of a living web, not a permanent diagram.
