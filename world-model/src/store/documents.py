"""
Document Store: SQLite-based document storage with full-text search
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class DocumentStore:
    """
    Document storage with metadata and full-text search.

    Uses SQLite with FTS5 for efficient text search.
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _init_db(self):
        """Initialize database schema"""
        self._conn = sqlite3.connect(str(self.path))
        self._conn.row_factory = sqlite3.Row

        # Main documents table
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                title TEXT,
                path TEXT,
                category TEXT,
                content TEXT,
                embedding BLOB,
                tags TEXT,
                entities TEXT,
                metadata TEXT,
                created TEXT,
                modified TEXT
            )
        """)

        # Full-text search virtual table
        self._conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
                id,
                title,
                content,
                tags,
                content='documents',
                content_rowid='rowid'
            )
        """)

        # Triggers to keep FTS in sync
        self._conn.execute("""
            CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
                INSERT INTO documents_fts(rowid, id, title, content, tags)
                VALUES (new.rowid, new.id, new.title, new.content, new.tags);
            END
        """)

        self._conn.execute("""
            CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
                INSERT INTO documents_fts(documents_fts, rowid, id, title, content, tags)
                VALUES('delete', old.rowid, old.id, old.title, old.content, old.tags);
            END
        """)

        self._conn.execute("""
            CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
                INSERT INTO documents_fts(documents_fts, rowid, id, title, content, tags)
                VALUES('delete', old.rowid, old.id, old.title, old.content, old.tags);
                INSERT INTO documents_fts(rowid, id, title, content, tags)
                VALUES (new.rowid, new.id, new.title, new.content, new.tags);
            END
        """)

        self._conn.commit()

    # ==================== CRUD OPERATIONS ====================

    def store(self, doc_id: str, doc: Dict[str, Any], embedding: Optional[List[float]] = None):
        """
        Store or update a document.

        Args:
            doc_id: Unique document identifier (usually relative path)
            doc: Document data with title, content, metadata, etc.
            embedding: Optional document-level embedding
        """
        now = datetime.now().isoformat()

        # Serialize complex fields
        tags_json = json.dumps(doc.get("tags", []))
        entities_json = json.dumps(doc.get("entities", []))
        metadata_json = json.dumps(doc.get("metadata", {}))
        embedding_blob = json.dumps(embedding) if embedding else None

        self._conn.execute("""
            INSERT OR REPLACE INTO documents
            (id, title, path, category, content, embedding, tags, entities, metadata, created, modified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc_id,
            doc.get("title", ""),
            doc.get("path", doc_id),
            doc.get("category", ""),
            doc.get("content", ""),
            embedding_blob,
            tags_json,
            entities_json,
            metadata_json,
            doc.get("created", now),
            now
        ))

        self._conn.commit()

    def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        cursor = self._conn.execute(
            "SELECT * FROM documents WHERE id = ?",
            (doc_id,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        return self._row_to_dict(row)

    def exists(self, doc_id: str) -> bool:
        """Check if document exists"""
        cursor = self._conn.execute(
            "SELECT 1 FROM documents WHERE id = ?",
            (doc_id,)
        )
        return cursor.fetchone() is not None

    def delete(self, doc_id: str) -> bool:
        """Delete document by ID"""
        cursor = self._conn.execute(
            "DELETE FROM documents WHERE id = ?",
            (doc_id,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def count(self) -> int:
        """Return total document count"""
        cursor = self._conn.execute("SELECT COUNT(*) FROM documents")
        return cursor.fetchone()[0]

    # ==================== SEARCH ====================

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Full-text search across documents.

        Args:
            query: Search query (supports FTS5 syntax)
            limit: Maximum results

        Returns:
            List of matching documents with relevance scores
        """
        # Use FTS5 match syntax
        cursor = self._conn.execute("""
            SELECT documents.*, bm25(documents_fts) as score
            FROM documents_fts
            JOIN documents ON documents_fts.id = documents.id
            WHERE documents_fts MATCH ?
            ORDER BY score
            LIMIT ?
        """, (query, limit))

        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def search_by_category(self, category: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get documents by category"""
        cursor = self._conn.execute(
            "SELECT * FROM documents WHERE category = ? LIMIT ?",
            (category, limit)
        )
        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def search_by_tag(self, tag: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get documents containing tag"""
        cursor = self._conn.execute(
            "SELECT * FROM documents WHERE tags LIKE ? LIMIT ?",
            (f'%"{tag}"%', limit)
        )
        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def list_all(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """List all documents"""
        cursor = self._conn.execute(
            "SELECT * FROM documents ORDER BY modified DESC LIMIT ?",
            (limit,)
        )
        return [self._row_to_dict(row) for row in cursor.fetchall()]

    def list_categories(self) -> List[str]:
        """Get list of all categories"""
        cursor = self._conn.execute(
            "SELECT DISTINCT category FROM documents WHERE category != ''"
        )
        return [row[0] for row in cursor.fetchall()]

    # ==================== UTILITIES ====================

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert database row to dictionary"""
        d = dict(row)

        # Deserialize JSON fields
        if d.get("tags"):
            d["tags"] = json.loads(d["tags"])
        if d.get("entities"):
            d["entities"] = json.loads(d["entities"])
        if d.get("metadata"):
            d["metadata"] = json.loads(d["metadata"])
        if d.get("embedding"):
            d["embedding"] = json.loads(d["embedding"])

        return d

    # ==================== PERSISTENCE ====================

    def save(self):
        """Commit any pending changes"""
        if self._conn:
            self._conn.commit()

    def load(self):
        """Reconnect to database (usually not needed)"""
        if not self._conn:
            self._init_db()

    def close(self):
        """Close database connection"""
        if self._conn:
            self._conn.close()
            self._conn = None
