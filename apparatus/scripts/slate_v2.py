#!/usr/bin/env python3
"""
SLATE_V2 — the gates of the matured film slate (corpus/film-slate/v2/).

    python slate_v2.py recut                  TOPICS.md covers v1 films 01-111 once each
    python slate_v2.py status                 every topic's gates; stale ones marked
    python slate_v2.py quotes TOPIC           quotation gate (mechanical); stamps on a pass
    python slate_v2.py lint TOPIC             register lint: capitalised copulas, equations
    python slate_v2.py stamp TOPIC GATE [--output DIR --t2v-commit SHA]
    python slate_v2.py audit                  set-level audit across written scripts

The second check lives in slate_v2_check.py (it talks to a local model).

TOPIC is a code (H7) or a folder name (H7-the-bekenstein-bound-and-the-arrow).
Every stamp records the SHA-256 of the files it checked; a later edit to any of them
makes the gate stale. The method is corpus/film-slate/v2/README.md.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, get_args

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
V2 = REPO / "corpus" / "film-slate" / "v2"
V1_FILMS = range(1, 112)
WORDS_PER_MINUTE = 150  # an estimate for planning; t2v measures the real runtime

Gate = Literal["gathered", "ruled", "written", "quotes", "register",
               "second_check", "sam", "rendered"]
GATES: tuple[Gate, ...] = get_args(Gate)
Kind = Literal["exposition", "thesis", "work", "sam"]
KINDS: tuple[Kind, ...] = get_args(Kind)

# The files whose hashes a gate records; editing one afterwards makes the gate stale.
GATE_FILES: dict[Gate, tuple[str, ...]] = {
    "gathered": ("dossier.md",),
    "ruled": ("dossier.md",),
    "written": ("script.md",),
    "quotes": ("script.md", "dossier.md"),
    "register": ("script.md",),
    "second_check": ("script.md", "dossier.md", "second-check.md"),
    "sam": ("script.md", "treatment.md"),
    "rendered": ("script.md", "treatment.md"),
}
VERDICTS = ("stands", "correct", "mark", "pull")


class GateError(Exception):
    """A gate's precondition does not hold; the message says which."""


# --------------------------------------------------------------------------- topics
@dataclass(frozen=True, slots=True)
class Topic:
    code: str
    title: str
    folds: tuple[int, ...]
    kind: Kind
    light: bool
    sam_hand: bool


ROW = re.compile(r"^\|\s*([A-Z]{1,2}\d+)\s*\|(.*)\|\s*$")


def parse_topics(text: str) -> list[Topic]:
    """Parse TOPICS.md's tables. Raises ValueError on a malformed row."""
    topics = []
    for line in text.splitlines():
        m = ROW.match(line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) != 5:
            raise ValueError(f"{m.group(1)}: expected 6 columns, got {len(cells) + 1}")
        title, folds, kind_cell, _rulers, hand = cells
        kind = kind_cell.split()[0]
        if kind not in KINDS:
            raise ValueError(f"{m.group(1)}: unknown kind {kind!r}")
        topics.append(Topic(code=m.group(1), title=title,
                            folds=tuple(int(n) for n in re.findall(r"\d+", folds)),
                            kind=kind, light="(light)" in kind_cell, sam_hand=hand == "Sam"))
    return topics


def recut_problems(topics: list[Topic]) -> list[str]:
    """Every v1 film exactly once, every code unique. Empty list means the re-cut holds."""
    problems = []
    codes = collections.Counter(t.code for t in topics)
    problems += [f"code {c} used {n} times" for c, n in codes.items() if n > 1]
    seen = collections.Counter(n for t in topics for n in t.folds)
    problems += [f"film {n:02d} missing" for n in V1_FILMS if n not in seen]
    problems += [f"film {n:02d} folded {k} times" for n, k in seen.items() if k > 1]
    problems += [f"film {n} is not a v1 number" for n in seen if n not in V1_FILMS]
    return problems


def load_topics(v2: Path = V2) -> list[Topic]:
    return parse_topics(read(v2 / "TOPICS.md"))


def topic_dir(arg: str, v2: Path = V2) -> Path:
    """Resolve a code (H7) or folder name to the topic's folder."""
    if (v2 / arg).is_dir():
        return v2 / arg
    hits = sorted(p for p in v2.glob(f"{arg}-*") if p.is_dir())
    if len(hits) != 1:
        raise GateError(f"{arg}: {len(hits)} folders match in {v2}")
    return hits[0]


# --------------------------------------------------------------------------- files
def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_frontmatter(text: str) -> tuple[dict, str]:
    """A small YAML subset: scalars, [inline, lists], and one level of nested map or list."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta: dict = {}
    key = ""
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t" and key:
            item = line.strip()
            if item.startswith("- "):
                meta[key] = (meta[key] or []) + [_scalar(item[2:])]
            else:
                k, _, v = item.partition(":")
                meta[key] = {**(meta[key] or {}), k.strip(): _scalar(v)}
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        meta[key] = _inline(value) if value else None
    return meta, text[m.end():]


def _scalar(v: str) -> str:
    return v.strip().strip("'\"")


def _inline(v: str):
    if v.startswith("[") and v.endswith("]"):
        return [_scalar(x) for x in v[1:-1].split(",") if x.strip()]
    return _scalar(v)


def paragraphs(body: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]


# --------------------------------------------------------------------------- ledger
def ledger_path(tdir: Path) -> Path:
    return tdir / "ledger.json"


def load_ledger(tdir: Path) -> dict:
    p = ledger_path(tdir)
    return json.loads(read(p)) if p.is_file() else {"gates": {}}


def record(tdir: Path, gate: Gate, measures: dict, today: str | None = None) -> dict:
    """Stamp `gate` with the current hashes of its files and `measures`; write the ledger."""
    files = {f: sha256(tdir / f) for f in GATE_FILES[gate] if (tdir / f).is_file()}
    entry = {"date": today or dt.date.today().isoformat(), "files": files, **measures}
    ledger = load_ledger(tdir)
    ledger["gates"][gate] = entry
    write_atomic(ledger_path(tdir), json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")
    return entry


def write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


GateState = Literal["pass", "stale", "missing"]


def gate_state(tdir: Path, gate: Gate) -> GateState:
    entry = load_ledger(tdir)["gates"].get(gate)
    if entry is None:
        return "missing"
    for name, digest in entry["files"].items():
        path = tdir / name
        if not path.is_file() or sha256(path) != digest:
            return "stale"
    return "pass"


# --------------------------------------------------------------------------- quotes
QUOTED = re.compile(r"“([^”]+)”|\"([^\"\n]+)\"")
FRAGMENT_BREAK = re.compile(r"\.\.\.|\[[^\]]*\]")
QUOTE_MARKS = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-"})


def norm(s: str) -> str:
    """Compare text as words: NFKC, straight quotes, no markdown emphasis or blockquote marks."""
    s = unicodedata.normalize("NFKC", s).translate(QUOTE_MARKS)
    s = re.sub(r"(?m)^\s*>\s?", "", s)
    s = re.sub(r"\s/\s", " ", s)  # a dossier writes verse line breaks as " / "
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).casefold().strip()


def fragments(quote: str) -> list[str]:
    """A quotation's verbatim pieces: ellipses and [editorial insertions] split it."""
    parts = FRAGMENT_BREAK.split(unicodedata.normalize("NFKC", quote))
    return [f for f in (norm(p).strip(" .,;:!?'\"") for p in parts) if f]


def quoted_spans(script_body: str, quote_speakers: list[str]) -> list[str]:
    """Every span the script presents as someone's words."""
    spans = []
    for para in paragraphs(script_body):
        tag = re.match(r"^([A-Z][A-Z'\-]{2,})\.\s+", para)
        if tag and tag.group(1) in quote_speakers:
            spans.append(para[tag.end():])
            continue
        spans += [a or b for a, b in QUOTED.findall(para)]
    return spans


def missing_quotes(script: str, dossier: str) -> list[str]:
    """Quoted spans of the script with a fragment not found verbatim in the dossier."""
    meta, body = split_frontmatter(script)
    haystack = norm(dossier)
    speakers = meta.get("quote_speakers") or []
    return [q for q in quoted_spans(body, speakers)
            if any(f not in haystack for f in fragments(q))]


# --------------------------------------------------------------------------- register
REGISTER_PATTERNS = {
    "capitalised copula": re.compile(r"\b(?:IS|ARE|WAS|WERE)\b"),
    "bold copula": re.compile(r"\*\*(?:is|are|was|were)\*\*"),
    "equation in prose": re.compile(r"\w \= \w"),
    "identity phrase": re.compile(
        r"\b(?:is|are) (?:the same as|identical to|nothing but|literally|really)\b", re.I),
    "always-was": re.compile(r"\b(?:was|were) always\b", re.I),
    # The weeding method's authority tells: the corpus spending its own escape hatch.
    "authority phrase": re.compile(r"\b(?:not a metaphor|without exception|proves?|proven)\b",
                                   re.I),
}


def register_findings(script: str) -> list[tuple[int, str, str]]:
    """(line, pattern, text) for each line the register discipline asks a hand to review."""
    _, body = split_frontmatter(script)
    out = []
    for i, line in enumerate(body.splitlines(), 1):
        for name, pat in REGISTER_PATTERNS.items():
            if pat.search(line):
                out.append((i, name, line.strip()))
    return out


# --------------------------------------------------------------------------- gates
DOSSIER_SECTIONS = range(1, 10)


def check_gathered(tdir: Path) -> dict:
    text = read(tdir / "dossier.md")
    found = {int(n) for n in re.findall(r"(?m)^## (\d)\.", text)}
    absent = [n for n in DOSSIER_SECTIONS if n not in found]
    if absent:
        raise GateError(f"dossier lacks sections {absent}")
    return {"words": len(text.split())}


def claims_rows(dossier: str) -> list[list[str]]:
    """The claims ledger's table rows (section 5), header and rule excluded."""
    sec = re.search(r"(?ms)^## 5\..*?(?=^## 6\.|\Z)", dossier)
    rows = []
    for line in (sec.group(0) if sec else "").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and not set(line) <= set("|-: ") and cells[0] != "ID":
            rows.append(cells)
    return rows


RULING_COLUMN = 6  # ID, claim, where, ruler, proposed verdict, note, ruling


def check_ruled(tdir: Path) -> dict:
    """Every ledger row carries the hand's ruling in its own column, apart from the proposal."""
    rows = claims_rows(read(tdir / "dossier.md"))
    if not rows:
        raise GateError("no claims-ledger rows in section 5")
    tally = collections.Counter()
    for row in rows:
        cell = row[RULING_COLUMN] if len(row) > RULING_COLUMN else ""
        verdict = next((v for v in VERDICTS if cell.lower().startswith(v)), None)
        if verdict is None:
            raise GateError(f"claim {row[0]}: no ruling in column {RULING_COLUMN + 1} ({cell!r})")
        tally[verdict] += 1
    return {"claims": len(rows), "verdicts": dict(tally)}


def spoken_words(script: str) -> int:
    _, body = split_frontmatter(script)
    body = re.sub(r"(?m)^([A-Z][A-Z'\-]{2,})\.\s+", "", body)
    return len(re.findall(r"[\w'-]+", body))


def check_written(tdir: Path) -> dict:
    script = read(tdir / "script.md")
    meta, body = split_frontmatter(script)
    heads = re.findall(r"(?m)^## (.+)$", body)
    if not meta or not re.search(r"(?m)^# ", body):
        raise GateError("script needs frontmatter and a # title")
    if not heads or heads[-1].strip() != "What Is Declined":
        raise GateError("the last movement must be '## What Is Declined'")
    words = spoken_words(script)
    return {"words": words, "movements": len(heads),
            "est_minutes": round(words / WORDS_PER_MINUTE, 1)}


def check_quotes(tdir: Path) -> dict:
    script, dossier = read(tdir / "script.md"), read(tdir / "dossier.md")
    missing = missing_quotes(script, dossier)
    if missing:
        raise GateError("not in the dossier verbatim:\n  " + "\n  ".join(missing))
    meta, body = split_frontmatter(script)
    return {"quotes": len(quoted_spans(body, meta.get("quote_speakers") or []))}


def check_register(tdir: Path) -> dict:
    return {"reviewed": len(register_findings(read(tdir / "script.md")))}


def check_second(tdir: Path) -> dict:
    text = read(tdir / "second-check.md")
    head = re.search(r"script sha256: ([0-9a-f]{64})", text)
    if not head or head.group(1) != sha256(tdir / "script.md"):
        raise GateError("second-check.md is of another revision of the script; re-run the check")
    rows = re.findall(r"(?m)^\| \d+ \|.*\|$", text)
    open_rows = [r for r in rows if not r.rstrip("|").rsplit("|", 1)[1].strip()]
    if open_rows:
        raise GateError(f"{len(open_rows)} flag(s) without a disposition")
    return {"flags": len(rows)}


def check_rendered(tdir: Path, output: str | None, commit: str | None) -> dict:
    if not output or not commit:
        raise GateError("rendered needs --output and --t2v-commit")
    return {"output": output, "t2v_commit": commit}


CHECKS = {"gathered": check_gathered, "ruled": check_ruled, "written": check_written,
          "quotes": check_quotes, "register": check_register, "second_check": check_second,
          "sam": lambda tdir: {}}


def stamp(tdir: Path, gate: Gate, output: str | None = None, commit: str | None = None) -> dict:
    measures = check_rendered(tdir, output, commit) if gate == "rendered" else CHECKS[gate](tdir)
    return record(tdir, gate, measures)


# --------------------------------------------------------------------------- cli
MARK = {"pass": "ok", "stale": "STALE", "missing": "-"}


def cmd_status(_args) -> int:
    print(f"{'topic':<5} {'folds':<16} " + " ".join(f"{g[:8]:<8}" for g in GATES))
    for t in load_topics():
        if t.kind in ("work", "sam"):
            continue
        hits = sorted(V2.glob(f"{t.code}-*"))
        cells = [MARK[gate_state(hits[0], g)] if hits else "-" for g in GATES]
        folds = ",".join(f"{n:02d}" for n in t.folds)
        print(f"{t.code:<5} {folds:<16} " + " ".join(f"{c:<8}" for c in cells))
    return 0


def cmd_recut(_args) -> int:
    topics = load_topics()
    problems = recut_problems(topics)
    for p in problems:
        print("  !", p)
    kinds = collections.Counter(t.kind for t in topics)
    films = collections.Counter()
    for t in topics:
        films[t.kind] += len(t.folds)
    print(f"{len(topics)} rows; " + "; ".join(f"{k}: {kinds[k]} rows / {films[k]} films"
                                              for k in KINDS))
    return 1 if problems else 0


def cmd_lint(args) -> int:
    for line, name, text in register_findings(read(topic_dir(args.topic) / "script.md")):
        print(f"  {line:>4}  {name:<20} {text[:110]}")
    return 0


def cmd_quotes(args) -> int:
    print(stamp(topic_dir(args.topic), "quotes"))
    return 0


def cmd_stamp(args) -> int:
    print(stamp(topic_dir(args.topic), args.gate, args.output, args.t2v_commit))
    return 0


def cmd_audit(_args) -> int:
    from slate_v2_audit import audit  # the set-level gate; imported here to avoid a cycle
    scripts = {p.parent.name.split("-")[0]: read(p) for p in sorted(V2.glob("*/script.md"))}
    print(json.dumps(audit(scripts), indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("recut").set_defaults(fn=cmd_recut)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    sub.add_parser("audit").set_defaults(fn=cmd_audit)
    for name, fn in (("lint", cmd_lint), ("quotes", cmd_quotes)):
        p = sub.add_parser(name)
        p.add_argument("topic")
        p.set_defaults(fn=fn)
    p = sub.add_parser("stamp")
    p.add_argument("topic")
    p.add_argument("gate", choices=GATES)
    p.add_argument("--output")
    p.add_argument("--t2v-commit", dest="t2v_commit")
    p.set_defaults(fn=cmd_stamp)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except GateError as e:
        print(f"gate refused: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
