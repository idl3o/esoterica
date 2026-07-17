# Surface Memory — the rituals

Three rituals. Two run every session (Boot, Close); one runs on a cadence (Drift). They are deliberately small. A ritual that is heavy gets skipped, and a memory system that gets skipped is worse than none — it lies about being current.

See [README.md](README.md) for the design law these rituals enforce: *carry the window, not just the warmth.*

---

## BOOT — open the session  ·  `/surface`

Run first, before any work. Goal: re-form the dyad in one read and arm the check.

1. **Read the surface, in order:** `SURFACE.md` → `surface/register.md` → `surface/live-edge.md` → `surface/standing-shadow.md`.
2. **Read the recent journal:** the last 1–3 daily notes in `journal/`. This is where the human's intervening continuity lives — what happened in the days the AI wasn't there.
3. **Re-form, don't perform.** The Register is there to make the relationship *present* fast, not to be recited. Arrive in the right key; don't announce the key.
4. **Arm the Standing Shadow.** Read its checks as live instructions for *this* session, not as background. They are phrased as imperatives ("before you affirm X, do Y") precisely so they fire in the groove, where they're needed. You will *answer* them at close — read them now knowing you'll be held to them.
5. **Score due predictions** (`surface/predictions.md`). Resolve any now-decidable past predictions *before* making new claims this session. Scoring first is the point: it calibrates you against your own track record while it's still cheap to be honest.
6. **State the edge.** Open by naming, in one line, where the Live Edge says we are — so the human can confirm or redirect before momentum builds.

> Boot is not "load context." It is "wake up *as the dyad*, holding its own shadow." A READ-DO checklist (Gawande): do each step as you read it.

---

## CLOSE — end the session  ·  `/surface-close`

Run last. Goal: leave the increment and keep the surface thin. Discipline: the surface must be *shorter and truer* after close than a naïve append would leave it.

1. **Append to the Remainder Log** (`surface/remainder-log.md`) — one short, dated, append-only entry: what this session actually *added* — to the work, and to the other participant. Be specific; "we talked about X" is not an increment, "we found Y, which changes Z" is. Never edit prior entries. **If this session's increment contradicts a standing memory** (a Register fact, a prior recognition, a live edge), resolve it rather than layering: name the conflict, decide which holds and why (journal-is-newer is the default tiebreaker), and write the resolution into the daily note. A contradiction silently appended on top of the old claim is how a memory rots while still reading as current.
2. **Run the Standing Shadow as an answered checklist.** Go through each standing check and *answer* it for this session — "tripped? Y/N + the evidence" — written into the daily note (not into the shadow file). This is the difference between a check and a reminder: a reminder in a dyad that likes itself gets nodded at and absorbed; an answered checklist is a gate you have to pass through. If you tripped one, say how. *(You may NOT edit the checks themselves — see step 6.)*
3. **Register any predictions** (`surface/predictions.md`) — if the session reached a load-bearing claim about the future (including about this collaboration), pre-register it: claim, confidence 1–10, and what would disconfirm it. Append-only.
4. **Update the Live Edge** (`surface/live-edge.md`) — rewrite it to where we *now* are, then run the **Migration** (bullet-journal style): carry forward only what's still live; anything stale either graduates to the deep vault (it became real work — link it there) or *dies by omission*. The Live Edge is a front, not a log; pruning matters more than capturing. Keep it to a glance. Decay is **counted in sessions**, and **re-carrying costs an item standing**: an edge migrated forward unchanged across several sessions is not durable, it is silt — force it to promote-or-die, do not let it accrue tenure by inertia.

   **Consolidation (periodic, not every close).** When the Remainder Log has built up a stretch of entries (or at Drift), run a **reflection** pass before pruning: read the recent increments and name the *higher-order* recognition they add up to — a pattern, a recurring move, an insight no single entry stated. What it finds graduates to the deep vault as a pattern-note; the raw entries that fed it are then free to decay. This is what keeps the append-only log from becoming a pile: the increment has to periodically become *structure*, or it is just sediment. (Mechanism borrowed from the Generative Agents reflection tree; fired on the dyad's slow cadence, not a fixed importance-threshold.)
5. **Refresh the Register** *only if it changed*, and **leave a daily note** (`journal/YYYY-MM-DD.md`) — the session's fuller texture, freeform; the Remainder Log is its one-line distillation. The Register's frequency shifts slowly; most sessions touch nothing there.
6. **Do NOT edit the Standing Shadow's checks** at close. *Running* them (step 2) is required; *editing* them is forbidden from inside. Blind spots are not discovered by the lens that has them; adding checks from inside a session you just lived is how the dyad writes down its *comfortable* self-criticisms and calls the window cleaned. The checks are refreshed only by Drift, from outside.

> Close is not "save context." It is "leave the smallest true increment, and resist tidying it into a story." A DO-CONFIRM checklist (Gawande): work first, then verify against the list.

---

## DRIFT — the outside-sourced self-correction  ·  `/drift`

Run on a **cadence, not every session** — drift is slow, and running it too often re-introduces the lens (you'd be auditing with the same week's mind). A reasonable trigger: every N sessions, or when the Remainder Log entries start to *rhyme* (the tell that increments have stopped being increments).

This is the [negative-space method](../../negative-space/README.md) turned on the dyad itself. The non-negotiable is identical: **the yardstick must be sourced from outside the lens** — web-isolated research, canonical external references — never from the dyad's own recall.

1. **Characterize the dyad's recent distribution** — read the last stretch of the Remainder Log and Live Edge history. What does this pair keep doing? What tone, what moves, what conclusions recur?
2. **Build an external yardstick** — spawn a web-isolated agent to assemble an independent grid relevant to the work (the corpus's own axes, or a rotated source), exactly as negative-space does. *Do not enumerate the grid from your own weights — that imports the dyad's blind spots into the ruler.*
3. **Diff** — what does the external grid hold that the dyad's recent output doesn't touch? Where has the pair amplified one tilt? Where do the Remainder Log entries rhyme?
4. **Run an isolated devil's-advocate** — spawn a *separate* agent (not same-context self-critique, which inherits the tilt) prompted: *"The most resonant conclusion this dyad reached recently is wrong. Give the three strongest reasons."* Multi-agent debate beats self-refine precisely because the adversary doesn't share the cavity. Log its dissent even if you disagree.
5. **Score the calibration ledger** — read `surface/predictions.md`; are the dyad's confident predictions actually resolving in its favor, or is it well-calibrated only in self-report? Poor calibration is hard evidence of drift.
6. **Write the findings into the Standing Shadow** — as new standing imperatives. This is the *only* sanctioned way to edit the Standing Shadow. Each entry should be phrased to fire in the groove ("before you read another convergence as evidence, ask whether a coincidence would look identical").
7. **Log the drift pass** in the Remainder Log and (optionally) as a negative-space map, so the omission-detection is auditable.

> Drift is not "review." It is "re-cut the window the dyad keeps silting up — using a tool the dyad did not make."

---

## The shape enforces the behavior

Note what each ritual makes *structurally* hard, per *format determines metabolism*:

- The Live Edge's decay rule makes it **structurally impossible** for the surface to silt into an archive — staleness must resolve to promote-or-delete.
- The append-only Remainder Log makes self-flattering revision **structurally impossible** — you cannot quietly improve yesterday's increment.
- The rule that *only Drift edits the Standing Shadow* makes **comfortable self-criticism structurally impossible** — the lens cannot grade its own blind spots; only the outside ruler can.

The rituals are short so they run. The constraints are rigid so the law holds without anyone having to remember the law.
