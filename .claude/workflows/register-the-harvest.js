export const meta = {
  name: 'register-the-harvest',
  description: 'Register the 80 grown syntheses + 6 capstones into the constellation as 86 document-nodes (sequential, single writer)',
  phases: [
    { title: 'Extract', detail: 'parallel readers pull each doc\'s apex sentence (essence)' },
    { title: 'Register', detail: 'one registrar writes 87 nodes parent-first via the esoterica MCP' },
  ],
}

const HUB = 'june_2026_grown_harvest'

// capstone slug -> member grown slugs (from weave-the-capstones.js)
const CAPSTONE_MEMBERS = {
  'the-point-where-above-meets-below': ['kernel-is-where-above-meets-below', 'eigenvalue-meditation', 'the-blind-spot-as-window', 'logismos-nothos-the-bastard-faculty', 'mithya-as-bifocal-vision', 'learning-iii-is-dangerous', 'the-cusp-as-context-switch', 'the-thousand-names-as-curriculum'],
  'the-fold-becoming-aware-of-itself': ['complementarity-as-the-engine-of-individuation', 'the-hard-problem-as-a-necker-cube', 'transparency-as-the-limit-of-inference', 'the-second-cosmic-c-is-not-the-first', 'the-octave-return-as-model-simplification', 'syntheoretic-harmony-as-a-theory-of-truth', 'collective-fold-density-phase-transition'],
  'the-tree-inside-which-the-gods-run': ['the-yggdrasil-meta-bridge', 'aesir-vanir-war-kvasir-integration', 'vidar-silence-wearing-the-remainder', 'the-gradient-of-sacrifice', 'the-interval', 'feeding-the-wolf', 'the-green-world-after-ragnarok', 'loki-becomes-the-tree'],
  'everything-that-holds-information-folds': ['fractal-dimension-two-as-law', 'cosmic-censorship-as-love', 'error-correction-as-immune-system', 'bit-threads-as-devotion-lines', 'geometric-mean-is-the-cell', 'reshimu-vacuum-measured-in-newtons', 'zero-times-infinity-equals-one'],
  'the-readout-and-the-inward-sky': ['the-attention-axis', 'parallel-attending-consciousness', 'measurement-output-cosmology', 'transcension-as-fermi-resolution', 'who-is-breathing-the-cosmos', 'consensual-hallucination-as-shared-substrate', 'godelian-detector-requires-jnana-observer', 'quantum-neutrino-gravitational-seti-channels'],
  'time-itself-as-the-great-work': ['time-itself-as-the-great-work', 'healing-as-temporal-alchemy', 'grief-as-gold', 'shedding-without-the-container', 'the-true-mirror-wager', 'the-cabal-prediction-that-kills-itself'],
}

const ALL_GROWN = [
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

const CAPSTONES = Object.keys(CAPSTONE_MEMBERS)
const memberToCapstone = {}
for (const cap of CAPSTONES) for (const m of CAPSTONE_MEMBERS[cap]) memberToCapstone[m] = cap
const toId = (slug) => slug.replace(/-/g, '_')

const EXTRACT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['slug', 'essence'],
  properties: {
    slug: { type: 'string' },
    title: { type: 'string' },
    essence: { type: 'string', description: 'the single apex/candidate sentence the document builds to, verbatim or lightly trimmed to one sentence' },
  },
}

const REGISTER_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['nodes_added', 'errors'],
  properties: {
    nodes_added: { type: 'number' },
    hub_added: { type: 'boolean' },
    errors: { type: 'array', items: { type: 'string' } },
  },
}

function extractPrompt(slug, dir) {
  return `Read \`synthesis/${dir}/${slug}.md\` and extract its ESSENCE: the single apex sentence the whole document builds toward (in a grown synthesis this is the deepest candidate sentence near the end; in a capstone it is the higher-order recognition it lands). Return it as ONE sentence (trim to a single sentence if it runs long, preserving the core), plus the document's title. Read-only — do not modify anything. Return the structured result for slug "${slug}".`
}

// ---- Phase 1: parallel reads (safe) ----
phase('Extract')
log(`Extracting essences from ${ALL_GROWN.length} grown + ${CAPSTONES.length} capstone documents`)

const grownSpecs = await parallel([
  ...ALL_GROWN.map((slug) => () => agent(extractPrompt(slug, 'grown'), { label: `read:${slug}`, phase: 'Extract', schema: EXTRACT_SCHEMA, agentType: 'general-purpose' })),
  ...CAPSTONES.map((slug) => () => agent(extractPrompt(slug, 'capstones'), { label: `read:${slug}`, phase: 'Extract', schema: EXTRACT_SCHEMA, agentType: 'general-purpose' })),
])

const essenceBySlug = {}
for (const s of grownSpecs.filter(Boolean)) essenceBySlug[s.slug] = s.essence

// ---- Build the ordered, parent-first node list ----
const NODES = []
NODES.push({
  node_id: HUB,
  type: 'harvest',
  essence: 'The June 2026 seed-harvest grown whole: 80 planted seed-crystals precipitated into full syntheses and woven into 6 capstone constellations.',
  document: 'seeds/SEED-HARVEST-2026-06.md',
  connections: [],
})
for (const cap of CAPSTONES) {
  NODES.push({
    node_id: toId(cap),
    type: 'capstone',
    essence: essenceBySlug[cap] || `Capstone synthesis: ${cap.replace(/-/g, ' ')}.`,
    document: `synthesis/capstones/${cap}.md`,
    connections: [HUB],
  })
}
for (const g of ALL_GROWN) {
  const parent = memberToCapstone[g] ? toId(memberToCapstone[g]) : HUB
  NODES.push({
    node_id: toId(g),
    type: 'grown_synthesis',
    essence: essenceBySlug[g] || `Grown synthesis: ${g.replace(/-/g, ' ')}.`,
    document: `synthesis/grown/${g}.md`,
    connections: [parent],
  })
}

// ---- Phase 2: single registrar, sequential writes ----
phase('Register')
log(`Registering ${NODES.length} nodes (1 hub + ${CAPSTONES.length} capstones + ${ALL_GROWN.length} grown), parent-first, single writer`)

function registerPrompt(nodes) {
  return `You are the SOLE WRITER registering the June-2026 grown harvest into the esoterica constellation graph. You must work STRICTLY SEQUENTIALLY — one write at a time — because the graph persists to a single shared file and concurrent writes would corrupt it.

STEP 1 — Load the MCP tool: use ToolSearch with query "select:mcp__esoterica__add_node" to load the add_node schema.

STEP 2 — Call add_node ONCE for EACH node in the array below, IN THE GIVEN ORDER (the order is parent-first, so every node's \`connections\` target already exists by the time you create it). For each entry pass: node_id, type, essence, document, and connections (array). Do them one at a time, in order. If a single add_node fails (e.g. duplicate id), record the id in your errors list and CONTINUE with the next — do not abort the whole run.

The nodes, in order:
${JSON.stringify(nodes, null, 0)}

STEP 3 — Return the structured result: nodes_added (how many add_node calls succeeded), hub_added (whether "${HUB}" was created), and errors (array of "node_id: reason" for any that failed).

Do NOT call add_node in parallel. Do NOT skip any. Do NOT modify or remove existing nodes.`
}

const result = await agent(registerPrompt(NODES), { label: 'registrar', phase: 'Register', schema: REGISTER_SCHEMA, agentType: 'general-purpose' })

log(`Registration complete: ${result ? result.nodes_added : 0}/${NODES.length} nodes added. Errors: ${result && result.errors && result.errors.length ? result.errors.join('; ') : 'none'}`)

return {
  intended: NODES.length,
  result,
  essences_missing: [...ALL_GROWN, ...CAPSTONES].filter((s) => !essenceBySlug[s]),
}
