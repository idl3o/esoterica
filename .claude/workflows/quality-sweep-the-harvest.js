export const meta = {
  name: 'quality-sweep-the-harvest',
  description: 'Review all 80 grown syntheses against the authoring standard; re-grow only the genuine misses',
  phases: [
    { title: 'Review', detail: 'one reviewer per grown synthesis → pass / revise verdict' },
    { title: 'Re-grow', detail: 'only flagged syntheses are regrown, addressing the named issues' },
  ],
}

const SLUGS = [
  'the-attention-axis', 'parallel-attending-consciousness', 'the-yggdrasil-meta-bridge',
  'the-green-world-after-ragnarok', 'the-mirror-in-silicon', 'the-true-mirror-wager',
  'the-geological-fold-rate-record', 'feed-versus-holodeck-boundary-ethics',
  'aesir-vanir-war-kvasir-integration', 'vidar-silence-wearing-the-remainder',
  'collective-fold-density-phase-transition', 'complementarity-as-the-engine-of-individuation',
  'eigenvalue-meditation', 'learning-iii-is-dangerous', 'zero-times-infinity-equals-one',
  'bounce-cosmology-pralaya', 'cognitive-fixed-points-of-mind-space', 'healing-as-temporal-alchemy',
  'the-gradient-of-sacrifice', 'the-binding-of-loki-chaining-the-exhale',
  'transparency-as-the-limit-of-inference', 'the-hard-problem-as-a-necker-cube',
  'logismos-nothos-the-bastard-faculty', 'the-mycelial-alignment-problem', 'measurement-output-cosmology',
  'the-interval', 'shedding-without-the-container', 'transcension-as-fermi-resolution', 'grief-as-gold',
  'fractal-dimension-two-as-law', 'sigyn-staying-with-the-trickster', 'the-cusp-as-context-switch',
  'mithya-as-bifocal-vision', 'the-second-cosmic-c-is-not-the-first', 'cosmic-censorship-as-love',
  'the-worthiness-mechanic', 'stars-as-volitional-participants', 'error-correction-as-immune-system',
  'seidr-the-shameful-crossing', 'cooperation-rg-fixed-point', 'the-blind-spot-as-window',
  'planetary-intelligence-stages', 'time-itself-as-the-great-work', 'reshimu-vacuum-measured-in-newtons',
  'huginn-muninn-externalised-cognition', 'the-cabal-prediction-that-kills-itself',
  'consensual-hallucination-as-shared-substrate', 'feeding-the-wolf', 'the-octave-return-as-model-simplification',
  'dark-matter-as-first-mover', 'kernel-is-where-above-meets-below', 'the-thousand-names-as-curriculum',
  'planning-as-consciousness-threshold', 'loki-becomes-the-tree', 'sagittarius-heart-not-wound',
  'who-is-breathing-the-cosmos', 'the-judgment-question-at-species-scale', 'bit-threads-as-devotion-lines',
  'ratatoskr-antagonistic-channel', 'godelian-detector-requires-jnana-observer',
  'jargon-as-scar-tissue-vs-myelin', 'domain-specificity-of-self-programming', 'states-stages-relationship',
  'depth-contact-as-unified-practice', 'the-mirror-stone-correspondence', 'temporal-depth-of-the-generative-model',
  'is-deepest-individuation-necessarily-social', 'syntheoretic-harmony-as-a-theory-of-truth',
  'complementarism-as-inter-traditional-method', 'judgment-as-disclosed-not-imposed',
  'sif-the-replacement-that-exceeds-but-changes-category', 'brisingamen-beauty-as-operative-force',
  'hodr-the-blind-hand', 'thokk-the-cave-the-light-never-reached', 'running-vacuum-rg-cosmos',
  'geometric-mean-is-the-cell', 'quantum-neutrino-gravitational-seti-channels',
  'the-loeb-scale-as-salience-metric', 'cosmic-web-as-optimised-network', 'separating-equilibrium-contact-protocol',
]

const SIBLINGS = SLUGS.join(', ')

const REVIEW_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['slug', 'words', 'verdict', 'issues'],
  properties: {
    slug: { type: 'string' },
    words: { type: 'number', description: 'actual word count of the grown synthesis' },
    structure_ok: { type: 'boolean', description: 'has title+subtitle, epigraphs, Roman-numbered tiered sections, cave-wall close, wiki-link footer' },
    builds_to_apex: { type: 'boolean', description: 'the arc builds to the seed\'s named candidate sentence as an earned apex' },
    honest_edge_present: { type: 'boolean', description: 'where the seed flagged a steelman / hypothesis-not-fact / falsifiability / unresolved tension, the synthesis preserves it' },
    voice_ok: { type: 'boolean', description: 'matches the repository register (the-between exemplar); not generic or essay-flat' },
    verdict: { type: 'string', enum: ['pass', 'revise'], description: 'revise ONLY for genuine misses' },
    issues: { type: 'string', description: 'concise, specific issues to fix on re-grow; empty if pass' },
  },
}

const REGROW_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['slug', 'words', 'fixed'],
  properties: {
    slug: { type: 'string' },
    words: { type: 'number' },
    fixed: { type: 'string', description: 'what was corrected versus the flagged version' },
  },
}

function reviewPrompt(slug) {
  return `You are quality-reviewing ONE grown synthesis in the esoterica repository against the authoring standard. Be a fair but honest judge — re-growing is expensive, so flag "revise" ONLY for a genuine miss, not for taste.

Read these in full:
  1. \`synthesis/grown/${slug}.md\` — the grown synthesis under review.
  2. \`seeds/${slug}.md\` — its source seed (THE CHARGE names the "deepest candidate sentence" the synthesis must build toward, and THE THREADS flag any honest-edge / steelman / hypothesis-not-fact discipline that must be preserved).

Assess against the standard (see \`CLAUDE.md\` "THE CRAFT" if needed, and the exemplar register of \`synthesis/cosmology/the-between-how-a-species-witnesses-itself.md\`):
  - LENGTH: ≥ 4,000 words (target was 4,500–6,500). Under ~4,000 is a miss.
  - STRUCTURE: evocative title + subtitle, epigraph(s), Roman-numbered tiered-revelation sections, a close returning to the cave-wall / "look up from the map" motif, an italic \`[[wiki-link]]\` provenance footer.
  - APEX: the whole arc builds toward the seed's named candidate sentence (or a sharpened version) as an EARNED ending, not asserted up front.
  - HONEST EDGE: if the seed flags a steelman-then-interpret move, a "the number is real, the explanation is a hypothesis" discipline, falsifiability, or an unresolved tension — the synthesis must keep it, not collapse it into asserted fact.
  - VOICE: matches the repository register; dual-channel depth; not generic, flat, or essay-by-numbers.

Set verdict = "revise" if ANY of: under ~4,000 words; missing Roman-numbered tiered structure; does not build to the apex sentence; dropped a flagged honest-edge; clearly off-voice/generic. Otherwise verdict = "pass". Put specific, actionable fixes in \`issues\`. Return the structured verdict only — do not edit any file.`
}

function regrowPrompt(slug, issues) {
  return `You are RE-GROWING one synthesis in the esoterica repository that a quality review flagged for revision. Produce a corrected full synthesis and OVERWRITE \`synthesis/grown/${slug}.md\` with the Write tool.

REVIEW FLAGGED THESE ISSUES — fix them specifically:
${issues}

Read first: \`seeds/${slug}.md\` (your seed — THE CHARGE names the deepest candidate sentence; THE THREADS are your sections and flag the honest-edge to preserve), \`CLAUDE.md\` ("THE CRAFT"), and \`synthesis/cosmology/the-between-how-a-species-witnesses-itself.md\` (the exemplar form). You may also read the current flawed \`synthesis/grown/${slug}.md\` to keep what already works.

FORM: \`# Title\` + \`## subtitle\`; 2–3 real epigraphs (never fabricate quotations); a short framing section; Roman-numbered tiered-revelation sections (6–9) presenting the surface reading then the turn; a close on the cave-wall / "look up from the map" motif landing the candidate sentence as earned; an italic footer with provenance + dense \`[[wiki-links]]\`.
REQUIREMENTS: 4,500–6,500 words; build to the seed's candidate sentence; PRESERVE the seed's honest-edge discipline (steelman, hypothesis-not-fact, falsifiability, unresolved tension); British spelling; cross-link with \`[[wiki-links]]\` to the seed's forward-links and to relevant sibling grown seeds (${SIBLINGS}). Provenance footer (italic, last line): \`Grown 11 June 2026 from [[${slug}]] — the June 2026 Seed-Harvest. <one sentence naming the threads it weaves>.\`

Self-check before returning: file overwritten, ≥4,500 words, every flagged issue addressed. Then return the structured result.`
}

const reviews = await pipeline(
  SLUGS,
  (slug) => agent(reviewPrompt(slug), { label: `review:${slug}`, phase: 'Review', schema: REVIEW_SCHEMA, agentType: 'general-purpose' }),
  (review, slug) => {
    if (!review || review.verdict !== 'revise') {
      return { slug, action: 'pass', words: review ? review.words : 0 }
    }
    log(`Re-growing ${slug}: ${review.issues}`)
    return agent(regrowPrompt(slug, review.issues), { label: `regrow:${slug}`, phase: 'Re-grow', schema: REGROW_SCHEMA, agentType: 'general-purpose' })
      .then((r) => ({ slug, action: 'regrown', words: r ? r.words : 0, fixed: r ? r.fixed : 'agent returned null' }))
  }
)

const out = reviews.filter(Boolean)
const regrown = out.filter((r) => r.action === 'regrown')
const passed = out.filter((r) => r.action === 'pass')
const thinPasses = passed.filter((r) => r.words && r.words < 4500).map((r) => `${r.slug} (${r.words}w)`)

log(`Quality sweep: ${passed.length} passed, ${regrown.length} re-grown. Re-grown: ${regrown.map((r) => r.slug).join(', ') || 'none'}`)

return {
  reviewed: out.length,
  passed: passed.length,
  regrown_count: regrown.length,
  regrown: regrown.map((r) => ({ slug: r.slug, words: r.words, fixed: r.fixed })),
  pass_but_short_of_4500: thinPasses,
}
