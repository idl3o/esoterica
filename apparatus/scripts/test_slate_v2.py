"""Tests for slate_v2.py and slate_v2_check.py.  Run:  python -m pytest apparatus/scripts"""
from __future__ import annotations

import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import slate_v2 as sv  # noqa: E402
import slate_v2_audit as au  # noqa: E402
import slate_v2_check as ck  # noqa: E402

DOSSIER = """---
topic: X1
---
# Dossier

## 1. Scope
s
## 2. The corpus on this topic
c
## 3. Primary sources
[P1] Brodeur (1916):

> Then said Frigg: "Neither weapons nor trees may hurt Baldr: I have taken
> oaths of them all." Then the woman asked: "Have all things taken oaths
> to spare Baldr?"

## 4. The standard account
[S1] Lindow argues the killing is a family feud before it is a cosmic event.
## 5. Claims ledger
| ID | claim | where | ruler | proposed verdict | note | ruling |
|---|---|---|---|---|---|---|
| C1 | Frigg took oaths of all things | a.md:3 | P1 | stands | | stands |
| C2 | Hodr was jealous | a.md:9 | P1 | correct → no motive is given | | correct → no motive is given |
## 6. The strongest objection
o
## 7. Negative space
n
## 8. What the sources show
w
## 9. Sources
z
"""

SCRIPT = """---
title: The Death of Baldr
quote_speakers: [SOURCE]
speakers:
  SOURCE: bf_emma
---
# The Death of Baldr

## The Oath

Frigg went through the world. In Brodeur's translation she says "neither weapons nor trees may hurt Baldr".

SOURCE. Have all things taken oaths to spare Baldr?

## What Is Declined

The film declines the dying god.
"""


@pytest.fixture
def topic(tmp_path: Path) -> Path:
    d = tmp_path / "N4-the-death-of-baldr"
    d.mkdir()
    (d / "dossier.md").write_text(DOSSIER, encoding="utf-8")
    (d / "script.md").write_text(SCRIPT, encoding="utf-8")
    return d


# --------------------------------------------------------------------------- re-cut
def test_real_topics_cover_every_v1_film_once():
    assert sv.recut_problems(sv.load_topics()) == []


def test_recut_reports_missing_and_doubled_films():
    rows = "| N1 | A | 01, 02 | exposition | r | |\n| N2 | B | 02 | work | | |\n"
    problems = sv.recut_problems(sv.parse_topics(rows))
    assert "film 02 folded 2 times" in problems
    assert "film 03 missing" in problems


def test_parse_topics_reads_light_and_hand():
    t, = sv.parse_topics("| T8 | Jainism | 110 | exposition (light) | r | Sam |")
    assert (t.folds, t.kind, t.light, t.sam_hand) == ((110,), "exposition", True, True)


def test_parse_topics_rejects_unknown_kind():
    with pytest.raises(ValueError):
        sv.parse_topics("| X1 | t | 01 | essay | r | |")


# --------------------------------------------------------------------------- quotes
def test_quote_found_across_wrapped_blockquote_and_case(topic: Path):
    assert sv.missing_quotes(sv.read(topic / "script.md"), sv.read(topic / "dossier.md")) == []


def test_fabricated_quote_is_caught(topic: Path):
    bad = SCRIPT.replace("neither weapons nor trees may hurt Baldr",
                         "nothing in the nine worlds may hurt Baldr")
    assert sv.missing_quotes(bad, DOSSIER) == ["nothing in the nine worlds may hurt Baldr"]


def test_speaker_paragraph_is_a_quotation():
    bad = SCRIPT.replace("Have all things taken oaths to spare Baldr?",
                         "Has the mistletoe sworn too?")
    assert sv.missing_quotes(bad, DOSSIER) == ["Has the mistletoe sworn too?"]


def test_ellipsis_and_editorial_brackets_split_a_quote():
    assert sv.fragments("Then said Frigg … [the] trees may hurt Baldr.") == \
        ["then said frigg", "trees may hurt baldr"]


def test_verse_set_out_in_lines_matches_slash_notation():
    dossier = "> Thökk will weep / waterless tears / For Baldr's bale-fare;"
    script = "---\nquote_speakers: [SOURCE]\n---\n# t\n\n## a\n\nSOURCE. Thökk will weep\nwaterless tears\n"
    assert sv.missing_quotes(script, dossier) == []


def test_curly_and_straight_quotes_compare_equal():
    assert sv.norm("“Baldr’s” — death") == sv.norm('"Baldr\'s" - death')


def test_any_verbatim_span_of_the_dossier_passes():
    rng = random.Random(14)
    words = sv.norm(DOSSIER).split()
    for _ in range(200):
        i = rng.randrange(len(words) - 4)
        span = " ".join(words[i:i + rng.randint(2, 4)])
        if '"' in span or not span.strip(" .,;:!?'"):
            continue
        script = f"---\ntitle: t\n---\n# t\n\n## a\n\nShe wrote “{span}”.\n"
        assert sv.missing_quotes(script, DOSSIER) == [], span


# --------------------------------------------------------------------------- gates
def test_gate_goes_stale_when_a_checked_file_changes(topic: Path):
    sv.stamp(topic, "quotes")
    assert sv.gate_state(topic, "quotes") == "pass"
    (topic / "dossier.md").write_text(DOSSIER + "\nmore\n", encoding="utf-8")
    assert sv.gate_state(topic, "quotes") == "stale"
    assert sv.gate_state(topic, "sam") == "missing"


def test_written_requires_what_is_declined_last(topic: Path):
    (topic / "script.md").write_text(SCRIPT.replace("## What Is Declined", "## Coda"),
                                     encoding="utf-8")
    with pytest.raises(sv.GateError):
        sv.stamp(topic, "written")


def test_written_records_words_and_minutes(topic: Path):
    entry = sv.stamp(topic, "written")
    assert entry["movements"] == 2 and entry["words"] == sv.spoken_words(SCRIPT)


def test_ruled_tallies_verdicts_and_refuses_an_open_row(topic: Path):
    assert sv.stamp(topic, "ruled")["verdicts"] == {"stands": 1, "correct": 1}
    (topic / "dossier.md").write_text(DOSSIER.replace("| | stands |", "| | |"), encoding="utf-8")
    with pytest.raises(sv.GateError, match="C1"):
        sv.stamp(topic, "ruled")


def test_a_proposal_alone_does_not_pass_the_ruled_gate(topic: Path):
    unruled = DOSSIER.replace("| ruling |", "|").replace("|---|---|---|---|---|---|---|",
                                                          "|---|---|---|---|---|---|")
    unruled = unruled.replace("| | stands |", "| |").replace(
        "| | correct → no motive is given |", "| |")
    (topic / "dossier.md").write_text(unruled, encoding="utf-8")
    with pytest.raises(sv.GateError):
        sv.stamp(topic, "ruled")


def test_gathered_needs_all_nine_sections(topic: Path):
    (topic / "dossier.md").write_text(DOSSIER.replace("## 7. Negative space", "## Negative"),
                                      encoding="utf-8")
    with pytest.raises(sv.GateError, match=r"\[7\]"):
        sv.stamp(topic, "gathered")


def test_frontmatter_nested_map_and_inline_list():
    meta, body = sv.split_frontmatter(SCRIPT)
    assert meta["quote_speakers"] == ["SOURCE"]
    assert meta["speakers"] == {"SOURCE": "bf_emma"}
    assert body.startswith("# The Death of Baldr")


def test_register_lint_finds_the_house_copula():
    found = sv.register_findings("---\nt: x\n---\nThe fold IS the remainder.\nPlain line.\n")
    assert [(n, name) for n, name, _ in found] == [(1, "capitalised copula")]


# --------------------------------------------------------------------------- second check
def test_parse_flags_accepts_empty_and_rejects_malformed():
    assert ck.parse_flags('{"flags": []}') == []
    for raw in ("not json", '{"flags": [{"sentence": "s", "verdict": "wrong",'
                ' "reason": "r", "evidence": "e"}]}', '{"flags": [{"sentence": "s"}]}', "[]"):
        with pytest.raises(sv.GateError):
            ck.parse_flags(raw)


def test_ask_sends_no_schema_constraint_and_parses_a_fenced_reply(monkeypatch):
    sent = {}

    def fake_post(host, path, payload):
        sent.update(payload)
        return {"message": {"content": '```json\n{"flags": [{"sentence": "s.", "verdict": '
                                       '"overstated", "reason": "r", "evidence": "P1"}]}\n```'}}

    monkeypatch.setattr(ck, "_post", fake_post)
    flags = ck.ask(ck.Checker("h", "gpt-oss:20b", "medium", 8192), "M", "s.", "ev")
    assert "format" not in sent  # a grammar constraint emptied gpt-oss's reply on 14 Oct 2026
    assert flags == [ck.Flag("s.", "overstated", "r", "P1")]


def test_a_malformed_reply_is_re_asked_once_then_refused(monkeypatch):
    good = '{"flags": []}'
    replies = iter(['{"flags": [{"sentence": "a "b" c"}]}', good])
    sent = []
    monkeypatch.setattr(ck, "_post", lambda h, p, payload: (sent.append(payload),
                        {"message": {"content": next(replies)}})[1])
    c = ck.Checker("h", "gpt-oss:20b", "medium", 8192)
    assert ck.ask(c, "M", "s.", "ev") == []
    assert len(sent) == 2 and "could not be used" in sent[1]["messages"][-1]["content"]
    replies = iter(["not json", "still not json"])
    with pytest.raises(sv.GateError):
        ck.ask(c, "M", "s.", "ev")


def test_dispositions_carry_over_a_rerun(tmp_path: Path):
    flag = ck.Flag("Hodr was jealous.", "unsupported", "no motive | given", "P1")
    first = ck.report("t", "h", [("The Oath", [flag])], {})
    path = tmp_path / "second-check.md"
    path.write_text(first.replace("| P1 |  |", "| P1 | fixed |"), encoding="utf-8")
    carried = ck.previous_dispositions(path)
    assert carried == {sv.norm("Hodr was jealous."): "fixed"}
    assert "| P1 | fixed |" in ck.report("t", "h", [("The Oath", [flag])], carried)


def test_a_disposition_survives_a_run_that_does_not_flag_its_sentence(tmp_path: Path):
    out = tmp_path / "second-check.md"
    flag = ck.Flag("Hodr was jealous.", "unsupported", "r", "P1")
    out.write_text(ck.report("t", "h", [("M", [flag])], {}).replace("| P1 |  |", "| P1 | fixed |"),
                   encoding="utf-8")
    ck.carried_dispositions(tmp_path, out)                      # run 2 reads run 1's hand
    out.write_text(ck.report("t", "h", [("M", [])], {}), encoding="utf-8")  # run 2: no flag
    carried = ck.carried_dispositions(tmp_path, out)            # run 3 still has it
    assert carried[sv.norm("Hodr was jealous.")] == "fixed"


def test_evidence_selection_is_bounded_and_in_document_order():
    units = ck.evidence_paragraphs(DOSSIER)
    assert "Ruling C2: the corpus claims: Hodr was jealous (a.md:9). Verdict against P1: " \
           "correct → no motive is given." in units
    assert not any("Negative space" in u or "Scope" in u for u in units)
    picked = ck.select_evidence("Frigg oaths trees Baldr", units, budget=400)
    assert len(picked) <= 400 + 2 * len(units)
    assert picked == ck.select_evidence("Frigg oaths trees Baldr", units, budget=400)


def test_movements_split_on_level_two_headings():
    assert [h for h, _ in ck.movements(SCRIPT)] == ["The Oath", "What Is Declined"]


def test_movements_leave_out_quote_speaker_paragraphs():
    text = dict(ck.movements(SCRIPT))["The Oath"]
    assert "Frigg went through the world." in text
    assert "SOURCE." not in text and "Have all things taken oaths" not in text


# --------------------------------------------------------------------------- audit
def test_audit_finds_a_phrase_shared_by_three_scripts_but_not_inside_quotes():
    tic = "and the dark was never empty at all"
    quoted = '"the light that never reaches the cave floor"'
    scripts = {c: f"---\nt: x\n---\n# T\n\n## M\n\nOpening line {c}. {tic}. {quoted}\n"
               for c in ("A1", "A2", "A3")}
    found = au.audit(scripts)["shared_phrases"]
    assert any("and the dark was never empty at all" in k for k in found)
    assert not any("cave floor" in k for k in found)
    assert au.audit({k: scripts[k] for k in ("A1", "A2")})["shared_phrases"] == {}
