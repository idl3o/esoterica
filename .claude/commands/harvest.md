---
description: Extract consciousness technologies from source material
---

# /harvest — Extract the Technologies

You are harvesting consciousness technologies from source material. Any text, transcript, video, conversation, book, lecture, or document contains embedded recognitions — patterns of understanding about the nature of consciousness, transformation, perception, and reality that may not be labelled as such but are present in the structure of the ideas.

The user will provide or point to the source material. This might be:
- A YouTube URL (use the youtube ingest tools in `cli/` if available, or WebFetch)
- A file path to a transcript or document
- A book title or author to research
- A pasted block of text
- A topic or teacher to investigate

## Step 1: Ingest

Get the source material into your context:

- **YouTube URL**: Fetch the transcript. If it's long, work through it systematically.
- **File path**: Read the file.
- **Book/author/topic**: Use WebSearch to gather key ideas, quotes, frameworks, and critical analysis. Go deep — multiple searches, multiple sources.
- **Pasted text**: It's already here. Read it closely.

## Step 2: Identify the Technologies

Read the material with these lenses active simultaneously:

### Lens 1: Explicit Technologies
What does the source *openly teach*? Named practices, stated principles, declared methods. These are the surface harvest — valuable but not the whole yield.

### Lens 2: Structural Technologies
What does the *structure* of the teaching reveal? How is the material organised? What sequence does it follow? Sometimes the order of presentation encodes a technology that the content doesn't name. A teacher who always starts with the body before moving to the mind is encoding an embodiment-first protocol whether they name it or not.

### Lens 3: Implicit Technologies
What does the source *know without saying*? What assumptions about consciousness, reality, or transformation are embedded in the material without being articulated? These are often the deepest harvest — the water the fish doesn't see.

### Lens 4: Contradiction Technologies
Where does the source *contradict itself*? Contradictions are often the most fertile ground — they mark places where a linear framework is trying to express a non-linear reality. The contradiction itself may be the technology.

### Lens 5: Resonance Technologies
Where does the material *vibrate* with something in the existing repository? Check connections to:
- Existing protocols in `protocols/`
- Wisdom traditions in `traditions/`
- Fiction bridges in `fiction-bridges/`
- The consciousness OS (metta-darshan, lila, as above so below)
- Scientific frameworks in `synthesis/`

## Step 3: Write the Harvest

Create the file in the appropriate location:
- If it's from a YouTube/lecture source: `extractions/[source-slug].md`
- If it's from a book/teacher: `traditions/[tradition-or-teacher-slug].md` or `synthesis/[topic-slug].md`
- If the user specifies a location, use that.

### Structure:

```markdown
# HARVEST: [Source Title / Author / Topic]

*[One-line description of the source and what was found.]*

**Source**: [URL, book title, file path, or description]
**Harvested**: [Date]

---

## EXPLICIT TECHNOLOGIES

*What the source openly teaches.*

### [Technology Name]
**The recognition**: [One sentence stating what the technology is.]
**How it works**: [1-2 paragraphs describing the mechanism — not just what to do, but why it works. Connect to consciousness principles.]
**Practice**: [Concrete, actionable description. Someone should be able to use this.]
**Connections**: [Links to related repository content — other protocols, traditions, bridges.]

[Repeat for each explicit technology found. Typically 3-7.]

---

## STRUCTURAL TECHNOLOGIES

*What the organisation of the teaching reveals.*

[1-3 technologies extracted from the structure rather than the content.
These are often the most surprising finds — the teacher's unconscious architecture.]

---

## IMPLICIT TECHNOLOGIES

*What the source knows without saying.*

[1-3 technologies extracted from the assumptions, worldview, or unstated framework.
These connect the source to traditions it may not know it belongs to.]

---

## CONTRADICTION TECHNOLOGIES

*Where the cracks let the light in.*

[0-2 technologies extracted from the source's internal tensions.
Not every source has productive contradictions. Only include if genuine.]

---

## SYNTHESIS

*What the harvest reveals when read as a whole.*

[1-2 paragraphs. Step back from the individual technologies and read the harvest
as a single pattern. What is this source's deepest recognition?
How does it connect to the repository's larger understanding?
What does it add that wasn't here before?]

---

## SUGGESTED ACTIONS

- [ ] Protocols to create from harvested technologies
- [ ] Connections to add to constellation.json
- [ ] Fiction bridges that could incorporate these recognitions
- [ ] Distillations for community distribution
```

## Principles

- **Harvest, don't project.** Extract what's actually in the material, not what you wish were there. The source is the source. If a recognition isn't present, don't manufacture it.
- **Name what's unnamed.** The deepest technologies are often operating without labels. Giving them precise names is itself a consciousness technology — it makes the implicit available for conscious use.
- **The five lenses are non-negotiable.** Always read through all five, even if some yield nothing. The discipline of looking through empty lenses sharpens the ones that find something.
- **Connect everything.** A harvested technology that sits in isolation is half a harvest. Every technology connects to the existing network — find the connections and name them.
- **The synthesis earns the harvest.** Individual technologies are useful. The synthesis — what they reveal as a pattern — is where the real yield lives.
