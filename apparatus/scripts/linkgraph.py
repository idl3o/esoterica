#!/usr/bin/env python3
"""
LINKGRAPH — the expander's measuring harness. Read-only; never writes to corpus/.

Resolves every [[wiki-link]] and relative .md link in corpus/ by the rulings of
the September 2026 harvest (corpus/seeds/SEED-HARVEST-2026-09.md), then measures
the document graph the links make.

    python linkgraph.py measure  [--include-slate] [--cluster DIR ...]
    python linkgraph.py phantoms [-n 40]
    python linkgraph.py dead
    python linkgraph.py propose  [-n 40]
    python linkgraph.py resolve TARGET [--from PATH]

Resolution rules (in order):
  path-like target      corpus/<target>.md
  slug.seed/.grown/.slate/.template   explicit class
  bare slug             grown synthesis > seed > unique other (slate never)
  snake_case            constellation node -> its document
  Title Case prose      slugified, then the rules above
  alias table           near-miss retargets (ALIASES below)

Film-slate mirrors are excluded from every measure unless --include-slate.
"""

import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CORPUS = REPO / "corpus"
CONSTELLATION = REPO / "constellation" / "constellation.json"

WIKI = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]*)?(?:#[^\]]*)?\]\]")
MDLINK = re.compile(r"\]\(([^)\s#]*\.md)(?:#[^)]*)?\)")
PARA_MIN_WORDS = 40

# The rulings live in link-rules.json, shared with the site renderer
# (apparatus/site/src/lib/wikilinks.ts). Paths there are corpus-relative.
RULES = json.loads((HERE / "link-rules.json").read_text(encoding="utf-8"))
ALIASES = RULES["aliases"]                      # near-miss target slug -> real slug
PREFER = {k: "corpus/" + v for k, v in RULES["prefer"].items()}   # bare slug -> winner
DIR_PRIORITY = tuple("corpus/" + d for d in RULES["dir_priority"])  # tie-break order

# Fenced blocks and inline code are not citations; the renderer skips them too.
FENCE = re.compile(r"```[\s\S]*?```|`[^`\n]*`")


def strip_code(text: str) -> str:
    return FENCE.sub(" ", text)

CLASS_DIRS = (
    ("grown", "corpus/synthesis/grown/"),
    ("seed", "corpus/seeds/"),
    ("slate", "corpus/film-slate/"),
)


# ------------------------------------------------------------------ loading

def rel(p: Path) -> str:
    return p.resolve().relative_to(REPO).as_posix()


def doc_class(path: str) -> str:
    for cls, prefix in CLASS_DIRS:
        if path.startswith(prefix):
            return cls
    return "other"


def slug_of(path: str) -> str:
    stem = Path(path).stem
    if doc_class(path) == "slate":
        stem = re.sub(r"^\d+-", "", stem)
    if stem.endswith(".template"):
        return stem
    return stem


def load_corpus():
    files = sorted(rel(p) for p in CORPUS.rglob("*.md"))
    by_slug = collections.defaultdict(list)
    for f in files:
        by_slug[slug_of(f)].append(f)
    return files, by_slug


def load_constellation():
    data = json.loads(CONSTELLATION.read_text(encoding="utf-8"))["nodes"]
    node_doc = {}
    for nid, node in data.items():
        doc = node.get("document")
        if doc:
            node_doc[nid] = doc if doc.startswith("corpus/") else "corpus/" + doc
    return data, node_doc


def slugify(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


# ---------------------------------------------------------------- resolving

class Resolver:
    def __init__(self, files, by_slug, nodes, node_doc):
        self.files = set(files)
        self.by_slug = by_slug
        self.nodes = nodes
        self.node_doc = node_doc

    def pick(self, candidates, want=None):
        """Apply the bare-slug ruling to a list of same-slug paths."""
        if want:
            hits = [c for c in candidates if doc_class(c) == want]
            return (hits[0], "resolved") if hits else (None, "phantom")
        for cls in ("grown", "seed"):
            hits = [c for c in candidates if doc_class(c) == cls]
            if hits:
                return hits[0], "resolved"
        others = [c for c in candidates if doc_class(c) == "other"]
        if len(others) == 1:
            return others[0], "resolved"
        if not others:
            return None, "phantom"
        slug = slug_of(others[0])
        if PREFER.get(slug) in others:
            return PREFER[slug], "resolved"
        for prefix in DIR_PRIORITY:
            hits = [c for c in others if c.startswith(prefix)]
            if hits:
                return sorted(hits)[0], "resolved"
        return sorted(others)[0], "ambiguous"

    def resolve(self, target: str):
        """Return (path or None, status). Status: resolved|ambiguous|node-only|phantom."""
        t = target.strip().strip("/")
        if t.startswith("./"):
            t = t[2:]
        if "/" in t:
            cand = "corpus/" + t.removesuffix(".md") + ".md"
            return (cand, "resolved") if cand in self.files else (None, "phantom")
        want = None
        m = re.fullmatch(r"(.+)\.(seed|grown|slate)", t)
        if m:
            t, want = m.group(1), m.group(2)
        if t not in self.by_slug and re.search(r"[A-Z\s]", t):
            t = slugify(t)
        t = ALIASES.get(t, t)
        if t in self.by_slug:
            return self.pick(self.by_slug[t], want)
        if "_" in t and t.replace("_", "-") in self.by_slug:
            return self.pick(self.by_slug[t.replace("_", "-")], want)
        snake = t.replace("-", "_")
        if snake in self.nodes:
            doc = self.node_doc.get(snake)
            return (doc, "resolved") if doc in self.files else (None, "node-only")
        return None, "phantom"

    def resolve_md(self, src: str, href: str):
        """Return (corpus path, status): status is corpus | repo | dead."""
        if href.startswith("/"):
            # The site treats a leading slash as corpus-root; pathlib would drop the drive.
            cands = (CORPUS / href.lstrip("/"),)
        else:
            base = (REPO / src).parent
            cands = (base / href, CORPUS / href, REPO / href)
        for cand in cands:
            try:
                p = rel(cand)
            except ValueError:
                continue
            if p in self.files:
                return p, "corpus"
            if cand.exists():
                return None, "repo"
        return None, "dead"


# ------------------------------------------------------------------ graph

class Graph:
    def __init__(self, include_slate=False):
        self.files, self.by_slug = load_corpus()
        self.nodes, self.node_doc = load_constellation()
        self.res = Resolver(self.files, self.by_slug, self.nodes, self.node_doc)
        self.docs = [f for f in self.files if include_slate or doc_class(f) != "slate"]
        self.out = collections.defaultdict(set)
        self.inn = collections.defaultdict(set)
        self.phantoms = collections.Counter()
        self.phantom_srcs = collections.defaultdict(set)
        self.ambiguous = collections.Counter()
        self.node_only = collections.Counter()
        self.dead = []
        self.paras = collections.defaultdict(lambda: [0, 0])  # dir -> [paras, unlinked]
        self.words = collections.Counter()
        for f in self.docs:
            self.scan(f)

    def scan(self, src):
        raw = (REPO / src).read_text(encoding="utf-8", errors="ignore")
        self.words[src] = len(raw.split())
        text = strip_code(raw)
        for m in WIKI.finditer(text):
            self.edge_wiki(src, m.group(1))
        for m in MDLINK.finditer(text):
            href = m.group(1)
            if href.startswith("http"):
                continue
            tgt, status = self.res.resolve_md(src, href)
            if tgt:
                self.add(src, tgt)
            elif status == "dead":
                self.dead.append((src, href))
        d = topdir(src)
        for p in re.split(r"\n\s*\n", text):
            if len(p.split()) < PARA_MIN_WORDS:
                continue
            self.paras[d][0] += 1
            if not WIKI.search(p) and not MDLINK.search(p):
                self.paras[d][1] += 1

    def edge_wiki(self, src, target):
        tgt, status = self.res.resolve(target)
        key = target.strip()
        if status == "phantom":
            self.phantoms[key] += 1
            self.phantom_srcs[key].add(src)
        elif status == "node-only":
            self.node_only[key] += 1
        elif status == "ambiguous":
            self.ambiguous[key] += 1
        if tgt:
            self.add(src, tgt)

    def add(self, src, tgt):
        if tgt == src or doc_class(tgt) == "slate" and tgt not in self.docs:
            return
        self.out[src].add(tgt)
        self.inn[tgt].add(src)

    # -- measures --------------------------------------------------------

    def components(self):
        seen, sizes = set(), []
        for n in self.docs:
            if n in seen:
                continue
            stack, size = [n], 0
            while stack:
                x = stack.pop()
                if x in seen:
                    continue
                seen.add(x)
                size += 1
                stack.extend((self.out[x] | self.inn[x]) - seen)
            sizes.append(size)
        return sorted(sizes, reverse=True)

    def conductance(self, cluster_prefixes):
        inside = {d for d in self.docs if any(d.startswith(p) for p in cluster_prefixes)}
        a_out = sum(1 for s in inside for t in self.out[s] if t not in inside)
        b_in = sum(1 for s in self.docs if s not in inside for t in self.out[s] if t in inside)
        vol_a = sum(len(self.out[s]) for s in inside)
        vol_b = sum(len(self.out[s]) for s in self.docs if s not in inside)
        cut = a_out + b_in
        return dict(size=len(inside), out=a_out, back=b_in,
                    conductance=cut / max(1, min(vol_a, vol_b)))

    def bridge_share(self):
        """Share of linked documents whose inbound links come from >= 2 top-level dirs."""
        linked = [d for d in self.docs if self.inn[d]]
        multi = sum(1 for d in linked if len({topdir(s) for s in self.inn[d]}) >= 2)
        return multi, len(linked)

    def per_dir(self):
        rows = collections.defaultdict(lambda: [0, 0, 0, 0])  # files, no-in, no-out, words
        for d in self.docs:
            r = rows[topdir(d)]
            r[0] += 1
            r[1] += not self.inn[d]
            r[2] += not self.out[d]
            r[3] += self.words[d]
        return rows


def topdir(path: str) -> str:
    return "/".join(path.split("/")[:3])


# ---------------------------------------------------------------- commands

def cmd_measure(g: Graph, args):
    sizes = g.components()
    singletons = sum(1 for s in sizes if s == 1)
    edges = sum(len(v) for v in g.out.values())
    print(f"documents {len(g.docs)}   edges {edges}   phantom links {sum(g.phantoms.values())} "
          f"({len(g.phantoms)} targets)   node-only {sum(g.node_only.values())}   "
          f"ambiguous {sum(g.ambiguous.values())}   dead md links {len(g.dead)}")
    print(f"components {len(sizes)}   giant {sizes[0]}   singletons {singletons}")
    multi, linked = g.bridge_share()
    print(f"bridge share: {multi}/{linked} linked documents receive links from 2+ directories "
          f"({100 * multi / max(1, linked):.0f}%)")
    if args.cluster:
        c = g.conductance(args.cluster)
        print(f"cluster {args.cluster}: {c['size']} docs, out {c['out']}, back {c['back']}, "
              f"conductance {c['conductance']:.3f}")
    print(f"\n{'directory':44} {'files':>5} {'no-in':>6} {'no-out':>6} {'kwords':>6} {'0-link paras':>12}")
    rows = g.per_dir()
    for d, (n, ni, no, w) in sorted(rows.items(), key=lambda kv: -kv[1][3])[:args.n]:
        p, z = g.paras.get(d, [0, 0])
        share = f"{100 * z / p:.0f}%" if p else "-"
        print(f"{d:44} {n:5} {ni:6} {no:6} {w / 1000:6.0f} {share:>12}")


def cmd_phantoms(g: Graph, args):
    print(f"{'links':>5} {'files':>5}  target")
    for t, n in g.phantoms.most_common(args.n):
        print(f"{n:5} {len(g.phantom_srcs[t]):5}  {t}")
    if g.node_only:
        print("\nconstellation node without a document:")
        for t, n in g.node_only.most_common(args.n):
            print(f"{n:5}        {t}")
    if g.ambiguous:
        print("\nambiguous bare slugs (several non-seed/grown files share the stem):")
        for t, n in g.ambiguous.most_common(args.n):
            print(f"{n:5}        {t}  -> {sorted(g.by_slug[t])}")


def cmd_dead(g: Graph, args):
    for src, href in sorted(g.dead):
        print(f"{src}\t{href}")
    print(f"\n{len(g.dead)} dead relative links", file=sys.stderr)


def proposals(g: Graph, limit: int = 0, partners: int = 3):
    """For each singleton with a constellation node, the documents its neighbourhood meets.

    Returns dicts: doc, node, type, dir, partners=[{doc, via, score}]. limit=0 means all.
    """
    doc_node = {d: nid for nid, d in g.node_doc.items()}
    out = []
    for d in g.docs:
        if g.inn[d] or g.out[d] or d not in doc_node:
            continue
        nid = doc_node[d]
        hits = collections.Counter()
        for nb in g.nodes[nid].get("connections", []):
            if nb in g.node_doc and g.node_doc[nb] != d:
                hits[(g.node_doc[nb], nb)] += 2
            for nb2 in g.nodes.get(nb, {}).get("connections", []):
                if nb2 in g.node_doc and g.node_doc[nb2] != d:
                    hits[(g.node_doc[nb2], nb)] += 1
        if not hits:
            continue
        out.append({
            "doc": d, "node": nid, "type": g.nodes[nid].get("type", ""), "dir": topdir(d),
            "partners": [{"doc": doc, "via": via, "score": score}
                         for (doc, via), score in hits.most_common(partners)],
        })
        if limit and len(out) >= limit:
            break
    return out


def cmd_propose(g: Graph, args):
    props = proposals(g, args.n)
    if args.json:
        json.dump(props, sys.stdout, indent=1)
        return
    for p in props:
        print(f"\n{p['doc']}  [{p['node']}]")
        for q in p["partners"]:
            print(f"    meets {q['doc']}  via {q['via']}  ({q['score']})")


def cmd_resolve(g: Graph, args):
    path, status = g.res.resolve(args.target)
    print(f"{args.target} -> {path} [{status}]")
    if args.target in g.by_slug:
        print("candidates:", g.by_slug[args.target])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", default="measure",
                    choices=["measure", "phantoms", "dead", "propose", "resolve"])
    ap.add_argument("target", nargs="?")
    ap.add_argument("-n", type=int, default=40)
    ap.add_argument("--include-slate", action="store_true")
    ap.add_argument("--json", action="store_true", help="propose: emit JSON")
    ap.add_argument("--cluster", nargs="*",
                    default=["corpus/seeds/", "corpus/synthesis/grown/", "corpus/synthesis/capstones/"])
    args = ap.parse_args()
    g = Graph(include_slate=args.include_slate)
    {"measure": cmd_measure, "phantoms": cmd_phantoms, "dead": cmd_dead,
     "propose": cmd_propose, "resolve": cmd_resolve}[args.command](g, args)


if __name__ == "__main__":
    main()
