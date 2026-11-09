# FILM SLATE v2 — The Matured Slate

The first slate (films 01–111, five waves) narrated one essay per film. A film was therefore as deep as the single document it read, and the treatment above that document reached the render only as a style string and a voice. v2 remakes the slate by **topic**. Each topic gathers everything the corpus holds on it, sets that against outside rulers, keeps the strongest objection, and only then writes a script for the ear.

Decided 14 October 2026 (Sam):

1. **Re-cut by topic.** Films from v1 that would draw on the same dossier fold into one v2 film. The mapping is in [TOPICS.md](TOPICS.md); every v1 number appears there exactly once.
2. **The argument sets the length.** The essays were written long for synthesis engines. A v2 script keeps the argument and drops the amplification. The dossier is the long companion. Expected runtime is 15–40 minutes, and no floor applies.
3. **The topic at its truest.** Outside sources and the strongest objection go into the dossier *and* into the film. A v2 film may disagree with the v1 essay it replaces.
4. **Agents gather and check, one hand writes.** Agents gather dossiers, and a different model family checks every script. A single mind writes every script, strand by strand, because fanning a shared tone target out to many writers produces a monoculture (the shared-target monoculture pattern, measured on v1 by text-to-video's `tools/shot_audit.py`).

These are decisions, not accidents. Do not undo them.

---

## Four kinds of v1 film

| kind | what v2 does |
|---|---|
| **Exposition**: a myth, tradition, science, thinker or fiction | dossier → rulings → script → checks → render |
| **House thesis**: the fold, convergence, the instruments | the same, with its prior art and its objection as the outside rulers |
| **Work**: parable, voice, native-form B half | carried over unchanged; re-rendered through the t2v direction layer, no dossier |
| **Sam's hand**: self-portrait and first-person recognitions | not remade without Sam's direction |

A work is not a claim, so maturing it would mean rewriting a finished artefact. The parables, the eleven voices and the B halves stay as written.

---

## A topic's folder

```
v2/<code>-<slug>/
  dossier.md       gathered by agents, ruled by the writing hand
  script.md        the narration — what the film says, word for word
  treatment.md     visual direction for the t2v shot planner
  second-check.md  the other model's flags and their dispositions
  ledger.json      the gates, each stamped with the hashes it checked
```

### dossier.md

Frontmatter has `topic`, `slug`, `title`, `folds` (v1 numbers), `gathered` (date) and `gatherer`. It has nine sections, in this order:

1. **Scope.** What the topic is, which v1 films fold in, and what is out of scope.
2. **The corpus on this topic.** Every corpus document that bears on the topic: the v1 sources, their link neighbours, and any doc a grep for the topic's terms turns up. Each entry gives the path, what the document contributes, and the checkable claims it makes, quoted with line numbers.
3. **Primary sources.** Verbatim excerpts, each with an ID (`[P1]`, `[P2]` …) and the translation or edition, URL and retrieval date. **Every excerpt is fetched text, never recalled text.** A source that could not be fetched is paraphrased, without quotation marks, and marked `[not fetched]`.
4. **The standard account.** What current scholarship or science holds, with named authors and works. Excerpts carry IDs `[S1]` … under the same fetch rule.
5. **Claims ledger.** One row per checkable claim the corpus makes on the topic, with columns `ID | claim as the corpus states it | path:line | ruler (excerpt ID) | proposed verdict | note | ruling`. The verdicts are *stands*, *correct → wording*, *mark* and *pull*. The gatherer fills `proposed verdict` and leaves `ruling` empty. The writing hand fills `ruling`. The `ruled` gate reads only that last column, so a proposal can never pass for a ruling. Corpus files are not edited from a dossier; a correction goes through `/weed`.
6. **The strongest objection.** The best case against the corpus's reading, made by an outside voice and cited.
7. **Negative space.** What the outside sources show matters and the corpus does not have.
8. **What the sources show.** Concrete things the primary sources themselves name, which the camera can film. These are literal, not in the house register.
9. **Sources.** A full list with URLs and retrieval dates, each marked *fetched* or *not fetched*.

### script.md

Frontmatter has `topic`, `title`, `folds`, `voice`, `speakers` (tag → voice, for example `SOURCE: bf_emma`) and `quote_speakers` (the tags whose paragraphs are quotations).

- `# Title`, then one `## ` heading per movement. The t2v script parser marks these as headings and the planner turns the imagery with them.
- A paragraph that opens with a cast tag (`SOURCE. `) is spoken by that voice and the tag is not read aloud. Use it for primary-source excerpts, so a reading of a source is heard as a reading.
- Quotation marks only for words that appear verbatim in the dossier. Paraphrase is attributed after the author and carries no marks (register discipline, 2026-09-08).
- A copula on a checkable claim is cashable against a dossier excerpt or carries its regime inline. The mythopoetic *IS* is kept for myth labelled as myth (register discipline, 2026-06-24).
- The last movement is `## What Is Declined`.
- Written for the ear. It renders **verbatim**, with no adapt pass: wave 5 showed that a rewrite pass finds a turn whether or not the script has one.

### treatment.md

The visual direction the t2v planner reads: the central image, the image register, what the sources show (from dossier §8), and what is never shown. It has no Sound & Score section and no source separator. It is short, because the script carries the structure.

### ledger.json

Written by `apparatus/scripts/slate_v2.py`. Each gate records the date, the SHA-256 of the files it checked and anything it measured. If one of those files changes afterwards, the gate is reported **stale**. This is the provenance v1 lacked: a weed corrected after a render leaves its film flagged stale, so it no longer goes unnoticed.

---

## The gates

| gate | how it passes | who |
|---|---|---|
| `gathered` | dossier present with all nine sections | agent, stamped by tool |
| `ruled` | every claims-ledger row has a ruled verdict | writing hand |
| `written` | script present; words and estimated minutes recorded | writing hand |
| `quotes` | every quoted span and every `quote_speakers` paragraph is found verbatim in the dossier | `slate_v2.py quotes` (mechanical) |
| `register` | every capitalised copula and bare equation listed by the lint has been reviewed | `slate_v2.py lint`, then the hand |
| `second_check` | a different model family (local `gpt-oss:20b`) has flagged unsupported or overstated sentences, and every flag has a disposition | `slate_v2.py check`, then the hand |
| `sam` | Sam's approval, required only for topics marked *Sam's hand* in TOPICS.md | Sam |
| `rendered` | render stamped with the script hash, output dir and t2v commit | after render |

The second check is noisy by design: a small local model reading 40,000 characters of evidence flags more than it should. In the pilot, before tuning, about nine flags in ten were false: evidence the dossier held and the model missed. Each one is disposed of with the excerpt that carries the sentence, and that takes a few minutes. What the noise buys is a reader from another model family. On the pilot it found an unsupported inference ("a brain, a soil or a data centre folds for its own reasons") and a true detail with no excerpt behind it (Odin "in disguise"), both written by the one hand. Its settings are fixed by experiment and are recorded in `slate_v2_check.py`. Do not change them back:

- no schema-constrained output;
- sections 2–6 given as evidence;
- `SOURCE.` paragraphs left out;
- medium reasoning (high reasoning returned nothing).

The quote gate checks the script against the dossier, not the dossier against the world. The dossier's excerpts carry their URLs so that link can be re-fetched. No tool checks it yet.

### Set-level gates

Per-film checks cannot see a shared tic. `slate_v2.py audit` runs across every written script and reports:

- opening sentences that share a shape;
- central images used more than once (as dough was in 74 and 76);
- word sequences repeated across scripts;
- the spread of runtimes.

It runs after each strand. A finding goes back to the writing hand, not into a prompt.

---

## Order of work

1. **Pilot**, three topics chosen to differ: H7 *The Bekenstein Bound and the Arrow* (physics, the strictest outside test), T2 *The Witness* (a tradition, folding three house-register films) and N4 *The Death of Baldr* (myth, folding four films). Each is rendered and watched beside its v1 originals. The method is kept only if the v2 film says things the originals could not.
2. **Strands**, in the order TOPICS.md gives, one strand per sitting, with the set audit after each.
3. **Works** re-rendered through the direction layer, whenever its plan stage is trusted.

Rendering waits for the t2v direction layer (the shot planner, timed segmenter and audit; `NEXTGEN-REWRITE.md` in text-to-video) to land, and every launch is Sam's call.

## What is declined

- **No 30-minute floor, no 4,000-word baseline.** The CLAUDE.md authoring standard governs corpus documents. The dossier meets it; the script is held to the argument.
- **No anthology binding.** v2 does not get a fifth movement in slate-conclusions. Whether slate-conclusions survives the truest stance is Sam's call, once the strands are in.
- **No maturation of works.** A parable corrected against the Eddas is no longer a parable.
- **No edits to corpus sources from a dossier.** A wrong claim in a root document goes through `/weed`, with its log. The dossier records the ruling and cites the log.
