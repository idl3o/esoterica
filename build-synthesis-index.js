#!/usr/bin/env node

/**
 * SYNTHESIS LIBRARY INDEX BUILDER
 * Builds separate indexes for public and private content
 *
 * PUBLIC INDEX (synthesis-index.json):
 *   - synthesis/ (original consciousness technology documents)
 *   - translated/ (synthesized translations - original work)
 *
 * PRIVATE INDEX (extractions-index.json):
 *   - extractions/ (YouTube transcripts - requires creator consent for public use)
 *
 * Features:
 * - Extracts frontmatter metadata
 * - Parses document structure
 * - Calculates reading time
 * - Extracts key quotes and excerpts
 * - Links to constellation tags
 * - Generates search-optimized index
 *
 * Usage:
 *   node build-synthesis-index.js          # Build both indexes
 *   node build-synthesis-index.js --public # Build only public index
 *   node build-synthesis-index.js --private # Build only private extractions index
 */

const fs = require('fs');
const path = require('path');

const SYNTHESIS_DIR = './synthesis';
const EXTRACTIONS_DIR = './extractions';
const TRANSLATED_DIR = './translated';

// Output files
const PUBLIC_OUTPUT = './synthesis-index.json';
const PRIVATE_OUTPUT = './extractions-index.json';

// ====================================
// DOCUMENT PARSING
// ====================================

function parseDocument(filePath, content) {
    const lines = content.split('\n');
    const { source, category, channel } = extractSourceAndCategory(filePath);
    const doc = {
        path: filePath.replace(/\\/g, '/'),
        fileName: path.basename(filePath),
        source: source,  // 'synthesis', 'extraction', or 'translated'
        category: category,
        channel: channel,  // YouTube channel name if extraction
        title: '',
        subtitle: '',
        recognitionType: '',
        discoveryMethod: '',
        applicationDomain: '',
        transmissionQuality: '',
        videoId: '',  // YouTube video ID if extraction
        videoUrl: '', // YouTube URL if extraction
        duration: '', // Video duration if extraction
        date: '',
        excerpt: '',
        tags: [],
        quotes: [],
        wordCount: 0,
        readingTime: 0,
        structure: []
    };

    let inFrontmatter = false;
    let frontmatterLines = [];
    let currentSection = '';
    let excerptCandidates = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Parse YAML frontmatter
        if (line === '---') {
            if (!inFrontmatter) {
                inFrontmatter = true;
                continue;
            } else {
                inFrontmatter = false;
                // Parse collected frontmatter
                const frontmatter = parseFrontmatter(frontmatterLines);
                if (frontmatter.title) doc.title = frontmatter.title;
                if (frontmatter.video_id) doc.videoId = frontmatter.video_id;
                if (frontmatter.url) doc.videoUrl = frontmatter.url;
                if (frontmatter.duration) doc.duration = frontmatter.duration;
                if (frontmatter.channel) doc.channel = frontmatter.channel;
                if (frontmatter.tags && Array.isArray(frontmatter.tags)) {
                    doc.tags = frontmatter.tags;
                }
                if (frontmatter.extracted) doc.date = frontmatter.extracted;
                if (frontmatter.upload_date) doc.date = frontmatter.upload_date;
                continue;
            }
        }

        if (inFrontmatter) {
            frontmatterLines.push(lines[i]);
            continue;
        }

        // Extract title (first # heading) if not from frontmatter
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

function parseFrontmatter(lines) {
    const result = {};
    for (const line of lines) {
        const match = line.match(/^(\w+):\s*(.+)$/);
        if (match) {
            let [, key, value] = match;
            // Remove quotes from values
            value = value.replace(/^["']|["']$/g, '').trim();
            // Parse JSON arrays
            if (value.startsWith('[') && value.endsWith(']')) {
                try {
                    result[key] = JSON.parse(value);
                } catch {
                    result[key] = value;
                }
            } else {
                result[key] = value;
            }
        }
    }
    return result;
}

function extractSourceAndCategory(filePath) {
    const parts = filePath.split(path.sep);
    let source = 'synthesis';
    let category = 'uncategorized';
    let channel = '';

    // Check which directory we're in
    if (parts.includes('extractions')) {
        source = 'extraction';
        const extractionsIndex = parts.indexOf('extractions');
        if (parts.length > extractionsIndex + 1) {
            channel = parts[extractionsIndex + 1];
            category = 'extraction';
        }
    } else if (parts.includes('translated')) {
        source = 'translated';
        category = 'translated';
    } else if (parts.includes('synthesis')) {
        const synthesisIndex = parts.indexOf('synthesis');
        if (parts.length > synthesisIndex + 1) {
            category = parts[synthesisIndex + 1];
        }
    }

    return { source, category, channel };
}

// Legacy function for backwards compatibility
function extractCategory(filePath) {
    const { category } = extractSourceAndCategory(filePath);
    return category;
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

/**
 * Build index from specified directories
 * @param {Array<{dir: string, label: string, emoji: string}>} directories - Directories to scan
 * @param {string} indexVersion - Version string for the index
 */
function buildIndex(directories, indexVersion = '3.0.0') {
    console.log('🔍 Scanning documents...');

    let files = [];

    // Scan each specified directory
    for (const { dir, label, emoji } of directories) {
        if (fs.existsSync(dir)) {
            const dirFiles = scanDirectory(dir);
            console.log(`${emoji} ${label}: ${dirFiles.length} files`);
            files = files.concat(dirFiles);
        }
    }

    console.log(`📚 Total: ${files.length} markdown files`);

    const documents = [];
    const stats = {
        totalWords: 0,
        totalReadingTime: 0,
        categoryCounts: {},
        sourceCounts: { synthesis: 0, extraction: 0, translated: 0 },
        channelCounts: {},
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
            stats.sourceCounts[doc.source] = (stats.sourceCounts[doc.source] || 0) + 1;

            if (doc.channel) {
                stats.channelCounts[doc.channel] = (stats.channelCounts[doc.channel] || 0) + 1;
            }

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
        version: indexVersion,
        generated: new Date().toISOString(),
        stats: {
            documentCount: documents.length,
            totalWords: stats.totalWords,
            totalReadingTime: stats.totalReadingTime,
            categories: Object.keys(stats.categoryCounts).length,
            averageWordsPerDoc: Math.round(stats.totalWords / documents.length),
            sourceCounts: stats.sourceCounts,
            channelCounts: stats.channelCounts,
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

function printStats(index, outputFile) {
    console.log(`\n📊 Statistics:`);
    console.log(`   Documents: ${index.stats.documentCount}`);
    console.log(`   Total Words: ${index.stats.totalWords.toLocaleString()}`);
    console.log(`   Reading Time: ${Math.round(index.stats.totalReadingTime / 60)}h ${index.stats.totalReadingTime % 60}m`);
    console.log(`   Categories: ${index.stats.categories}`);
    if (index.stats.documentCount > 0) {
        console.log(`   Average Length: ${index.stats.averageWordsPerDoc.toLocaleString()} words`);
    }
    console.log(`\n💾 Saved to: ${outputFile}`);

    if (index.stats.topTags && index.stats.topTags.length > 0) {
        console.log(`\n🏷️  Top Tags:`);
        index.stats.topTags.slice(0, 10).forEach(({ tag, count }) => {
            console.log(`   ${tag}: ${count}`);
        });
    }
}

function main() {
    console.log('✧ SYNTHESIS LIBRARY INDEX BUILDER ✧\n');

    const args = process.argv.slice(2);
    const buildPublic = args.length === 0 || args.includes('--public');
    const buildPrivate = args.length === 0 || args.includes('--private');

    try {
        // Build PUBLIC index (synthesis + translated - for online serving)
        if (buildPublic) {
            console.log('═══════════════════════════════════════════════');
            console.log('  📢 PUBLIC INDEX (synthesis + translated)');
            console.log('═══════════════════════════════════════════════\n');

            const publicDirs = [
                { dir: SYNTHESIS_DIR, label: 'Synthesis', emoji: '📄' },
                { dir: TRANSLATED_DIR, label: 'Translated', emoji: '🔄' }
            ];

            const publicIndex = buildIndex(publicDirs, '3.0.0-public');
            fs.writeFileSync(PUBLIC_OUTPUT, JSON.stringify(publicIndex, null, 2), 'utf-8');

            console.log('\n✨ Public index built successfully!');
            printStats(publicIndex, PUBLIC_OUTPUT);
        }

        // Build PRIVATE index (extractions only - local use, requires consent for public)
        if (buildPrivate) {
            console.log('\n═══════════════════════════════════════════════');
            console.log('  🔒 PRIVATE INDEX (extractions only)');
            console.log('  ⚠️  Requires creator consent for public use');
            console.log('═══════════════════════════════════════════════\n');

            const privateDirs = [
                { dir: EXTRACTIONS_DIR, label: 'Extractions', emoji: '🎬' }
            ];

            const privateIndex = buildIndex(privateDirs, '3.0.0-private');
            fs.writeFileSync(PRIVATE_OUTPUT, JSON.stringify(privateIndex, null, 2), 'utf-8');

            console.log('\n✨ Private index built successfully!');
            printStats(privateIndex, PRIVATE_OUTPUT);
        }

        console.log('\n═══════════════════════════════════════════════');
        console.log('  ✅ Index building complete!');
        console.log('═══════════════════════════════════════════════');

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
