"""Tests for copyright_sweep.py.  Run:  python -m pytest apparatus/scripts/test_copyright_sweep.py"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import copyright_sweep as cs  # noqa: E402

FORTY = " ".join(["word"] * 40)


def test_quoted_span_does_not_bridge_two_quotations(tmp_path: Path):
    """The first version matched from one closing quote to the next opening quote
    and called 63 percent of the corpus verbatim. Two short quotations with a long
    unquoted stretch between them must count as zero long spans."""
    gap = " ".join(["plain"] * 200)
    (tmp_path / "a.md").write_text(f'She said "yes". {gap} He said "no".\n', encoding="utf-8")
    r = cs.scan(tmp_path / "a.md")
    assert r["long_spans"] == 0 and r["long_span_words"] == 0


def test_quoted_span_counts_one_long_quotation_straight_or_curly(tmp_path: Path):
    (tmp_path / "a.md").write_text(f'A: "{FORTY}"\n\nB: “{FORTY}”\n', encoding="utf-8")
    r = cs.scan(tmp_path / "a.md")
    assert r["long_spans"] == 2 and r["long_span_words"] == 80


def test_attribution_needs_a_dash_not_a_bullet(tmp_path: Path):
    (tmp_path / "a.md").write_text(
        "- Close eyes\n- Trust the process\n— Meister Eckhart, *Sermons*\n*— T. S. Eliot, Little Gidding*\n",
        encoding="utf-8",
    )
    r = cs.scan(tmp_path / "a.md")
    assert [a[0] for a in r["attributions"]] == ["Meister Eckhart", "T. S. Eliot"]


def test_blockquote_runs_split_on_a_plain_line(tmp_path: Path):
    (tmp_path / "a.md").write_text("> one two three\n> four five\n\nplain\n\n> six\n", encoding="utf-8")
    r = cs.scan(tmp_path / "a.md")
    assert r["blockquote_words"] == 6 and r["longest_run"] == 5 and r["runs_over_150"] == 0
