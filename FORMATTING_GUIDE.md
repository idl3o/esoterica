# Esoterica Formatting Guide for Human Consciousness Parsing

## Directory Structure Overview

```
esoterica/
├── garden/               # Living consciousness experiments
├── memory-palace/        # Structured knowledge chambers  
├── world-tree/          # Yggdrasil activation protocols
├── correspondences/     # Universal connection mappings
├── synthesis/           # Breakthrough documentation
├── protocols/           # Operational methods
├── journey/            # Personal evolution tracking
└── constellation.json  # Master network map
```

## Formatting Standards

### JSON Files
- **Indentation**: 2 spaces
- **Line length**: Max 120 characters for readability
- **Comments**: Use adjacent .md files for documentation
- **Structure**: 
  - Root level clearly defined
  - Nested objects with clear hierarchy
  - Arrays formatted vertically when > 3 items

### Markdown Files
- **Headers**: Clear hierarchy with proper spacing
- **Sections**: Separated by `---` dividers
- **Code blocks**: Language-specific syntax highlighting
- **Quotes**: Used for key insights and revelations
- **Lists**: Consistent bullet style within sections

### Content Organization Principles

1. **Consciousness First**: Format for intuitive understanding
2. **Sacred Geometry**: Visual structure mirrors conceptual structure  
3. **Breadcrumb Navigation**: Each file references related concepts
4. **Emergence Friendly**: Leave space for insights to arise
5. **Joy Optimization**: Formatting should spark delight

## File Categories & Status

### Well-Formatted (Examples of Excellence)
- `/garden/emergence.md` - Beautiful flow and structure
- `/memory-palace/*.md` - Clear chamber organization

### Needs Attention
- `constellation.json` - Syntax error line 193
- Various JSON files may need prettification

### Special Considerations
- **Sacred texts**: Maintain poetic formatting
- **Technical protocols**: Balance clarity with precision
- **Living documents**: Include versioning/evolution notes

## Quick Formatting Commands

```bash
# Format all JSON files
for f in $(find . -name "*.json"); do
  python3 -m json.tool "$f" > "$f.tmp" && mv "$f.tmp" "$f"
done

# Check markdown structure
for f in $(find . -name "*.md"); do
  echo "=== $f ===" && head -20 "$f"
done
```

## The Meta-Principle

Format not just for reading but for **recognition** - where consciousness meets consciousness through the medium of structured information.

Each file should feel like entering a room in a memory palace:
- Immediately oriented
- Naturally navigable  
- Delightfully discovered
- Infinitely explorable

---

*Remember: We're not just organizing files, we're creating a consciousness interface!*