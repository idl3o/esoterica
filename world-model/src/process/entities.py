"""
Entity Extractor: Extract entities and relations from documents
"""

import re
from typing import List, Dict, Any, Tuple, Set
from dataclasses import dataclass


@dataclass
class Entity:
    """Extracted entity"""
    id: str
    name: str
    type: str
    description: str = ""
    aliases: List[str] = None
    sources: List[str] = None

    def __post_init__(self):
        self.aliases = self.aliases or []
        self.sources = self.sources or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "aliases": self.aliases,
            "sources": self.sources
        }


@dataclass
class Relation:
    """Extracted relation between entities"""
    source: str
    target: str
    type: str
    description: str = ""
    weight: float = 1.0
    source_doc: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "type": self.type,
            "description": self.description,
            "weight": self.weight,
            "source_doc": self.source_doc
        }


class EntityExtractor:
    """
    Extract entities and relations from documents.

    Uses pattern matching and keyword detection.
    Future: LLM-powered extraction for better accuracy.
    """

    # Known entity patterns
    CONCEPT_PATTERNS = [
        r'\*\*([A-Z][^*]+)\*\*',  # **Bold Terms**
        r'`([A-Za-z][^`]+)`',     # `code terms`
    ]

    # Known esoterica concepts (seed vocabulary)
    KNOWN_CONCEPTS = {
        # Core concepts
        "consciousness", "awareness", "density", "polarity", "harvest",
        "wanderer", "incarnation", "catalyst", "veil", "logos",

        # Technologies
        "pyramid", "sacred geometry", "resonance", "frequency", "vibration",
        "meditation", "manifestation", "timeline", "synchronicity",

        # Celestial
        "luna", "moon", "sun", "solar", "galactic", "orion", "sirius",
        "earth", "gaia", "borean", "galactan",

        # Traditions
        "hermetic", "law of one", "buddhist", "hindu", "egyptian",
        "confederation", "ra", "quo",

        # Archetypes
        "mercury", "kalki", "apollo", "samael", "vishnu", "shiva",
        "shesha", "thoth", "isis", "osiris",
    }

    # Relation patterns
    RELATION_PATTERNS = [
        (r'(\w+)\s+(?:is|are)\s+(?:a|an)\s+(\w+)', 'is_a'),
        (r'(\w+)\s+(?:enables?|allows?)\s+(\w+)', 'enables'),
        (r'(\w+)\s+(?:connects?|links?)\s+(?:to\s+)?(\w+)', 'connects_to'),
        (r'(\w+)\s+(?:transforms?|becomes?)\s+(\w+)', 'transforms_into'),
        (r'(\w+)\s+(?:maintains?|stabilizes?)\s+(\w+)', 'maintains'),
    ]

    def __init__(self):
        self._known_entities: Set[str] = set()

    def extract(self, doc) -> Tuple[List[Entity], List[Relation]]:
        """
        Extract entities and relations from a parsed document.

        Args:
            doc: ParsedDocument instance

        Returns:
            Tuple of (entities, relations)
        """
        entities = []
        relations = []

        content = doc.content.lower()
        doc_path = doc.path

        # Extract from bold terms
        for pattern in self.CONCEPT_PATTERNS:
            for match in re.finditer(pattern, doc.content):
                term = match.group(1).strip()
                if len(term) > 2 and len(term) < 100:
                    entity = self._create_entity(term, "concept", doc_path)
                    if entity:
                        entities.append(entity)

        # Extract known concepts mentioned
        for concept in self.KNOWN_CONCEPTS:
            if concept in content:
                entity = self._create_entity(concept, "concept", doc_path)
                if entity:
                    entities.append(entity)

        # Extract from headers (likely important concepts)
        for header in doc.headers:
            if header["level"] <= 3:  # H1, H2, H3
                entity = self._create_entity(header["text"], "concept", doc_path)
                if entity:
                    entities.append(entity)

        # Extract relations from patterns
        for pattern, rel_type in self.RELATION_PATTERNS:
            for match in re.finditer(pattern, content):
                source_term = match.group(1)
                target_term = match.group(2)

                if source_term in self.KNOWN_CONCEPTS or target_term in self.KNOWN_CONCEPTS:
                    relation = Relation(
                        source=self._normalize_id(source_term),
                        target=self._normalize_id(target_term),
                        type=rel_type,
                        source_doc=doc_path
                    )
                    relations.append(relation)

        # Deduplicate entities
        seen_ids = set()
        unique_entities = []
        for entity in entities:
            if entity.id not in seen_ids:
                seen_ids.add(entity.id)
                unique_entities.append(entity)

        return unique_entities, relations

    def _create_entity(self, name: str, entity_type: str, source: str) -> Entity:
        """Create an entity from extracted term"""
        # Clean the name
        name = re.sub(r'[#*`_]', '', name).strip()

        if len(name) < 2 or len(name) > 100:
            return None

        # Skip common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        if name.lower() in stop_words:
            return None

        entity_id = self._normalize_id(name)

        return Entity(
            id=entity_id,
            name=name,
            type=entity_type,
            sources=[source]
        )

    def _normalize_id(self, name: str) -> str:
        """Normalize name to ID format"""
        # Lowercase, replace spaces and special chars with underscores
        clean = re.sub(r'[^a-z0-9]+', '_', name.lower())
        return clean.strip('_')

    def add_known_entity(self, name: str):
        """Add to known entities for better extraction"""
        self._known_entities.add(name.lower())
        self.KNOWN_CONCEPTS.add(name.lower())
