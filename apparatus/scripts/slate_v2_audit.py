#!/usr/bin/env python3
"""
SLATE_V2_AUDIT — the set-level gate: what no single script's check can see.

    python slate_v2.py audit

Over every written v2 script: movement openers that share their first three words, phrases
of six or more words that recur in three or more scripts (quotations excluded, since a shared
source is not a tic), and the spread of estimated runtimes. A finding goes back to the
writing hand, not into a prompt (corpus/film-slate/v2/README.md, "Set-level gates").
"""
from __future__ import annotations

import collections
import re
import statistics

from slate_v2 import WORDS_PER_MINUTE, paragraphs, split_frontmatter, spoken_words

def _first_sentences(body: str) -> list[str]:
    out = []
    for block in re.split(r"(?m)^## .+$", body)[1:]:
        paras = [p for p in paragraphs(block) if not re.match(r"^[A-Z][A-Z'\-]{2,}\.\s", p)]
        if paras:
            out.append(re.split(r"(?<=[.!?])\s", paras[0])[0])
    return out


def _own_words(body: str) -> list[str]:
    """The writer's words: quotations and quote-speaker paragraphs removed."""
    body = re.sub(r"(?m)^[A-Z][A-Z'\-]{2,}\.\s.*$", " ", body)
    body = re.sub(r"“[^”]*”|\"[^\"\n]*\"", " ", body)
    return re.findall(r"[a-z']+", body.lower())


def shared_phrases(words: dict[str, list[str]], n: int = 6, min_scripts: int = 3) -> dict:
    """Maximal word runs that recur in at least `min_scripts` scripts, built from shared n-grams."""
    seen = collections.defaultdict(set)
    for code, ws in words.items():
        for i in range(len(ws) - n + 1):
            seen[tuple(ws[i:i + n])].add(code)
    joined = {code: " " + " ".join(ws) + " " for code, ws in words.items()}
    runs: dict[str, list[str]] = {}
    for ws in words.values():
        i = 0
        while i <= len(ws) - n:
            if len(seen[tuple(ws[i:i + n])]) < min_scripts:
                i += 1
                continue
            j = i
            while j + 1 <= len(ws) - n and len(seen[tuple(ws[j + 1:j + 1 + n])]) >= min_scripts:
                j += 1
            run = " ".join(ws[i:j + n])
            holders = sorted(c for c, t in joined.items() if f" {run} " in t)
            if len(holders) >= min_scripts:
                runs[run] = holders
            i = j + 1
    return runs


def audit(scripts: dict[str, str], min_scripts: int = 3) -> dict:
    """Set-level findings over {code: script text}: shared openers, phrases, runtimes."""
    openers = collections.defaultdict(set)
    words, minutes = {}, {}
    for code, text in scripts.items():
        _, body = split_frontmatter(text)
        for s in _first_sentences(body):
            openers[" ".join(s.lower().split()[:3])].add(code)
        words[code] = _own_words(body)
        minutes[code] = round(spoken_words(text) / WORDS_PER_MINUTE, 1)
    spread = sorted(minutes.values())
    return {
        "shared_openers": {k: sorted(v) for k, v in openers.items() if len(v) > 1},
        "shared_phrases": shared_phrases(words, min_scripts=min_scripts),
        "minutes": minutes,
        "spread": (spread[0], statistics.median(spread), spread[-1]) if spread else (),
    }
