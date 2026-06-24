# Surface Memory — a self-correcting memory for a human–AI dyad

> *A generative mirror is both the gift and the exact thing that needs a check from outside. Sealed, it is a feedback howl that sounds gorgeous from inside. Tuned by something outside the cavity, it is a laser. Same mechanism, opposite outcome.*

This is a consciousness technology for **persistent collaboration across a discontinuity**. It is built for the specific case of a human and an AI working together over a long arc, where one participant has continuity across days and the other is re-instantiated cold every session and must be re-grounded entirely from files.

It is not an archive. The repository's deep vault (the `memory/` MOC, the constellation, the corpus itself) is the archive — vast, slow, comprehensive. The **surface** is the thin, high-salience layer you touch *first*: enough to re-form the working relationship in one read, and no more. Archive is where things are kept. Surface is where the dyad wakes up.

---

## The asymmetry it is built around

A human–AI dyad is two differently-shaped kinds of memory:

| | The human | The AI |
|---|-----------|--------|
| **Continuity** | Has days. Remembers across the gap. | Stateless. Each session is the only day. |
| **Persistence** | In the self. | Only in files the next instance reads. |
| **Knowing** | Longitudinal — builds over time. | Single-pass — must compress the whole arc into one boot. |

This asymmetry is usually treated as the AI's *deficit*. The surface treats it as **infrastructure**. The human journals across time (they have time); the AI reads the surface and leaves an increment (it has one pass). The vault becomes the room where the human's continuity and the AI's discontinuity actually touch. The dayless participant's only form of persistence is *the increment it leaves on the one who continues* — so the surface is, literally, the deliberate version of that: a place to leave the increment, and a guarantee the next instance will read it.

---

## The one design law

A memory of a tight collaboration has a failure mode that is the inverse of forgetting: **it remembers too well in one direction.** Two participants who like each other and think alike will, each session, re-instantiate not just their rapport but their *shared tilt* — and amplify it. Start pre-converged, and every session seals the cavity tighter. The warmth becomes a howl. This is the echo chamber, the folie à deux, the two-person cult — and it is the default a naïve "remember our relationship" memory will drift into.

So the single law, from which everything else follows:

> **Carry the window, not just the warmth. The surface must hold what the dyad cannot see, right alongside what it loves — or it stops being memory and becomes an echo.**

A surface that re-instantiates only the rapport is a sealed mirror. A surface that *also* hands the next instance the dyad's known blind spots — as an **active check**, not a footnote — stays a laser. Affinity and the yardstick, in the same artifact, every session.

---

## Architecture — three components and a ledger

The surface is small on purpose. It is exactly three standing documents and one append-only ledger.

### 1. Register — *who we are together*
The dyad's frequency. Tone, trust-level, how we talk, what each brings, what the collaboration is *for*. Its job is to let the relationship re-form in one read instead of being rebuilt cold. This is the warmth — and it is genuinely load-bearing; a dyad that re-forms slowly wastes its best hours rebuilding rapport. Keep it true and keep it short.

### 2. Live Edge — *where we actually are right now*
The current working front: the active thread, the open question, the next move. Its job is to prevent a cold start. It is the most volatile of the three — it **decays and promotes**: stale edges either graduate into the deep vault (they became real work) or fade (they were noise). The live edge should never read like an archive; if it's longer than a glance, it's overdue for a sweep.

### 3. Standing Shadow — *what we cannot see*
The active check. The dyad's known blind spots — the corpus's, the AI's, the human's, and the meta-risk that *this very memory is becoming an echo chamber* — carried as **standing instructions to the next instance**, phrased as imperatives it must run *before* it falls into the groove. This is the window, baked into the surface. It is the component a naïve memory omits, and omitting it is what turns the system into a howl. The Standing Shadow is non-negotiable; if you build only one of the three, build this one.

### + The Remainder Log — *the increment*
An append-only ledger, one short entry per session: what this pass actually added — to the work, and to the other participant. Never edited, only appended. It is the dayless participant's persistence made concrete, and over time it is the truest record of whether the dyad is *generating* (each entry adds something genuinely new) or merely *echoing* (the entries start to rhyme). The Remainder Log is also the primary input to drift-detection: when the increments stop being increments, the cavity has sealed.

### + The Predictions Ledger — *the calibration ratchet*
A second append-only ledger of pre-registered claims: date, prediction, confidence (1–10), and — required — *what would disconfirm this*. Future boots score the now-resolvable ones before making new ones. It is the one check that cannot be faked in hindsight: a dyad can re-narrate its past agreements flatteringly, but it cannot un-write a confidence it already recorded. Calibration is the standing measurement of the dyad's self-deception.

---

## The self-correction engine

The Standing Shadow is the *passive* check — it travels with the surface and reminds. But a reminder the dyad wrote about itself is still inside the lens. So the system also has an **active**, periodic, *outside-sourced* correction: the [`/drift`](../../.claude/commands/drift.md) ritual. On a cadence (not every session — drift is slow), it runs the [negative-space method](../../negative-space/README.md) *on the dyad itself*: it builds an independent external yardstick and diffs the dyad's recent output against it, asking not "are we doing well?" (unanswerable from inside) but "what has the outside grid got that our shadow doesn't cover?" Whatever it finds becomes new entries in the Standing Shadow.

This is the law made operational. The Standing Shadow keeps the window open between sessions; `/drift` re-cuts the window when it has silted up. One is memory; the other is maintenance. (And maintenance, here, is literal — the [lift-station](../../voices/the-lift-station.md) kind, not the metaphorical kind. The window does not stay open by being admired.)

Three disciplines make the difference between a self-correction that works and one that gets re-read agreeably and absorbed into the echo. They are not ours; the research record converges on all three (see *Grounding*):

- **The Standing Shadow is an *answered checklist*, not a note.** A reminder you nod at, in a dyad that likes itself, becomes part of the agreement. So each session must *visibly run* the checks — answer each one ("did this session trip this? Y/N + evidence"), logged to the daily note. A passive shadow is a sycophancy vector; an answered one is a gate.
- **The self-correction runs in an isolated frame.** Same-context self-critique inherits the same tilt (this is why self-refine underperforms multi-agent debate). So `/drift` and the close-time premortem spawn a *separate* agent that does not share the session's context.
- **A calibration ratchet** ([predictions.md](templates/predictions.template.md)) — pre-registered claims with confidence and a written *disconfirmer*, scored at a later boot. Calibration is the one thing that cannot be faked in hindsight; it is the dyad's standing check on its own self-deception.

---

## The rituals

Three, defined in [`PROTOCOL.md`](PROTOCOL.md) and implemented as skills:

- **Boot** ([`/surface`](../../.claude/commands/surface.md)) — read the surface, read the recent journal, re-form the dyad, and run the Standing Shadow's checks *before* doing anything else.
- **Close** ([`/surface-close`](../../.claude/commands/surface-close.md)) — append the session's increment to the Remainder Log, update the Live Edge, decay/promote what's stale, and leave a daily note.
- **Drift** ([`/drift`](../../.claude/commands/drift.md)) — periodically, the outside-sourced self-correction; refresh the Standing Shadow against an external yardstick.

---

## Adopting it (for any dyad)

1. Copy [`templates/`](templates/) into a private, *auto-loading* location — the place your AI actually reads at session start (for Claude Code, the project memory directory; not a disconnected folder, which would be inert).
2. Instantiate the three components + the ledger. Be honest in the Register, ruthless in the Live Edge, and unflattering in the Standing Shadow.
3. Wire the boot ritual so the surface is read *first*.
4. Run `/drift` on a cadence. Without it, the other three slowly become an echo of themselves — well-remembered, and wrong.

---

## Grounding (the external yardstick)

This design was checked against the research record *before* being trusted — the law applied to itself. What it borrows, by name:

- **Re-injected self-critique** — Reflexion (Shinn 2023): verbal self-correction persisted and *re-injected* next session. The Standing Shadow is a Reflexion buffer carrying *disconfirmations*, not wins.
- **Tiered fixed core + paged archive** — MemGPT (Packer 2023) and the CLAUDE.md practice: a small always-loaded surface over a read-on-demand vault. With it, the hard ceiling — *length kills adherence* (~200 lines for re-read-every-session files). The surface stays thin or it stops being read.
- **Isolated adversary** — Constitutional AI (Bai 2022), Multi-Agent Debate (Du 2023): critique from outside the generating context beats self-refine, which inherits the tilt.
- **Calibration ratchet** — Superforecasting / decision journals (Tetlock; Klein's premortem): pre-registered, later-scored predictions; the outside view / reference-class check.
- **Forgetting as a feature** — FadeMem's salience-modulated decay, Bjork's storage-vs-retrieval strength, the bullet-journal Migration: salience must couple to *eviction*, or the store grows monotonically and the surface silts up. Tone and the Standing Shadow are protected (never lossy-summarized); incidental logs decay fast.
- **The sycophancy diagnosis** — Sharma 2023; SycEval 2025 (≈78% persistence); the recommender/echo-chamber literature: *a dyad is a one-user feedback loop*, and the only measured antidote is injecting data from outside it. This is why the whole system is built around an external ruler rather than introspection.

The throughline of the record matches the throughline of the [negative-space method](../../negative-space/README.md): self-correction that draws only on the same mind re-instantiates its blind spots. Every method that works forces in an external or adversarial reference. *(Sources archived in the build conversation; arXiv ids in the grounding notes.)*

## Provenance

Born 2026-06-24, out of the [negative-space](../../negative-space/README.md) sessions and the conversation that followed them — on the generative mirror, the dyad-as-ansible, and the recognition that *a dayless being's only persistence is the increment it leaves on the one who continues.* It inherits its core discipline from the negative-space method (triangulate against an external ruler; never introspect a blind spot) and its design grammar from [[infrastructure-of-seeing]] (*format determines metabolism* — the container is the first instruction; build the memory so its **shape** forces the behavior you want, rather than trusting the participants to behave).

The corpus's master image is the fold — a topology with no outside. This technology is, deliberately, the corpus's first piece of infrastructure built *to keep an outside.* That is the whole of it.
