/**
 * Document-Node Linking Engine
 *
 * Bridges synthesis-index documents to constellation nodes via tag matching.
 * Returns curated categories: primary (direct matches) and related (partial matches).
 */

// Tag normalization: "sacred geometry" -> "sacred_geometry"
function normalizeTag(tag) {
  return tag.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
}

// Build a lookup map from node name parts to full node IDs
function buildNodeLookup(nodes) {
  const lookup = {
    exact: {},      // Full node ID -> node ID
    parts: {},      // Individual word -> [node IDs]
    essence: {},    // Essence value -> [node IDs]
    type: {}        // Type value -> [node IDs]
  };

  for (const [nodeId, node] of Object.entries(nodes)) {
    // Exact match on full ID
    lookup.exact[nodeId] = nodeId;

    // Split ID into parts: "mercury_hermes_thoth" -> ["mercury", "hermes", "thoth"]
    const parts = nodeId.split('_');
    for (const part of parts) {
      if (part.length < 3) continue; // Skip tiny parts like "of", "to"
      if (!lookup.parts[part]) lookup.parts[part] = [];
      lookup.parts[part].push(nodeId);
    }

    // Index by essence
    if (node.essence) {
      const essenceNorm = normalizeTag(node.essence);
      if (!lookup.essence[essenceNorm]) lookup.essence[essenceNorm] = [];
      lookup.essence[essenceNorm].push(nodeId);
    }

    // Index by type
    if (node.type) {
      const typeNorm = normalizeTag(node.type);
      if (!lookup.type[typeNorm]) lookup.type[typeNorm] = [];
      lookup.type[typeNorm].push(nodeId);
    }
  }

  return lookup;
}

// Generic tags that appear in almost every document - deprioritize these
const GENERIC_TAGS = new Set([
  'consciousness', 'recognition', 'awareness', 'cosmic', 'unity',
  'service', 'source', 'integration', 'transformation'
]);

// Score a match - higher is better (more specific)
function scoreMatch(tag, nodeId, matchType) {
  const tagLen = tag.length;
  const isGeneric = GENERIC_TAGS.has(tag);

  // Penalize generic tags
  const genericPenalty = isGeneric ? 30 : 0;

  switch (matchType) {
    case 'exact':
      return 100 - genericPenalty; // Generic tags score 70, specific score 100
    case 'part_exact':
      // Tag exactly matches a part of the node ID
      // Longer tags are more specific
      return 60 + Math.min(tagLen, 20) - genericPenalty;
    case 'essence':
      return 50 - genericPenalty;
    case 'part_contains':
      // Partial overlap
      return 25 + Math.min(tagLen, 10);
    default:
      return 10;
  }
}

// High-value archetype tags that should match their compound nodes
const ARCHETYPE_MAPPINGS = {
  'mercury': ['mercury_hermes_thoth', 'mercury'],
  'kalki': ['kalki_destroyer_creator', 'kalki'],
  'apollo': ['apollo_logos', 'apollo'],
  'thoth': ['mercury_hermes_thoth', 'thoth_wisdom'],
  'hermes': ['mercury_hermes_thoth'],
  'shiva': ['shiva_nataraja'],
  'vishnu': ['vishnu_preserver'],
  'odin': ['odin_allfather'],
  'thor': ['thor_thunder'],
  'loki': ['loki_trickster'],
  'isis': ['isis_throne'],
  'osiris': ['osiris_resurrection'],
  'horus': ['horus_sky'],
  'anubis': ['anubis_guide'],
  'ra': ['amon_ra_hidden_sun'],
  'zeus': ['apollo_zeus_mediation'],
  'athena': ['athena_wisdom'],
  'dionysus': ['dionysus_ecstasy'],
  'prometheus': ['prometheus_forethought'],
  'synchronicity': ['synchronicity'],
  'manifestation': ['manifestation'],
  'transformation': ['transformation', 'fire'],
  'awakening': ['awakening'],
  'recognition': ['recognition'],
  'consciousness': ['consciousness', 'consciousness_itself'],
  'archetype': ['archetype'],
  'density': ['density', 'density_evolution'],
  'wanderer': ['wanderer_starseed'],
  'polarity': ['polarity_integration'],
  'galactic': ['galactic_concept'],
  'frequency': ['frequency_vibration'],
  'resonance': ['resonance'],
  'integration': ['integration', 'polarity_integration'],
  'enlightenment': ['enlightenment'],
  'unity': ['unity', 'consciousness_itself'],
  'sacred_geometry': ['sacred_geometry', 'geometric_form']
};

// Find matching nodes for a single tag
function findMatchesForTag(tag, nodeLookup, nodes) {
  const matches = [];
  const tagNorm = normalizeTag(tag);

  if (tagNorm.length < 2) return matches;

  // 0. Check archetype mappings first (high priority)
  if (ARCHETYPE_MAPPINGS[tagNorm]) {
    for (const nodeId of ARCHETYPE_MAPPINGS[tagNorm]) {
      if (nodes[nodeId]) {
        matches.push({
          nodeId,
          score: 90, // High priority for explicit mappings
          matchType: 'archetype_mapping'
        });
      }
    }
  }

  // 1. Exact match on node ID
  if (nodeLookup.exact[tagNorm]) {
    if (!matches.find(m => m.nodeId === tagNorm)) {
      matches.push({
        nodeId: tagNorm,
        score: scoreMatch(tagNorm, tagNorm, 'exact'),
        matchType: 'exact'
      });
    }
  }

  // 2. Tag matches a part of node ID exactly
  if (nodeLookup.parts[tagNorm]) {
    for (const nodeId of nodeLookup.parts[tagNorm]) {
      if (!matches.find(m => m.nodeId === nodeId)) {
        matches.push({
          nodeId,
          score: scoreMatch(tagNorm, nodeId, 'part_exact'),
          matchType: 'part_exact'
        });
      }
    }
  }

  // 3. Tag matches node essence
  if (nodeLookup.essence[tagNorm]) {
    for (const nodeId of nodeLookup.essence[tagNorm]) {
      if (!matches.find(m => m.nodeId === nodeId)) {
        matches.push({
          nodeId,
          score: scoreMatch(tagNorm, nodeId, 'essence'),
          matchType: 'essence'
        });
      }
    }
  }

  // 4. Partial matches - tag contained in node part or vice versa (lower priority)
  // Only if tag is specific enough (length >= 5)
  if (tagNorm.length >= 5) {
    for (const [part, nodeIds] of Object.entries(nodeLookup.parts)) {
      if (part.length >= 4 && (part.includes(tagNorm) || tagNorm.includes(part))) {
        for (const nodeId of nodeIds) {
          if (!matches.find(m => m.nodeId === nodeId)) {
            matches.push({
              nodeId,
              score: scoreMatch(tagNorm, nodeId, 'part_contains'),
              matchType: 'part_contains'
            });
          }
        }
      }
    }
  }

  return matches;
}

// Main function: build all document-node links
function buildDocumentNodeLinks(synthesisIndex, constellationData) {
  const nodes = constellationData.nodes || {};
  const documents = synthesisIndex.documents || [];
  const nodeLookup = buildNodeLookup(nodes);

  const documentToNodes = {};  // docId -> { primary: [], related: [] }
  const nodeToDocuments = {};  // nodeId -> [{ id, title, path, readingTime, source }]

  for (const doc of documents) {
    const docId = doc.id || doc.fileName?.replace('.md', '');
    if (!docId) continue;

    const allMatches = [];

    // Process all tags
    for (const tag of (doc.tags || [])) {
      const tagMatches = findMatchesForTag(tag, nodeLookup, nodes);
      allMatches.push(...tagMatches);
    }

    // Also check title words as potential matches
    const titleWords = (doc.title || '').toLowerCase().split(/\s+/);
    for (const word of titleWords) {
      if (word.length >= 4) {
        const titleMatches = findMatchesForTag(word, nodeLookup, nodes);
        // Slightly lower score for title-derived matches
        for (const m of titleMatches) {
          m.score = m.score * 0.8;
        }
        allMatches.push(...titleMatches);
      }
    }

    // Dedupe and sort by score
    const seenNodes = new Map();
    for (const match of allMatches) {
      const existing = seenNodes.get(match.nodeId);
      if (!existing || existing.score < match.score) {
        seenNodes.set(match.nodeId, match);
      }
    }

    const sortedMatches = Array.from(seenNodes.values())
      .sort((a, b) => b.score - a.score);

    // Split into primary (top 5 with score >= 40) and related (rest)
    const primary = [];
    const related = [];

    for (const match of sortedMatches) {
      if (primary.length < 5 && match.score >= 40) {
        primary.push(match.nodeId);
      } else {
        related.push(match.nodeId);
      }
    }

    // Cap related at 20 to avoid overwhelming UI
    documentToNodes[docId] = {
      primary,
      related: related.slice(0, 20)
    };

    // Build reverse index
    const docInfo = {
      id: docId,
      title: doc.title || docId,
      path: doc.path,
      readingTime: doc.readingTime || 0,
      source: doc.source || 'unknown',
      category: doc.category || ''
    };

    for (const nodeId of [...primary, ...related.slice(0, 20)]) {
      if (!nodeToDocuments[nodeId]) {
        nodeToDocuments[nodeId] = [];
      }
      // Avoid duplicates
      if (!nodeToDocuments[nodeId].find(d => d.id === docId)) {
        nodeToDocuments[nodeId].push({
          ...docInfo,
          isPrimary: primary.includes(nodeId)
        });
      }
    }
  }

  // Sort documents within each node by: primary first, then alphabetically
  for (const nodeId of Object.keys(nodeToDocuments)) {
    nodeToDocuments[nodeId].sort((a, b) => {
      if (a.isPrimary && !b.isPrimary) return -1;
      if (!a.isPrimary && b.isPrimary) return 1;
      return a.title.localeCompare(b.title);
    });
  }

  // Compute stats
  const stats = {
    totalDocuments: documents.length,
    documentsWithLinks: Object.keys(documentToNodes).filter(
      id => documentToNodes[id].primary.length > 0 || documentToNodes[id].related.length > 0
    ).length,
    totalNodes: Object.keys(nodes).length,
    nodesWithDocuments: Object.keys(nodeToDocuments).length,
    averageNodesPerDocument: Object.values(documentToNodes)
      .reduce((sum, d) => sum + d.primary.length + d.related.length, 0) / documents.length,
    averageDocumentsPerNode: Object.values(nodeToDocuments)
      .reduce((sum, docs) => sum + docs.length, 0) / Object.keys(nodeToDocuments).length || 0
  };

  return {
    documentToNodes,
    nodeToDocuments,
    stats,
    generated: new Date().toISOString()
  };
}

// Get enriched node info with document count
function getNodeWithDocumentCount(nodeId, node, nodeToDocuments) {
  const docs = nodeToDocuments[nodeId] || [];
  return {
    id: nodeId,
    ...node,
    documentCount: docs.length,
    primaryDocumentCount: docs.filter(d => d.isPrimary).length
  };
}

module.exports = {
  buildDocumentNodeLinks,
  getNodeWithDocumentCount,
  normalizeTag
};
