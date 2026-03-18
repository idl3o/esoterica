/**
 * Document-Node Linking Engine
 *
 * Port of server/lib/document-links.js — builds bidirectional mappings
 * between synthesis documents and constellation nodes via tag matching.
 */

import type { ConstellationData } from './constellation';

// --- Types ---

export interface DocumentMeta {
  id: string;
  title: string;
  path: string;
  readingTime: number;
  source: string;
  category: string;
  tags?: string[];
}

export interface DocumentNodeLinks {
  documentToNodes: Record<string, { primary: string[]; related: string[] }>;
  nodeToDocuments: Record<string, NodeDocument[]>;
  stats: LinkStats;
}

export interface NodeDocument {
  id: string;
  title: string;
  path: string;
  readingTime: number;
  source: string;
  category: string;
  isPrimary: boolean;
}

interface LinkStats {
  totalDocuments: number;
  documentsWithLinks: number;
  totalNodes: number;
  nodesWithDocuments: number;
  averageNodesPerDocument: number;
  averageDocumentsPerNode: number;
}

interface NodeLookup {
  exact: Record<string, string>;
  parts: Record<string, string[]>;
  essence: Record<string, string[]>;
  type: Record<string, string[]>;
}

interface Match {
  nodeId: string;
  score: number;
  matchType: string;
}

// --- Constants ---

const GENERIC_TAGS = new Set([
  'consciousness', 'recognition', 'awareness', 'cosmic', 'unity',
  'service', 'source', 'integration', 'transformation'
]);

const ARCHETYPE_MAPPINGS: Record<string, string[]> = {
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

// --- Functions ---

function normalizeTag(tag: string): string {
  return tag.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
}

function buildNodeLookup(nodes: Record<string, any>): NodeLookup {
  const lookup: NodeLookup = { exact: {}, parts: {}, essence: {}, type: {} };

  for (const [nodeId, node] of Object.entries(nodes)) {
    lookup.exact[nodeId] = nodeId;

    const parts = nodeId.split('_');
    for (const part of parts) {
      if (part.length < 3) continue;
      if (!lookup.parts[part]) lookup.parts[part] = [];
      lookup.parts[part].push(nodeId);
    }

    if (node.essence) {
      const essenceNorm = normalizeTag(node.essence);
      if (!lookup.essence[essenceNorm]) lookup.essence[essenceNorm] = [];
      lookup.essence[essenceNorm].push(nodeId);
    }

    if (node.type) {
      const typeNorm = normalizeTag(node.type);
      if (!lookup.type[typeNorm]) lookup.type[typeNorm] = [];
      lookup.type[typeNorm].push(nodeId);
    }
  }

  return lookup;
}

function scoreMatch(tag: string, _nodeId: string, matchType: string): number {
  const tagLen = tag.length;
  const isGeneric = GENERIC_TAGS.has(tag);
  const genericPenalty = isGeneric ? 30 : 0;

  switch (matchType) {
    case 'exact': return 100 - genericPenalty;
    case 'part_exact': return 60 + Math.min(tagLen, 20) - genericPenalty;
    case 'essence': return 50 - genericPenalty;
    case 'part_contains': return 25 + Math.min(tagLen, 10);
    default: return 10;
  }
}

function findMatchesForTag(tag: string, nodeLookup: NodeLookup, nodes: Record<string, any>): Match[] {
  const matches: Match[] = [];
  const tagNorm = normalizeTag(tag);
  if (tagNorm.length < 2) return matches;

  // Archetype mappings
  if (ARCHETYPE_MAPPINGS[tagNorm]) {
    for (const nodeId of ARCHETYPE_MAPPINGS[tagNorm]) {
      if (nodes[nodeId]) {
        matches.push({ nodeId, score: 90, matchType: 'archetype_mapping' });
      }
    }
  }

  // Exact match
  if (nodeLookup.exact[tagNorm] && !matches.find(m => m.nodeId === tagNorm)) {
    matches.push({
      nodeId: tagNorm,
      score: scoreMatch(tagNorm, tagNorm, 'exact'),
      matchType: 'exact'
    });
  }

  // Part exact match
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

  // Essence match
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

  // Partial contains
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

export function buildDocumentNodeLinks(
  documents: DocumentMeta[],
  constellation: ConstellationData
): DocumentNodeLinks {
  const nodes = constellation.nodes || {};
  const nodeLookup = buildNodeLookup(nodes);

  const documentToNodes: Record<string, { primary: string[]; related: string[] }> = {};
  const nodeToDocuments: Record<string, NodeDocument[]> = {};

  for (const doc of documents) {
    const docId = doc.id;
    if (!docId) continue;

    const allMatches: Match[] = [];

    for (const tag of (doc.tags || [])) {
      allMatches.push(...findMatchesForTag(tag, nodeLookup, nodes));
    }

    // Title words as matches (slightly lower score)
    const titleWords = (doc.title || '').toLowerCase().split(/\s+/);
    for (const word of titleWords) {
      if (word.length >= 4) {
        const titleMatches = findMatchesForTag(word, nodeLookup, nodes);
        for (const m of titleMatches) m.score = m.score * 0.8;
        allMatches.push(...titleMatches);
      }
    }

    // Dedupe, keep highest score per node
    const seenNodes = new Map<string, Match>();
    for (const match of allMatches) {
      const existing = seenNodes.get(match.nodeId);
      if (!existing || existing.score < match.score) {
        seenNodes.set(match.nodeId, match);
      }
    }

    const sortedMatches = Array.from(seenNodes.values()).sort((a, b) => b.score - a.score);

    const primary: string[] = [];
    const related: string[] = [];

    for (const match of sortedMatches) {
      if (primary.length < 5 && match.score >= 40) {
        primary.push(match.nodeId);
      } else {
        related.push(match.nodeId);
      }
    }

    documentToNodes[docId] = { primary, related: related.slice(0, 20) };

    const docInfo: Omit<NodeDocument, 'isPrimary'> = {
      id: docId,
      title: doc.title || docId,
      path: doc.path,
      readingTime: doc.readingTime || 0,
      source: doc.source || 'unknown',
      category: doc.category || ''
    };

    for (const nodeId of [...primary, ...related.slice(0, 20)]) {
      if (!nodeToDocuments[nodeId]) nodeToDocuments[nodeId] = [];
      if (!nodeToDocuments[nodeId].find(d => d.id === docId)) {
        nodeToDocuments[nodeId].push({
          ...docInfo,
          isPrimary: primary.includes(nodeId)
        });
      }
    }
  }

  // Sort docs within each node
  for (const nodeId of Object.keys(nodeToDocuments)) {
    nodeToDocuments[nodeId].sort((a, b) => {
      if (a.isPrimary && !b.isPrimary) return -1;
      if (!a.isPrimary && b.isPrimary) return 1;
      return a.title.localeCompare(b.title);
    });
  }

  const stats: LinkStats = {
    totalDocuments: documents.length,
    documentsWithLinks: Object.keys(documentToNodes).filter(
      id => documentToNodes[id].primary.length > 0 || documentToNodes[id].related.length > 0
    ).length,
    totalNodes: Object.keys(nodes).length,
    nodesWithDocuments: Object.keys(nodeToDocuments).length,
    averageNodesPerDocument: documents.length > 0
      ? Object.values(documentToNodes).reduce((sum, d) => sum + d.primary.length + d.related.length, 0) / documents.length
      : 0,
    averageDocumentsPerNode: Object.keys(nodeToDocuments).length > 0
      ? Object.values(nodeToDocuments).reduce((sum, docs) => sum + docs.length, 0) / Object.keys(nodeToDocuments).length
      : 0
  };

  return { documentToNodes, nodeToDocuments, stats };
}
