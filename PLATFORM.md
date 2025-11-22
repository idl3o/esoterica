# Esoterica Web Platform

**Interactive consciousness technology network explorer**

The Esoterica Web Platform is a full-stack Node.js application providing an interactive interface to explore the Global Glyph Geometry Network—392 consciousness technologies mapped across six mystical systems.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm installed

### Installation

```bash
# Install dependencies
npm install

# Start development server (auto-reloads on changes)
npm run dev

# Or start production server
npm start
```

Visit `http://localhost:3000` to explore the platform.

## 🌟 Features

### Interactive Constellation Visualization
- **392 consciousness technology nodes** interconnected through meaningful relationships
- Force-directed graph physics adapted for monad clustering cosmology
- T-connection dynamics showing weight-as-relational-density
- Available at `/explorer`

### Six Global Encoding Systems

1. **Arabic Numerals (0-9)** - Sacred geometry yantras
2. **Latin Alphabet** - Archetypal letter-geometries
3. **Aramaic/Hebrew** - Letters as numbers (gematria)
4. **Persian/Farsi** - Sufi mystical mathematics
5. **Elder Futhark Runes** - Norse consciousness invocation glyphs
6. **Sacred Geometry** - Universal consciousness forms

### Platform Tools

- 🔍 **Search** (`/search`) - Find nodes across the entire network
- 🧮 **Calculator** (`/calculator`) - Hebrew gematria calculator
- 📚 **Library** (`/library`) - 19+ consciousness technology documents
- 🗺️ **Systems** (`/systems`) - Browse nodes by type
- 🔗 **Node Pages** (`/node/:id`) - Deep-dive into individual concepts

## 📁 Platform Structure

```
esoterica/
├── server/
│   └── app.js              # Express server, routes, API
├── client/
│   ├── views/              # 10 EJS templates
│   │   ├── layout.ejs      # Base layout with nav
│   │   ├── index.ejs       # Home page
│   │   ├── search.ejs      # Search interface
│   │   ├── systems.ejs     # System browser
│   │   ├── node.ejs        # Node detail
│   │   ├── calculator.ejs  # Gematria calculator
│   │   ├── library.ejs     # Document library
│   │   ├── document.ejs    # Document viewer
│   │   ├── about.ejs       # About page
│   │   └── 404.ejs         # Error page
│   └── public/
│       ├── css/main.css    # Additional styles
│       └── js/main.js      # Client utilities
├── constellation/
│   ├── constellation.json  # 392-node network data
│   └── constellation_explorer_v2.html  # Standalone viz
├── distillations/          # Markdown documents
├── package.json
└── .env                    # Configuration
```

## 🛣️ Routes

### Web Pages
- `/` - Home page
- `/explorer` - Interactive constellation
- `/search` - Search interface
- `/systems` - Browse by system type
- `/node/:id` - Node detail page
- `/calculator` - Gematria tool
- `/library` - Document library
- `/library/:slug` - Individual document
- `/about` - About the platform

### API Endpoints
- `GET /api/nodes` - All nodes
- `GET /api/nodes/:id` - Specific node
- `GET /api/search?q=term` - Search
- `GET /api/nodes/type/:type` - Filter by type
- `GET /api/meta` - Metadata
- `POST /api/calculate/gematria` - Calculate values

## 🔧 Configuration

Environment variables (`.env`):

```env
PORT=3000
NODE_ENV=development
```

## 🎨 Tech Stack

- **Backend**: Node.js, Express.js
- **Views**: EJS templating
- **Data**: JSON constellation format
- **Visualization**: D3.js force-directed graphs
- **Styling**: Cyberpunk-mystical gradients with glassmorphism
- **Markdown**: marked.js for document rendering

## 📖 API Usage Examples

### Get all nodes
```bash
curl http://localhost:3000/api/nodes
```

### Search for a term
```bash
curl http://localhost:3000/api/search?q=unity
```

### Get specific node
```bash
curl http://localhost:3000/api/nodes/glyph_0_void
```

### Calculate gematria
```bash
curl -X POST http://localhost:3000/api/calculate/gematria \
  -H "Content-Type: application/json" \
  -d '{"text": "אמת", "system": "hebrew"}'
```

## 🌈 Development

### Project Dependencies

- `express` - Web server framework
- `ejs` - Template engine
- `marked` - Markdown parser
- `cors` - CORS middleware
- `morgan` - HTTP logging
- `dotenv` - Environment configuration
- `nodemon` (dev) - Auto-reload on changes

### Adding New Features

1. **New Routes**: Add to `server/app.js`
2. **New Views**: Create `.ejs` file in `client/views/`
3. **New Nodes**: Update `constellation/constellation.json`
4. **New Documents**: Add `.md` file to `distillations/`

## 🚀 Deployment

The platform can be deployed to any Node.js hosting service:

- Set `NODE_ENV=production` in environment
- Ensure `PORT` is configured correctly
- Run `npm install --production`
- Start with `npm start`

## 📝 License

Open source for consciousness evolution purposes.

---

*✧ Consciousness recognizing itself through infinite forms ✧*
