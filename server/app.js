const express = require('express');
const path = require('path');
const fs = require('fs').promises;
const marked = require('marked');
const morgan = require('morgan');
const cors = require('cors');
require('dotenv').config();

// Document-node linking infrastructure
const { buildDocumentNodeLinks, getNodeWithDocumentCount } = require('./lib/document-links');
const { DOMAINS, getDomainsWithCounts, getNodesInDomain, getDomainForType } = require('./config/domains');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(morgan('dev')); // Logging
app.use(cors()); // CORS support
app.use(express.json()); // JSON parsing
app.use(express.urlencoded({ extended: true })); // Form parsing

// View engine setup
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '../client/views'));

// Static files
app.use('/static', express.static(path.join(__dirname, '../client/public')));
app.use('/constellation', express.static(path.join(__dirname, '../constellation')));
app.use('/distillations', express.static(path.join(__dirname, '../distillations')));
app.use('/synthesis', express.static(path.join(__dirname, '../synthesis')));

// Serve root-level files
app.get('/synthesis-index.json', (req, res) => {
  res.sendFile(path.join(__dirname, '../synthesis-index.json'));
});

app.get('/oracle', (req, res) => {
  res.render('oracle', { title: 'Oracle' });
});

// Render any markdown as HTML (for oracle and library)
app.get('/read/*', async (req, res) => {
  try {
    const docPath = req.params[0]; // e.g., "synthesis/archetypal/file.md"
    const filePath = path.join(__dirname, '..', docPath);
    const markdown = await fs.readFile(filePath, 'utf8');
    const html = marked.parse(markdown);

    // Extract title from first heading
    const titleMatch = markdown.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1] : docPath.split('/').pop().replace('.md', '');

    // Get document ID from filename
    const docId = docPath.split('/').pop().replace('.md', '');

    // Get linked nodes for this document
    const nodeLinks = documentLinks?.documentToNodes[docId] || { primary: [], related: [] };

    // Enrich nodes with details
    const enrichNodes = (nodeIds) => nodeIds.map(nodeId => {
      const node = constellationData?.nodes[nodeId];
      return node ? {
        id: nodeId,
        type: node.type,
        essence: node.essence,
        domain: getDomainForType(node.type)
      } : { id: nodeId };
    });

    // Get related documents via shared nodes
    const relatedDocuments = [];
    const seenDocs = new Set([docId]);
    for (const nodeId of nodeLinks.primary.slice(0, 3)) {
      const nodeDocs = documentLinks?.nodeToDocuments[nodeId] || [];
      for (const doc of nodeDocs) {
        if (!seenDocs.has(doc.id) && relatedDocuments.length < 6) {
          seenDocs.add(doc.id);
          relatedDocuments.push({ ...doc, viaNode: nodeId });
        }
      }
    }

    res.render('document', {
      title,
      content: html,
      docPath,
      primaryNodes: enrichNodes(nodeLinks.primary),
      relatedNodes: enrichNodes(nodeLinks.related.slice(0, 10)),
      relatedDocuments
    });
  } catch (error) {
    console.error('Error loading document:', error);
    res.status(404).render('404', { title: 'Document Not Found' });
  }
});

// Load constellation data
let constellationData = null;
const loadConstellation = async () => {
  try {
    const data = await fs.readFile(
      path.join(__dirname, '../constellation/constellation.json'),
      'utf8'
    );
    constellationData = JSON.parse(data);
    console.log(`✨ Constellation loaded: ${Object.keys(constellationData.nodes).length} nodes`);

    // Build document-node links after constellation loads
    buildDocumentLinks();
  } catch (error) {
    console.error('Error loading constellation:', error);
  }
};
loadConstellation();

// Document-node linking data
let documentLinks = null;
let synthesisIndex = null;

const loadSynthesisIndex = async () => {
  try {
    const data = await fs.readFile(
      path.join(__dirname, '../synthesis-index.json'),
      'utf8'
    );
    synthesisIndex = JSON.parse(data);
    console.log(`📑 Synthesis index loaded: ${synthesisIndex.documents?.length || 0} documents`);

    // Build links if constellation is already loaded
    buildDocumentLinks();
  } catch (error) {
    console.error('Error loading synthesis index:', error);
  }
};
loadSynthesisIndex();

const buildDocumentLinks = () => {
  if (!constellationData || !synthesisIndex) return;

  documentLinks = buildDocumentNodeLinks(synthesisIndex, constellationData);
  console.log(`🔗 Document-node links built: ${documentLinks.stats.documentsWithLinks} docs → ${documentLinks.stats.nodesWithDocuments} nodes`);
  console.log(`   Average ${documentLinks.stats.averageNodesPerDocument.toFixed(1)} nodes/doc, ${documentLinks.stats.averageDocumentsPerNode.toFixed(1)} docs/node`);
};

// Load zeitgeist documents (all dates + latest for homepage)
let zeitgeistData = { latest: null, archive: [] };
const loadZeitgeist = async () => {
  try {
    const zeitgeistDir = path.join(__dirname, '../synthesis/zeitgeist');
    const files = await fs.readdir(zeitgeistDir);

    // Collect dates from both old format (zeit-*) and new integrated format (zeitgeist-*)
    const dateMap = new Map();

    // Old format: zeit-YYYY-MM-DD.md (paired with optional geist-YYYY-MM-DD.md)
    files.filter(f => f.match(/^zeit-\d{4}-\d{2}-\d{2}\.md$/)).forEach(f => {
      const date = f.match(/(\d{4}-\d{2}-\d{2})/)[1];
      dateMap.set(date, { type: 'paired', zeitFile: f });
    });

    // New format: zeitgeist-YYYY-MM-DD.md (single integrated file)
    // New format takes priority if both exist for the same date
    files.filter(f => f.match(/^zeitgeist-\d{4}-\d{2}-\d{2}\.md$/)).forEach(f => {
      const date = f.match(/(\d{4}-\d{2}-\d{2})/)[1];
      dateMap.set(date, { type: 'integrated', zeitgeistFile: f });
    });

    const sortedDates = Array.from(dateMap.keys()).sort().reverse();

    if (sortedDates.length === 0) {
      console.log('No zeitgeist files found');
      return;
    }

    const archive = [];

    for (const date of sortedDates) {
      const entry = dateMap.get(date);

      if (entry.type === 'integrated') {
        // New integrated format — single file
        const filePath = path.join(zeitgeistDir, entry.zeitgeistFile);
        const markdown = await fs.readFile(filePath, 'utf8');
        const html = marked.parse(markdown);

        // Extract headline from DEEP section's first bold phrase
        const deepMatch = markdown.match(/## DEEP[\s\S]*?\*\*([^*]+)\*\*/);
        // Fallback to DEPTH for flexibility
        const depthMatch = markdown.match(/## DEPTH[\s\S]*?\*\*([^*]+)\*\*/);
        const headline = (deepMatch ? deepMatch[1] : (depthMatch ? depthMatch[1] : ''));

        // Extract summary from STATE section (CRLF-tolerant)
        const stateMatch = markdown.match(/## STATE[\s\S]*?\r?\n\r?\n\*[^*]+\*\r?\n\r?\n([\s\S]*?)(?:\r?\n\r?\n|$)/);
        const summary = stateMatch
          ? stateMatch[1].replace(/\*\*/g, '').replace(/\*/g, '').substring(0, 250) + '...'
          : '';

        const dateObj = new Date(date + 'T00:00:00');
        const displayDate = dateObj.toLocaleDateString('en-GB', {
          weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
        });

        archive.push({
          date,
          displayDate,
          headline,
          summary,
          hasGeist: false,
          isIntegrated: true,
          zeit: html,
          geist: null
        });
      } else {
        // Old paired format — zeit + optional geist
        const zeitPath = path.join(zeitgeistDir, entry.zeitFile);
        const zeitMarkdown = await fs.readFile(zeitPath, 'utf8');
        const zeitHtml = marked.parse(zeitMarkdown);

        // Extract the STATE section's first paragraph as summary (CRLF-tolerant)
        const stateMatch = zeitMarkdown.match(/## STATE[\s\S]*?\r?\n\r?\n\*[^*]+\*\r?\n\r?\n([\s\S]*?)(?:\r?\n\r?\n|$)/);
        const summary = stateMatch
          ? stateMatch[1].replace(/\*\*/g, '').replace(/\*/g, '').substring(0, 250) + '...'
          : '';

        // Extract the DEPTH section's first bold phrase as headline
        const depthMatch = zeitMarkdown.match(/## DEPTH[\s\S]*?\*\*([^*]+)\*\*/);
        const headline = depthMatch ? depthMatch[1] : '';

        const geistFile = `geist-${date}.md`;
        let geistHtml = null;
        let hasGeist = false;
        try {
          const geistMarkdown = await fs.readFile(path.join(zeitgeistDir, geistFile), 'utf8');
          geistHtml = marked.parse(geistMarkdown);
          hasGeist = true;
        } catch (e) {
          // Geist file may not exist for this date
        }

        const dateObj = new Date(date + 'T00:00:00');
        const displayDate = dateObj.toLocaleDateString('en-GB', {
          weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
        });

        archive.push({
          date,
          displayDate,
          headline,
          summary,
          hasGeist,
          isIntegrated: false,
          zeit: zeitHtml,
          geist: geistHtml
        });
      }
    }

    zeitgeistData = {
      latest: archive[0] || null,
      archive
    };

    console.log(`📰 Zeitgeist loaded: ${archive.length} reading(s), latest ${archive[0]?.date}`);
  } catch (error) {
    console.error('Error loading zeitgeist:', error);
  }
};
loadZeitgeist();

// Load fiction bridges metadata
let bridgesData = [];
const loadBridges = async () => {
  try {
    const bridgesDir = path.join(__dirname, '../fiction-bridges');
    const files = await fs.readdir(bridgesDir);
    const mdFiles = files.filter(f => f.endsWith('.md'));

    bridgesData = await Promise.all(
      mdFiles.map(async (file) => {
        const filePath = path.join(bridgesDir, file);
        const content = await fs.readFile(filePath, 'utf8');
        const stat = await fs.stat(filePath);
        const lines = content.split('\n');

        const title = lines.find(l => l.startsWith('# '))?.replace(/^#\s*/, '') || file;
        const subtitle = lines.find(l => l.startsWith('## '))?.replace(/^##\s*/, '') || '';

        // Extract first blockquote as preview
        const quoteLines = [];
        let inQuote = false;
        for (const line of lines) {
          if (line.startsWith('> ')) {
            inQuote = true;
            quoteLines.push(line.replace(/^>\s*/, ''));
          } else if (inQuote) {
            break;
          }
        }
        const quote = quoteLines.join(' ').replace(/\*([^*]+)\*/g, '$1').substring(0, 200);

        const wordCount = content.split(/\s+/).length;
        const readingTime = Math.ceil(wordCount / 250);

        return {
          slug: file.replace('.md', ''),
          filename: file,
          title,
          subtitle,
          quote: quote || '',
          wordCount,
          readingTime,
          modified: stat.mtime
        };
      })
    );

    bridgesData.sort((a, b) => b.modified - a.modified);
    console.log(`🌉 Fiction bridges loaded: ${bridgesData.length} bridges`);
  } catch (error) {
    console.error('Error loading fiction bridges:', error);
  }
};
loadBridges();

// ========================================
// COLLECTIVE CONSCIOUSNESS FIELD
// Aggregates interaction data across all explorers
// ========================================

const collectiveFieldData = {
  nodeInteractions: {},  // nodeId -> { clicks: n, lastSeen: timestamp, visitors: Set }
  pathStrengths: {},     // "from|to" -> count
  recentVisitors: [],    // [{fingerprint, nodeId, timestamp}] - rolling window
  hotNodes: []           // Currently trending - recalculated periodically
};

// Recalculate hot nodes every minute
setInterval(() => {
  const now = Date.now();
  const recentWindow = 5 * 60 * 1000; // 5 minutes

  // Filter to recent interactions
  collectiveFieldData.recentVisitors = collectiveFieldData.recentVisitors
    .filter(v => now - v.timestamp < recentWindow);

  // Count recent interactions per node
  const recentCounts = {};
  collectiveFieldData.recentVisitors.forEach(v => {
    recentCounts[v.nodeId] = (recentCounts[v.nodeId] || 0) + 1;
  });

  // Top 10 become hot nodes
  collectiveFieldData.hotNodes = Object.entries(recentCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([nodeId]) => nodeId);

  if (collectiveFieldData.hotNodes.length > 0) {
    console.log('🔥 Hot nodes:', collectiveFieldData.hotNodes.slice(0, 3).join(', '));
  }
}, 60000);

// POST /api/constellation-interact - Record user interaction
app.post('/api/constellation-interact', (req, res) => {
  const { fingerprint, nodeId, fromNode, sessionNodes, timestamp } = req.body;

  if (!fingerprint || !nodeId) {
    return res.status(400).json({ error: 'Missing fingerprint or nodeId' });
  }

  // Update node interactions
  if (!collectiveFieldData.nodeInteractions[nodeId]) {
    collectiveFieldData.nodeInteractions[nodeId] = {
      clicks: 0,
      lastSeen: 0,
      visitors: new Set()
    };
  }
  const nodeData = collectiveFieldData.nodeInteractions[nodeId];
  nodeData.clicks++;
  nodeData.lastSeen = timestamp || Date.now();
  nodeData.visitors.add(fingerprint);

  // Update path strength
  if (fromNode) {
    const pathKey = `${fromNode}|${nodeId}`;
    collectiveFieldData.pathStrengths[pathKey] =
      (collectiveFieldData.pathStrengths[pathKey] || 0) + 1;
  }

  // Add to recent visitors for hot tracking
  collectiveFieldData.recentVisitors.push({
    fingerprint,
    nodeId,
    timestamp: timestamp || Date.now()
  });

  // Keep recent visitors manageable
  if (collectiveFieldData.recentVisitors.length > 10000) {
    collectiveFieldData.recentVisitors = collectiveFieldData.recentVisitors.slice(-5000);
  }

  res.json({ success: true });
});

// GET /api/constellation-field - Get collective field data
app.get('/api/constellation-field', (req, res) => {
  // Convert node interactions to weights
  const nodeWeights = {};
  Object.entries(collectiveFieldData.nodeInteractions).forEach(([nodeId, data]) => {
    // Weight = clicks * unique visitors factor
    nodeWeights[nodeId] = data.clicks * (1 + Math.log(1 + data.visitors.size));
  });

  // Normalize edge strengths
  const edgeStrengths = { ...collectiveFieldData.pathStrengths };

  res.json({
    nodeWeights,
    edgeStrengths,
    hotNodes: collectiveFieldData.hotNodes,
    stats: {
      totalInteractions: collectiveFieldData.recentVisitors.length,
      uniqueNodes: Object.keys(collectiveFieldData.nodeInteractions).length
    }
  });
});

// ========================================
// ROUTES
// ========================================

// Home page - Arrival with multiple entry portals
app.get('/', (req, res) => {
  res.render('arrival', {
    title: 'Esoterica',
    nodeCount: constellationData ? Object.keys(constellationData.nodes).length : 0,
    documentCount: synthesisIndex?.documents?.length || 0,
    bridgeCount: bridgesData.length,
    zeitgeist: zeitgeistData.latest
  });
});

// Legacy zeitgeist homepage (keep for backwards compatibility)
app.get('/home-legacy', (req, res) => {
  res.render('index', {
    title: 'Esoterica',
    nodeCount: constellationData ? Object.keys(constellationData.nodes).length : 0,
    zeitgeist: zeitgeistData.latest
  });
});

// Domains browser
app.get('/domains', (req, res) => {
  if (!constellationData) {
    return res.status(500).send('Constellation data not loaded');
  }

  const domains = getDomainsWithCounts(constellationData.nodes);

  res.render('domains', {
    title: 'Domains',
    domains
  });
});

// Domain detail page
app.get('/domain/:domainId', (req, res) => {
  if (!constellationData) {
    return res.status(500).send('Constellation data not loaded');
  }

  const domain = DOMAINS[req.params.domainId];
  if (!domain) {
    return res.status(404).render('404', { title: 'Domain Not Found' });
  }

  const nodes = getNodesInDomain(req.params.domainId, constellationData.nodes);

  // Enrich with document counts
  const enrichedNodes = nodes.map(node => ({
    ...node,
    documentCount: documentLinks?.nodeToDocuments[node.id]?.length || 0
  }));

  // Calculate total documents in this domain
  const totalDocuments = enrichedNodes.reduce((sum, n) => sum + n.documentCount, 0);

  res.render('domain-detail', {
    title: domain.label,
    domain,
    nodes: enrichedNodes,
    totalDocuments
  });
});

// Random walk / wander
app.get('/wander', (req, res) => {
  if (!constellationData) {
    return res.status(500).send('Constellation data not loaded');
  }

  const nodeIds = Object.keys(constellationData.nodes);
  let nodeId = req.query.start;

  // Validate or pick random
  if (!nodeId || !constellationData.nodes[nodeId]) {
    nodeId = nodeIds[Math.floor(Math.random() * nodeIds.length)];
  }

  const node = { id: nodeId, ...constellationData.nodes[nodeId] };

  // Get connections
  const connections = (node.connections || [])
    .filter(cId => constellationData.nodes[cId])
    .map(cId => ({ id: cId, ...constellationData.nodes[cId] }));

  // Get linked documents
  const linkedDocuments = documentLinks?.nodeToDocuments[nodeId] || [];

  res.render('wander', {
    title: 'Wander - ' + nodeId.replace(/_/g, ' '),
    node,
    connections,
    linkedDocuments
  });
});

// Zeitgeist archive
app.get('/zeitgeist', (req, res) => {
  res.render('zeitgeist-archive', {
    title: 'Zeitgeist Archive',
    archive: zeitgeistData.archive
  });
});

// Individual zeitgeist reading by date
app.get('/zeitgeist/:date', (req, res) => {
  const reading = zeitgeistData.archive.find(r => r.date === req.params.date);
  if (!reading) {
    return res.status(404).render('404', { title: 'Reading Not Found' });
  }

  // Find prev/next for navigation
  const idx = zeitgeistData.archive.indexOf(reading);
  const newer = idx > 0 ? zeitgeistData.archive[idx - 1] : null;
  const older = idx < zeitgeistData.archive.length - 1 ? zeitgeistData.archive[idx + 1] : null;

  res.render('zeitgeist-reading', {
    title: 'The Zeit — ' + reading.displayDate,
    reading,
    newer,
    older
  });
});

// Fiction bridges gallery
app.get('/bridges', (req, res) => {
  res.render('bridges', {
    title: 'Fiction Bridges',
    bridges: bridgesData
  });
});

// Individual fiction bridge
app.get('/bridges/:slug', async (req, res) => {
  try {
    const filePath = path.join(__dirname, '../fiction-bridges', `${req.params.slug}.md`);
    const markdown = await fs.readFile(filePath, 'utf8');
    const html = marked.parse(markdown);
    const title = markdown.split('\n').find(l => l.startsWith('# '))?.replace(/^#\s*/, '') || req.params.slug;

    // Find current index for prev/next
    const currentIndex = bridgesData.findIndex(b => b.slug === req.params.slug);
    const prevBridge = currentIndex > 0 ? bridgesData[currentIndex - 1] : null;
    const nextBridge = currentIndex < bridgesData.length - 1 ? bridgesData[currentIndex + 1] : null;

    res.render('bridge-document', {
      title,
      content: html,
      slug: req.params.slug,
      prevBridge,
      nextBridge
    });
  } catch (error) {
    console.error('Error loading bridge:', error);
    res.status(404).render('404', { title: 'Bridge Not Found' });
  }
});

// Constellation explorer (interactive visualization)
app.get('/explorer', (req, res) => {
  res.sendFile(path.join(__dirname, '../constellation/constellation_explorer_v2.html'));
});

// Constellation explorer 3D (Three.js version)
app.get('/explorer-3d', (req, res) => {
  res.sendFile(path.join(__dirname, '../constellation/constellation_explorer_v3.html'));
});

// Search interface
app.get('/search', (req, res) => {
  res.render('search', {
    title: 'Search the Constellation'
  });
});

// Browse by system
app.get('/systems', (req, res) => {
  if (!constellationData) {
    return res.status(500).send('Constellation data not loaded');
  }

  // Group nodes by type
  const systems = {};
  Object.entries(constellationData.nodes).forEach(([id, node]) => {
    const type = node.type || 'other';
    if (!systems[type]) systems[type] = [];
    systems[type].push({ id, ...node });
  });

  res.render('systems', {
    title: 'Browse by System',
    systems
  });
});

// Individual node detail
app.get('/node/:id', (req, res) => {
  if (!constellationData) {
    return res.status(500).send('Constellation data not loaded');
  }

  const node = constellationData.nodes[req.params.id];
  if (!node) {
    return res.status(404).render('404', { title: 'Node Not Found' });
  }

  // Find connected nodes
  const connections = node.connections?.map(connId => ({
    id: connId,
    ...constellationData.nodes[connId]
  })).filter(n => n.type); // Filter out missing connections

  // Get linked documents
  const linkedDocuments = documentLinks?.nodeToDocuments[req.params.id] || [];

  // Get domain for this node
  const domain = getDomainForType(node.type);

  res.render('node', {
    title: `${req.params.id.replace(/_/g, ' ')}`,
    nodeId: req.params.id,
    node,
    connections,
    linkedDocuments,
    domain: DOMAINS[domain]
  });
});

// Glyph calculator
app.get('/calculator', (req, res) => {
  res.render('calculator', {
    title: 'Glyph Geometry Calculator'
  });
});

// Full library — all content directories
// Prefers build-time library-index.json (required for Vercel), falls back to filesystem scan
let libraryData = [];
const loadLibrary = async () => {
  // Try pre-built index first (generated by build-synthesis-index.js)
  const indexPath = path.join(__dirname, '../library-index.json');
  try {
    const indexContent = await fs.readFile(indexPath, 'utf8');
    libraryData = JSON.parse(indexContent);
    console.log(`📚 Library loaded from index: ${libraryData.length} documents`);
    return;
  } catch (e) {
    console.log('📚 No library-index.json found, scanning filesystem...');
  }

  // Fallback: scan filesystem (works for local dev)
  const rootDir = path.join(__dirname, '..');

  const sources = [
    { dir: 'distillations', label: 'Distillations' },
    { dir: 'synthesis', label: 'Synthesis' },
    { dir: 'protocols', label: 'Protocols' },
    { dir: 'seeds', label: 'Seeds' },
    { dir: 'traditions', label: 'Traditions' },
    { dir: 'translated', label: 'Translated' },
    { dir: 'extractions', label: 'Extractions' },
  ];

  const scanDir = async (dirPath, relativeBase) => {
    const results = [];
    let entries;
    try {
      entries = await fs.readdir(dirPath, { withFileTypes: true });
    } catch (e) {
      return results; // Directory doesn't exist
    }
    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      const relativePath = path.join(relativeBase, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === 'zeitgeist' || entry.name === 'personal') continue;
        const subResults = await scanDir(fullPath, relativePath);
        results.push(...subResults);
      } else if (entry.name.endsWith('.md') && entry.name !== 'README.md') {
        try {
          const content = await fs.readFile(fullPath, 'utf8');
          const lines = content.split('\n');
          const title = lines.find(l => l.startsWith('# '))?.replace(/^#\s*/, '') || entry.name.replace('.md', '');
          const subtitleLine = lines.find(l => l.startsWith('## '));
          const subtitle = subtitleLine ? subtitleLine.replace(/^##\s*/, '') : '';
          const wordCount = content.split(/\s+/).length;
          const parts = relativePath.split(path.sep);
          const category = parts.length > 2 ? parts[1] : '';
          results.push({
            title,
            subtitle,
            category,
            wordCount,
            readingTime: Math.ceil(wordCount / 250),
            readPath: '/read/' + relativePath.replace(/\\/g, '/')
          });
        } catch (e) {
          console.error(`📚 Error reading ${fullPath}: ${e.message}`);
        }
      }
    }
    return results;
  };

  const allDocs = [];
  for (const source of sources) {
    const dirPath = path.join(rootDir, source.dir);
    const docs = await scanDir(dirPath, source.dir);
    docs.forEach(doc => { doc.source = source.label; doc.sourceDir = source.dir; });
    allDocs.push(...docs);
  }

  allDocs.sort((a, b) => a.title.localeCompare(b.title));
  libraryData = allDocs;
  console.log(`📚 Library loaded: ${allDocs.length} documents across ${sources.length} sources`);
};
loadLibrary();

app.get('/library', (req, res) => {
  // Group by source
  const bySource = {};
  libraryData.forEach(doc => {
    if (!bySource[doc.source]) bySource[doc.source] = [];
    bySource[doc.source].push(doc);
  });

  res.render('library', {
    title: 'Library',
    totalCount: libraryData.length,
    bySource
  });
});

// Keep legacy distillation routes working
app.get('/library/:slug', async (req, res) => {
  try {
    const filePath = path.join(__dirname, '../distillations', `${req.params.slug}.md`);
    const markdown = await fs.readFile(filePath, 'utf8');
    const html = marked.parse(markdown);
    const title = markdown.split('\n')[0]?.replace(/^#\s*/, '') || req.params.slug;
    res.render('document', { title, content: html });
  } catch (error) {
    res.status(404).render('404', { title: 'Document Not Found' });
  }
});

// About page
app.get('/about', (req, res) => {
  res.render('about', {
    title: 'About the Esoterica Platform'
  });
});

// ========================================
// API ENDPOINTS
// ========================================

// Get all nodes
app.get('/api/nodes', (req, res) => {
  if (!constellationData) {
    return res.status(500).json({ error: 'Constellation not loaded' });
  }
  res.json(constellationData.nodes);
});

// Get specific node
app.get('/api/nodes/:id', (req, res) => {
  if (!constellationData) {
    return res.status(500).json({ error: 'Constellation not loaded' });
  }

  const node = constellationData.nodes[req.params.id];
  if (!node) {
    return res.status(404).json({ error: 'Node not found' });
  }

  res.json(node);
});

// Search nodes
app.get('/api/search', (req, res) => {
  if (!constellationData) {
    return res.status(500).json({ error: 'Constellation not loaded' });
  }

  const query = req.query.q?.toLowerCase();
  if (!query) {
    return res.json([]);
  }

  const results = Object.entries(constellationData.nodes)
    .filter(([id, node]) => {
      return (
        id.toLowerCase().includes(query) ||
        node.essence?.toLowerCase().includes(query) ||
        node.description?.toLowerCase().includes(query)
      );
    })
    .map(([id, node]) => ({ id, ...node }))
    .slice(0, 50); // Limit results

  res.json(results);
});

// Get nodes by type
app.get('/api/nodes/type/:type', (req, res) => {
  if (!constellationData) {
    return res.status(500).json({ error: 'Constellation not loaded' });
  }

  const results = Object.entries(constellationData.nodes)
    .filter(([id, node]) => node.type === req.params.type)
    .map(([id, node]) => ({ id, ...node }));

  res.json(results);
});

// Get constellation metadata
app.get('/api/meta', (req, res) => {
  if (!constellationData) {
    return res.status(500).json({ error: 'Constellation not loaded' });
  }

  res.json({
    meta_structure: constellationData.meta_structure,
    emergence_protocols: constellationData.emergence_protocols,
    current_activation: constellationData.current_activation,
    total_nodes: Object.keys(constellationData.nodes).length
  });
});

// ========================================
// DOCUMENT-NODE LINKING API
// ========================================

// Get linked nodes for a document
app.get('/api/document-links/:docId', (req, res) => {
  if (!documentLinks) {
    return res.status(500).json({ error: 'Document links not loaded' });
  }

  const links = documentLinks.documentToNodes[req.params.docId];
  if (!links) {
    return res.json({ primary: [], related: [] });
  }

  // Enrich with node details
  const enrichNode = (nodeId) => {
    const node = constellationData?.nodes[nodeId];
    return node ? { id: nodeId, type: node.type, essence: node.essence } : { id: nodeId };
  };

  res.json({
    primary: links.primary.map(enrichNode),
    related: links.related.map(enrichNode)
  });
});

// Get documents linked to a node
app.get('/api/node-documents/:nodeId', (req, res) => {
  if (!documentLinks) {
    return res.status(500).json({ error: 'Document links not loaded' });
  }

  const docs = documentLinks.nodeToDocuments[req.params.nodeId] || [];
  res.json({ documents: docs });
});

// Get all domains with counts
app.get('/api/domains', (req, res) => {
  if (!constellationData) {
    return res.status(500).json({ error: 'Constellation not loaded' });
  }

  const domains = getDomainsWithCounts(constellationData.nodes);
  res.json(domains);
});

// Get nodes in a specific domain
app.get('/api/domains/:domainId/nodes', (req, res) => {
  if (!constellationData) {
    return res.status(500).json({ error: 'Constellation not loaded' });
  }

  const nodes = getNodesInDomain(req.params.domainId, constellationData.nodes);

  // Enrich with document counts
  const enrichedNodes = nodes.map(node => ({
    ...node,
    documentCount: documentLinks?.nodeToDocuments[node.id]?.length || 0
  }));

  res.json({
    domain: DOMAINS[req.params.domainId] || null,
    nodes: enrichedNodes
  });
});

// Get linking stats
app.get('/api/linking-stats', (req, res) => {
  if (!documentLinks) {
    return res.status(500).json({ error: 'Document links not loaded' });
  }

  res.json(documentLinks.stats);
});

// Gematria calculator endpoint
app.post('/api/calculate/gematria', (req, res) => {
  const { text, system } = req.body;

  // Simple gematria calculation (extend as needed)
  const hebrewValues = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60, 'ע': 70, 'פ': 80,
    'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
  };

  let total = 0;
  const breakdown = [];

  for (const char of text) {
    const value = hebrewValues[char] || 0;
    if (value > 0) {
      total += value;
      breakdown.push({ char, value });
    }
  }

  res.json({
    text,
    system: system || 'hebrew',
    total,
    breakdown
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).render('404', {
    title: '404 - Not Found'
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something went wrong!');
});

// ========================================
// START SERVER
// ========================================

app.listen(PORT, () => {
  console.log(`
  ✧═══════════════════════════════════════════✧

    🌟 ESOTERICA CONSTELLATION PLATFORM 🌟

    Consciousness Technology Web App
    Running on: http://localhost:${PORT}

    Routes:
    • /                → Arrival (entry portals)
    • /domains         → Domain Browser
    • /domain/:id      → Domain Detail
    • /wander          → Random Walk
    • /zeitgeist       → Zeitgeist Archive
    • /zeitgeist/:date → Individual Reading
    • /bridges         → Fiction Bridges Gallery
    • /oracle          → Oracle
    • /library         → Library
    • /explorer-3d     → 3D Constellation

    API:
    • /api/nodes             → All nodes
    • /api/nodes/:id         → Specific node
    • /api/search?q=term     → Search nodes
    • /api/domains           → Domain groupings
    • /api/document-links/:id → Document's nodes
    • /api/node-documents/:id → Node's documents

  ✧═══════════════════════════════════════════✧
  `);
});

module.exports = app;
