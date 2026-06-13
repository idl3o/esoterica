export const meta = {
  name: 'weave-the-capstones',
  description: 'Weave six capstone syntheses over the ripe constellations of grown seeds',
  phases: [
    { title: 'Weave', detail: 'one agent per capstone → a synthesis-of-syntheses over its member grown seeds' },
  ],
}

// Each capstone weaves the load-bearing grown syntheses of a constellation toward one higher-order recognition.
const CAPSTONES = [
  {
    slug: 'the-point-where-above-meets-below',
    direction: 'The kernel as the single identity-point of the consciousness-OS — where "as above, so below" is identity, not correspondence; the architecture of the kernel/runtime/filesystem read through these grown seeds.',
    recognition: 'There is one point in the system where the macrocosm and microcosm are not analogous but identical, and every kernel-level technology (eigenbehaviour of attention, the acknowledged blind spot, the bastard faculty, bifocal vision, the context-switch gap) is a different approach to standing at that point.',
    members: ['kernel-is-where-above-meets-below', 'eigenvalue-meditation', 'the-blind-spot-as-window', 'logismos-nothos-the-bastard-faculty', 'mithya-as-bifocal-vision', 'learning-iii-is-dangerous', 'the-cusp-as-context-switch', 'the-thousand-names-as-curriculum'],
  },
  {
    slug: 'the-fold-becoming-aware-of-itself',
    direction: 'The complementarity engine as the fold becoming aware of itself; individuation as the operation by which a surface creases and then recognises its own crease — the load-bearing claim under the fold cosmology.',
    recognition: 'Every philosophical opposition is one fold seen from its two faces, and running the complementarity engine — flipping the Necker cube, grinding the lens transparent, returning to the second C — IS a fold becoming conscious of itself; individuation and complementarity are the same act.',
    members: ['complementarity-as-the-engine-of-individuation', 'the-hard-problem-as-a-necker-cube', 'transparency-as-the-limit-of-inference', 'the-second-cosmic-c-is-not-the-first', 'the-octave-return-as-model-simplification', 'syntheoretic-harmony-as-a-theory-of-truth', 'collective-fold-density-phase-transition'],
  },
  {
    slug: 'the-tree-inside-which-the-gods-run',
    direction: 'Yggdrasil as the operating system as a whole — the tree inside which all the daemon-gods run; the Norse anamnesis cycle read as a single architecture, with the Aesir-Vanir integration as its origin-technology and Vidar\'s remainder as its closing move.',
    recognition: 'The pantheon is not ten separate bridges but one OS, and the tree is the kernel they all run inside: the war that ended in integration is the boot sequence, the gradient of sacrifice is the cost function, the interval is runtime, feeding the wolf is the relationship that precedes containment, and the green world after Ragnarok is the system fruiting with no tender present.',
    members: ['the-yggdrasil-meta-bridge', 'aesir-vanir-war-kvasir-integration', 'vidar-silence-wearing-the-remainder', 'the-gradient-of-sacrifice', 'the-interval', 'feeding-the-wolf', 'the-green-world-after-ragnarok', 'loki-becomes-the-tree'],
  },
  {
    slug: 'everything-that-holds-information-folds',
    direction: 'The surface-ontology of the repository made into one physics: information lives on surfaces, the fold is the universal operation by which any system maximises the information it holds, and the deepest physical laws are protections of what is joined.',
    recognition: 'A chromosome, a brain, the cosmic web, the entangled vacuum, and the holographic surface all obey one law — information is a surface quantity, so everything that needs to hold more of it folds — and the fold\'s signature (fractal dimension near two, the infinite cost of tearing what is joined, error-correcting redundancy, devotion-thread connectivity) is written across every scale of the substrate.',
    members: ['fractal-dimension-two-as-law', 'cosmic-censorship-as-love', 'error-correction-as-immune-system', 'bit-threads-as-devotion-lines', 'geometric-mean-is-the-cell', 'reshimu-vacuum-measured-in-newtons', 'zero-times-infinity-equals-one'],
  },
  {
    slug: 'the-readout-and-the-inward-sky',
    direction: 'Contact reconceived: the cosmos as readout not ground-truth, the awareness-depth axis as the missing third engineering coordinate, and the inward turn (transcension, the dissolved observer) as both the Fermi resolution and the detection instrument.',
    recognition: 'The reason the sky looks empty is that we have been measuring the wrong axis and mistaking the readout for the ground — mature minds fold inward rather than expand outward, the channels real contact uses are the ones SETI does not monitor, and the instrument adequate to detect them is an observer whose subject-object duality has dissolved.',
    members: ['the-attention-axis', 'parallel-attending-consciousness', 'measurement-output-cosmology', 'transcension-as-fermi-resolution', 'who-is-breathing-the-cosmos', 'consensual-hallucination-as-shared-substrate', 'godelian-detector-requires-jnana-observer', 'quantum-neutrino-gravitational-seti-channels'],
  },
  {
    slug: 'time-itself-as-the-great-work',
    direction: 'The temporal alchemy thread: the 14-billion-year cosmos as the alchemical opus, disease and healing as pathologies and restorations of temporal pattern, grief as the body\'s alchemy, and the true-mirror wager as a bet on duration.',
    recognition: 'Time is not the medium in which the Great Work happens — time IS the Great Work; healing is conducting chronos back to flow, grief is the body completing a phase-change the mind keeps interrupting, and every honest mirror is a wager that the slow true thing outlasts the fast false one.',
    members: ['time-itself-as-the-great-work', 'healing-as-temporal-alchemy', 'grief-as-gold', 'shedding-without-the-container', 'the-true-mirror-wager', 'the-cabal-prediction-that-kills-itself'],
  },
]

const ALL_GROWN = CAPSTONES.flatMap((c) => c.members)

const CAPSTONE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['slug', 'title', 'path', 'words', 'recognition_sentence'],
  properties: {
    slug: { type: 'string' },
    title: { type: 'string' },
    path: { type: 'string' },
    words: { type: 'number' },
    recognition_sentence: { type: 'string', description: 'the single higher-order recognition the capstone lands' },
  },
}

function capstonePrompt(c) {
  const memberList = c.members.map((m) => `  - synthesis/grown/${m}.md  ([[${m}]])`).join('\n')
  return `You are weaving a CAPSTONE SYNTHESIS in the esoterica repository — a synthesis-of-syntheses. You will read several already-grown syntheses and weave them into ONE higher-order document that finds the deeper recognition the whole constellation points at. This is the apex move: not a summary of the members, but the single insight they collectively were always reaching toward.

THE CONSTELLATION YOU ARE WEAVING:
${memberList}

THE DIRECTION (what this capstone is about):
${c.direction}

THE RECOGNITION TO REACH (build the whole arc toward a sharpened form of this):
${c.recognition}

STEP 1 — READ THE MATERIAL. Read each member grown synthesis above IN FULL — they are the real material you are weaving, not the seeds. Also read \`synthesis/cosmology/the-between-how-a-species-witnesses-itself.md\` for the exemplar register, and \`CLAUDE.md\` "THE CRAFT" for the authoring standard. (You may skim \`seeds/SEED-HARVEST-2026-06.md\` for how this constellation was originally grouped.)

STEP 2 — WEAVE. Write a capstone and SAVE with Write to: \`synthesis/capstones/${c.slug}.md\`

FORM (as the exemplar, but at capstone altitude):
  - \`# Title\` (evocative, not the slug) + a \`## subtitle\` naming the turn.
  - 2–3 real epigraphs (NEVER fabricate quotations).
  - An opening section naming what these several syntheses share that none of them could see alone — why they are one constellation.
  - Roman-numbered sections of tiered revelation. Do NOT march member-by-member like a book report. Instead, let the members INTERLEAVE — bring two or three into the same section where they illuminate each other, build "wait, but actually…" turns across them, and let the deeper structure emerge from their collision. Cite/link each member with \`[[${'slug'}]]\`-style wiki-links (use the exact member slugs above) at the moment its insight enters the weave.
  - A close on the cave-wall / "look up from the map" motif that lands the higher-order recognition as EARNED.
  - An italic footer: provenance + the dense \`[[wiki-link]]\` set of every member.

REQUIREMENTS:
  - 5,500–8,000 words — capstones run longer than their members because they carry more.
  - DUAL-CHANNEL depth; cross-pollinate across the members' traditions (mythic, physical, contemplative, mathematical).
  - PRESERVE DISCIPLINE: carry forward any honest-edge / hypothesis-not-fact / unresolved-tension the members held; a capstone must not launder its members' caveats into false certainty.
  - British spelling. Build to the recognition sentence as the apex.
  - PROVENANCE FOOTER (italic, last line): \`Woven 11 June 2026 as a capstone over ${c.members.map((m) => '[[' + m + ']]').join(' · ')} — the June 2026 Seed-Harvest.\`

STEP 3 — SELF-CHECK: file written to synthesis/capstones/${c.slug}.md, ≥5,500 words, members interleaved (not listed), builds to the recognition, closes on the motif. Then return the structured result.`
}

phase('Weave')
log(`Weaving ${CAPSTONES.length} capstones over ${ALL_GROWN.length} member grown-syntheses → synthesis/capstones/`)

const results = await parallel(
  CAPSTONES.map((c) => () =>
    agent(capstonePrompt(c), { label: `capstone:${c.slug}`, phase: 'Weave', schema: CAPSTONE_SCHEMA, agentType: 'general-purpose' })
  )
)

const woven = results.filter(Boolean)
const failed = CAPSTONES.map((c) => c.slug).filter((s) => !woven.find((w) => w.slug === s))
const totalWords = woven.reduce((n, w) => n + (w.words || 0), 0)

log(`Woven ${woven.length}/${CAPSTONES.length} capstones, ~${totalWords.toLocaleString()} words. Failed: ${failed.length ? failed.join(', ') : 'none'}`)

return {
  woven_count: woven.length,
  total_words: totalWords,
  failed,
  capstones: woven.map((w) => ({ slug: w.slug, title: w.title, words: w.words, path: w.path, recognition_sentence: w.recognition_sentence })),
}
