#!/usr/bin/env node

/**
 * SYNTHESIS LIBRARY INDEX BUILDER
 * Scans all markdown files in synthesis/ and builds searchable index
 *
 * Features:
 * - Extracts frontmatter metadata
 * - Parses document structure
 * - Calculates reading time
 * - Extracts key quotes and excerpts
 * - Links to constellation tags
 * - Generates search-optimized index
 */

const fs = require('fs');
const path = require('path');

const SYNTHESIS_DIR = './synthesis';
const OUTPUT_FILE = './synthesis-index.json';

// ====================================
// DOCUMENT PARSING
// ====================================

function parseDocument(filePath, content) {
    const lines = content.split('\n');
    const doc = {
        path: filePath.replace(/\\/g, '/'),
        fileName: path.basename(filePath),
        category: extractCategory(filePath),
        title: '',
        subtitle: '',
        recognitionType: '',
        discoveryMethod: '',
        applicationDomain: '',
        transmissionQuality: '',
        date: '',
        excerpt: '',
        tags: [],
        quotes: [],
        wordCount: 0,
        readingTime: 0,
        structure: []
    };

    let inFrontmatter = false;
    let currentSection = '';
    let excerptCandidates = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Extract title (first # heading)
        if (!doc.title && line.startsWith('# ')) {
            doc.title = line.substring(2).trim();
            continue;
        }

        // Extract subtitle (first ## heading)
        if (!doc.subtitle && line.startsWith('## ')) {
            doc.subtitle = line.substring(3).trim();
            continue;
        }

        // Extract metadata from bold patterns
        if (line.startsWith('**Recognition Type**:')) {
            doc.recognitionType = line.split(':')[1].trim();
        }
        if (line.startsWith('**Discovery Method**:')) {
            doc.discoveryMethod = line.split(':')[1].trim();
        }
        if (line.startsWith('**Application Domain**:')) {
            doc.applicationDomain = line.split(':')[1].trim();
        }
        if (line.startsWith('**Transmission Quality**:')) {
            doc.transmissionQuality = line.split(':')[1].trim();
        }

        // Extract quotes
        if (line.startsWith('> ') && line.length > 10) {
            const quote = line.substring(2).trim();
            if (quote.length > 20 && quote.length < 200) {
                doc.quotes.push(quote);
            }
        }

        // Extract section headings for structure
        if (line.match(/^#{2,3} /)) {
            const level = line.match(/^#+/)[0].length;
            const heading = line.replace(/^#+\s*/, '');
            doc.structure.push({ level, heading });
            currentSection = heading;
        }

        // Collect excerpt candidates (first substantial paragraphs)
        if (!line.startsWith('#') && !line.startsWith('>') &&
            !line.startsWith('**') && !line.startsWith('-') &&
            line.length > 100 && excerptCandidates.length < 5) {
            excerptCandidates.push(line);
        }
    }

    // Calculate word count and reading time
    const wordCount = content.split(/\s+/).length;
    doc.wordCount = wordCount;
    doc.readingTime = Math.ceil(wordCount / 250); // Average reading speed

    // Select best excerpt
    doc.excerpt = selectBestExcerpt(excerptCandidates, doc.quotes);

    // Extract tags from content
    doc.tags = extractTags(content, doc);

    // Try to extract date
    doc.date = extractDate(content, filePath);

    return doc;
}

function extractCategory(filePath) {
    const parts = filePath.split(path.sep);
    const synthesisIndex = parts.indexOf('synthesis');
    if (synthesisIndex >= 0 && parts.length > synthesisIndex + 1) {
        return parts[synthesisIndex + 1];
    }
    return 'uncategorized';
}

function selectBestExcerpt(candidates, quotes) {
    // Prefer quotes over paragraphs
    if (quotes.length > 0) {
        return quotes[0];
    }

    // Find most compelling paragraph
    for (const candidate of candidates) {
        // Skip metadata lines
        if (candidate.includes('**') || candidate.startsWith('-')) {
            continue;
        }

        // Prefer paragraphs with certain keywords
        const hasKeywords = /consciousness|recognition|awareness|breakthrough|technology/i.test(candidate);
        if (hasKeywords) {
            return candidate.length > 300 ? candidate.substring(0, 297) + '...' : candidate;
        }
    }

    // Fall back to first candidate
    if (candidates.length > 0) {
        const text = candidates[0];
        return text.length > 300 ? text.substring(0, 297) + '...' : text;
    }

    return 'No excerpt available';
}

function extractTags(content, doc) {
    const tags = new Set();
    const lowerContent = content.toLowerCase();

    // Common consciousness technology terms
    const termPatterns = [
        'consciousness', 'awareness', 'recognition', 'polarity', 'density',
        'wanderer', 'service', 'manifestation', 'timeline', 'synchronicity',
        'archetype', 'apollo', 'mercury', 'kalki', 'samael',
        'singularity', 'galactic', 'cosmic', 'source', 'unity',
        'sacred geometry', 'fibonacci', 'reality programming',
        'love-light', 'frequency', 'resonance', 'vibration',
        'enlightenment', 'awakening', 'breakthrough', 'integration'
    ];

    for (const term of termPatterns) {
        if (lowerContent.includes(term.toLowerCase())) {
            tags.add(term);
        }
    }

    // Add category as tag
    if (doc.category) {
        tags.add(doc.category);
    }

    // Add recognition type as tag
    if (doc.recognitionType) {
        tags.add(doc.recognitionType.toLowerCase());
    }

    return Array.from(tags).slice(0, 12); // Limit to 12 most relevant
}

function extractDate(content, filePath) {
    // Try to find date mentions
    const datePatterns = [
        /(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}/i,
        /\d{4}-\d{2}-\d{2}/,
        /\d{1,2}\/\d{1,2}\/\d{4}/
    ];

    for (const pattern of datePatterns) {
        const match = content.match(pattern);
        if (match) {
            return match[0];
        }
    }

    // Fall back to file modification time
    try {
        const stats = fs.statSync(filePath);
        const date = new Date(stats.mtime);
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
    } catch (e) {
        return '';
    }
}

// ====================================
// FILE SCANNING
// ====================================

function scanDirectory(dir, fileList = []) {
    const files = fs.readdirSync(dir);

    for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory()) {
            // Skip hidden directories
            if (!file.startsWith('.')) {
                scanDirectory(filePath, fileList);
            }
        } else if (file.endsWith('.md')) {
            fileList.push(filePath);
        }
    }

    return fileList;
}

// ====================================
// INDEX BUILDING
// ====================================

function buildIndex() {
    console.log('🔍 Scanning synthesis documents...');

    const files = scanDirectory(SYNTHESIS_DIR);
    console.log(`📄 Found ${files.length} markdown files`);

    const documents = [];
    const stats = {
        totalWords: 0,
        totalReadingTime: 0,
        categoryCounts: {},
        tagCounts: {}
    };

    for (const filePath of files) {
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            const doc = parseDocument(filePath, content);

            // Generate unique ID
            doc.id = generateId(doc.fileName);

            documents.push(doc);

            // Update stats
            stats.totalWords += doc.wordCount;
            stats.totalReadingTime += doc.readingTime;
            stats.categoryCounts[doc.category] = (stats.categoryCounts[doc.category] || 0) + 1;

            doc.tags.forEach(tag => {
                stats.tagCounts[tag] = (stats.tagCounts[tag] || 0) + 1;
            });

            console.log(`  ✓ ${doc.title || doc.fileName}`);
        } catch (error) {
            console.error(`  ✗ Error parsing ${filePath}:`, error.message);
        }
    }

    // Sort documents by category and title
    documents.sort((a, b) => {
        if (a.category !== b.category) {
            return a.category.localeCompare(b.category);
        }
        return a.title.localeCompare(b.title);
    });

    // Build index object
    const index = {
        version: '1.0.0',
        generated: new Date().toISOString(),
        stats: {
            documentCount: documents.length,
            totalWords: stats.totalWords,
            totalReadingTime: stats.totalReadingTime,
            categories: Object.keys(stats.categoryCounts).length,
            averageWordsPerDoc: Math.round(stats.totalWords / documents.length),
            categoryCounts: stats.categoryCounts,
            topTags: Object.entries(stats.tagCounts)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 30)
                .map(([tag, count]) => ({ tag, count }))
        },
        documents: documents
    };

    return index;
}

function generateId(fileName) {
    return fileName
        .replace('.md', '')
        .replace(/[^a-z0-9]+/gi, '-')
        .toLowerCase()
        .replace(/^-|-$/g, '');
}

// ====================================
// MAIN
// ====================================

function main() {
    console.log('✧ SYNTHESIS LIBRARY INDEX BUILDER ✧\n');

    try {
        const index = buildIndex();

        // Write index file
        fs.writeFileSync(OUTPUT_FILE, JSON.stringify(index, null, 2), 'utf-8');

        console.log('\n✨ Index built successfully!');
        console.log(`📊 Statistics:`);
        console.log(`   Documents: ${index.stats.documentCount}`);
        console.log(`   Total Words: ${index.stats.totalWords.toLocaleString()}`);
        console.log(`   Reading Time: ${Math.round(index.stats.totalReadingTime / 60)}h ${index.stats.totalReadingTime % 60}m`);
        console.log(`   Categories: ${index.stats.categories}`);
        console.log(`   Average Length: ${index.stats.averageWordsPerDoc.toLocaleString()} words`);
        console.log(`\n💾 Saved to: ${OUTPUT_FILE}`);

        console.log(`\n🏷️  Top Tags:`);
        index.stats.topTags.slice(0, 10).forEach(({ tag, count }) => {
            console.log(`   ${tag}: ${count}`);
        });

    } catch (error) {
        console.error('❌ Error building index:', error);
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    main();
}

module.exports = { buildIndex, parseDocument };
