#!/bin/bash

# SYNTHESIS LIBRARY LAUNCHER
# Quick script to rebuild index and open library

echo "✧ SYNTHESIS LIBRARY LAUNCHER ✧"
echo ""

# Check if we're in the right directory
if [ ! -d "synthesis" ]; then
    echo "❌ Error: synthesis/ directory not found"
    echo "Please run this script from the esoterica root directory"
    exit 1
fi

# Rebuild index
echo "🔄 Rebuilding document index..."
node build-synthesis-index.js

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to build index"
    exit 1
fi

echo ""
echo "✨ Index built successfully!"
echo ""

# Check if synthesis-index.json was created
if [ ! -f "synthesis-index.json" ]; then
    echo "❌ Error: synthesis-index.json not found"
    exit 1
fi

# Start a simple HTTP server
echo "🌐 Starting local server..."
echo ""

# Try different server options
if command -v python3 &> /dev/null; then
    echo "📡 Server running at: http://localhost:8000"
    echo "📚 Library URL: http://localhost:8000/synthesis-library.html"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    echo "📡 Server running at: http://localhost:8000"
    echo "📚 Library URL: http://localhost:8000/synthesis-library.html"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    python -m SimpleHTTPServer 8000
elif command -v npx &> /dev/null; then
    echo "📡 Server running at: http://localhost:8080"
    echo "📚 Library URL: http://localhost:8080/synthesis-library.html"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    npx http-server -p 8080
else
    echo "⚠️  No HTTP server found (python or npx required)"
    echo ""
    echo "You can still open synthesis-library.html directly in your browser"
    echo "Or install a server with: npm install -g http-server"
    exit 1
fi
