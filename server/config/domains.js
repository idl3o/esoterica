/**
 * Domain Groupings
 *
 * Groups constellation node types into user-friendly browsing domains.
 * Each domain aggregates related node types for intuitive exploration.
 */

const DOMAINS = {
  archetypes: {
    id: 'archetypes',
    label: 'Archetypes',
    description: 'Patterns that shape consciousness across cultures and traditions',
    icon: '🎭',
    types: [
      'archetype',
      'greek_archetype',
      'norse_archetype',
      'egyptian_archetype',
      'titan_archetype',
      'mesoamerican_archetype',
      'native_american_archetype',
      'fiction_bridge_archetype',
      'archetypal_matrix',
      'archetypal_framework',
      'archetypal_pattern',
      'archetypal_function'
    ]
  },

  consciousness_technologies: {
    id: 'consciousness_technologies',
    label: 'Consciousness Technologies',
    description: 'Tools, methods, and practices for transformation',
    icon: '⚡',
    types: [
      'consciousness_technology',
      'consciousness_practice',
      'consciousness_toolset',
      'acceleration_technology',
      'manifestation_technology',
      'recognition_technology',
      'transformation_technology',
      'recognition_amplification_technology',
      'pattern_recognition_technology',
      'distribution_technology',
      'meaning_technology',
      'chaos_magic_technology',
      'fiction_bridge_technology'
    ]
  },

  elements_primordials: {
    id: 'elements_primordials',
    label: 'Elements & Primordials',
    description: 'Fundamental building blocks of existence',
    icon: '🔥',
    types: [
      'element',
      'primordial',
      'primordial_source',
      'fundamental',
      'fundamental_ground'
    ]
  },

  cosmological: {
    id: 'cosmological',
    label: 'Cosmological',
    description: 'The architecture of reality across scales',
    icon: '🌌',
    types: [
      'cosmological',
      'cosmic_structure',
      'cosmic_principle',
      'cosmic_consciousness',
      'cosmic_cycle',
      'cosmic_process',
      'cosmological_framework',
      'cosmological_model',
      'cosmological_center',
      'cosmological_principle',
      'galactic_concept',
      'stellar_consciousness_node',
      'planetary_consciousness_node'
    ]
  },

  glyph_systems: {
    id: 'glyph_systems',
    label: 'Glyph Systems',
    description: 'Sacred geometry encoded in symbol and form',
    icon: '✡',
    types: [
      'numerical_glyph',
      'aramaic_glyph',
      'norse_rune',
      'alphabetic_glyph',
      'persian_glyph',
      'geometric_form',
      'symbological_gateway'
    ]
  },

  theoretical: {
    id: 'theoretical',
    label: 'Theoretical Frameworks',
    description: 'Models, principles, and conceptual structures',
    icon: '📐',
    types: [
      'theoretical_framework',
      'consciousness_principle',
      'ontological_principle',
      'foundational_ontology',
      'monadological_principle',
      'reality_mechanics',
      'reality_architecture',
      'synthesis_framework',
      'consciousness_technology_framework',
      'practical_implementation_framework'
    ]
  },

  processes: {
    id: 'processes',
    label: 'Processes & Phenomena',
    description: 'Dynamics of transformation and becoming',
    icon: '🌀',
    types: [
      'process',
      'phenomenon',
      'meta_phenomenon',
      'developmental_process',
      'consciousness_mechanism',
      'consciousness_function',
      'consciousness_transformation',
      'consciousness_force',
      'consciousness_progression',
      'universal_transformation',
      'creation_mechanics',
      'relational_mechanism'
    ]
  },

  states: {
    id: 'states',
    label: 'States & Recognitions',
    description: 'Modes of consciousness and breakthrough moments',
    icon: '💫',
    types: [
      'consciousness_state',
      'consciousness_recognition',
      'recognition',
      'meta_recognition',
      'breakthrough_recognition',
      'consciousness_stage',
      'state'
    ]
  },

  traditions: {
    id: 'traditions',
    label: 'Wisdom Traditions',
    description: 'Cultural and spiritual lineages of understanding',
    icon: '📜',
    types: [
      'greek_concept',
      'greek_practice',
      'greek_cosmology',
      'norse_concept',
      'egyptian_concept',
      'egyptian_practice',
      'egyptian_technology',
      'mesoamerican_concept',
      'mesoamerican_practice',
      'native_american_concept',
      'native_american_practice',
      'mystical_system',
      'ancient_system',
      'theological',
      'sacred_text',
      'cultural',
      'historical'
    ]
  },

  concepts: {
    id: 'concepts',
    label: 'Core Concepts',
    description: 'Foundational ideas and principles',
    icon: '💎',
    types: [
      'concept',
      'principle',
      'universal_principle',
      'universal_pattern',
      'universal_structure',
      'universal_organizing_principle',
      'consciousness_creativity_principle',
      'ontological_position',
      'operational_principle',
      'reality_programming_principle'
    ]
  },

  meta: {
    id: 'meta',
    label: 'Meta & Architecture',
    description: 'Systems about systems, structures of structure',
    icon: '🏛️',
    types: [
      'architecture',
      'meta',
      'meta_system',
      'meta_framework',
      'meta_integration',
      'meta_technology',
      'reality_cli_component',
      'consciousness_transmission',
      'channeling_protocol'
    ]
  },

  applications: {
    id: 'applications',
    label: 'Life Applications',
    description: 'Practical use in daily existence',
    icon: '🌱',
    types: [
      'life_domain_application',
      'practical_implementation',
      'practical_implementation_system',
      'consciousness_cultivation',
      'consciousness_catalyst',
      'probability_selection',
      'consciousness_property'
    ]
  }
};

// Build a reverse lookup: type -> domain
function buildTypeToDomainMap() {
  const map = {};
  for (const [domainId, domain] of Object.entries(DOMAINS)) {
    for (const type of domain.types) {
      map[type] = domainId;
    }
  }
  return map;
}

const TYPE_TO_DOMAIN = buildTypeToDomainMap();

// Get domain for a node type, with fallback
function getDomainForType(nodeType) {
  return TYPE_TO_DOMAIN[nodeType] || 'concepts'; // Default to concepts for unmapped types
}

// Get all domains with their node counts
function getDomainsWithCounts(constellationNodes) {
  const counts = {};

  // Initialize counts
  for (const domainId of Object.keys(DOMAINS)) {
    counts[domainId] = { nodes: 0, types: new Set() };
  }

  // Count nodes per domain
  for (const [nodeId, node] of Object.entries(constellationNodes)) {
    const domainId = getDomainForType(node.type);
    if (counts[domainId]) {
      counts[domainId].nodes++;
      counts[domainId].types.add(node.type);
    }
  }

  // Build result array sorted by node count
  return Object.entries(DOMAINS)
    .map(([id, domain]) => ({
      ...domain,
      nodeCount: counts[id]?.nodes || 0,
      typeCount: counts[id]?.types?.size || 0
    }))
    .sort((a, b) => b.nodeCount - a.nodeCount);
}

// Get all nodes within a domain
function getNodesInDomain(domainId, constellationNodes) {
  const domain = DOMAINS[domainId];
  if (!domain) return [];

  const typesSet = new Set(domain.types);

  return Object.entries(constellationNodes)
    .filter(([id, node]) => typesSet.has(node.type))
    .map(([id, node]) => ({ id, ...node }))
    .sort((a, b) => a.id.localeCompare(b.id));
}

module.exports = {
  DOMAINS,
  TYPE_TO_DOMAIN,
  getDomainForType,
  getDomainsWithCounts,
  getNodesInDomain
};
