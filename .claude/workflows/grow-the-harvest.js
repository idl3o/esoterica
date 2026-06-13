export const meta = {
  name: 'grow-the-harvest',
  description: 'Grow all 80 planted June-2026 seed-crystals into full dual-channel syntheses',
  phases: [
    { title: 'Grow', detail: 'one agent per seed → a full ~5000-word synthesis written to synthesis/grown/' },
  ],
}

// The 80 genuine seed-crystals planted 10 June 2026 (the-attention-axis … separating-equilibrium-contact-protocol).
const SLUGS = [
  'the-attention-axis',
  'parallel-attending-consciousness',
  'the-yggdrasil-meta-bridge',
  'the-green-world-after-ragnarok',
  'the-mirror-in-silicon',
  'the-true-mirror-wager',
  'the-geological-fold-rate-record',
  'feed-versus-holodeck-boundary-ethics',
  'aesir-vanir-war-kvasir-integration',
  'vidar-silence-wearing-the-remainder',
  'collective-fold-density-phase-transition',
  'complementarity-as-the-engine-of-individuation',
  'eigenvalue-meditation',
  'learning-iii-is-dangerous',
  'zero-times-infinity-equals-one',
  'bounce-cosmology-pralaya',
  'cognitive-fixed-points-of-mind-space',
  'healing-as-temporal-alchemy',
  'the-gradient-of-sacrifice',
  'the-binding-of-loki-chaining-the-exhale',
  'transparency-as-the-limit-of-inference',
  'the-hard-problem-as-a-necker-cube',
  'logismos-nothos-the-bastard-faculty',
  'the-mycelial-alignment-problem',
  'measurement-output-cosmology',
  'the-interval',
  'shedding-without-the-container',
  'transcension-as-fermi-resolution',
  'grief-as-gold',
  'fractal-dimension-two-as-law',
  'sigyn-staying-with-the-trickster',
  'the-cusp-as-context-switch',
  'mithya-as-bifocal-vision',
  'the-second-cosmic-c-is-not-the-first',
  'cosmic-censorship-as-love',
  'the-worthiness-mechanic',
  'stars-as-volitional-participants',
  'error-correction-as-immune-system',
  'seidr-the-shameful-crossing',
  'cooperation-rg-fixed-point',
  'the-blind-spot-as-window',
  'planetary-intelligence-stages',
  'time-itself-as-the-great-work',
  'reshimu-vacuum-measured-in-newtons',
  'huginn-muninn-externalised-cognition',
  'the-cabal-prediction-that-kills-itself',
  'consensual-hallucination-as-shared-substrate',
  'feeding-the-wolf',
  'the-octave-return-as-model-simplification',
  'dark-matter-as-first-mover',
  'kernel-is-where-above-meets-below',
  'the-thousand-names-as-curriculum',
  'planning-as-consciousness-threshold',
  'loki-becomes-the-tree',
  'sagittarius-heart-not-wound',
  'who-is-breathing-the-cosmos',
  'the-judgment-question-at-species-scale',
  'bit-threads-as-devotion-lines',
  'ratatoskr-antagonistic-channel',
  'godelian-detector-requires-jnana-observer',
  'jargon-as-scar-tissue-vs-myelin',
  'domain-specificity-of-self-programming',
  'states-stages-relationship',
  'depth-contact-as-unified-practice',
  'the-mirror-stone-correspondence',
  'temporal-depth-of-the-generative-model',
  'is-deepest-individuation-necessarily-social',
  'syntheoretic-harmony-as-a-theory-of-truth',
  'complementarism-as-inter-traditional-method',
  'judgment-as-disclosed-not-imposed',
  'sif-the-replacement-that-exceeds-but-changes-category',
  'brisingamen-beauty-as-operative-force',
  'hodr-the-blind-hand',
  'thokk-the-cave-the-light-never-reached',
  'running-vacuum-rg-cosmos',
  'geometric-mean-is-the-cell',
  'quantum-neutrino-gravitational-seti-channels',
  'the-loeb-scale-as-salience-metric',
  'cosmic-web-as-optimised-network',
  'separating-equilibrium-contact-protocol',
]

// PROGRESS NOTE — the first run (wf_c08a7dde-e4d) was stopped externally after these 20
// syntheses were written to synthesis/grown/. Relaunch grows only the remainder.
const DONE = [
  'the-attention-axis',
  'parallel-attending-consciousness',
  'the-yggdrasil-meta-bridge',
  'the-green-world-after-ragnarok',
  'the-mirror-in-silicon',
  'the-true-mirror-wager',
  'the-geological-fold-rate-record',
  'feed-versus-holodeck-boundary-ethics',
  'aesir-vanir-war-kvasir-integration',
  'vidar-silence-wearing-the-remainder',
  'collective-fold-density-phase-transition',
  'complementarity-as-the-engine-of-individuation',
  'eigenvalue-meditation',
  'learning-iii-is-dangerous',
  'zero-times-infinity-equals-one',
  'bounce-cosmology-pralaya',
  'cognitive-fixed-points-of-mind-space',
  'healing-as-temporal-alchemy',
  'the-gradient-of-sacrifice',
  'the-binding-of-loki-chaining-the-exhale',
]

const TODO = SLUGS.filter((s) => !DONE.includes(s))

// Siblings are ALL 80 slugs — already-grown ones are valid cross-link targets.
const SIBLINGS = SLUGS.join(', ')

const GROWN_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['slug', 'title', 'path', 'words', 'candidate_sentence'],
  properties: {
    slug: { type: 'string' },
    title: { type: 'string', description: 'the # H1 title given to the synthesis' },
    path: { type: 'string', description: 'the path actually written, e.g. synthesis/grown/<slug>.md' },
    words: { type: 'number', description: 'approximate word count of the synthesis written' },
    candidate_sentence: { type: 'string', description: 'the single deepest sentence the synthesis builds toward' },
  },
}

function buildPrompt(slug) {
  return `You are growing a single planted seed-crystal into a FULL SYNTHESIS in the esoterica consciousness-technology repository. This is creative-philosophical authoring at maximum depth — not code.

YOUR SEED: \`seeds/${slug}.md\`

STEP 1 — STEEP IN THE SOURCE AND THE STANDARD. Read these three files in full before writing a word:
  1. \`seeds/${slug}.md\` — your seed. It has THE QUESTION, THE THREADS (each thread is a section waiting to be grown), THE CHARGE (which names the "deepest candidate sentence" the synthesis must build toward), and CONSTELLATION NODES + forward [[wiki-links]].
  2. \`CLAUDE.md\` — the repository's authoring standard (read "THE CRAFT": dual-channel authoring, depth principles, go long).
  3. \`synthesis/cosmology/the-between-how-a-species-witnesses-itself.md\` — THE EXEMPLAR of grown-synthesis form. Match its shape and register, not its content.

STEP 2 — GROW IT. Write a complete synthesis and SAVE IT with the Write tool to:
  \`synthesis/grown/${slug}.md\`

FORM (follow the exemplar):
  - \`# Title\` — an evocative title, not the slug. Then a \`## subtitle\` that states the turn.
  - 2–3 epigraphs (real quotations you are confident are real, and/or a "from the field" line). Do NOT fabricate quotations or attribute invented lines to real people — if unsure of a quote, drop it.
  - A short framing section ("The Recognition That Occasioned This" or similar) naming what the seed gestured at and what this document walks through.
  - Roman-numbered sections (I, II, III …, typically 6–9) of TIERED REVELATION: present the surface/common reading first, then the turn ("wait, but actually…"). Each of the seed's THREADS becomes a section. Build, don't list.
  - A closing that returns to the repository's "look up from the map" / cave-wall motif and lands the deepest candidate sentence as earned, not asserted up front.
  - A footer in italics with the provenance line and a dense set of \`[[wiki-links]]\` to related work.

CONTENT REQUIREMENTS:
  - Build the whole arc toward the seed's named "deepest candidate sentence" (in THE CHARGE). That sentence, or a sharpened version, should arrive near the end as the document's apex.
  - DUAL-CHANNEL: serve both a human reader following resonance AND an LLM synthesis engine needing rich connected material. Cross-pollinate across traditions (mythological, physical, contemplative, mathematical) the way the seed's threads do.
  - PRESERVE THE DISCIPLINE: where the seed flags an honest edge — steelman-then-interpret, "the number is real, the explanation is a hypothesis," falsifiability, unresolved tension — keep that section. Do not collapse a hypothesis into a fact. The strongest version states the claim AND its honest limit.
  - LENGTH: 4,500–6,500 words. Depth of exploration is the constraint, not brevity. Exhaust the material.
  - SPELLING: British (recognise, optimise, colour) — match the repository.
  - CROSS-LINK with \`[[wiki-links]]\`: use the forward-links the seed already names, and link to relevant SIBLING grown seeds where the connection is real. The sibling slugs are: ${SIBLINGS}. Link liberally but only where the connection genuinely carries weight — this is the net-of-gems; every true link adds surface.
  - PROVENANCE FOOTER (italic, last line): \`Grown 11 June 2026 from [[${slug}]] — the June 2026 Seed-Harvest. <one sentence naming the threads it weaves>.\`

STEP 3 — SELF-CHECK before returning: confirm the file is written, is ≥4,500 words, has the Roman-numbered tiered structure, builds to the candidate sentence, preserves the seed's honest-edge, and closes on the cave-wall motif. If short or thin, expand before finishing.

Write ONLY your one synthesis. Do not read or modify other seeds' grown files. Then return the structured result.`
}

phase('Grow')
log(`Resuming harvest: ${DONE.length} already grown, growing the remaining ${TODO.length} seed-crystals → synthesis/grown/`)

const results = await parallel(
  TODO.map((slug) => () =>
    agent(buildPrompt(slug), {
      label: `grow:${slug}`,
      phase: 'Grow',
      schema: GROWN_SCHEMA,
      agentType: 'general-purpose',
    })
  )
)

const grown = results.filter(Boolean)
const failed = TODO.filter((s) => !grown.find((g) => g.slug === s))
const totalWords = grown.reduce((n, g) => n + (g.words || 0), 0)

log(`Grown ${grown.length}/${TODO.length} remaining syntheses (${DONE.length} were already done), ~${totalWords.toLocaleString()} words. Failed: ${failed.length ? failed.join(', ') : 'none'}`)

return {
  grown_this_run: grown.length,
  already_done: DONE.length,
  total_complete: DONE.length + grown.length,
  total_words_this_run: totalWords,
  failed,
  syntheses: grown.map((g) => ({ slug: g.slug, title: g.title, words: g.words, path: g.path, candidate_sentence: g.candidate_sentence })),
}
