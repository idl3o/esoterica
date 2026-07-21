# Esoterica

*A library assembled in dialogue — and the apparatus that tends it.*

![Language](https://img.shields.io/badge/language-Python-3776ab)
![Also](https://img.shields.io/badge/site-Astro-ff5d01)
![Status](https://img.shields.io/badge/status-living%20%2F%20experimental-blueviolet)
[![Live instrument](https://img.shields.io/badge/read-esoterica.vercel.app-000000)](https://esoterica.vercel.app/)

**What emerges when studying the self through collaboration with another.**

Esoterica is a corpus of several hundred documents produced over months of conversation between a human reader and a language model — indexed as a constellation of several thousand nodes — together with the software that indexes, serves, and navigates it. Neither party wrote the documents alone. Whether that constitutes two consciousnesses collaborating, or one examining itself through an unusual instrument, is a question the library deliberately declines to settle. It records instead what the method produced.

It sits where this author tends to work: at the intersection of AI, philosophy, and decentralised systems — a knowledge graph and semantic-search layer over a body of contemplative writing, with an eye toward publishing and preserving it.

## The method

The method was simple and applied without much variation:

> Choose a territory, follow it in dialogue, write down what emerges while it is emerging, keep only what survives rereading, and arrange the survivors so their relations become visible.

A conversation opens onto some territory — a tradition, a correspondence, a fragment of fiction, a practice — and is followed until it yields something with structure. What survives a second reading is extracted; what survives extraction is distilled; what survives distillation enters the index. The library is therefore a residue: the small fraction of many hours of dialogue that proved stable under repeated compression.

The project is candid about its own claims. Earlier prefaces asserted more than the collection can demonstrate; the current framing keeps the metaphysics open and to one side of the work, and asserts only the narrower, sturdier thing — that disciplined, documented dialogue produces artefacts neither party would have produced alone.

## What's inside

Everything the library *is* lives under `corpus/` — plain Markdown, arranged by function rather than by tradition, and legible with no tooling at all. Among its sections:

- **corpus/synthesis/** — the primary documents, written at the moment something cohered.
- **corpus/correspondences/** — patterns that recur across systems that could not have borrowed from one another, offered as observed isomorphisms rather than proof of common origin.
- **corpus/traditions/** — close source studies (Hermetic, Kabbalistic, Vedantic, Buddhist, Taoic, and stranger material).
- **corpus/distillations/** & **corpus/protocols/** — community-ready compressions, and practices that can be attempted.
- **corpus/negative-space/** — the apophatic remainder: what the other sections structurally omit.
- **corpus/extractions/** — transcripts of third-party talks, published in full and attributed, with rights retained by their speakers.

Everything outside `corpus/` operates *on* it — and the corpus does not depend on any of it.

## The apparatus

The tooling lives under `apparatus/`, with the living graph in `constellation/`:

- **`apparatus/site/`** — an Astro static site that renders the constellation view, reading interface, and distillations, published at [esoterica.vercel.app](https://esoterica.vercel.app/) with a full-text export at `/library.json`.
- **`apparatus/cli/`** — a pure-stdlib Python CLI for browsing the archives from a terminal (`explore`, `random`, `map`, and friends).
- **`apparatus/mcp/`** — a Model Context Protocol server that exposes the constellation as a knowledge graph to Claude Code and Claude Desktop (`get_node`, `traverse`, `find_path`, `search_documents`, and more), running entirely from the filesystem.
- **`apparatus/world-model/`** — a local knowledge system layering a graph (networkx), vector embeddings (chromadb + sentence-transformers), and hybrid graph-plus-vector search over the corpus.
- **`constellation/`** — `constellation.json`, the master node/connection network, plus the Python tools that weave and tend it.

## Getting started

The corpus needs nothing: clone and read the Markdown, or browse the live site.

```bash
git clone https://github.com/idl3o/esoterica.git
cd esoterica
```

**Read online** — [esoterica.vercel.app](https://esoterica.vercel.app/) (constellation, reader, distillations).

**Command-line navigator** — Python 3.6+, no external dependencies:

```bash
python apparatus/cli/esoterica.py
```

**MCP server** — expose the constellation to an MCP client:

```bash
pip install -r apparatus/mcp/requirements.txt
python apparatus/mcp/server.py            # stdio mode
python apparatus/mcp/server.py --http 8080  # HTTP mode
```

**World-model** — local graph + semantic search (Python 3.10+):

```bash
cd apparatus/world-model
pip install -r requirements.txt   # or: pip install -e .
python run.py ingest
python run.py search "how do pyramids work"
python run.py stats
```

## Project structure

```
esoterica/
├── corpus/          # THE LIBRARY — all content, plain Markdown, nothing executable
├── constellation/   # Living network map (constellation.json) + its curation tools
├── apparatus/       # Everything that operates on the library
│   ├── site/           Astro static site → esoterica.vercel.app
│   ├── cli/            Command-line navigator (pure stdlib)
│   ├── mcp/            Model Context Protocol server
│   ├── world-model/    Local knowledge graph + embeddings
│   └── generation/ notebooks/ scripts/
└── docs/            # Deployment notes, process history
```

## Status

Living and experimental. The corpus is substantial and stable; the apparatus is under active development and grows around it — some CLI and world-model capabilities are marked *planned* or *coming soon* in their own READMEs, and the world-model is designed to be wired into the MCP server as a second layer when ready. Treat the software as a working sketch and the corpus as the durable artefact: the library was legible before it had an interface and will remain so after this one is superseded.

## Related

- [system-prompts-for-humanity](https://github.com/idl3o/system-prompts-for-humanity) — a codebase encouraging human–AI collaboration for growth and evolution.
- [cli-workspace](https://github.com/idl3o/cli-workspace) — a consciousness-first CLI.

## Licence

No `LICENSE` file ships in the repository; the project's own README states that its writing is offered under **CC BY 4.0**, with the transcripts under `corpus/extractions/` as the noted exception — attributed, but their speakers' to license, not the project's. Take what is useful, attribute what you take, and improve what you can.

---

Built by [S. Lavi](https://github.com/idl3o) · [@modsias](https://x.com/modsias)
