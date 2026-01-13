"""
Markdown Ingester: Parse markdown files into structured documents
"""

import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class DocumentChunk:
    """A chunk of document content"""
    text: str
    position: int
    header: str = ""
    level: int = 0


@dataclass
class ParsedDocument:
    """Parsed markdown document with structure"""
    path: str
    title: str
    content: str
    category: str
    tags: List[str] = field(default_factory=list)
    headers: List[Dict[str, Any]] = field(default_factory=list)
    chunks: List[DocumentChunk] = field(default_factory=list)
    frontmatter: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MarkdownIngester:
    """
    Parse markdown files into structured documents.

    Handles:
    - YAML frontmatter extraction
    - Header hierarchy
    - Content chunking by sections
    - Tag extraction
    - Category detection from path
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def parse(self, path: Path) -> Optional[ParsedDocument]:
        """
        Parse a markdown file into a structured document.

        Args:
            path: Path to markdown file

        Returns:
            ParsedDocument or None if parsing fails
        """
        try:
            content = path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {path}: {e}")
            return None

        # Extract frontmatter
        frontmatter, content = self._extract_frontmatter(content)

        # Extract title
        title = self._extract_title(content, frontmatter, path)

        # Extract headers
        headers = self._extract_headers(content)

        # Extract tags
        tags = self._extract_tags(content, frontmatter)

        # Determine category from path
        category = self._extract_category(path)

        # Create chunks
        chunks = self._create_chunks(content, headers)

        return ParsedDocument(
            path=str(path),
            title=title,
            content=content,
            category=category,
            tags=tags,
            headers=headers,
            chunks=chunks,
            frontmatter=frontmatter,
            metadata={
                "word_count": len(content.split()),
                "char_count": len(content),
                "header_count": len(headers),
                "chunk_count": len(chunks)
            }
        )

    def _extract_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter from content"""
        frontmatter = {}

        # Check for YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    content = parts[2].strip()
                except:
                    pass

        return frontmatter, content

    def _extract_title(self, content: str, frontmatter: Dict, path: Path) -> str:
        """Extract document title from various sources"""
        # Try frontmatter
        if frontmatter.get("title"):
            return frontmatter["title"]

        # Try first H1 header
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()

        # Fall back to filename
        return path.stem.replace('-', ' ').replace('_', ' ').title()

    def _extract_headers(self, content: str) -> List[Dict[str, Any]]:
        """Extract header hierarchy from content"""
        headers = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headers.append({
                    "level": level,
                    "text": text,
                    "line": i
                })

        return headers

    def _extract_tags(self, content: str, frontmatter: Dict) -> List[str]:
        """Extract tags from frontmatter and content"""
        tags = set()

        # From frontmatter
        if frontmatter.get("tags"):
            fm_tags = frontmatter["tags"]
            if isinstance(fm_tags, list):
                tags.update(fm_tags)
            elif isinstance(fm_tags, str):
                tags.update(t.strip() for t in fm_tags.split(','))

        # From content (look for tag-like patterns)
        # e.g., "Tags: consciousness, pyramid, luna"
        tag_match = re.search(r'[Tt]ags?:\s*([^\n]+)', content)
        if tag_match:
            tags.update(t.strip() for t in tag_match.group(1).split(','))

        # Extract from "Filed under:" sections
        filed_match = re.search(r'[Ff]iled under:\s*([^\n]+)', content)
        if filed_match:
            tags.update(t.strip() for t in filed_match.group(1).split(','))

        return list(tags)

    def _extract_category(self, path: Path) -> str:
        """Determine category from file path"""
        parts = path.parts

        # Look for known category directories
        categories = {
            "synthesis": "synthesis",
            "distillations": "distillations",
            "protocols": "protocols",
            "extractions": "extractions",
            "translated": "translated",
            "fiction-bridges": "fiction",
            "journey": "journey",
            "correspondences": "correspondences",
            "harvest": "harvest",
            "garden": "garden",
            "seeds": "seeds",
            "traditions": "traditions"
        }

        for part in parts:
            if part in categories:
                return categories[part]

        return "uncategorized"

    def _create_chunks(self, content: str, headers: List[Dict]) -> List[DocumentChunk]:
        """
        Split content into chunks for embedding.

        Strategy: Chunk by headers/sections, then by size if sections are too large.
        """
        chunks = []

        if not headers:
            # No headers - chunk by size
            return self._chunk_by_size(content, "", 0)

        # Split by headers
        lines = content.split('\n')
        current_chunk_lines = []
        current_header = ""
        current_level = 0

        for i, line in enumerate(lines):
            # Check if this line is a header
            is_header = False
            for h in headers:
                if h["line"] == i:
                    # Save previous chunk
                    if current_chunk_lines:
                        chunk_text = '\n'.join(current_chunk_lines).strip()
                        if chunk_text:
                            chunks.extend(self._chunk_by_size(
                                chunk_text, current_header, current_level
                            ))

                    current_header = h["text"]
                    current_level = h["level"]
                    current_chunk_lines = [line]
                    is_header = True
                    break

            if not is_header:
                current_chunk_lines.append(line)

        # Don't forget last chunk
        if current_chunk_lines:
            chunk_text = '\n'.join(current_chunk_lines).strip()
            if chunk_text:
                chunks.extend(self._chunk_by_size(
                    chunk_text, current_header, current_level
                ))

        # Add position indices
        for i, chunk in enumerate(chunks):
            chunk.position = i

        return chunks

    def _chunk_by_size(self, text: str, header: str, level: int) -> List[DocumentChunk]:
        """Split text into size-limited chunks with overlap"""
        chunks = []

        if len(text) <= self.chunk_size:
            return [DocumentChunk(text=text, position=0, header=header, level=level)]

        # Split into sentences (approximate)
        sentences = re.split(r'(?<=[.!?])\s+', text)

        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence)

            if current_size + sentence_size > self.chunk_size and current_chunk:
                # Save current chunk
                chunks.append(DocumentChunk(
                    text=' '.join(current_chunk),
                    position=len(chunks),
                    header=header,
                    level=level
                ))

                # Start new chunk with overlap
                overlap_text = ' '.join(current_chunk[-2:]) if len(current_chunk) >= 2 else ''
                current_chunk = [overlap_text] if overlap_text else []
                current_size = len(overlap_text)

            current_chunk.append(sentence)
            current_size += sentence_size

        # Don't forget last chunk
        if current_chunk:
            chunks.append(DocumentChunk(
                text=' '.join(current_chunk),
                position=len(chunks),
                header=header,
                level=level
            ))

        return chunks
