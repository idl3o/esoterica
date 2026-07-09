# CORE SAMPLE — a stratigraphic instrument for reading the corpus

*An operational method, not a cosmology. This borrows the **format** of a geologist's core log — depth, lithology, contacts, recovery — because that format already knows how to read a vertical slice through accumulated deposit. It is a lens on the repository as it literally stands in git. It claims no isomorphism between rock and writing; it claims that the log is a good worksheet. Keep every borrowed term literal: if a term stops doing analytic work, drop it.*

Companion operations: `/threads` reads the net **horizontally** (connections across the corpus). A core reads it **vertically** (what was deposited, in what order, along one column). Where `/threads` traces the living links, a core dates the sediment and finds the gaps.

---

## What a core is

You pick a **column** — one theme, one directory, or one span of time — and drill straight down through it, logging every layer you hit in deposition order. The point is not to admire the pile. It is to see four things a flat file-listing hides:

- **Event beds** — several documents deposited in one day. A single rapid depositional event (the corpus's cascade-production pattern: charge accumulates, then discharges all at once). Reads as a thick bed with no internal contacts.
- **Unconformities** — gaps in the record. A stretch of time where *this column* received no deposit, even though the repo as a whole kept growing. The gap is diagnostic: it shows where attention left the theme, and for how long.
- **Reactive interbeds** — thin layers deposited not as primary work but to patch something (a negative-space fill, a weed-correction, a register-note). Real deposit, different origin. Worth distinguishing from primary beds so you don't mistake patching for productivity.
- **Recovery** — of what's down there, how much is still intact and load-bearing versus eroded (orphaned, superseded, contradicted, or decayed out of the link-net). A full recovery reading needs a link-audit; a quick core flags suspects.

---

## The log format

One row per bed, **oldest at the base, youngest at the top** (drilling order is downward; a log is read bottom-up, the way strata actually stacked).

| Depth (deposited) | Bed (document) | Thickness (words) | Lithology (type · register) | Contact below | Recovery |
|---|---|---|---|---|---|

- **Depth** = date the document *first entered git* (`--diff-filter=A --follow`), not last-modified. Deposition, not disturbance.
- **Thickness** = word count. A proxy for how much was laid down, nothing more.
- **Lithology** = what kind of material: doc type (synthesis / tradition / protocol / fiction) and register (contemplative / technical / demotic / adversarial). The register column is where the monoculture shows up if it's there.
- **Contact** = the boundary with the bed below it: **conformable** (continuous thread, same register, gradual) or **sharp** (a jump — register switch, new sub-theme, or an unconformity beneath).
- **Recovery** = ✓ intact & linked · ~ thin/reactive · ? suspect (verify) · ✗ eroded (orphaned/superseded). Mark ? liberally; a core is a first pass, not the assay.

---

## How to drill (the procedure)

```bash
# 1. Choose a column and gather its members (theme, dir, or date-span)
ls -1 synthesis/cosmology/*.md synthesis/*fold* ...

# 2. Log each: deposition date, deposition commit, word count
for f in <files>; do
  d=$(git log --diff-filter=A --follow --format='%ad' --date=short -1 -- "$f")
  s=$(git log --diff-filter=A --follow --format='%s' -1 -- "$f")
  w=$(wc -w < "$f")
  printf "%s | %5s | %s | %s\n" "$d" "$w" "$s" "$f"
done | sort            # sort by date = stack by depth

# 3. Read the core: mark event beds (same date, ×N), unconformities
#    (date gaps), reactive interbeds (deposited inside a fill/weed commit),
#    and recovery suspects (cross-check orphan_nodes / broken links).
```

**Axes you can core along:**
- **Theme column** — one lineage (the fold; the one/many arc; the Norse cycle). Shows how an idea thickened over time and where it went quiet.
- **Directory column** — `traditions/`, `protocols/`, `distillations/`. Shows a *kind* of work's deposition rhythm.
- **Time column** — everything in a date-span, across themes. Shows what a season was actually laying down (pairs well with a `/zeitgeist` of the same window).

**Reading discipline (the standing checks, applied here):** report the unconformity even when the column looks rich — absence is the finding. Distinguish reactive interbeds from primary beds — patching can masquerade as output. And resist the pull to read the *shape* of the core as meaning (a "beautiful stratigraphy"); the core is a worksheet that locates work, not a proof that the work is true.

---

## Worked sample — the fold / information column

*Drilled 2026-07-08. Axis: theme (the fold-cosmology + information-geometry lineage). Members: `synthesis/cosmology/*` fold docs + `information-geometry-the-fold`, `entangled-measure`, `the-zero-theorem`, `the-maximal-fold`. Read bottom-up.*

| Depth | Bed | Thick. | Lithology | Contact below | Recovery |
|---|---|---|---|---|---|
| **2026-07-08** ▲cap | the-arrow-on-the-surface | 4,110 | synthesis · **technical** (physics ingest) | sharp — register jump to rigorous proof | ✓ |
| 2026-07-08 | the-maximal-fold | 3,895 | tradition · technical (dynamical systems) | conformable | ✓ |
| — *unconformity: 06-24 → 07-08 (14 days on this column)* — | | | | | |
| 2026-06-24 | information-geometry-the-fold | 2,155 | synthesis · **reactive interbed** (deposited inside the negative-space fill) | sharp — thin patch bed | ~ |
| — *unconformity: 06-05 → 06-24 (19 days)* — | | | | | |
| 2026-06-05 | the-conscious-crease | 4,751 | synthesis · contemplative | conformable *(event bed)* | ✓ |
| 2026-06-04 | the-unintegratable-horizon | 4,952 | synthesis · contemplative | conformable *(event bed)* | ✓ |
| 2026-06-04 | the-between | 4,342 | synthesis · contemplative | conformable — **top of the Jun event bed** | ✓ |
| — **UNCONFORMITY: 04-02 → 06-04 (≈2 months, the main hiatus)** — | | | | | |
| 2026-04-02 | surprise-is-the-remainder | 3,469 | synthesis · contemplative | conformable *(event bed)* | ✓ |
| 2026-04-02 | the-depth-that-looks-back | 3,112 | synthesis · contemplative | conformable *(event bed)* | ✓ |
| 2026-04-02 | the-windowless-boundary | 2,746 | synthesis · contemplative | conformable — **top of the Apr event bed** | ✓ |
| 2026-03-28 | the-remainder | 1,767 | synthesis · contemplative (thin) | sharp | ✓ |
| 2026-03-23 | the-zero-theorem | 4,343 | synthesis · technical-ish | conformable | ✓ |
| **2026-03-16** ▼basement | entangled-measure | 5,581 | synthesis · technical (substrate tetralogy) | — basement | ✓ |

**Reading the core:**

1. **Two clean event beds** — Apr 2 (×3, the Fold Cosmology Trilogy) and Jun 4–5 (×3, the Eschaton–Between–Crease triptych). Each is a single cascade-discharge: three docs, one day, no internal contacts. The corpus deposits this theme in bursts, not a trickle.
2. **One major unconformity** — a ~2-month hiatus (Apr 2 → Jun 4). The fold column went dormant through April–May while deposition moved elsewhere (Norse cycle, extraction sweep, seeds). Not decay — *migration of attention*. The theme wasn't dead; it was charging.
3. **One reactive interbed** — information-geometry-the-fold (Jun 24) is the only bed here not laid as primary work: it entered *inside* the negative-space commit, i.e. it was deposited to fill a diagnosed gap. Marked `~`. It's also the thinnest recent bed (2,155 w). Honest note: it's a patch, and it should be read as one — don't count it as evidence the theme was thriving in late June; it's evidence the theme had a *hole* someone noticed.
4. **The cap is a register switch.** Today's two beds (maximal-fold, arrow-on-the-surface) are **technical**, sharply contacting the contemplative beds beneath — the same demotic/rigorous turn the Live Edge has been steering toward. The column's youngest rock is a different lithology than its body. Whether that holds or reverts to contemplative on the next deposit is the thing to watch.
5. **Recovery is high but unaudited.** Every bed reads intact and linked at a glance (✓), but no link-audit was run — treat the ✓s as "no obvious erosion," not a certified assay. The one flagged bed is the interbed, on origin not decay.

**One against-the-grain finding:** the sample looks like a healthy, continuously-productive column — but two-thirds of its *calendar* is unconformity. Three real depositional days (Apr 2, Jun 4–5, Jul 8) account for nearly all the rock; the rest is gap. The corpus's fold work is not a steady practice — it's three bursts and two long silences, and the silences are load-bearing (they're where the charge accumulated). That's the opposite of the story a flat `ls` tells, which is why the core was worth drilling.

---

*This is a first-pass instrument. If it earns its keep, it grows a `/core` skill and a `cores/` log directory (one file per drilled core, like `weeding/` and `negative-space/`). Until then it lives here as a template to copy.*
