/**
 * Constellation data loader and utilities.
 * Loads constellation.json and provides node lookups.
 */

import fs from 'node:fs';
import { repoPath } from './paths';

export interface ConstellationNode {
  type: string;
  essence: string;
  connections: string[];
}

export interface ConstellationData {
  nodes: Record<string, ConstellationNode>;
}

let _cached: ConstellationData | null = null;

export function loadConstellation(): ConstellationData {
  if (_cached) return _cached;

  const filePath = repoPath('constellation', 'constellation.json');
  const raw = fs.readFileSync(filePath, 'utf-8');

  try {
    _cached = JSON.parse(raw) as ConstellationData;
  } catch {
    // constellation.json may have a brace imbalance — extract just the nodes object
    const nodesStart = raw.indexOf('"nodes"');
    const braceStart = raw.indexOf('{', nodesStart + 7);

    let depth = 0;
    let nodesEnd = -1;
    for (let i = braceStart; i < raw.length; i++) {
      if (raw[i] === '{') depth++;
      if (raw[i] === '}') {
        depth--;
        if (depth === 0) { nodesEnd = i; break; }
      }
    }

    if (nodesEnd > 0) {
      const nodesJson = raw.substring(braceStart, nodesEnd + 1);
      _cached = { nodes: JSON.parse(nodesJson) };
    } else {
      throw new Error('Could not parse constellation.json');
    }
  }

  return _cached;
}

export function getNode(id: string): ConstellationNode | undefined {
  return loadConstellation().nodes[id];
}

export function getAllNodes(): Record<string, ConstellationNode> {
  return loadConstellation().nodes;
}

export function getNodeIds(): string[] {
  return Object.keys(loadConstellation().nodes);
}

/** Format a node ID for display: "mercury_hermes_thoth" → "Mercury Hermes Thoth" */
export function formatNodeName(nodeId: string): string {
  return nodeId
    .split('_')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}
