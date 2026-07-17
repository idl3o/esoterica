# Deployment

The site is a static Astro build hosted on Vercel at
[esoterica.vercel.app](https://esoterica.vercel.app/).

## How it builds

`vercel.json` at the repo root directs the whole process:

```json
{
  "installCommand": "cd apparatus/site && npm ci",
  "buildCommand":   "cd apparatus/site && npm run build",
  "outputDirectory": "apparatus/site/dist",
  "framework": "astro"
}
```

- **`npm ci`, not `npm install`** — the build installs from the committed
  `apparatus/site/package-lock.json`. This is load-bearing: without a lockfile,
  a fresh resolve once pulled two major versions of Vite into one build (a
  Tailwind peer-range widening) and the site became undeployable for months
  without any commit touching it. The lockfile is committed on purpose; see the
  note in `.gitignore`.
- **`prebuild`** (`apparatus/site/package.json`) runs
  `scripts/sync-public-data.mjs`, which copies `constellation/constellation.json`
  into the site's `public/` for the 3D explorer and fails the build rather than
  shipping an empty or unparseable graph.

## What reads what

The site reads corpus markdown and the constellation graph **at build time**,
directly from the repository — there is no separate content database. The path
layer (`apparatus/site/src/lib/paths.ts`) locates the repo root by climbing for
the `corpus/` + `constellation/` pair, so the site can move within the tree
without path surgery.

## Content is not coupled to the build

The corpus is legible as plain markdown with no tooling at all. The apparatus
indexes, serves, and visualizes it; it does not own it. If this deployment is
ever retired, the library is untouched.

## History

Superseded deployment and process records — from the earlier Express/EJS
platform and the v1/v2 static library — are preserved under
[`history/`](history/). They describe infrastructure that no longer runs and are
kept for provenance only.
