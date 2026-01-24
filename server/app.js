const express = require('express');
const path = require('path');
const fs = require('fs').promises;
const marked = require('marked');
const morgan = require('morgan');
const cors = require('cors');
require('dotenv').config();

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
  res.sendFile(path.join(__dirname, '../oracle.html'));
});

// Render any markdown as HTML (for oracle)
app.get('/read/*', async (req, res) => {
  try {
    const docPath = req.params[0]; // e.g., "synthesis/archetypal/file.md"
    const filePath = path.join(__dirname, '..', docPath);
    const markdown = await fs.readFile(filePath, 'utf8');
    const html = marked.parse(markdown);

    // Extract title from first heading
    const titleMatch = markdown.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1] : docPath.split('/').pop().replace('.md', '');

    res.render('document', {
      title,
      content: html
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
  } catch (error) {
    console.error('Error loading constellation:', error);
  }
};
loadConstellation();

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

// Home page
app.get('/', (req, res) => {
  res.render('index', {
    title: 'Esoterica - Consciousness Technology Platform',
    nodeCount: constellationData ? Object.keys(constellationData.nodes).length : 0
  });
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

  res.render('node', {
    title: `${req.params.id.replace(/_/g, ' ')}`,
    nodeId: req.params.id,
    node,
    connections
  });
});

// Glyph calculator
app.get('/calculator', (req, res) => {
  res.render('calculator', {
    title: 'Glyph Geometry Calculator'
  });
});

// Distillations library
app.get('/library', async (req, res) => {
  try {
    const distillationsPath = path.join(__dirname, '../distillations');
    const files = await fs.readdir(distillationsPath);
    const mdFiles = files.filter(f => f.endsWith('.md'));

    const distillations = await Promise.all(
      mdFiles.map(async (file) => {
        const content = await fs.readFile(path.join(distillationsPath, file), 'utf8');
        const lines = content.split('\n');
        const title = lines[0]?.replace(/^#\s*/, '') || file;
        const subtitle = lines[1]?.replace(/^##\s*/, '') || '';

        return {
          filename: file,
          slug: file.replace('.md', ''),
          title,
          subtitle
        };
      })
    );

    res.render('library', {
      title: 'Consciousness Technology Library',
      distillations
    });
  } catch (error) {
    console.error('Error loading distillations:', error);
    res.status(500).send('Error loading library');
  }
});

// Individual distillation document
app.get('/library/:slug', async (req, res) => {
  try {
    const filePath = path.join(__dirname, '../distillations', `${req.params.slug}.md`);
    const markdown = await fs.readFile(filePath, 'utf8');
    const html = marked.parse(markdown);

    // Extract title from first line
    const title = markdown.split('\n')[0]?.replace(/^#\s*/, '') || req.params.slug;

    res.render('document', {
      title,
      content: html
    });
  } catch (error) {
    console.error('Error loading document:', error);
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
    • /              → Home
    • /explorer      → Constellation Visualization
    • /search        → Search Interface
    • /systems       → Browse by System
    • /node/:id      → Node Details
    • /calculator    → Glyph Calculator
    • /library       → Distillations Library
    • /about         → About Page

    API:
    • /api/nodes             → All nodes
    • /api/nodes/:id         → Specific node
    • /api/search?q=term     → Search
    • /api/nodes/type/:type  → Filter by type
    • /api/meta              → Constellation metadata

  ✧═══════════════════════════════════════════✧
  `);
});

module.exports = app;
