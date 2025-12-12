#!/bin/bash

# QUICK INDEX UPDATE
# Run this after adding/editing synthesis documents

echo "🔄 Updating synthesis library index..."

# Check directory
if [ ! -d "synthesis" ]; then
    echo "❌ Error: Run from esoterica root directory"
    exit 1
fi

# Rebuild index
node build-synthesis-index.js

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Index updated successfully!"
    echo "🌐 Refresh synthesis-library.html in your browser to see changes"
else
    echo ""
    echo "❌ Index update failed"
    exit 1
fi
