#!/usr/bin/env python3
"""
SLATE_V2_CHECK — the second check: a different model family reads a v2 script against its dossier.

    python slate_v2_check.py TOPIC [--model gpt-oss:20b] [--think medium] [--num-ctx 32768]
                                   [--budget 40000] [--host http://localhost:11434]

For each movement of script.md, the dossier's evidence (sections 2-6) is ranked by the content
words each paragraph shares with the movement, and the best fit up to --budget characters goes to
the model with the movement. The model returns only the sentences the evidence does not carry:
unsupported, contradicted, or overstated (a hedge dropped, a regime left out, a rounder number).
Its reply is parsed strictly; a reply that does not parse is an error, never an empty pass.

Writes second-check.md beside the script. A disposition already written for a sentence carries
over when the check is re-run, so fixing the script and checking again keeps the hand's work.
Then stamp the gate:  python slate_v2.py stamp TOPIC second_check

Local by design: the checker is a different family from the writer, and nothing leaves the machine.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, get_args

from slate_v2 import (GateError, norm, paragraphs, read, sha256, split_frontmatter,
                      topic_dir, write_atomic)

Verdict = Literal["unsupported", "contradicted", "overstated"]
VERDICTS: tuple[Verdict, ...] = get_args(Verdict)
SEED = 7

SYSTEM = (
    "You check one movement of a documentary script against an evidence file of sourced "
    "excerpts and rulings. You are not the author's ally. Report each sentence of the MOVEMENT "
    "that makes a checkable claim (a fact, date, number, attribution, quotation, or a textual "
    "or scientific statement) and that the EVIDENCE does not support, contradicts, or states "
    "more strongly than the evidence does (a hedge dropped, a regime or boundary condition left "
    "out, a rounder number, one source's view given as settled). Interpretation that is "
    "labelled as interpretation is not a claim; neither is a question, nor a sentence about "
    "what this film itself does, shows or declines. A 'Ruling' line reports a claim the corpus "
    "made and the verdict on it: the claim is evidence only as far as its verdict allows. "
    "Before flagging a sentence, look in the EVIDENCE for its names, dates and key terms: a "
    "sentence that restates or paraphrases what an excerpt says is supported, even if the words "
    "differ. Flag only what you cannot find support for after looking. "
    "Copy each sentence "
    "exactly. In 'evidence' give the excerpt ID or a short quotation from the EVIDENCE that "
    "bears on it, or 'none found'. If every claim is carried, return an empty list.\n"
    'Reply with one JSON object and nothing else: {"flags": [{"sentence": "...", '
    '"verdict": "unsupported|contradicted|overstated", "reason": "...", "evidence": "..."}]}'
)
# Ollama's schema-constrained `format` is not used. In the 14 Oct 2026 smoke test gpt-oss's
# reasoning found both planted errors and the constrained reply was {"flags": []}: the grammar
# discarded what the thinking concluded. The shape is asked for in the prompt and parse_flags
# is the boundary, so a malformed reply fails loudly instead of passing as clean.


@dataclass(frozen=True, slots=True)
class Flag:
    sentence: str
    verdict: Verdict
    reason: str
    evidence: str


@dataclass(frozen=True, slots=True)
class Checker:
    host: str
    model: str
    think: bool | str
    num_ctx: int


# --------------------------------------------------------------------------- inputs
def movements(script: str) -> list[tuple[str, str]]:
    """(heading, text) for each '## ' movement, without its quote-speaker paragraphs.

    Those paragraphs are verbatim excerpts the quotes gate has already matched against the
    dossier mechanically; sent to the checker, they only drew flags on the sources' own words.
    """
    meta, body = split_frontmatter(script)
    tags = tuple(f"{t}. " for t in meta.get("quote_speakers") or [])
    parts = re.split(r"(?m)^## (.+)$", body)
    out = []
    for i in range(1, len(parts) - 1, 2):
        kept = [p for p in paragraphs(parts[i + 1]) if not (tags and p.startswith(tags))]
        out.append((parts[i].strip(), "\n\n".join(kept)))
    return out


def evidence_paragraphs(dossier: str) -> list[str]:
    """Sections 2-6 of the dossier as rankable units; a table becomes one unit per row.

    Section 2, the corpus survey, is the ruler for what a script says the earlier films and
    essays claimed; without it the A/B of 14 Oct flagged every such sentence as unsupported.
    """
    units = []
    for num, text in re.findall(r"(?ms)^## ([2-6])\.(.*?)(?=^## \d\.|\Z)", dossier):
        for block in paragraphs(text):
            lines = block.splitlines()
            prose = [ln for ln in lines if not ln.lstrip().startswith("|")]
            if prose:
                units.append("\n".join(prose))
            rows = [ln for ln in lines if ln.lstrip().startswith("|")
                    and not set(ln) <= set("|-: ") and not re.match(r"^\|\s*ID\s*\|", ln)]
            units += [_ruling(r) if num == "5" else r for r in rows]
    return units


def _ruling(row: str) -> str:
    """A claims-ledger row as a sentence, so the claim column is not read as evidence for itself."""
    c = [x.strip() for x in row.strip().strip("|").split("|")]
    if len(c) < 5:
        return row
    note = f" Note: {c[5]}" if len(c) > 5 and c[5] else ""
    return (f"Ruling {c[0]}: the corpus claims: {c[1]} ({c[2]}). "
            f"Verdict against {c[3]}: {c[4]}.{note}")


STOP = set("that this with from have were been their there which about would could should "
           "into than then them they what when where while also only more most such these "
           "those very will your over upon each other being does said says".split())


def _content(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-zà-ž]{4,}", norm(text)) if w not in STOP}


def select_evidence(movement: str, units: list[str], budget: int) -> str:
    """The units sharing most content words with the movement, up to budget chars, in order."""
    want = _content(movement)
    scored = sorted(range(len(units)), key=lambda i: -len(want & _content(units[i]))
                    / math.sqrt(len(units[i].split()) + 1))
    keep, used = set(), 0
    for i in scored:
        if used + len(units[i]) > budget:
            continue
        keep.add(i)
        used += len(units[i])
    return "\n\n".join(units[i] for i in sorted(keep))


# --------------------------------------------------------------------------- model
def _post(host: str, path: str, payload: dict | None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(host + path, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        return json.loads(r.read().decode("utf-8"))


def model_digest(c: Checker) -> str:
    for m in _post(c.host, "/api/tags", None)["models"]:
        if m["name"] == c.model:
            return m["digest"][:12]
    raise GateError(f"model {c.model} is not pulled on {c.host}")


def parse_flags(raw: str) -> list[Flag]:
    """The trust boundary: the model's reply becomes Flags or a GateError, nothing between."""
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        raise GateError(f"checker reply is not JSON: {e}") from e
    items = obj.get("flags") if isinstance(obj, dict) else None
    if not isinstance(items, list):
        raise GateError("checker reply has no 'flags' list")
    flags = []
    for it in items:
        fields = {k: it.get(k) if isinstance(it, dict) else None
                  for k in ("sentence", "verdict", "reason", "evidence")}
        if not all(isinstance(v, str) and v.strip() for v in fields.values()):
            raise GateError(f"malformed flag: {it!r}")
        if fields["verdict"] not in VERDICTS:
            raise GateError(f"unknown verdict {fields['verdict']!r}")
        flags.append(Flag(**{k: v.strip() for k, v in fields.items()}))
    return flags


def ask(c: Checker, heading: str, text: str, evidence: str) -> list[Flag]:
    """One movement's flags. A reply that does not parse is sent back once with its error
    (H7, 14 Oct: an unescaped quotation mark broke the JSON); a second failure raises."""
    user = f"EVIDENCE:\n{evidence}\n\n----------\n\nMOVEMENT: {heading}\n\n{text}"
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
    raw = _chat(c, messages)
    try:
        return parse_flags(raw)
    except GateError as e:
        messages += [{"role": "assistant", "content": raw},
                     {"role": "user", "content": f"That reply could not be used ({e}). Return the "
                      "same flags as one valid JSON object and nothing else; escape any double "
                      "quotation marks inside strings."}]
        return parse_flags(_chat(c, messages))


def _chat(c: Checker, messages: list[dict]) -> str:
    reply = _post(c.host, "/api/chat", {
        "model": c.model, "stream": False, "think": c.think, "messages": messages,
        "options": {"temperature": 0, "seed": SEED, "num_ctx": c.num_ctx},
    })
    return reply["message"]["content"]


# --------------------------------------------------------------------------- report
def _cell(s: str) -> str:
    return re.sub(r"\s+", " ", s).replace("|", "\\|").strip()


def previous_dispositions(path: Path) -> dict[str, str]:
    """{normalised sentence: disposition} from an earlier second-check.md."""
    if not path.is_file():
        return {}
    out = {}
    for row in re.findall(r"(?m)^\| \d+ \|(.*)\|$", read(path)):
        cells = re.split(r"(?<!\\)\|", row)
        if len(cells) >= 5 and cells[-1].strip():
            out[norm(cells[0].replace("\\|", "|"))] = cells[-1].strip()
    return out


def report(title: str, header: str, results: list[tuple[str, list[Flag]]],
           carried: dict[str, str]) -> str:
    lines = [f"# Second check — {title}", "", header, "",
             "Each flag needs a disposition: **fixed** (the script changed), **stands** (with the "
             "reason), or **dossier** (the evidence was missing and the dossier now carries it).", ""]
    n = 0
    for heading, flags in results:
        lines += [f"## {heading}", ""]
        if not flags:
            lines += ["No flags.", ""]
            continue
        lines += ["| # | sentence | verdict | reason | evidence | disposition |",
                  "|---|---|---|---|---|---|"]
        for f in flags:
            n += 1
            disp = carried.get(norm(f.sentence), "")
            lines.append(f"| {n} | {_cell(f.sentence)} | {f.verdict} | {_cell(f.reason)} | "
                         f"{_cell(f.evidence)} | {_cell(disp)} |")
        lines.append("")
    return "\n".join(lines)


def run(tdir: Path, c: Checker, budget: int, log=print) -> Path:
    script, dossier = read(tdir / "script.md"), read(tdir / "dossier.md")
    meta, _ = split_frontmatter(script)
    units = evidence_paragraphs(dossier)
    if not units:
        raise GateError("dossier sections 2-6 are empty")
    results = []
    for heading, text in movements(script):
        log(f"  checking '{heading}' ...")
        results.append((heading, ask(c, heading, text, select_evidence(text, units, budget))))
    header = (f"model: {c.model} (digest {model_digest(c)}) · think: {c.think} · seed {SEED} · "
              f"num_ctx {c.num_ctx} · evidence budget {budget} chars\n"
              f"date: {dt.date.today().isoformat()} · script sha256: {sha256(tdir / 'script.md')}"
              f" · dossier sha256: {sha256(tdir / 'dossier.md')}")
    out = tdir / "second-check.md"
    carried = carried_dispositions(tdir, out)
    text = report(meta.get("title") or tdir.name, header, results, carried)
    write_atomic(out, text + "\n")
    return out


ARCHIVE = "dispositions.json"


def carried_dispositions(tdir: Path, out: Path) -> dict[str, str]:
    """Every disposition the hand has written for this topic, across all runs.

    A run that does not flag a sentence used to drop its disposition, so the next run that
    flagged it again asked for it twice (H7, 14 Oct). The archive keeps them; the newest wins.
    """
    path = tdir / ARCHIVE
    archive = json.loads(read(path)) if path.is_file() else {}
    archive.update(previous_dispositions(out))
    write_atomic(path, json.dumps(archive, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
    return archive


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("topic")
    ap.add_argument("--model", default="gpt-oss:20b")
    ap.add_argument("--think", default="medium", help="low|medium|high for gpt-oss; true|false")
    ap.add_argument("--num-ctx", type=int, default=32768)
    ap.add_argument("--budget", type=int, default=40000, help="evidence characters per movement")
    ap.add_argument("--host", default="http://localhost:11434")
    a = ap.parse_args(argv)
    think = {"true": True, "false": False}.get(a.think, a.think)
    try:
        out = run(topic_dir(a.topic), Checker(a.host, a.model, think, a.num_ctx), a.budget)
    except GateError as e:
        print(f"check refused: {e}", file=sys.stderr)
        return 2
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
