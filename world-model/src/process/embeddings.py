"""
Embedding Generator: Generate vector embeddings for documents and chunks
"""

from typing import List, Optional
from pathlib import Path
import json


class EmbeddingGenerator:
    """
    Generate embeddings using sentence-transformers or fallback.

    Supports:
    - sentence-transformers (local, default)
    - OpenAI embeddings (API, optional)
    - Ollama embeddings (local, optional)
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        self._dimension = 384  # Default for MiniLM

        self._init_model()

    def _init_model(self):
        """Initialize embedding model"""
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            self._dimension = self._model.get_sentence_embedding_dimension()
            print(f"Loaded embedding model: {self.model_name} (dim={self._dimension})")
        except ImportError:
            print("sentence-transformers not available, using fallback embeddings")
            self._model = None

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a text string.

        Args:
            text: Input text

        Returns:
            Embedding vector as list of floats
        """
        if not text:
            return [0.0] * self._dimension

        if self._model:
            embedding = self._model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        else:
            return self._fallback_embed(text)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (batched).

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        if self._model:
            embeddings = self._model.encode(texts, convert_to_numpy=True)
            return [e.tolist() for e in embeddings]
        else:
            return [self._fallback_embed(t) for t in texts]

    def embed_document(self, doc) -> List[float]:
        """
        Generate embedding for entire document.

        Uses title + first chunk for representation.
        """
        text = doc.title
        if doc.chunks:
            text += " " + doc.chunks[0].text[:500]
        return self.embed_text(text)

    def embed_chunks(self, chunks: List) -> List[List[float]]:
        """Generate embeddings for document chunks"""
        texts = [c.text for c in chunks]
        return self.embed_texts(texts)

    def _fallback_embed(self, text: str) -> List[float]:
        """
        Simple fallback embedding using character/word statistics.

        Not semantically meaningful but maintains dimensionality.
        """
        import hashlib

        # Use hash to generate deterministic pseudo-embedding
        text_hash = hashlib.sha256(text.encode()).hexdigest()

        # Convert hash to floats
        embedding = []
        for i in range(0, min(len(text_hash), self._dimension * 2), 2):
            byte_val = int(text_hash[i:i+2], 16)
            embedding.append((byte_val - 128) / 128.0)  # Normalize to [-1, 1]

        # Pad if needed
        while len(embedding) < self._dimension:
            embedding.append(0.0)

        return embedding[:self._dimension]

    @property
    def dimension(self) -> int:
        """Return embedding dimension"""
        return self._dimension
