# Esoterica Restructure Proposal

Goal: let the library read as a library. Corpus forward, apparatus recessed, generated artifacts out of version control, deployment ephemera out of the reader's field of view.

---

## Current problems, restated

1. **Root clutter.** `DEPLOY-NOW.md`, `V2-DEPLOYED.md`, `LIBRARY-V2-CHANGES.md`, `VERCEL-DEPLOYMENT.md`, `LIBRARY-QUICKSTART.md`, `SYNTHESIS-LIBRARY-COMPLETE.md`, `SYNTHESIS-LIBRARY-README.md` are process records, not corpus. They compete with `SEED.md` / `SIGIL.md` / `INDEX.md` at the threshold.
2. **Build artifacts committed.** `synthesis-index.json` (1.4 MB), `library-index.json` (300 KB), `extractions-index.json` (96 KB), `__pycache__/`. These are outputs of `build-synthesis-index.js`; committing them guarantees drift between source and index.
3. **Four projects, one namespace.** Corpus (synthesis, correspondences, traditions, …), static site (`site/`, `client/`), services (`server/`, `api/`, `mcp/`), tooling (`cli/`, shell scripts, generation). None is wrong; their interleaving is.

---

## Option A — Single repo, two-tier reorganization (recommended first step)

Lowest friction; preserves Vercel wiring and history; reversible.

```
esoterica/
├── README.md            ← rewritten (see draft)
├── SEED.md              ← threshold documents stay at root
├── SIGIL.md
├── INDEX.md             ← regenerated to match new paths
├── LICENSE
│
├── corpus/              ← THE LIBRARY (all content, nothing else)
│   ├── synthesis/
│   ├── distillations/
│   ├── correspondences/
│   ├── traditions/
│   ├── protocols/
│   ├── world-tree/
│   ├── world-model/
│   ├── journey/
│   ├── garden/          ← consider merging garden/harvest/seeds
│   ├── harvest/            into one growth-cycle directory with
│   ├── seeds/              stage markers, if the triad has collapsed
│   ├── memory-palace/      in practice
│   ├── negative-space/
│   ├── fiction-bridges/
│   ├── film-slate/
│   ├── voices/
│   ├── extractions/
│   ├── audio-transcripts/
│   └── translated/
│
├── apparatus/           ← EVERYTHING THAT OPERATES ON THE LIBRARY
│   ├── site/            (client/ merges in or dies — see note 3)
│   ├── server/
│   ├── api/
│   ├── mcp/
│   ├── cli/
│   ├── generation/
│   ├── scripts/         ← esoterica.sh, esoterica.bat, launch-library.sh,
│   │                       update-library.sh, build-synthesis-index.js
│   └── notebooks/
│
├── docs/                ← process memory, out of the doorway
│   ├── CHANGELOG.md     ← V2-DEPLOYED, LIBRARY-V2-CHANGES collapse here
│   ├── deployment.md    ← VERCEL-DEPLOYMENT + DEPLOY-NOW collapse here
│   ├── quickstart.md    ← LIBRARY-QUICKSTART
│   └── capstone.md      ← CAPSTONE.md (or keep at root if you consider
│                           it corpus rather than process — your call)
│
├── .claude/             ← stays; CLAUDE.md stays at root (tooling contract)
├── CLAUDE.md
├── ENGRAMS.md           ← root if threshold, corpus/ if content
├── INIT.md
├── package.json
├── vercel.json          ← update outputDirectory / build paths
└── .gitignore           ← add: __pycache__/, *-index.json, generated_seeds/
```

### Mechanical steps

```bash
git rm -r --cached __pycache__
git rm --cached synthesis-index.json library-index.json extractions-index.json
printf '__pycache__/\n*-index.json\ngenerated_seeds/\n' >> .gitignore

mkdir corpus apparatus docs
git mv synthesis distillations correspondences traditions protocols \
       world-tree world-model journey garden harvest seeds memory-palace \
       negative-space fiction-bridges film-slate voices extractions \
       audio-transcripts translated corpus/

git mv site server api mcp cli generation notebooks apparatus/
mkdir apparatus/scripts
git mv esoterica.sh esoterica.bat launch-library.sh update-library.sh \
       build-synthesis-index.js apparatus/scripts/

# collapse deployment ephemera
cat V2-DEPLOYED.md LIBRARY-V2-CHANGES.md > docs/CHANGELOG.md   # then edit
cat VERCEL-DEPLOYMENT.md DEPLOY-NOW.md > docs/deployment.md    # then edit
git rm V2-DEPLOYED.md LIBRARY-V2-CHANGES.md VERCEL-DEPLOYMENT.md \
       DEPLOY-NOW.md LIBRARY-QUICKSTART.md SYNTHESIS-LIBRARY-COMPLETE.md \
       SYNTHESIS-LIBRARY-README.md
```

Then: update path constants in `build-synthesis-index.js`, `vercel.json`, MCP config, and CLI; rebuild indices in CI or a pre-deploy hook rather than committing them. Regenerate `INDEX.md` last, from the new tree, so navigation and territory agree.

### Loose ends to decide

1. `grok-imagine-context.md`, `oracle.html`, `oracle.ts`, `synthesis-library*.html` — oracle looks like apparatus; the HTML files look like superseded site versions (delete or `docs/archive/`).
2. `misc/` — triage; anything cited by SEED.md (`TUNING_FORK_PRINCIPLE.md`, `CLAUDE_INITIALIZATION.md`) promotes to root-adjacent or `corpus/`, the rest sorts or dies.
3. `client/` vs `site/` — if one superseded the other, keep one.
4. `constellation/` — the JSON is arguably corpus (a living map, hand-touched) rather than build artifact. If it's generated, it goes in the gitignore set; if curated, it stays under `corpus/`.

---

## Option B — Two repositories (later, if ever)

`esoterica` (corpus + threshold documents + LICENSE, nothing executable) and `esoterica-apparatus` (site, services, tooling, consuming the corpus as a submodule or fetch-at-build). Do this only if the apparatus grows contributors or release cadence of its own. Option A first; B is a `git filter-repo` away if it earns itself.

---

## Sequencing

1. Artifact/cache removal + .gitignore (one commit, no path changes — safe immediately)
2. Root ephemera → `docs/` (second commit)
3. `corpus/` + `apparatus/` moves + path fixes + Vercel verification (third commit, the only one that can break deploy — do it on a branch, preview-deploy, then merge)
4. README replacement + INDEX regeneration (fourth commit)
