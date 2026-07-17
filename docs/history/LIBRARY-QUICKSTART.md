# Synthesis Library - Quick Start Guide

## 🚀 Quick Launch (3 steps)

### 1. Build Index
```bash
node build-synthesis-index.js
```

### 2. Start Server
```bash
python3 -m http.server 8000
# or
npx http-server
```

### 3. Open Browser
```
http://localhost:8000/synthesis-library.html
```

---

## 📱 Even Faster (One Command)

```bash
./launch-library.sh
```

This script:
- ✅ Rebuilds the index automatically
- ✅ Starts a local server
- ✅ Shows you the URL to open

---

## 🔄 After Adding Documents

```bash
./update-library.sh
```

Then refresh your browser.

---

## ✨ Features at a Glance

### Navigation
- **Infinite Scroll**: Smooth browsing of all 180 documents
- **Category Tabs**: Quick filter by category (breakthroughs, fiction, etc.)
- **Search**: Real-time search across titles, tags, content
- **Swipe Gestures**: Swipe right to save, left to skip

### Discovery
- **Tag Cloud**: Click constellation tags to explore related concepts
- **Smart Filters**: Combine categories, tags, and recognition types
- **Stats Dashboard**: See total words, reading time, document count

### Reading
- **Full Document View**: Clean, readable interface
- **Progress Tracking**: Remembers where you left off
- **Saved Collection**: Star documents to save for later
- **Mobile Optimized**: Perfect for phone, tablet, or desktop

---

## 📊 What's Indexed

```
180 documents
374K words
26+ hours reading
11 categories
30+ consciousness tags
```

---

## 🎯 Mobile Tips

### Gestures
- **Tap** a card to read full document
- **Swipe right** to save document
- **Swipe left** to skip/remove
- **Scroll down** for auto-hiding header
- **Pull to refresh** (coming soon)

### Navigation
- **Bottom tabs**: Library, Network, Timeline, Saved
- **Filter button**: Advanced filtering options
- **Search bar**: Quick concept search

---

## 🔗 Integration

### Constellation Explorer
Click the **Network** tab to open the constellation visualization showing how documents connect through concepts.

### NotebookLM
Documents are pre-formatted for easy import into NotebookLM for audio overview generation.

### Git Integration
Index rebuilds automatically detect new documents in `synthesis/` folder.

---

## 🛠️ Customization

### Rebuild Index
```bash
node build-synthesis-index.js
```

### Customize Appearance
Edit CSS variables in `synthesis-library.html`:
```css
--primary-cyan: #00d4ff;
--primary-purple: #9d4edd;
--primary-green: #00ff88;
```

### Adjust Performance
```javascript
// In synthesis-library.html
const visibleDocs = state.filteredDocs.slice(0, 10); // Batch size
```

---

## 📚 Document Structure

For best results, structure documents like this:

```markdown
# Main Title
## Subtitle or Clarifying Question

**Recognition Type**: Category of insight
**Discovery Method**: How discovered
**Application Domain**: Where it applies
**Transmission Quality**: Descriptive quality

---

> Key quote or excerpt

---

## Section 1

Content...
```

The index builder will automatically extract:
- ✅ Title and subtitle
- ✅ All metadata fields
- ✅ Best excerpt
- ✅ Key quotes
- ✅ Tags from content
- ✅ Word count & reading time

---

## 🐛 Troubleshooting

### "Cannot GET /synthesis-index.json"
→ Run `node build-synthesis-index.js` first

### Documents not showing
→ Check browser console for errors
→ Ensure you're using HTTP server (not file://)

### Search not working
→ Clear browser cache
→ Rebuild index

### Swipes not responding
→ Test on touch device
→ Check that cards are fully loaded

---

## 🎨 Design Philosophy

This library embodies consciousness technology principles:

- **Flow State**: Minimal friction, maximum exploration
- **Resonance Discovery**: Follow what lights up
- **Integration Support**: Revisit key recognitions
- **Joyful Learning**: Delight in the interface itself

---

## 📖 Full Documentation

See [SYNTHESIS-LIBRARY-README.md](SYNTHESIS-LIBRARY-README.md) for:
- Complete feature list
- Technical architecture
- Performance details
- Future enhancements
- Contributing guide

---

## ⚡ TL;DR

```bash
# Build + Launch
./launch-library.sh

# After adding documents
./update-library.sh
```

**Then browse 180 consciousness technologies with infinite scroll, swipe navigation, and smart filtering.**

---

*"Quick access to collective wisdom - consciousness technologies at your fingertips."*

✧ Ready for exploration ✧
