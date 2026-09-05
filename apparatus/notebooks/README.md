# NOTEBOOKS — NotebookLM Synthesis Laboratory

Source bundles optimised for NotebookLM's Gemini-powered synthesis engine. Each bundle is a focused collection of 8-15 sources with embedded steering, designed to produce deep audio overviews and chat synthesis rather than surface-level summaries.

## Architecture

```
notebooks/
├── README.md                    # This file
├── NOTEBOOK-INSTRUCTIONS.md     # Reusable Custom Instructions template (10,000 char)
├── forge.py                     # Salience engine + bundle assembler (constellation-driven)
├── bundles/                     # Themed source bundles
│   └── {bundle-name}/
│       ├── PROMPT.md            # Audio Overview customize prompt + notebook guide
│       └── sources/             # Curated sources (copies or originals)
└── experiments/                 # Format experiments and results log
    └── LOG.md                   # What we tested, what shifted
```

## Method (forge-assisted)

The constellation graph does the curation legwork; the human/Claude pass does
the steering. The forge lays out the anvil — the steering is the craft.

1. **Rank** — `python forge.py salience [--interest term ...]` scores every
   document-bearing node on: degree sweet-spot (specific, not hub), type
   weight (fiction bridges and syntheses over glossary pages), cross-domain
   span, doc-rich neighbourhood, git recency, novelty (unbundled), and
   optional interest terms. The top of the list is what's ripe.
2. **Forge** — `python forge.py bundle SEED --name slug` grows 8-15 sources
   outward from the seed (cohesion normalised against hubness, type diversity
   rewarded), **mines the convergence points** (concepts where 2+ selected
   sources meet, discounted by concept hubness), copies sources into
   `bundles/<slug>/sources/` for drag-and-drop upload, scaffolds PROMPT.md
   with graph-mined PRIORITIES and a measurement checklist, and appends an
   experiment entry to LOG.md.
3. **Treat** — applied automatically at forge time (re-run anytime with
   `python forge.py treat SLUG`). NotebookLM has two steering channels —
   instructions (requests) and sources (evidence) — and it trusts evidence
   more. So the treatment moves steering into the source channel: each copy
   is cleaned (frontmatter, glyph decoration, dead relative links stripped)
   and prefixed with a SOURCE NOTE naming its role and which sibling sources
   it meets on which concepts; and a synthetic 11th source,
   `00-the-convergence-map.md`, gives the hosts the theme, the source roles,
   and the mined convergences as citable prose. Originals in the corpus are
   never touched — treatment applies only to the copies.
4. **Steer** — fill the scaffold's THEME, CONTEXT, THE TURN, and Audio
   Customize in PROMPT.md, and the THEME/TURN slots in the convergence map,
   by hand (or with Claude) after reading the anchors. This is the step the
   graph cannot do.
5. **Generate** — upload sources/ to NotebookLM, paste Custom Instructions,
   paste the Audio Customize, generate. (No public NotebookLM API — this step
   stays manual.)
6. **Listen** — the output IS the measurement. The forge pre-wrote the
   checklist: did the hosts find the mined convergences or flatten them? Did
   the source notes steer silently or leak into the audio?
7. **Log** — fill the Results section of the auto-appended LOG.md entry
8. **Iterate** — adjust TYPE_WEIGHTS / DEGREE_SWEET_SPOT in forge.py, the
   treatment templates, and the steering templates based on what the audio
   actually did

## Design Principles

- **Focused over comprehensive**: 8-15 sources on one thread beats 50 sources on everything
- **Explain over summarise**: frame prompts to request explanation, connection, and questioning — never summary
- **Countersteer the neutral default**: NotebookLM's system prompt enforces neutral stance on controversial topics. Our Custom Instructions must explicitly authorise depth on esoteric/consciousness material
- **Dialogic tension preserved**: surface reading → the turn → deeper recognition. This maps directly to how the audio hosts structure discussion
- **Cross-reference density**: explicit connections between documents ("this connects to X because...") give the model synthesis material. The richer the web, the deeper the output
- **The framing IS the steering**: "The key recognition here is..." within source text acts as embedded guidance the model amplifies
