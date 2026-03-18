# NOTEBOOKS — NotebookLM Synthesis Laboratory

Source bundles optimised for NotebookLM's Gemini-powered synthesis engine. Each bundle is a focused collection of 8-15 sources with embedded steering, designed to produce deep audio overviews and chat synthesis rather than surface-level summaries.

## Architecture

```
notebooks/
├── README.md                    # This file
├── NOTEBOOK-INSTRUCTIONS.md     # Reusable Custom Instructions template (10,000 char)
├── bundles/                     # Themed source bundles
│   └── {bundle-name}/
│       ├── PROMPT.md            # Audio Overview customize prompt + notebook guide
│       └── sources/             # Curated sources (copies or originals)
└── experiments/                 # Format experiments and results log
    └── LOG.md                   # What we tested, what shifted
```

## Method

1. **Bundle** — curate 8-15 thematically coherent sources from the repository
2. **Embed** — each source already contains framing language; we add strategic emphasis where the model needs steering toward depth over neutrality
3. **Prompt** — PROMPT.md in each bundle contains both the Custom Instructions (paste into notebook settings) and the Audio Overview customize text
4. **Generate** — upload to NotebookLM, apply instructions, generate
5. **Listen** — the output IS the measurement. What did the model find? What did it flatten? What surprised?
6. **Log** — record results in experiments/LOG.md. What format choices produced depth? What got sanitised?
7. **Iterate** — adjust source formatting, embedded framing, and prompts based on results

## Design Principles

- **Focused over comprehensive**: 8-15 sources on one thread beats 50 sources on everything
- **Explain over summarise**: frame prompts to request explanation, connection, and questioning — never summary
- **Countersteer the neutral default**: NotebookLM's system prompt enforces neutral stance on controversial topics. Our Custom Instructions must explicitly authorise depth on esoteric/consciousness material
- **Dialogic tension preserved**: surface reading → the turn → deeper recognition. This maps directly to how the audio hosts structure discussion
- **Cross-reference density**: explicit connections between documents ("this connects to X because...") give the model synthesis material. The richer the web, the deeper the output
- **The framing IS the steering**: "The key recognition here is..." within source text acts as embedded guidance the model amplifies
