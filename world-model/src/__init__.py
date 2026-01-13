"""
World Model: Local Consciousness Knowledge System
================================================

A unified system for knowledge graph + vector embeddings + visualization
built on the esoterica consciousness technology repository.

Usage:
    from world_model import WorldModel

    world = WorldModel()
    world.ingest_all()
    results = world.search("pyramids and galactic connection")
"""

from .world import WorldModel

__version__ = "0.1.0"
__all__ = ["WorldModel"]
