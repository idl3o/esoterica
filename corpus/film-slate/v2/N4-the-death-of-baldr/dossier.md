---
topic: N4
slug: the-death-of-baldr
title: The Death of Baldr
folds: ["07", "08", "29", "30"]
gathered: 2026-10-14
gatherer: Claude Opus 5.5 (Claude Code subagent); texts fetched from Wikisource, heimskringla.no, Project Gutenberg, Wikipedia and folklorefellows.fi
---

# N4 · The Death of Baldr · dossier

## 1. Scope

**The topic.** The death of Baldr as the sources tell it: Baldr's dreams; Odin's ride to the seeress; Frigg's oaths and the one sprout she left unsworn; the gods' sport; Loki's visit to Fensalir; Höðr's shot; the gods' grief and the sanctuary that stops their vengeance; the funeral on Hringhorni; Hermóðr's ride to Hel; Hel's condition; the weeping of all things and Thökk's refusal; the vengeance of Váli on Höðr; the binding of Loki, which Snorri presents as the payment for Baldr, with Sigyn's basin; and the return of Baldr and Höðr after Ragnarök. Saxo's Danish version, in which Hotherus kills Balderus with a sword over Nanna, belongs to the topic as the main variant.

**The v1 films that fold in.**

| v1 | film-slate file | corpus root | root lines | film copy offset |
|---|---|---|---|---|
| 07 | `film-slate/wave-1/07-sigyn-staying-with-the-trickster.md` | `synthesis/grown/sigyn-staying-with-the-trickster.md` | 162 | +49 |
| 08 | `film-slate/wave-1/08-thokk-the-cave-the-light-never-reached.md` | `synthesis/grown/thokk-the-cave-the-light-never-reached.md` | 176 | +45 |
| 29 | `film-slate/wave-2/29-balder-the-light-that-learned-the-dark.md` | `fiction-bridges/balder-the-light-that-learned-the-dark.md` | 349 | +49 |
| 30 | `film-slate/wave-2/30-hodr-the-blind-hand.md` | `synthesis/grown/hodr-the-blind-hand.md` | 162 | +46 |

Each film-slate file is a treatment header (logline, synopsis, movements) followed by its root reproduced verbatim (checked by `diff`: the only hunk is the header). A root line *n* therefore sits at line *n* + offset in the film copy, and any `/weed` correction to a root has a runner in the film copy. The treatment headers add three claims of their own, ruled in §5 with their roots (Hringhorni burning "into the sea", Höðr returning "able to see", the gods who "went home").

**Out of scope.** Loki as a figure (N5); the binding of Fenrir (N6); the forging of Draupnir and the other treasures (N7); Ragnarök and the green world as a whole, including Viðarr's shoe and the "every cobbler" ruling (N8). Frigg as a seeress is in scope only for what she does in the Baldr story. The corpus's applied registers (harm reduction, addiction, AI alignment, social exclusion, complicity) are not checked here except where they rest on a claim about the myth.

**Numbering.** Gylfaginning chapters follow Brodeur's roman numerals (XLIX = 49). Völuspá in translation is cited in Bellows' numbering. Through the Baldr stanzas it runs one ahead of the common numbering that the Old Norse edition (Guðni Jónsson) and TOPICS.md use: Bellows 32–34 are common 31–33, and Bellows 35 (Sigyn) is common 35. Common 34, in which Váli twists bonds from guts, is a Hauksbók stanza that Bellows gives only in a note (S2). The bracketed numbers inside Bellows' text are his footnote references, left as fetched. The Bellows translation on Wikisource is the 1923 edition; the sacred-texts.com copy named in the brief is the 1936 printing of the same translation and could not be fetched (§9).

## 2. The corpus on this topic

A grep of `corpus/` (excluding `corpus/film-slate/`) for Baldr, Balder, Baldur, Höðr, Hodr, Thökk, Thokk, Þökk, Sigyn, mistletoe, Hermóðr, Hermod, Nanna, Hringhorni, Draupnir, Frigg, Breiðablik, Gjallarbrú, Móðguðr, Váli, Rindr, Hotherus and Balderus returned 88 files. One is a false positive (`synthesis/grown/fractal-dimension-two-as-law.md:20`, the "rind" of the cortex). A first pass without word boundaries had also matched "thermodynamic" and "Inanna"; those hits are excluded. The four film-slate copies were diffed against their roots, the three weeding logs read in full, and `constellation/constellation.json` searched for the weeded phrasings.

### 2.1 The four v1 sources

**`fiction-bridges/balder-the-light-that-learned-the-dark.md`** (v1 29; 349 lines; written 8 April 2026 as the third of the Norse tetralogy). The fullest retelling in the corpus and the root of most Baldr claims elsewhere. It walks the dreams (43–55), Frigg's oaths and the "invulnerability paradox" (59–81), the mistletoe as a plant "between worlds" with Pliny's druids (85–103), the game (107–123), Höðr's throw (127–151), the funeral on Hringhorni (155–171), Hermóðr's ride (175–191), Thökk (195–233), Baldr's long wait (237–255), the return (259–281) and a Baldr–Christ comparison (285–301). Its quoted claims: an epigraph from Gylfaginning (5), a line attributed to Matthew Arnold (8), a Snorri portrait in quotation marks (25), Frigg's reason (75), Thökk's verse (209–213), Snorri's identification of Thökk (217), a Völuspá quotation (265–267). Its checkable narrative claims include "Hringhorni sails burning into the sea" (165), "Every being in creation weeps" at the funeral (167), Módguðr hearing "more noise from Balder's single passage than from five troops of dead men" (183), Baldr sending "his wife Nanna's linen back to Frigg" (187), "Thokk is Loki" (219), "all evil shall be healed. Not punished" (273), "What the sources describe instead is a Balder who reconciles" (277) and "The Balder-Christ parallel is not analogy. It is structural identity" (287).

**`synthesis/grown/thokk-the-cave-the-light-never-reached.md`** (v1 08; 176 lines; grown 11 June 2026). Reads Thökk's refusal as "accuracy" rather than malice: the light "never reached her cave" (24), "Light that has not been through the darkness leaves the darkness unchanged" (70), her refusal as "the correction that completes the light" (86), "Every universal good has its Thökk" (102), then a section that holds both readings and proposes a test, "Did the light genuinely not reach the cave?" (132). Its checkable claims: the epigraph "Thökk will weep dry tears for Balder's death. Let Hel hold what she has." (11); "Ragnarök is now inevitable" (20); "The myth strongly hints that Thökk is Loki in disguise" (20); an Old Norse quotation, "men hafa þat fyrir satt at þar hafi verit Loki", glossed "people hold it for true that this was Loki" (38); "a flower is named for the whiteness of his brow" (52); "the Balder who returns is not the Balder who died" (90); "For a thousand years" the world read her as a villain (18, 160).

**`synthesis/grown/hodr-the-blind-hand.md`** (v1 30; 162 lines; grown 11 June 2026). Reads Höðr through its subtitle, "the Unconscious Instrument" (3): "unconsciousness, not malice, is how the light dies in the world" (38); Höðr is "innocent and the instrument of catastrophe" (60), reconciled with Baldr in the green world rather than punished (74–84), with a test separating real from "motivated" blindness (88–98). Its checkable claims: an epigraph "after Snorri" in quotation marks (11); a quoted exchange between Loki and Höðr, "'Because I am blind,' says Höðr, 'and I have no weapon'" (34); "the myth says they are reconciled" (76); "This is not what a justice-myth would do. A justice-myth would punish Höðr… The Norse cosmology does the opposite" (78); "Höðr was never guilty in the punishable sense" (78); "In the green world, Höðr is presumably no longer blind" (82); "Höðr can see" (128).

**`synthesis/grown/sigyn-staying-with-the-trickster.md`** (v1 07; 162 lines; grown 11 June 2026). Builds a practice from Sigyn: "three refusals" (not freeing, not approving, not leaving) (30–44), the bowl as "harm-reduction as devotion" (48–62), the earthquake as the cost of attention's lapse (66–80), Sigyn as "the dark-cave complement of Frigga" (84–100), and the claim that "the only bound thing that can ever be safely released is one that was never abandoned in its binding" (114). Its checkable claims: the gods "fix him beneath a serpent set to drip venom on his face forever, and then… they leave" (18); Sigyn "has no illusions about what her husband did" (22) and knows the venom is "in a real sense, deserved" (40); "Frigga knew Balder would die. She knew the means, perhaps. And she did not… break the silence" (86); Ragnarök's Loki as one "bound and abandoned beneath the serpent" (110).

### 2.2 Load-bearing neighbours

**The three seeds** (`seeds/thokk-the-cave-the-light-never-reached.md`, `seeds/hodr-the-blind-hand.md`, `seeds/sigyn-staying-with-the-trickster.md`; planted 10 June 2026). Each carries the claims its grown form expands. Thökk seed:9 has "A giantess named Thökk (widely suspected to be Loki) refuses: *'Thökk will weep dry tears for Balder's death. Let Hel hold what she has.'*" Höðr seed:21: "the myth says they are *reconciled*, the killed and the blind killer together in the new world"; and "Höðr, in the new world, presumably no longer blind". Sigyn seed:15: "She does not *approve* — she has no illusions about what he did".

**`seeds/frigga-the-one-who-knew-and-did-not-tell.md`** (10 April 2026). The source of the "Frigga knows and withholds" frame used by the Sigyn synthesis and five others. Line 11: "Frigga sits on Hlidskjalf beside Odin. She sees the fates of all beings. She tells none." Line 13: "She tried *once* to intervene — Balder's bargain — and the intervention created the very vulnerability it sought to prevent." Line 13 fits Gylfaginning 49. "She tells none" meets the fact that she told Loki the one thing that mattered (C72).

**`fiction-bridges/loki-the-lie-that-tells-the-truth.md`** (the tetralogy's Loki bridge). Lines 67–93 retell the killing: "Loki finds the mistletoe. Loki fashions it into a dart. Loki places the dart in the hand of Hodr" (71); "the Balder who returns from Hel after Ragnarok is not the same as the Balder who was killed" (83). Line 171: "the entrails of his own son Narfi — killed before Loki's eyes… for eternity." Section IX (219–235) is the first corpus treatment of Sigyn: "She is the most neglected figure in Norse mythology" (221); "she maintains the possibility that what comes after Ragnarok includes Loki rather than excludes him" (235).

**`synthesis/grown/the-binding-of-loki-chaining-the-exhale.md`** (and its seed). The sibling of the Sigyn synthesis. Line 18 retells Gylfaginning 50 accurately (Váli turned wolf, Narfi torn, entrails to iron, three stones, Skaði's serpent, the bowl, the earthquake, "until the end of the world") and adds that the gods "leave". Section III (60–70) is the Sigyn reading in short. The seed (line 9) has "his writhing IS the earthquake", a mythic aetiology the sources state.

**`synthesis/grown/the-green-world-after-ragnarok.md`** (and its seed). Line 82: Baldr "comes back **reconciled with Höðr**". Line 86: "The Old Norse Völuspá and Snorri's account give us something far more difficult: *böls mun alls batna*… If this were victory, Höðr would be the villain, punished or erased." Seed:19: "Baldr and Höðr return reconciled".

**`synthesis/capstones/the-tree-inside-which-the-gods-run.md`** (the Norse capstone). Treats Baldr in two places. Lines 66 and 70 ask whether "Vidar's silence, Sigyn's held bowl" are a sixth topology of sacrifice or "the *kernel's mode of accumulation*", and leave it open ("a conjecture"). Line 130: "It reads *evil healed, not conquered*: Baldr returns reconciled with Höðr, the blind hand that killed him; the interrupt and the test no longer oppose each other." The capstone depends on the reconciliation claim (C60) and on the green world's "healed, not conquered" (C40, C78).

**`synthesis/grown/the-cabal-prediction-that-kills-itself.md`** (and its seed). Uses Frigg's oaths as its model: "Frigga foresaw Balder's death and extracted oaths from every thing in creation… The comprehensive protection created the singular vulnerability" (40), then "The myth's deepest teaching is her *restraint* afterward" (42) and "Frigga, after Balder, looked at the future and saw something to be left *unknown*" (174). The first is fair to Gylfaginning 49; the after-story has no source (C82).

**`synthesis/traditions/norse-cosmology.md`**. Lines 157–170 give the green world and quote Völuspá in marks: "Then unsown will the fields grow, / all ills will be healed, Balder will come back; / Höðr and Balder, the gods of slaughter, will live happily together / in the wise gods' dwelling-places." The translation is unnamed and not traced (C79).

**`synthesis/cosmological/nine-realms-density-cosmology.md`**. Line 204: "Hel's literally split body — half alive, half dead… She rules the realm where Balder… sits in the seat of honour after his death — not as captive but as guest". Line 261: "Hermod rides nine nights to Hel". Line 348: "Balder and Hodr — the most beloved god and his blind brother, returning *together* from Hel."

**`synthesis/cosmological/post-ragnarok-cycles.md`**. Line 12: "he returns as what he learned by dying. His light now contains shadow-wisdom." Line 309: "Balder returns because Balder never left". No source is cited.

**`threads/norse-anamnesis-cycle.md`**. The thread note. Line 28 describes the Balder bridge and concedes: "Its edge is the structural identity with Christ, argued as pattern rather than derivation." That sentence names the rival explanation (derivation) that the bridge itself does not test (§6).

**`fiction-bridges/heimdall-the-god-who-watched.md`**. Line 213: "He watches Loki engineer Balder's death… watches the most beautiful god die and does not intervene." Line 255: "Balder returns from Hel. Höðr returns."

**`synthesis/archetypal/loki-catalyst.md`**. Line 99: "An old woman, Þökk, refusing to weep for Baldur". Line 101: "He becomes Þökk to ensure Baldur stays in Hel". Line 318 retells the binding consistently with the sources.

**`fiction-bridges/odin-the-one-who-went-first.md`**. Lines 29, 226 and 342 make Odin the "architect" of Baldr's death through his blood-brotherhood with Loki ("He knew, when he bound himself to Loki, that the bond would cost him Balder"). No source gives Odin this knowledge; Baldrs draumar has him learn the outcome from the seeress (P18).

### 2.3 The rest, one line each

- `correspondences/archetypal/divine-tetrad-synthesis.md:217` — "Balder-Tyr" pairing; no checkable claim.
- `correspondences/archetypal/primarch-mythological-resonances.md:189` — "Balder the Beautiful dying", a list item.
- `correspondences/universal-pantheon-matrix.md:61, 112, 250` — Frigg, "Hel/Baldr's return" and Baldr as a light god in correspondence tables.
- `correspondences/universal-pantheon-redemption.md:36, 42` — Frigg "knowing all futures but allowing free will"; Baldur "innocence whose death triggers transformation".
- `distillations/promethean-choice-mythology.md:323` — the binding and Sigyn's bowl summarised; consistent with Gylfaginning 50.
- `extractions/robert-edward-grant/the-path-to-bliss-is-through-suffering-richard-rudd-think-ta.md:214` — a third-party speaker says Baldur was "shot by Loki through the ankle with an arrow of mistletoe"; a transcript, kept as record, not ruled.
- `fiction-bridges/freyja-the-one-who-taught-them-to-see.md:84, 104, 163` — Draupnir as gold; "Draupnir replicates but stays on Odin's arm" (Snorri has Odin lay it on the pyre); Freyja absent after Ragnarök.
- `fiction-bridges/freyr-the-sword-given-for-a-garden.md:88` — Skírnir carries Draupnir to Gerðr (Skírnismál; not checked here).
- `fiction-bridges/sif-the-hair-that-became-a-hammer.md:48, 124, 177` — Loki as "architect of Balder's death"; Draupnir's forging (N7).
- `fiction-bridges/thor-the-hammer-and-the-walking-stick.md:197, 199` — the survivors "find Mjolnir in the grass" (Snorri: Móði and Magni "shall have Mjöllnir"; the chess-pieces are what is found in the grass, P14); "Balder returns *changed*" (C53).
- `fiction-bridges/tyr-the-hand-that-knew.md:206, 222` — Baldr's death inside the interval Týr's sacrifice buys; no checkable Baldr claim.
- `journey/journal-2026-04-08.md:9, 23, 35` — the session that wrote the tetralogy; dated record, not ruled.
- `journey/journal-2026-04-09.md:23`, `journey/journal-2026-04-29.md:21, 71`, `journey/journal-2026-05-01.md:25` — records of the green-world and Frigga threads.
- `seeds/SEED-HARVEST-2026-06.md:95–97` — the catalogue lines for the Höðr, Thökk and Sigyn seeds.
- `seeds/SEED-HARVEST-2026-09.md:49` — link counts for the Norse cycle.
- `seeds/conference-of-the-birds-seven-valleys.md:151`, `seeds/dark-matter-as-first-mover.md:17`, `seeds/the-garden-grows-in-the-dark.md:58`, `seeds/the-true-mirror-wager.md:25` — Frigga as the one who knows and withholds; derivative of the Frigga seed.
- `seeds/feeding-the-wolf.md:19` and `synthesis/grown/feeding-the-wolf.md:70, 116, 142` — the "Tyr, Loki, Sigyn" trilogy (feed it, bind it, stay with it); line 70 says Sigyn "keeps the line open toward an eventual integration that the myth defers to after Ragnarök", which no source defers (C75).
- `seeds/loki-becomes-the-tree.md:23` and `synthesis/grown/loki-becomes-the-tree.md:100, 108, 136` — Loki as the one who "orchestrates the death of Balder"; Sigyn as the grounding the trickster lacked.
- `seeds/the-yggdrasil-meta-bridge.md:9, 25`, `synthesis/grown/the-yggdrasil-meta-bridge.md:18, 160`, `synthesis/grown/aesir-vanir-war-kvasir-integration.md:18`, `synthesis/grown/consciousness-os.md:112`, `synthesis/galactic-perspectives/galactic-status-report-2026-06.md:21` — Baldr as the "test suite" of the Norse OS mapping; consciousness-os:112 restates the bridge's thesis "untested light has a weakness only its death can reveal".
- `synthesis/afterlife-cartography-consciousness-map.md:240, 302` — Gjallarbrú and Módguðr ("she questions the living"), Hermóðr rides to Hel; consistent with P8.
- `synthesis/archetypal/set.md:111, 217` — "Baldur returns to rule a renewed world" (C80).
- `synthesis/capstones/time-itself-as-the-great-work.md:100` — "the controller's grip as the thing Sigyn's bowl is held against".
- `synthesis/collectives/social-memory-complex.md:160`, `synthesis/consciousness-technologies/ka-destiny.md:128`, `synthesis/consciousness-technologies/ka-tet-network.md:255`, `synthesis/consciousness-technologies/elder-futhark-runes.md:259` — Frigg in lists and correspondences.
- `synthesis/concepts/death-rebirth-mysteries.md:98`, `synthesis/consciousness-technologies/cyclical-evolution.md:118–120`, `synthesis/cosmological/yggdrasil-world-tree.md:56`, `synthesis/glyphs/gateway-key-kalki.md:207`, `synthesis/frameworks/galactic-perspective.md:135`, `synthesis/cosmological/fifth-sun-universal-syncretization.md:62` — Baldr's return in summaries of the green world; the chess-pieces in the grass stand (P14, P22).
- `synthesis/cosmological/solar-gods-prophecies-now.md:58–60, 247` — "Death: By mistletoe (smallest darkness)"; "Balder returns with new sun" (Snorri lists the sun's daughter separately; he does not join them).
- `synthesis/grown/brisingamen-beauty-as-operative-force.md:158`, `synthesis/grown/depth-contact-as-unified-practice.md:124`, `synthesis/grown/healing-as-temporal-alchemy.md:104, 172`, `synthesis/grown/mithya-as-bifocal-vision.md:120`, `synthesis/grown/the-blind-spot-as-window.md:78`, `synthesis/grown/the-worthiness-mechanic.md:94`, `synthesis/grown/transparency-as-the-limit-of-inference.md:136`, `synthesis/grown/vidar-silence-wearing-the-remainder.md:44`, `threads/cosmic-serpent.md:31` — Sigyn's bowl, Höðr's hand or Thökk's cave used as a figure; no new claim about the sources.
- `synthesis/grown/the-gradient-of-sacrifice.md:148` — Sigyn, Viðarr and Thökk as "sacrifice as withholding".
- `synthesis/grown/the-second-cosmic-c-is-not-the-first.md:86` — "Baldr returns from Hel, the cycle of vengeance that drove the old order is broken"; no source says so (not ruled separately; see C61).
- `synthesis/grown/the-true-mirror-wager.md:128` — "Frigga knew Baldr's death and did not speak it" (C72).
- `synthesis/personal/sam-complete-archetypal-constellation-butterfly-emergence.md:33` — Baldur as innocence whose death triggers transformation, in Sam's archetypal list; Sam's hand, not ruled.
- `synthesis/practices/prima-materia-transmission.md:162, 164` — "Baldr's death and the impossible mistletoe" as "operations performed on the listener".
- `synthesis/sessions/2025-12-12-sons-of-the-sun-extended.md:257–268` — an Apollo–Baldr table; "Dies by mistletoe".
- `synthesis/traditions/apollo-zeus-mediation.md:173` — "*Hermod* descends to Hel to negotiate Baldr's return"; stands (P6, P8).
- `threads/fiction-bridges.md:17`, `threads/seed-harvest-grown.md:7`, `threads/seeds-planting.md:9, 19` — indexes; "Frigga-form" named after the Frigga seed.
- `vignettes/loki-the-lie-that-tells-the-truth.md:35` — "You emptied Balder out of the whole world"; a work, not a claim.
- `weeding/logs/2026-09-08-september-syntheses-external-claims.md:100, 132, 143` — the "every cobbler" ruling (§2.4).

### 2.4 Rulings in the weeding logs that touch the cycle

- **2026-06-24** (load-bearing physics copula). No Norse finding. Its standing clause applies here: "When a synthesis says *X IS Y* about a checkable claim, the copula must be cashable against canon or carry its regime / boundary condition inline." It governs the bridge's "structural identity with Christ" (C43) and the flat "Thokk is Loki" (C34).
- **2026-09-08** (September syntheses). Two Norse findings. (a) "every cobbler ever trimmed": Gylfaginning 51 has shoe-*wearers* cut the scraps (Gylfaginning LI, the chapter of P12; Brodeur: "the scraps of leather which men cut out of their shoes at toe or heel"), proposed as Tier 2 across six Norse-cycle files and, by the log's status line, applied by Sam's ruling of 2026-09-09. It concerns Viðarr (N8). None of the four N4 documents contains "cobbler"; the word's remaining corpus hits are in the Viðarr synthesis and its relatives. (b) "Vidar's shoe is spent at Ragnarök; the leather goes into the wolf's jaw" was ruled invented (N8). The log's flower list for consciousness-os records "every Norse detail except Sif's scissors (a modern embellishment)". Its second standing clause applies throughout this dossier: "Quotation marks are for words the source actually contains. A paraphrase is attributed *after* its author and carries no marks." Rows C1, C3, C6, C12, C32, C33, C39, C45, C55, C57 and C79 are that clause.
- **2026-10-13** (wave-5 house register). No Norse finding. Its notes that "corrections are material too" and that "The adjudicator shares the generator that wrote the sources, so the citations carry the independence, not the verdicts" hold for this dossier: the gatherer is the same model family as the writer of the four v1 documents. The excerpts carry the independence; the verdicts do not.

## 3. Primary sources

All excerpts below were fetched on 2026-10-14 and are copied verbatim. Verse line-breaks are shown as " / ", zero-width characters and the Wikisource em-space caesuras were normalised to ordinary spaces, and bracketed footnote numbers are left as fetched. "[…]" marks an omission between two fetched segments. Fetch method for each source is in §9.

**[P1]** Snorri Sturluson, *Gylfaginning* XXII (Baldr; Breiðablik), tr. Arthur Gilchrist Brodeur, *The Prose Edda* (1916). https://en.wikisource.org/wiki/The_Prose_Edda_(1916_translation_by_Arthur_Gilchrist_Brodeur)/Gylfaginning — retrieved 2026-10-14.

> XXII. Then said Gangleri: "I would ask tidings of more Æsir." Hárr replied: "The second son of Odin is Baldr, and good things are to be said of him. He is best, and all praise him; he is so fair of feature, and so bright, that light shines from him. A certain herb is so white that it is likened to Baldr's brow; of all grasses it is whitest, and by it thou mayest judge his fairness, both in hair and in body. He is the wisest of the Æsir, and the fairest-spoken and most gracious; and that quality attends him, that none may gainsay his judgments. He dwells in the place called Breidablik,[39] which is in heaven; in that place may nothing unclean be, even as is said here:
>
> Breidablik 't is called, / where Baldr has / A hall made for himself: / In that land / where I know lie / Fewest baneful runes.

**[P2]** *Gylfaginning* ch. 22 (Baldr), Old Norse, ed. Guðni Jónsson (*Edda Snorra Sturlusonar*), heimskringla.no. https://heimskringla.no/wiki/Gylfaginning — retrieved 2026-10-14. The last clause ("en sú náttúra fylgir honum, at engi má haldast dómr hans") is the one Brodeur renders "that none may gainsay his judgments"; read word for word, it says that no judgment of his may hold (*haldast*, be kept, stand). The two renderings point in opposite directions; the gatherer does not settle the crux.

> Hárr segir: "Annarr sonr Óðins er Baldr, ok er frá honum gott at segja. Hann er beztr, ok hann lofa allir. Hann er svá fagr álitum ok bjartr, svá at lýsir af honum, ok eitt gras er svá hvítt, at jafnat er til Baldrs brár. Þat er allra grasa hvítast, ok þar eftir máttu marka fegurð hans bæði á hár ok á líki. Hann er vitrastr ásanna ok fegrst talaðr ok líknsamastr, en sú náttúra fylgir honum, at engi má haldast dómr hans. Hann býr þar, sem heitir Breiðablik. Þat er á himni. Í þeim stað má ekki vera óhreint

**[P3]** *Gylfaginning* XX (Frigg), tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> Frigg is his wife, and she knows all the fates of men, though she speaks no prophecy,—as is said here, when Odin himself spake with him of the Æsir whom men call Loki:
>
> Thou art mad now, / Loki, and reft of mind,— / Why, Loki, leav'st thou not off? / Frigg, methinks, / is wise in all fates, / Though herself say them not!

**[P4]** *Gylfaginning* XXV (Týr), XXVIII (Höðr), XXX (Váli), XXXII (Forseti), XXXIV (Hel), tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> Yet remains that one of the Æsir who is called Týr: he is most daring, and best in stoutness of heart, and he has much authority over victory in battle; it is good for men of valor to invoke him. It is a proverb, that he is Týr-valiant, who surpasses other men and does not waver. He is wise, so that it is also said, that he that is wisest is Týr-prudent.
>
> […]
>
> XXVIII. "One of the Æsir is named Hödr: he is blind. He is of sufficient strength, but the gods would desire that no occasion should rise of naming this god, for the work of his hands shall long be held in memory among gods and men.
>
> […]
>
> XXX. "One is called Áli or Váli, son of Odin and Rindr: he is daring in fights, and a most fortunate marksman.
>
> […]
>
> XXXII. "Forseti is the name of the son of Baldr and Nanna daughter of Nep: he has that hall in heaven which is called Glitnir. All that come to him with such quarrels as arise out of law-suits, all these return thence reconciled. That is the best seat of judgment among gods and men
>
> […]
>
> She is half blue-black and half flesh-color (by which she is easily recognized), and very lowering and fierce.

**[P5]** *Gylfaginning* XLIX, opening: the dreams, the oaths, the sport, Loki at Fensalir. Tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> XLIX. Then spake Gangleri: "Have any more matters of note befallen among the Æsir? A very great deed of valor did Thor achieve on that journey." Hárr made answer: "Now shall be told of those tidings which seemed of more consequence to the Æsir. The beginning of the story is this, that Baldr the Good dreamed great and perilous dreams touching his life. When he told these dreams to the Æsir, then they took counsel together: and this was their decision: to ask safety for Baldr from all kinds of dangers. And Frigg took oaths to this purport, that fire and water should spare Baldr, likewise iron and metal of all kinds, stones, earth, trees, sicknesses, beasts, birds, venom, serpents. And when that was done and made known, then it was a diversion of Baldr's and the Æsir, that he should stand up in the Thing,[54] and all the others should some shoot at him, some hew at him, some beat him with stones; but whatsoever was done hurt him not at all, and that seemed to them all a very worshipful thing.
>
> "But when Loki Laufeyarson saw this, it pleased him ill that Baldr took no hurt. He went to Fensalir to Frigg, and made himself into the likeness of a woman. Then Frigg asked if that woman knew what the Æsir did at the Thing. She said that all were shooting at Baldr, and moreover, that he took no hurt. Then said Frigg: 'Neither weapons nor trees may hurt Baldr: I have taken oaths of them all.' Then the woman asked: 'Have all things taken oaths to spare Baldr?' and Frigg answered: 'There grows a tree-sprout alone westward of Valhall: it is called Mistletoe; I thought it too young to ask the oath of.' Then straightway the woman turned away; but Loki took Mistletoe and pulled it up and went to the Thing.

**[P6]** *Gylfaginning* XLIX: Höðr's shot, the sanctuary, the gods' grief, Frigg's call for a rider. Tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> "Hödr stood outside the ring of men, because he was blind. Then spake Loki to him: 'Why dost thou not shoot at Baldr?' He answered: 'Because I see not where Baldr is; and for this also, that I am weaponless.' Then said Loki: 'Do thou also after the manner of other men, and show Baldr honor as the other men do. I will direct thee where he stands; shoot at him with this wand.' Hödr took Mistletoe and shot at Baldr, being guided by Loki: the shaft flew through Baldr, and he fell dead to the earth; and that was the greatest mischance that has ever befallen among gods and men.
>
> "Then, when Baldr was fallen, words failed all the Æsir, and their hands likewise to lay hold of him; each looked at the other, and all were of one mind as to him who had wrought the work, but none might take vengeance, so great a sanctuary was in that place. But when the Æsir tried to speak, then it befell first that weeping broke out, so that none might speak to the others with words concerning his grief. But Odin bore that misfortune by so much the worst, as he had most perception of how great harm and loss for the Æsir were in the death of Baldr.
>
> "Now when the gods had come to themselves, Frigg spake, and asked who there might be among the Æsir who would fain have for his own all her love and favor: let him ride the road to Hel, and seek if he may find Baldr, and offer Hel a ransom if she will let Baldr come home to Ásgard. And he is named Hermódr the Bold, Odin's son, who undertook that embassy. Then Sleipnir was taken, Odin's steed, and led forward; and Hermódr mounted on that horse and galloped off.

**[P7]** *Gylfaginning* XLIX: the funeral on Hringhorni. Tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> "The Æsir took the body of Baldr and brought it to the sea. Hringhorni is the name of Baldr's ship: it was greatest of all ships; the gods would have launched it and made Baldr's pyre thereon, but the ship stirred not forward. Then word was sent to Jötunheim after that giantess who is called Hyrrokkin. When she had come, riding a wolf and having a viper for bridle, then she leaped off the steed; and Odin called to four berserks to tend the steed; but they were not able to hold it until they had felled it. Then Hyrrokkin went to the prow of the boat and thrust it out at the first push, so that fire burst from the rollers, and all lands trembled. Thor became angry and clutched his hammer, and would straightway have broken her head, had not the gods prayed for peace for her.
>
> "Then was the body of Baldr borne out on shipboard; and when his wife, Nanna the daughter of Nep, saw that, straightway her heart burst with grief, and she died; she was borne to the pyre, and fire was kindled. Then Thor stood by and hallowed the pyre with Mjöllnir; and before his feet ran a certain dwarf which was named Litr; Thor kicked at him with his foot and thrust him into the fire, and he burned. People of many races visited this burning: First is to be told of Odin, how Frigg and the Valkyrs went with him, and his ravens; but Freyr drove in his chariot with the boar called Gold-Mane, or Fearful-Tusk, and Heimdallr rode the horse called Gold-Top, and Freyja drove her cats. Thither came also much people of the Rime-Giants and the Hill-Giants. Odin laid on the pyre that gold ring which is called Draupnir; this quality attended it, that every ninth night there dropped from it eight gold rings of equal weight. Baldr's horse was led to the bale-fire with all his trappings.

**[P8]** *Gylfaginning* XLIX: Hermóðr's ride, Módguðr, Hel's condition, the gifts. Tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> "Now this is to be told concerning Hermódr, that he rode nine nights through dark dales and deep, so that he saw not before he was come to the river Gjöll and rode onto the Gjöll-Bridge; which bridge is thatched with glittering gold. Módgudr is the maiden called who guards the bridge; she asked him his name and race, saying that the day before there had ridden over the bridge five companies of dead men; but the bridge thunders no less under thee alone, and thou hast not the color of dead men. Why ridest thou hither on Hel-way?' He answered: 'I am appointed to ride to Hel to seek out Baldr. Hast thou perchance seen Baldr on Hel-way?' She said that Baldr had ridden there over Gjöll's Bridge,—'but down and north lieth Hel-way.'
>
> 'Then Hermódr rode on till he came to Hel-gate; he dismounted from his steed and made his girths fast, mounted and pricked him with his spurs; and the steed leaped so hard over the gate that he came nowise near to it. Then Hermódr rode home to the hall and dismounted from his steed, went into the hall, and saw sitting there in the high-seat Baldr, his brother; and Hermódr tarried there overnight. At morn Hermódr prayed Hel that Baldr might ride home with him, and told her how great weeping was among the Æsir. But Hel said that in this wise it should be put to the test, whether Baldr were so all-beloved as had been said: 'If all things in the world, quick and dead, weep for him, then he shall go back to the Æsir; but he shall remain with Hel if any gainsay it or will not weep.' Then Hermódr arose; but Baldr led him out of the hall, and took the ring Draupnir and sent it to Odin for a remembrance. And Nanna sent Frigg a linen smock, and yet more gifts, and to Fulla a golden finger-ring.

**[P9]** *Gylfaginning* XLIX, close: the weeping and Thökk. Tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> "Then Hermódr rode his way back, and came into Ásgard, and told all those tidings which he had seen and heard. Thereupon the Æsir sent over all the world messengers to pray that Baldr be wept out of Hel; and all men did this, and quick things, and the earth, and stones, and trees, and all metals,—even as thou must have seen that these things weep when they come out of frost and into the heat. Then, when the messengers went home, having well wrought their errand, they found, in a certain cave, where a giantess sat: she called herself Thökk. They prayed her to weep Baldr out of Hel; she answered:
>
> Thökk will weep / waterless tears / For Baldr's bale-fare; / Living or dead, / I loved not the churl's son; / Let Hel hold to that she hath!
>
> And men deem that she who was there was Loki Laufeyarson, who hath wrought most ill among the Æsir."

**[P10]** *Gylfaginning* ch. 49, Old Norse, ed. Guðni Jónsson, heimskringla.no: Frigg's answer and the shot; Módguðr's words; Hel's condition; Thökk. https://heimskringla.no/wiki/Gylfaginning — retrieved 2026-10-14. Notes for the ledger: *viðarteinungr*, a sprout or shoot of wood; *vendi þessum*, "this wand"; *at tilvísun Loka*, by Loki's direction; *undir einum þér*, under you alone (Hermóðr); *kykvir ok dauðir*, quick and dead, which Thökk's *kyks né dauðs* answers; *nautk-a ek*, I had no use or benefit of; *þess geta menn*, people guess or suppose.

> Þá svarar Frigg: "Vex viðarteinungr einn fyrir vestan Valhöll. Sá er mistilteinn kallaðr. Sá þótti mér ungr at krefja eiðsins."
>
> Því næst hvarf konan á braut, en Loki tók mistiltein ok sleit upp ok gekk til þings. En Höðr stóð útarliga í mannhringnum, því at hann var blindr.
>
> Þá mælti Loki við hann: "Hví skýtr þú ekki at Baldri?"
>
> Hann svarar: "Því, at ek sé eigi, hvar Baldr er, ok þat annat, at ek em vápnlauss."
>
> Þá mælti Loki: "Gerðu þó í líking annarra manna ok veit Baldri sæmð sem aðrir menn. Ek mun vísa þér til, hvar hann stendr. Skjót at honum vendi þessum."
>
> Höðr tók mistiltein ok skaut at Baldri at tilvísun Loka.
>
> […]
>
> Móðguðr er nefnd mær sú, er gætir brúarinnar. Hon spurði hann at nafni eða at ætt ok sagði, at inn fyrra dag riðu um brúna fimm fylki dauðra manna - "en eigi dynr brúin minnr undir einum þér, ok eigi hefir þú lit dauðra manna. Hví ríðr þú hér á helveg?"
>
> […]
>
> En Hel sagði, at þat skyldi svá reyna, hvárt Baldr var svá ástsæll - "sem sagt er. Ok ef allir hlutir í heiminum, kykvir ok dauðir, gráta hann, þá skal hann fara til ása aftr, en haldast með Helju, ef nakkvarr mælir við eða vill eigi gráta."
>
> […]
>
> Þá er sendimenn fóru heim ok höfðu vel rekit sín erendi, finna þeir í helli nökkurum, hvar gýgr sat. Hon nefndist Þökk. Þeir biðja hana gráta Baldr ór Helju. Hon segir:
>
> 54. / "Þökk mun gráta / þurrum tárum / Baldrs bálfarar; / kyks né dauðs / nautk-a ek Karls sonar, / haldi Hel því, er hefir."
>
> En þess geta menn, at þar hafi verit Loki Laufeyjarson, er flest hefir illt gert með ásum."

**[P11]** *Gylfaginning* L, opening question and close: the binding of Loki as repayment for Baldr, and Sigyn's basin. Tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> L. Then said Gangleri: "Exceeding much Loki had brought to pass, when he had first been cause that Baldr was slain, and then that he was not redeemed out of Hel. Was any vengeance taken on him for this?" Hárr answered: "This thing was repaid him in such wise that he shall remember it long.
>
> […]
>
> "Now Loki was taken truceless, and was brought with them into a certain cave. Thereupon they took three flat stones, and set them on edge and drilled a hole in each stone. Then were taken Loki's sons, Vili and Nari or Narfi; the Æsir changed Váli into the form of a wolf, and he tore asunder Narfi his brother. And the Æsir took his entrails and bound Loki with them over the three stones: one stands under his shoulders, the second under his loins, the third under his boughs; and those bonds were turned to iron. Then Skadi took a venomous serpent and fastened it up over him, so that the venom should drip from the serpent into his face. But Sigyn, his wife, stands near him and holds a basin under the venom-drops; and when the basin is full, she goes and pours out the venom, but in the meantime the venom drips into his face. Then he writhes against it with such force that all the earth trembles: ye call that 'earthquakes.' There he lies in bonds till the Weird of the Gods."

**[P12]** *Gylfaginning* LI: Loki at Ragnarök. Tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> Hrymr is the name of the giant who steers Naglfar.
>
> […]
>
> then Loki and Hrymr shall come there also, and with him all the Rime-Giants. All the champions of Hel follow Loki;
>
> […]
>
> Loki shall have battle with Heimdallr, and each be the slayer of the other.

**[P13]** *Gylfaginning* LII: the abodes after the burning, Gimlé and Nástrand. Tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> Then Thridi answered: "In that time the good abodes shall be many, and many the ill; then it shall be best to be in Gimlé in Heaven. Moreover, there is plenteous abundance of good drink, for them that esteem that a pleasure, in the hall which is called Brimir: it stands in Ókólnir. That too is a good hall which stands in Nida Fells, made of red gold; its name is Sindri. In these halls shall dwell good men and pure in heart.
>
> "On Nástrand[55] is a great hall and evil, and its doors face to the north: it is all woven of serpent-backs like a wattle-house; and all the snake-heads turn into the house and blow venom, so that along the hall run rivers of venom; and they who have broken oaths, and murderers, wade those rivers, even as it says here:
>
> I know a hall standing far from the sun, / In Nástrand: the doors; to northward are turned; / Venom-drops fill down from the roof-holes; / That hall is bordered with backs of serpents. / There are doomed to wade the weltering streams / Men that are mansworn, and they that murderers are.

**[P14]** *Gylfaginning* LIII: the new earth; Baldr and Höðr from Hel. Tr. Brodeur (1916). Same URL as P1 — retrieved 2026-10-14.

> Hárr answered: "In that time the earth shall emerge out of the sea, and shall then be green and fair; then shall the fruits of it be brought forth unsown. Vídarr and Váli shall be living, inasmuch as neither sea nor the fire of Surtr shall have harmed them; and they shall dwell at Ida-Plain, where Ásgard was before. And then the sons of Thor, Módi and Magni, shall come there, and they shall have Mjöllnir there. After that Baldr shall come thither, and Hödr, from Hel; then all shall sit down together and hold speech with one another, and call to mind their secret wisdom, and speak of those happenings which have been before: of the Midgard Serpent and of Fenris-Wolf. Then they shall find in the grass those golden chess-pieces which the Æsir had had;

**[P15]** *Skáldskaparmál* V, XII, XIII (kennings for Baldr, Váli and Höðr), tr. Brodeur (1916). https://en.wikisource.org/wiki/The_Prose_Edda_(1916_translation_by_Arthur_Gilchrist_Brodeur)/Skáldskaparmál — retrieved 2026-10-14.

> V. "How should one periphrase Baldr? By calling him Son of Odin and Frigg, Husband of Nanna, Father of Forseti, Possessor of Hringhorni and Draupnir, Adversary of Hödr, Companion of Hel, God of Tears. Úlfr Uggason, following the story of Baldr, has composed a long passage in the Húsdrápa; and examples are recorded earlier to the effect that Baldr is so termed.
>
> […]
>
> XII. "How should Váli be periphrased? Thus: by calling him Son of Odin and Rindr, Stepson of Frigg, Brother of the Æsir, Baldr's Avenger, Foe and Slayer of Hödr, Dweller in the Homesteads of the Fathers.
>
> XIII. "How should one periphrase Hödr? Thus: by calling him the Blind God, Baldr's Slayer, Thrower of the Mistletoe, Son of Odin, Companion of Hel, Foe of Váli.

**[P16]** Úlfr Uggason, *Húsdrápa*, the Baldr's-funeral stanzas as quoted in *Skáldskaparmál*, tr. Brodeur (1916). Each stanza is introduced there by "Thus sang Úlfr Uggason" (the Freyr stanza by "Thus speaks Úlfr Uggason"). Same URL as P15 — retrieved 2026-10-14. The refrain "With old tales the hall was painted" marks the poem as a description of pictures in a hall (S19). The Hyrrokkin stanza of *Húsdrápa* is not in Brodeur's partial translation and was not fetched.

> Swiftly the Far-Famed rideth, / The Foretelling God, to the fire speeds, / To the wide pyre of his offspring; / Through my cheeks praise-songs are pouring.
>
> […]
>
> There I think the Valkyrs follow, / And ravens, Victorious Odin / To the blood of holy Baldr. / With old tales the hall was painted.
>
> […]
>
> His steed the lordly Heimdallr / Spurs to the pyre gods builded / For the fallen son of Odin, / The All-Wise Raven-Ruler.
>
> […]
>
> The battle-bold Freyr rideth / First on the golden-bristled / Barrow-boar to the bale-fire / Of Baldr, and leads the people.

**[P17]** Þjóðólfr of Hvinir, *Haustlöng*, the Sigyn kenning as quoted in *Skáldskaparmál* XXII, tr. Brodeur (1916). Same URL as P15 — retrieved 2026-10-14.

> The Arm-Burden then of Sigyn, / Whom all the gods in bonds see, / Firmly forthwith was fastened / To the Fosterer of Skadi;

**[P18]** *Baldrs draumar* 1–7, tr. Henry Adams Bellows, *The Poetic Edda* (1923). https://en.wikisource.org/wiki/The_Poetic_Edda_(tr._Bellows)/Baldrs_Draumar — retrieved 2026-10-14.

> 1.[1] Once were the gods together met, / And the goddesses came and council held, / And the far-famed ones the truth would find, / Why baleful dreams to Baldr had come.
>
> 2.[2] Then Othin rose, the enchanter old, / And the saddle he laid on Sleipnir's back; / Thence rode he down to Niflhel deep, / And the hound he met that came from hell.
>
> 3.[3] Bloody he was on his breast before, / At the father of magic he howled from afar; / Forward rode Othin, the earth resounded / Till the house so high of Hel he reached.
>
> 4. Then Othin rode to the eastern door, / There, he knew well, was the wise-woman's grave; / Magic he spoke and mighty charms, / Till spell-bound she rose, and in death she spoke:
>
> 5. "What is the man, to me unknown, / That has made me travel the troublous road? / I was snowed on with snow, and smitten with rain, / And drenched with dew; long was I dead."
>
> Othin spake:
>
> 6.[4] "Vegtam my name, I am Valtam's son; / Speak thou of hell, for of heaven I know: / For whom are the benches bright with rings, / And the platforms gay bedecked with gold?"
>
> The Wise-Woman spake:
>
> 7.[5] "Here for Baldr the mead is brewed, / The shining drink, and a shield lies o'er it; / But their hope is gone from the mighty gods. / Unwilling I spake, and now would be still."

**[P18b]** *Baldrs draumar* 8–14, tr. Bellows (1923). Same URL as P18 — retrieved 2026-10-14.

> 8. "Wise-woman, cease not! I seek from thee / All to know that I fain would ask: / Who shall the bane of Baldr become, / And steal the life from Othin's son?"
>
> The Wise-Woman spake:
>
> 9.[6] "Hoth thither bears the far-famed branch, / He shall the bane of Baldr become, / And steal the life from Othin's son. / Unwilling I spake, and now would be still."
>
> Othin spake:
>
> 10.[7] "Wise-woman, cease not! I seek from thee / All to know that I fain would ask: / Who shall vengeance win for the evil work, / Or bring to the flames the slayer of Baldr?"
>
> The Wise-Woman spake:
>
> 11.[8] "Rind bears Vali in Vestrsalir, / And one night old fights Othin's son; / His hands he shall wash not, his hair he shall comb not, / Till the slayer of Baldr he brings to the flames. / Unwilling I spake, and now would be still."
>
> Othin spake:
>
> 12.[9] "Wise-woman, cease not! I seek from thee / All to know that I fain would ask: / What maidens are they who then shall weep, / And toss to the sky the yards of the sails?"
>
> The Wise-Woman spake:
>
> 13.[10] "Vegtam thou art not, as erstwhile I thought; / Othin thou art, the enchanter old."
>
> Othin spake:
>
> "No wise-woman art thou, nor wisdom hast; / Of giants three the mother art thou."
>
> The Wise-Woman spake:
>
> 14.[11] "Home ride, Othin, be ever proud; / For no one of men shall seek me more / Till Loki wanders loose from his bonds, / And to the last strife the destroyers come."

**[P19]** *Völuspá* 32–35 in Bellows' numbering (common 31–33 and 35), tr. Bellows (1923). https://en.wikisource.org/wiki/The_Poetic_Edda_(tr._Bellows)/Voluspo — retrieved 2026-10-14.

> 32.[28] I saw for Baldr, the bleeding god, / The son of Othin, his destiny set: / Famous and fair in the lofty fields, / Full grown in strength the mistletoe stood.
>
> 33.[29] From the branch which seemed so slender and fair / Came a harmful shaft that Hoth should hurl; / But the brother of Baldr was born ere long, / And one night old fought Othin's son.
>
> 34.[30] His hands he washed not, his hair he combed not, / Till he bore to the bale-blaze Baldr's foe. / But in Fensalir did Frigg weep sore / For Valhall's need: would you know yet more?
>
> 35.[31] One did I see in the wet woods bound, / A lover of ill, and to Loki like; / By his side does Sigyn sit, nor is glad / To see her mate: would you know yet more?

**[P19b]** *Völuspá* 31–35 (common numbering), Old Norse, ed. Guðni Jónsson, heimskringla.no. https://heimskringla.no/wiki/Völuspá — retrieved 2026-10-14. The stanza numbers 32–35 printed inside the excerpt are the edition's; stanza 31 begins "Ek sá Baldri". Notes: *stóð of vaxinn völlum hæri / mjór ok mjök fagr / mistilteinn*, the mistletoe stood grown, higher than the fields, slender and very fair; *harmflaug*, harm-flight, a shaft; *und Hveralundi*, under the grove of hot springs; *þeygi of sínum ver vel glýjuð*, not at all glad about her husband.

> Ek sá Baldri, / blóðgum tívur, / Óðins barni, / örlög folgin; / stóð of vaxinn / völlum hæri / mjór ok mjök fagr / mistilteinn.
>
> 32. / Varð af þeim meiði, / er mær sýndisk, / harmflaug hættlig, / Höðr nam skjóta; / Baldrs bróðir var / of borinn snemma, / sá nam Óðins sonr / einnættr vega.
>
> 33. / Þó hann æva hendr / né höfuð kembði, / áðr á bál of bar / Baldrs andskota; / en Frigg of grét / í Fensölum / vá Valhallar. / Vituð ér enn - eða hvat?
>
> 34. / Þá kná Váli / vígbönd snúa, / heldr váru harðgör / höft ór þörmum.
>
> 35. / Haft sá hon liggja / und Hveralundi, / lægjarns líki / Loka áþekkjan; / þar sitr Sigyn / þeygi of sínum / ver vel glýjuð.

**[P20]** *Völuspá* 38–39, tr. Bellows (1923). Same URL as P19 — retrieved 2026-10-14.

> 38.[34] A hall I saw, far from the sun, / On Nastrond it stands, and the doors face north; / Venom drops through the smoke-vent down, / For around the walls do serpents wind.
>
> 39.[35] I saw there wading through rivers wild / Treacherous men and murderers too. / And workers of ill with the wives of men; / There Nithhogg sucked the blood of the slain, / And the wolf tore men; would you know yet more?

**[P21]** *Völuspá* 51, tr. Bellows (1923). Same URL as P19 — retrieved 2026-10-14.

> 51.[47] O'er the sea from the north there sails a ship / With the people of Hel, at the helm stands Loki; / After the wolf do wild men follow, / And with them the brother of Byleist goes.

**[P22]** *Völuspá* 59–62 and 64, tr. Bellows (1923). Same URL as P19 — retrieved 2026-10-14.

> 59.[55] Now do I see the earth anew / Rise all green from the waves again; / The cataracts fall, and the eagle flies, / And fish he catches beneath the cliffs.
>
> 60.[56] The gods in Ithavoll meet together, / Of the terrible girdler of earth they talk, / And the mighty past they call to mind, / And the ancient runes of the Ruler of Gods.
>
> 61.[57] In wondrous beauty once again / Shall the golden tables stand mid the grass, / Which the gods had owned in the days of old, / ..................
>
> 62.[58] Then fields unsowed bear ripened fruit, / All ills grow better, and Baldr comes back; / Baldr and Hoth dwell in Hropt's battle-hall, / And the mighty gods: would you know yet more?
>
> […]
>
> 64.[60] More fair than the sun, a hall I see, / Roofed with gold, on Gimle it stands; / There shall the righteous rulers dwell, / And happiness ever there shall they have.

**[P22b]** *Völuspá* 62 (common numbering), Old Norse, ed. Guðni Jónsson, heimskringla.no. Same URL as P19b — retrieved 2026-10-14. Notes: *böls mun alls batna*, all ill will get better; *búa þeir Höðr ok Baldr Hrofts sigtoftir*, Höðr and Baldr will dwell in Hroptr's (Odin's) victory-sites.

> Munu ósánir / akrar vaxa, / böls mun alls batna, / Baldr mun koma; / búa þeir Höðr ok Baldr / Hrofts sigtoftir, / vé valtíva.

**[P23]** *Lokasenna* 27–29, tr. Bellows (1923). https://en.wikisource.org/wiki/The_Poetic_Edda_(tr._Bellows)/Lokasenna — retrieved 2026-10-14.

> 27.[33] "If a son like Baldr were by me now, / Here within Ægir's hall, / From the sons of the gods thou shouldst go not forth / Till thy fierceness in fight were tried."
>
> Loki spake:
>
> 28. "Thou wilt then, Frigg, that further I tell / Of the ill that now I know; / Mine is the blame that Baldr no more / Thou seest ride home to the hall."
>
> Freyja spake:
>
> 29.[34] "Mad art thou, Loki, that known thou makest / The wrong and shame thou hast wrought; / The fate of all does Frigg know well, / Though herself she says it not."

**[P24]** *Lokasenna*, closing prose, tr. Bellows (1923). Same URL as P23 — retrieved 2026-10-14.

> And after that Loki hid himself in Franang's[64] waterfall in the guise of a salmon, and there the gods took him. He was bound with the bowels of his son Vali[65], but his son Narfi[65] was changed to a wolf. Skathi took a poison-snake and fastened it up over Loki's face, and the poison dropped thereon. Sigyn[66], Loki's wife, sat there and held a shell under the poison, but when the shell was full she bore away the poison, and meanwhile the poison dropped on Loki. Then he struggled so hard that the whole earth shook therewith; and now that is called an earthquake.

**[P25]** *Vafþrúðnismál* 54–55, tr. Bellows (1923). https://en.wikisource.org/wiki/The_Poetic_Edda_(tr._Bellows)/Vafthruthnismol — retrieved 2026-10-14.

> 54.[37] "Much have I fared, much have I found, / Much have I got from the gods: / What spake Othin himself in the ears of his son, / Ere in the bale-fire he burned?"
>
> Vafthruthnir spake:
>
> 55.[38] "No man can tell what in olden time / Thou spak'st in the ears of thy son; / With fated mouth the fall of the gods / And mine olden tales have I told; / With Othin in knowledge now have I striven, / And ever the wiser thou art."

**[P26]** Saxo Grammaticus, *Gesta Danorum* Book III, tr. Oliver Elton, *The Danish History, Books I–IX* (Project Gutenberg eBook #1150, whose front matter gives "translated by Oliver Elton (Norroena Society, New York, 1905)"). https://www.gutenberg.org/cache/epub/1150/pg1150.txt — retrieved 2026-10-14.

> When Helgi had slain Hodbrodd, his son Hother passed the length of his boyhood under the tutelage of King Gewar. While a stripling, he excelled in strength of body all his foster-brethren and compeers. Moreover, he was gifted with many accomplishments of mind. He was very skilled in swimming and archery, and also with the gloves; and further was as nimble as such a youth could be, his training being equal to his strength. Though his years were unripe, his richly-dowered spirit surpassed them. None was more skilful on lyre or harp; and he was cunning on the timbrel, on the lute, and in every modulation of string instruments.
>
> […]
>
> Now it befell that Balder the son of Odin was troubled at the sight of Nanna bathing, and was seized with boundless love. He was kindled by her fair and lustrous body, and his heart was set on fire by her manifest beauty; for nothing exciteth passion like comeliness. Therefore he resolved to slay with the sword Hother, who, he feared, was likeliest to baulk his wishes; so that his love, which brooked no postponement, might not be delayed in the enjoyment of its desire by any obstacle.

**[P26b]** Saxo, *Gesta Danorum* Book III: Gewar on Balder's body and Miming's sword; the sea-battle. Tr. Elton. Same URL as P26 — retrieved 2026-10-14.

> Gewar answered that he would most gladly favour him, but that he feared if he rejected Balder he would incur his wrath; for Balder, he said, had proffered him a like request. For he said that the sacred strength of Balder's body was proof even against steel; adding, however, that he knew of a sword which could deal him his death, which was fastened up in the closest bonds; this was in the keeping of Miming, the Satyr of the woods, who also had a bracelet of a secret and marvellous virtue, that used to increase the wealth of the owner. Moreover, the way to these regions was impassable and filled with obstacles, and therefore hard for mortal men to travel. For the greater part of the road was perpetually beset with extraordinary cold. So he advised him to harness a car with reindeer, by means of whose great speed he could cross the hard-frozen ridges.
>
> […]
>
> One would have thought it a contest of men against gods, for Odin and Thor and the holy array of the gods fought for Balder. There one could have beheld a war in which divine and human might were mingled. But Hother was clad in his steel-defying tunic, and charged the closest bands of the gods, assailing them as vehemently as a son of earth could assail the powers above. However, Thor was swinging his club with marvellous might, and shattered all interposing shields, calling as loudly on his foes to attack him as upon his friends to back him up. No kind of armour withstood his onset, no man could receive his stroke and live. Whatsoever his blow fended off it crushed; neither shield nor helm endured the weight of its dint; no greatness of body or of strength could serve. Thus the victory would have passed to the gods, but that Hother, though his line had already fallen back, darted up, hewed off the club at the haft, and made it useless.

**[P27]** Saxo, *Gesta Danorum* Book III: the maidens' food, the wound and the death of Balder, tr. Elton. Same URL as P26 — retrieved 2026-10-14.

> When they asked him who he was, he answered, a lutanist, nor did the trial belie his profession. For when the lyre was offered him, he tuned its strings, ordered and governed the chords with his quill, and with ready modulation poured forth a melody pleasant to the ear. Now they had three snakes, of whose venom they were wont to mix a strengthening compound for the food of Balder, and even now a flood of slaver was dripping on the food from the open mouths of the serpents. And some of the maidens would, for kindness sake, have given Hother a share of the dish, had not eldest of the three forbidden them, declaring that Balder would be cheated if they increased the bodily powers of his enemy. He had said, not that he was Hother, but that he was one of his company. Now the same nymphs, in their gracious kindliness, bestowed on him a belt of perfect sheen and a girdle which assured victory.
>
> Retracing the path by which he had come, he went back on the same road, and meeting Balder plunged his sword into his side, and laid him low half dead. When the news was told to the soldiers, a cheery shout of triumph rose from all the camp of Hother, while the Danes held a public mourning for the fate of Balder. He, feeling no doubt of his impending death, and stung by the anguish of his wound, renewed the battle on the morrow; and, when it raged hotly, bade that he should be borne on a litter into the fray, that he might not seem to die ignobly within his tent. On the night following, Proserpine was seen to stand by him in a vision, and to promise that on the morrow he should have her embrace. The boding of the dream was not idle; for when three days had passed, Balder perished from the excessive torture of his wound; and his body given a royal funeral, the army causing it to be buried in a barrow which they had made.

**[P28]** Pliny the Elder, *Natural History* 16.95 and the separate passage on Italian practice, as quoted and paraphrased by James George Frazer, *The Golden Bough* (abridged edition, 1922), ch. LXV, "Balder and the Mistletoe" (Project Gutenberg eBook #3623). https://www.gutenberg.org/cache/epub/3623/pg3623.txt — retrieved 2026-10-14. The translation of Pliny is Frazer's; Pliny was not fetched separately. The first sentence of the second segment onwards is Frazer's paraphrase, not a quotation of Pliny.

> It was worshipped by the Druids, as we learn from a famous passage of Pliny.
>
> […]
>
> The mistletoe is very rarely to be met with; but when it is found, they gather it with solemn ceremony. This they do above all on the sixth day of the moon, from whence they date the beginnings of their months, of their years, and of their thirty years' cycle, because by the sixth day the moon has plenty of vigour and has not run half its course. After due preparations have been made for a sacrifice and a feast under the tree, they hail it as the universal healer and bring to the spot two white bulls, whose horns have never been bound before. A priest clad in a white robe climbs the tree and with a golden sickle cuts the mistletoe, which is caught in a white cloth.
>
> […]
>
> In another passage Pliny tells us that in medicine the mistletoe which grows on an oak was esteemed the most efficacious, and that its efficacy was by some superstitious people supposed to be increased if the plant was gathered on the first day of the moon without the use of iron, and if when gathered it was not allowed to touch the earth; oak-mistletoe thus obtained was deemed a cure for epilepsy; carried about by women it assisted them to conceive; and it healed ulcers most effectually,

**[P29]** Henry Wadsworth Longfellow, "Tegnér's Death", *The Seaside and the Fireside* (Boston: Ticknor, Reed and Fields), pp. 77–81; the fetched page gives no year. https://en.wikisource.org/wiki/The_Seaside_and_the_Fireside/Tegnér's_Death — retrieved 2026-10-14. (The space after each opening quotation mark is in the fetched text.)

> I heard a voice, that cried, / “ Balder the Beautiful / Is dead, is dead!” / And through the misty air / Passed like the mournful cry / Of sunward sailing cranes. / I saw the pallid corpse / Of the dead sun / Borne through the Northern sky. / Blasts from Niffelheim / Lifted the sheeted mists / Around him as he passed. / And the voice for ever cried, / “ Balder the Beautiful / Is dead, is dead!” / And died away / Through the dreary night, / In accents of despair.

**[P30]** Matthew Arnold, "Balder Dead" (*The Poetical Works of Matthew Arnold*, 1855 text on Wikisource), part II, Módgud at the bridge. https://en.wikisource.org/wiki/The_poetical_works_of_Matthew_Arnold/Balder_Dead — retrieved 2026-10-14. The whole fetched poem (2,421 lines of text) was searched for "is dead, is dead" and "the beautiful"; neither phrase occurs.

> So on the bridge that damsel blocked the way, / And questioned Hermod as he came, and said,— / "Who art thou on thy black and fiery horse, / Under whose hoofs the bridge o'er Giall's stream / Rumbles and shakes? Tell me thy race and home. / But yester-morn, five troops of dead passed by, / Bound on their way below to Hela's realm, / Nor shook the bridge so much as thou alone. / And thou hast flesh and color on thy cheeks, / Like men who live, and draw the vital air; / Nor look'st thou pale and wan, like men deceased, / Souls bound below, my daily passers here."

## 4. The standard account

**What current scholarship holds, in outline.** The death of Baldr is told at length only by Snorri (Gylfaginning 49; his *Edda* is dated c. 1220 and was written well after Iceland's conversion around 1000, S20) and, very differently, by Saxo (Gesta Danorum III, written at the end of the twelfth century, S13). The Eddic poems allude to it rather than narrate it: Völuspá names the mistletoe, Höðr's shot, Váli's vengeance, Frigg's weeping and Sigyn by the bound Loki, and the return of Baldr and Höðr; Baldrs draumar has Odin learn from a dead seeress that Höðr will kill Baldr and Váli avenge him; Lokasenna has Loki claim the blame and closes with a prose account of his binding; Vafþrúðnismál ends on the unanswerable question of what Odin said into his dead son's ear. The skald Úlfr Uggason, in stanzas Snorri quotes, describes Baldr's funeral as pictured in a hall (P16, S19). John Lindow's monograph (1997) reads the story "in the context of its thirteenth century recording" and stresses that it "always involves acts of vengeance" (S6); its last chapter is titled "Baldr and Hodr: Ragnarok and Reconciliation", with reconciliation as the last of four feud stages, after revenge (S7). Frazer's reading of Baldr as a vegetation god whose life lay in the mistletoe (S5) and the wider "dying-and-rising god" category are no longer the consensus (S8). Whether Snorri's Baldr, and Völuspá's, carry Christian influence is an old and continuing question: Bugge held that nearly all Old Norse myths derive from Christian and late classical concepts, and "Bugge's theories were generally vehemently rejected, but have had some influence" (S9); Bellows found Christian influence in Völuspá "sufficiently striking" (S1); Lindow sees a Christian parallel in the bound Loki (S15); Choe (2021) reads Snorri's treatment of Höðr against thirteenth-century Christian Iceland (S20).

**The brief's specific questions.**

- *Who identifies Thökk with Loki?* Only Snorri, in the sentence after the verse, and he reports it as a supposition: "En þess geta menn, at þar hafi verit Loki Laufeyjarson" (P10), "men deem" in Brodeur (P9). No other fetched source contains the verse or the identification; Wikipedia's article on Þökk cites Gylfaginning 49 alone (S12). The name means "thanks" (S12).
- *Where is Sigyn's bowl attested?* In two prose passages: Gylfaginning 50 (P11; Brodeur "basin") and the closing prose of Lokasenna (P24; Bellows "shell"). Lokasenna "is found only in Regius" (S3), so the second attestation is the Codex Regius of the Poetic Edda alone. Gylfaginning survives in four main manuscripts, Codex Regius, Codex Wormianus, Codex Trajectinus and Codex Upsaliensis, none complete (S17); which of them contain chapter 50 was not established from fetched material. Sigyn without the bowl appears in Völuspá 35, whose last two lines (the Sigyn lines) are shared by the Regius and Hauksbók versions (S2), and in the skaldic kenning "The Arm-Burden then of Sigyn" for Loki in Haustlöng (P17; S11 dates the poem to the ninth century). The Gosforth Cross has been interpreted as showing her (S11).
- *Is Höðr's blindness old?* Snorri states it (Gylfaginning 28 and 49) and gives the kenning "the Blind God" (P15). The fetched Völuspá and Baldrs draumar do not mention it (P18, P18b, P19). Saxo's Hother is a sighted human hero (P26, S4). Skaldic poets use Höðr's name in warrior-kennings, which some scholars find hard to square with Snorri's blind god (S10). Choe (2021) argues that Snorri's Edda is the only source that describes the blindness (S20, paraphrased).
- *The Baldr–Christ parallels and the Christian-influence debate.* See S1, S9, S14, S15, S20 and §6. The original works (Bugge 1881; the Baldr chapters of Lindow 1997) were not fetched.
- *Frazer's dying god and its rejection.* See S5 and S8. J. Z. Smith's 1987 entry is quoted at second hand in S8; the original was not fetched.

**[S1]** Henry Adams Bellows, introductory note to *Völuspá*, *The Poetic Edda* (1923). URL as P19 — retrieved 2026-10-14.

> This final passage, in particular, has caused wide differences of opinion as to the date and character of the poem. That the poet was heathen and not Christian seems almost beyond dispute; there is an intensity and vividness in almost every stanza which no archaizing Christian could possibly have achieved. On the other hand, the evidences of Christian influence are sufficiently striking to outweigh the arguments of Finnur Jonsson, Müllenhoff and others who maintain that the Voluspo is purely a product of heathendom. The roving Norsemen of the tenth century, very few of whom had as yet accepted Christianity, were nevertheless in close contact with Celtic races which had already been converted, and in many ways the Celtic influence was strongly felt. It seems likely, then, that the Voluspo was the work of a poet living chiefly in Iceland, though possibly in the "Western Isles," in the middle of the tenth century, a vigorous believer in the old gods, and yet with an imagination active enough to be touched by the vague tales of a different religion emanating from his neighbor Celts.

**[S2]** Bellows' notes to *Völuspá* 32, 33, 35 and 62 (his numbering). URL as P19 — retrieved 2026-10-14. The first note, a retelling of Snorri, is the earliest fetched text in which Loki "guided his hand".

> ↑ Baldr: The death of Baldr, the son of Othin and Frigg, was the first of the great disasters to the gods. The story is fully told by Snorri. Frigg had demanded of all created things, saving only the mistletoe, which she thought too weak to be worth troubling about, an oath that they would not harm Baldr. Thus it came to be a sport for the gods to hurl weapons at Baldr, who, of course, was totally unharmed thereby. Loki, the trouble-maker, brought the mistletoe to Baldr's blind brother, Hoth, and guided his hand in hurling the twig. Baldr was slain, and grief came upon all the gods. Cf. Baldrs Draumar.
>
> […]
>
> ↑ The lines in this and the following stanza have been combined in various ways by editors, lacunae having been freely conjectured, but the manuscript version seems clear enough. The brother of Baldr: Vali, whom Othin begot expressly to avenge Baldr's death. The day after his birth he fought and slew Hoth.
>
> […]
>
> ↑ The translation here follows the Regius version. The Hauksbok has the same final two lines, but in place of the first pair has, "I know that Vali his brother gnawed, / With his bowels then was Loki bound."
>
> […]
>
> ↑ Baldr: cf. stanza 32 and note. Baldr and his brother, Hoth, who unwittingly slew him at Loki's instigation, return together, their union being a symbol of the new age of peace.

**[S3]** Bellows' introductory note and note on stanza 11 of *Baldrs draumar*; two passages of the introductory note and two notes on *Lokasenna*. URLs as P18 and P23 — retrieved 2026-10-14.

> Baldrs Draumar is found only in the Arnamagnæan Codex, where it follows the Harbarthsljoth fragment. It is preserved in various late paper manuscripts, with the title Vegtamskvitha (The Lay of Vegtam), which has been used by some editors.
>
> […]
>
> In any case, Baldrs Draumar presumably assumed its present form not later than the first half of the tenth century.
>
> […]
>
> ↑ Rind: mentioned by Snorri as one of the goddesses. Concerning her son Vali, begotten by Othin for the express purpose of avenging Baldr's death, and his slaying of Hoth the day after his birth
>
> […]
>
> The Lokasenna is found only in Regius, where it follows the Hymiskvitha; Snorri quotes four lines of it, grouped together as a single stanza.
>
> […]
>
> The prose notes are long and of unusual interest. The introductory one links the poem closely to the Hymiskvitha, much as the Reginsmol, Fafnismol and Sigrdrifumol are linked together; the others fill in the narrative gaps in the dialogue—very like stage directions,—and provide a conclusion by relating Loki's punishment, which, presumably, is here connected with the wrong incident.
>
> […]
>
> ↑ Prose: Snorri tells the same story, with minor differences, but makes it the consequence of Loki's part in the slaying of Baldr, which undoubtedly represents the correct tradition. The compiler of the poems either was confused or thought the incident was useful as indicating what finally happened to Loki. Possibly he did not mean to imply that Loki's fate was brought upon him by his abuse of the gods, but simply tried to round out the story.
>
> […]
>
> ↑ Sigyn: cf. Voluspo, 35, the only other place where she is mentioned in the poems.

**[S4]** The introduction to the Project Gutenberg edition of Elton's translation, *The Danish History, Books I–IX*: its summary of Book III and its note on Miming's sword. The fetched text does not name the author of the introduction. URL as P26 — retrieved 2026-10-14.

> Woden had a son Balder, rival of Hother for the love of Nanna, daughter of King Gewar. Woden and Thor his son fought for him against Hother, but in vain, for Hother won the laity and put Balder to shameful flight; however, Balder, half-frenzied by his dreams of Nanna, in turn drove him into exile (winning the lady); finally Hother, befriended hy luck and the Wood Maidens, to whom he owed his early successes and his magic coat, belt, and girdle (there is obvious confusion here in the text), at last met Balder and stabbed him in the side. Of this wound Balder died in three days, as was foretold by the awful dream in which Proserpina (Hela) appeared to him. Balder's grand burial, his barrow, and the magic flood which burst from it when one Harald tried to break into it, and terrified the robbers, are described.
>
> […]
>
> The death of Balder led Woden to seek revenge. Hrossthiof the wizard, whom he consulted, told him he must beget a son by "Wrinda" (Rinda, daughter of the King of the Ruthenians), who should avenge his half-brother.
>
> […]
>
> and ("Wale") "Bous" was born, who, after some years, slew Hother in battle, and died himself of his wounds. Bous' barrow in Bohusland, Balder's haven, Balder's well, are named as local attestations of the legend, which is in a late form, as it seems.
>
> […]
>
> The dwarf Miming, who lives in the desert, has a precious sword of sharpness (Mistletoe?) that could even pierce skin-hard Balder, and a ring (Draupnir) that multiplied itself for its possessor. He is trapped by the hero and robbed of his treasures.

**[S5]** James George Frazer, *The Golden Bough* (abridged, 1922), ch. LXI, "The Myth of Balder", and ch. LXV, "Balder and the Mistletoe". URL as P28 — retrieved 2026-10-14.

> A DEITY whose life might in a sense be said to be neither in heaven nor on earth but between the two, was the Norse Balder, the good and beautiful god, the son of the great god Odin, and himself the wisest, mildest, best beloved of all the immortals.
>
> […]
>
> That the Norse story of Balder was a myth of this sort will become probable if we can prove that ceremonies resembling the incidents in the tale have been performed by Norsemen and other European peoples.
>
> […]
>
> On this view the invulnerable Balder is neither more nor less than a personification of a mistletoe-bearing oak.

**[S6]** John Lindow, *Murder and Vengeance among the Gods: Baldr in Scandinavian Mythology*, FF Communications 262 (Helsinki: Suomalainen Tiedeakatemia, 1997): the Folklore Fellows publisher's description. https://www.folklorefellows.fi/?p=171 — retrieved 2026-10-14. The book itself was not fetched.

> The death of Baldr and its aftermath comprise the central moment of Scandinavian mythology. This book attempts to make sense of that story in the context of its thirteenth century recording by paying close attention to the texts themselves rather than to hypothetical background in cult or ritual. It elucidates both the literary and probable socio- historical context, and in connection with the latter it draws special attention to the fact that Baldr’s story does not end with his death but always involves acts of vengeance, thus suggesting an involvement with bloodfeud.

**[S7]** Anna-Leena Siikala, review of Lindow (1997), *FF Network* 15 (April 1998), 21–22. https://www.folklorefellows.fi/?p=1157 — retrieved 2026-10-14. The quotation marked (28) is Lindow's own words as Siikala quotes them.

> Lindow does not attempt to trace any assumed latent meanings in Baldr myths, but instead addresses the texts with a respect for their expression: his interest is in the myth “in forms in which we have it and the meaning it might have borne for those who knew it in those forms” (28).
>
> […]
>
> The last chapter, “Baldr and Hodr: Ragnarok and Reconciliation”, puts the myth of Baldr in a larger cosmological setting: after the destruction of the world in the fight of the gods, a new, better world will emerge with Baldr. The elements of the Baldr story, Conflict, Climax, Revenge and Reconciliation belong – according to Lindow – to the cultural system of managing disputes, feud, and organize the narrative world of sagas and myths, as well.

**[S8]** Wikipedia, "Dying-and-rising god", revision 1370695398 (22 August 2026). https://en.wikipedia.org/wiki/Dying-and-rising_god — retrieved 2026-10-14. J. Z. Smith's words inside it are quoted at second hand.

> By the end of the 20th century the scholarly consensus was that most of the gods Frazer listed as "dying-and-rising" only died and did not rise.
>
> […]
>
> One of the leading scholars in the deconstruction of Frazer's "dying-and-rising god" category was Jonathan Z. Smith, whose 1969 dissertation discusses Frazer's Golden Bough, and who in Mircea Eliade's 1987 Encyclopedia of religion wrote the "Dying and rising gods" entry, where he dismisses the category as "largely a misnomer based on imaginative reconstructions and exceedingly late or highly ambiguous texts", suggesting a more detailed categorisation into "dying gods" and "disappearing gods", arguing that before Christianity, the two categories were distinct and gods who "died" did not return, and those who returned never truly "died".
>
> […]
>
> Against this view, Mettinger (2001) affirms that many of the gods of the mystery religions do indeed die, descend to the underworld, are lamented and retrieved by a woman and restored to life.
>
> […]
>
> As of 2009, the Encyclopedia of Psychology and Religion summarizes the current scholarly consensus as ambiguous, with some scholars rejecting Frazer's "broad universalist category" preferring to emphasize the differences between the various traditions, but others continue to view the category as applicable.

**[S9]** Wikipedia, "Sophus Bugge", revision 1320167341 (3 November 2025). https://en.wikipedia.org/wiki/Sophus_Bugge — retrieved 2026-10-14.

> In his 1881 work, Studier over de nordiske Gude- og Heltesagns Oprindelse (Studies on the Origin of the Nordic Legends of Gods and Heroes), Bugge theorized that nearly all myths in Old Norse literature derive from Christian and late classical concepts. Bugge's theories were generally vehemently rejected, but have had some influence.

**[S10]** Wikipedia, "Höðr", revision 1346894239 (3 April 2026). https://en.wikipedia.org/wiki/Höðr — retrieved 2026-10-14.

> None of those kennings, however, are actually found in surviving skaldic poetry. Neither are Snorri's kennings for Váli, which are also of interest in this context.
>
> It is clear from this that Snorri was familiar with the role of Váli as Höðr's slayer, even though he does not relate that myth in the Gylfaginning prose. His emphasis is rather on the impossibility of restoring Höðr to life, despite his godhood.
>
> […]
>
> The poem Vafþrúðnismál informs us that the gods who survive Ragnarök are Viðarr, Váli, Móði and Magni, with no mention of Höðr and Baldr.
>
> […]
>
> Some scholars have found the fact that the poets should want to compare warriors with Höðr to be incongruous with Snorri's description of him as a blind god, unable to harm anyone without assistance. It is possible that this indicates that some of the poets were familiar with other myths about Höðr than the one related in Gylfaginning – perhaps some where Höðr has a more active role.

**[S11]** Wikipedia, "Sigyn", revision 1282676327 (27 March 2025). https://en.wikipedia.org/wiki/Sigyn — retrieved 2026-10-14.

> In stanza 35 of the Poetic Edda poem Völuspá, a völva tells Odin that, amongst many other things, she sees Sigyn sitting very unhappily with her bound husband, Loki, under a "grove of hot springs".
>
> […]
>
> Sigyn is mentioned a second (and final) time in the ending prose section of the poem Lokasenna. In the prose, Loki has been bound by the gods with the guts of his son Nari, his son Váli is described as having been turned into a wolf, and the goddess Skaði fastens a venomous snake over Loki's face, from which venom drips. Sigyn holds a basin under the dripping venom.
>
> […]
>
> and in kennings for Loki: "husband of Sigyn", "cargo [Loki] of incantation-fetter's [Sigyn's] arms", and in a passage quoted from the 9th-century Haustlöng, "the burden of Sigyn's arms".
>
> […]
>
> The mid-11th century Gosforth Cross located in Cumbria, England, has been interpreted as featuring various figures from Norse mythology. The bottom portion of the west side of the cross features a depiction of a long-haired female, kneeling figure holding an object above another prostrate, bound figure. Above and to their left is a knotted serpent. This has been interpreted as Sigyn soothing the bound Loki.
>
> […]
>
> she appears in the 9th century skaldic poem Haustlöng from pagan times, written by the skald Þjóðólfr of Hvinir. Due to this early connection with Loki, Sigyn has been theorized as a god dating back to an older form of Germanic paganism.

**[S12]** Wikipedia, "Þökk", revision 1302913557 (28 July 2025). https://en.wikipedia.org/wiki/Þökk — retrieved 2026-10-14. The article's only source text is Brodeur's Gylfaginning 49; its reference is Andy Orchard, *Dictionary of Norse Myth and Legend* (1997).

> Þökk (also Thökk) (Old Norse / Icelandic "Thanks") is a jötunn in Norse mythology, presumed to be Loki in disguise, who refuses to weep for the slain Baldr, thus forcing Baldr to stay in Hel.

**[S13]** Wikipedia, "Baldr", revision 1376572028 (25 September 2026). https://en.wikipedia.org/wiki/Baldr — retrieved 2026-10-14. The same article repeats several errors this dossier rules on (that Loki "made a magical spear", that Baldr and Höðr "would be reconciled and rule the new earth"); it is used only for the two passages below, both attributed.

> All objects made this vow, save for the mistletoe—a detail which has traditionally been explained with the idea that it was too unimportant and nonthreatening to bother asking it to make the vow, but which Merrill Kaplan has instead argued echoes the fact that young people were not eligible to swear legal oaths, which could make them a threat later in life.
>
> […]
>
> Writing during the end of the 12th century, the Danish historian Saxo Grammaticus tells the story of Baldr (recorded as Balderus) in a form that professes to be historical. According to him, Balderus and Høtherus were rival suitors for the hand of Nanna, daughter of Gewar, King of Norway. Balderus was a demigod and common steel could not wound his sacred body.

**[S14]** Wikipedia, "Völuspá", revision 1315226517 (5 October 2025). https://en.wikipedia.org/wiki/Völuspá — retrieved 2026-10-14.

> Some scholars hold that there are Christian influences in the text, emphasizing parallels with the Sibylline Prophecies.

**[S15]** Wikipedia, "Loki", revision 1373790847 (7 September 2026). https://en.wikipedia.org/wiki/Loki — retrieved 2026-10-14.

> In 1889, Sophus Bugge theorized Loki to be variant of Lucifer of Christianity, an element of Bugge's larger effort to find a basis of Christianity in Norse mythology.
>
> […]
>
> The scholar John Lindow highlights the recurring pattern of the bound monster in Norse mythology as being particularly associated to Loki. Loki and his three children by Angrboda were all bound in some way, and were all destined to break free at Ragnarok to wreak havoc on the world. He suggests a borrowed element from the traditions of the Caucasus region, and identifies a mythological parallel with the "Christian legend of the bound Antichrist awaiting the Last Judgment".

**[S16]** Wikipedia, "Weapons of Norse mythology" (section Mistilteinn), revision 1371559745 (27 August 2026). https://en.wikipedia.org/wiki/Weapons_of_Norse_mythology — retrieved 2026-10-14.

> Mistilteinn (Old Norse, lit. 'Mistletoe'; cf. Old English: Mistiltán; Old Swedish: Misteltein; Swedish: Mistelten) is Hrómundr Gripsson's sword in Hrómundar saga Gripssonar, a legendary saga from Iceland.

**[S17]** Wikipedia, "Prose Edda", revision 1367985894 (6 August 2026). https://en.wikipedia.org/wiki/Prose_Edda — retrieved 2026-10-14. The second segment is the article's quotation of Anthony Faulkes.

> Seven manuscripts of the Prose Edda have survived into the present day: Six copies from the medieval period and another dating to the 1600s. No one manuscript is complete, and each has variations. In addition to three fragments, the four main manuscripts are Codex Regius, Codex Wormianus, Codex Trajectinus, and the Codex Upsaliensis:
>
> […]
>
> Snorri's authorship of the Prose Edda was upheld by the renaissance scholar Arngrímur Jónsson (1568–1648), and since his time it has generally been accepted without question. But the surviving manuscripts, which were all written more than half a century after Snorri's death, differ from each other considerably and it is not likely that any of them preserves the work quite as he wrote it.

**[S18]** Wikipedia, "Frigg", revision 1372114178 (30 August 2026). https://en.wikipedia.org/wiki/Frigg — retrieved 2026-10-14. The translator of the quoted Gylfaginning lines is not named in the fetched extract. These lines are the nearest fetched match to the bridge's epigraph (C1, C12).

> Frigg explains that "Weapons and wood will not hurt Baldr. I have received oaths from them all." The woman asks Frigg if all things have sworn not to hurt Baldr, to which Frigg notes one exception; "there grows a shoot of a tree to the west of Val-hall. It is called mistletoe. It seemed young to me to demand the oath from."

**[S19]** Wikipedia, "Húsdrápa", revision 1273392099 (2 February 2025). https://en.wikipedia.org/wiki/Húsdrápa — retrieved 2026-10-14.

> Húsdrápa (Old Norse: 'House-Lay') is a skaldic poem partially preserved in the Prose Edda where disjoint stanzas of it are quoted. It is attributed to the skald Úlfr Uggason. The poem describes mythological scenes carved on kitchen panels. In the stanzas that have come down to us three such scenes are described.

**[S20]** Sharon Choe, "'Hann var blindr': The Function of Disability in the Aftermath of Ragnarǫk", *Mirator* 20:2 (2021), 5–20, CC BY-NC-ND 4.0. https://journal.fi/mirator/article/view/91899 — retrieved 2026-10-14 (WebFetch; the article page summary and the PDF at https://journal.fi/mirator/article/download/91899/60267/187125). The PDF's text layer extracted only in fragments, so no quotation is used. Paraphrase, without quotation marks: Choe argues that Höðr, a minor and neglected figure, is one of the most important actors in the fall of the Æsir; that Snorri's Edda is the only source that describes his blindness, which the eddic poems do not mention; that Snorri's handling of him reflects the shift towards ecclesiastical power in thirteenth-century Iceland; that the reunion of Baldr and Höðr after Ragnarök suggests reconciliation and an end to the cycle of vengeance; and that a Höðr whose impairment is cleansed in the new world fits the patristic idea of the body perfected at the resurrection, a Christian frame. Choe also argues that by giving Loki an explicit motive and more agency than earlier tradition, Snorri lays a clearer Christian structure over older material; notes that the poetic versions show no interference from Loki at the shot; cites John Stanley Martin's view that Loki's part is a late development in the tradition; and cites Vésteinn Ólason's caution that Christian parallels are easily found by Christian readers. [fetched; paraphrased]

**Not fetched, named for completeness.** Anthony Faulkes's translation of the *Edda* (Everyman, 1987), which the corpus's epigraphs appear to follow; Lindow (1997) itself; Anatoly Liberman, "Some Controversial Aspects of the Myth of Baldr", *Alvíssmál* 11 (2004), 17–54 (no copy found; a search summary said Liberman takes the mistletoe to have been another plant originally, which is not relied on here); Merrill Kaplan's argument on oath-age (known here only through S13); J. Z. Smith, "Dying and Rising Gods" (1987); Tryggve Mettinger, *The Riddle of Resurrection* (2001); Sophus Bugge, *Studier over de nordiske Gude- og Heltesagns Oprindelse* (1881–89); Edward Pettit, *The Poetic Edda: A Dual-Language Edition* (Open Book Publishers, 2023), blocked by a bot check.

## 5. Claims ledger

Paths are relative to `corpus/` unless they begin otherwise. Film-slate runners sit at root line + offset (§1). "Ruler" names the excerpt that decides the row; "—" means the row turns on the corpus's own wording or on a register clause. The verdict is the gatherer's proposal. The writing hand ruled on 14 October 2026 (last column), accepting the proposals after re-fetching P6, P8, P9, P10 and P18b and finding the load-bearing quotations verbatim; and any correction to a corpus file goes through `/weed`. The last column is left empty for the hand's ruling, which `slate_v2.py` reads for the `ruled` gate.

| ID | claim as the corpus states it | path:line | ruler | proposed verdict | note | ruling (writing hand) |
|---|---|---|---|---|---|---|
| C1 | Epigraph in marks, attributed to Gylfaginning: "Then Frigg said: 'Things have sworn oaths not to hurt Balder — fire and water, iron and all kinds of metal, stones, the earth, trees, diseases, the animals, the birds, poisons, serpents.' Then said Loki: 'Has everything sworn oaths not to hurt Balder?' Frigg answered: 'There grows a shoot of a tree to the west of Valhalla. It is called mistletoe. It seemed young to me to demand the oath of.'" | fiction-bridges/balder-the-light-that-learned-the-dark.md:5 | P5, P10, S18 | correct → wording | The oath list is Snorri's narration, not Frigg's speech; her words are "Neither weapons nor trees may hurt Baldr: I have taken oaths of them all." The questioner is "the woman", Loki disguised. The mistletoe sentence is near the unnamed translation in S18 ("Val-hall", "from"). Name the translation and quote it as printed, or quote Brodeur. | correct → as proposed |
| C2 | "Balder the beautiful is dead, is dead!" — Matthew Arnold, "Balder Dead" | fiction-bridges/balder-the-light-that-learned-the-dark.md:8 | P29, P30 | correct → wording | The line is Longfellow's, "Tegnér's Death" in *The Seaside and the Fireside*: "Balder the Beautiful / Is dead, is dead!" The fetched text of Arnold's "Balder Dead" does not contain it. Runner: film 29:57. | correct → as proposed |
| C3 | "Untested virtue is no virtue at all." — Paraphrase of Kierkegaard | fiction-bridges/balder-the-light-that-learned-the-dark.md:14 | — | correct → wording | 2026-09-08 clause: a paraphrase carries no marks. No Kierkegaard text checked. | correct → as proposed |
| C4 | "The wound is the place where the Light enters you." — Rumi | fiction-bridges/balder-the-light-that-learned-the-dark.md:11 | — | mark | Not checked in this task; no Persian source or translation named. Outside the topic; listed because it is a quotation. | mark |
| C5 | "He is not the most just — that is Tyr." | fiction-bridges/balder-the-light-that-learned-the-dark.md:23 | P4 | correct → wording | Snorri calls Týr "most daring" and wise; "the best seat of judgment among gods and men" is Forseti's, Baldr's own son. | correct → as proposed |
| C6 | Snorri in marks: "He is the best of them and everyone praises him… He is the wisest of the Aesir and the most beautifully spoken and the most merciful." | fiction-bridges/balder-the-light-that-learned-the-dark.md:25 | P1, P2 | correct → wording | Wording is not Brodeur's; translator unnamed. The quotation stops before the clause that ends Snorri's sentence: Brodeur "that none may gainsay his judgments"; Old Norse "at engi má haldast dómr hans", which read word for word says no judgment of his may hold. Name the translation and keep the clause. | correct → as proposed |
| C7 | "Notice what Snorri does not say… He says Balder is *beautiful*, *merciful*, and *praised*." | fiction-bridges/balder-the-light-that-learned-the-dark.md:27 | P1, P2 | mark | Rests on the truncated quotation of C6. Snorri's next words are about Baldr's judgments, the one place he gives Baldr a function; on the word-for-word reading of the Old Norse, those judgments do not hold. | mark |
| C8 | "Tammuz in Mesopotamia — the shepherd-god whose annual death and return marked the seasons" (with Osiris, Adonis, Christ as one pattern) | fiction-bridges/balder-the-light-that-learned-the-dark.md:29 | S8 | mark | Frazer's category. By the end of the twentieth century the consensus held that most of Frazer's gods "only died and did not rise"; Mettinger dissents. | mark |
| C9 | Baldrs draumar "opens with this crisis… Over and over, in the dark behind his closed divine eyes, Balder watches himself die." | fiction-bridges/balder-the-light-that-learned-the-dark.md:43 | P18, P5 | correct → wording | No source gives the dreams' content: "Why baleful dreams to Baldr had come" (P18); "great and perilous dreams touching his life" (P5). | correct → as proposed |
| C10 | Odin "wakes her from her grave with rune-songs and demands to know why Hel's halls are decorated as if for a feast… Mead has been brewed for Balder." | fiction-bridges/balder-the-light-that-learned-the-dark.md:53 | P18 | correct → wording | "Magic he spoke and mighty charms"; no runes. Benches "bright with rings", platforms "bedecked with gold", mead brewed for Baldr: stands. The bridge omits that the seeress names Höðr as killer and Váli as avenger (P18b). | correct → as proposed |
| C11 | Frigg extracts oaths: "Fire… Water… Iron… Every metal, every stone, every disease, every poison, every beast, every bird, every serpent" | fiction-bridges/balder-the-light-that-learned-the-dark.md:61–63 | P5 | stands | Snorri's list: fire, water, iron, metal of all kinds, stones, earth, trees, sicknesses, beasts, birds, venom, serpents. "Walks the entire manifest universe" is the bridge's image. | stands |
| C12 | "The Prose Edda gives her reason: 'It seemed young to me to demand the oath of.'" | fiction-bridges/balder-the-light-that-learned-the-dark.md:75 | P5, P10, S18 | correct → wording | Sense stands. Brodeur: "I thought it too young to ask the oath of"; Old Norse "Sá þótti mér ungr at krefja eiðsins". Name the translation. | correct → as proposed |
| C13 | "Not a tree, not an herb — a parasitic plant that grows between earth and sky, touching neither" | fiction-bridges/balder-the-light-that-learned-the-dark.md:75 | P5, P10, P19, P19b, S5 | correct → wording | Snorri calls it "a tree-sprout" (*viðarteinungr*). Völuspá has it "Full grown in strength", standing higher than the fields. "Between earth and sky" is in neither source; Frazer opens his Balder chapter on a god "neither in heaven nor on earth but between the two" (S5). | correct → as proposed |
| C14 | Pliny "describes druids harvesting mistletoe from oak trees with golden sickles on the sixth day of the moon — a ritual that required the plant to be caught in a white cloth before it touched the ground, because its power resided in its *betweenness*" | fiction-bridges/balder-the-light-that-learned-the-dark.md:91 | P28, S5 | correct → wording | Pliny (in Frazer's version) gives the white robe, golden sickle, white cloth and sixth day. The rule against touching the earth belongs to a separate passage on Italian medical use (first day of the moon, no iron), which Frazer joins to the druids. "Betweenness" is Frazer's framing, not Pliny's. | correct → as proposed |
| C15 | "Not the sky-realm (Frigg asked fire and air)." | fiction-bridges/balder-the-light-that-learned-the-dark.md:93 | P5 | correct → wording | Air is not in Snorri's list. | correct → as proposed |
| C16 | "Loki finds the mistletoe." (Loki bridge: "Loki finds the mistletoe. Loki fashions it into a dart.") | fiction-bridges/balder-the-light-that-learned-the-dark.md:97; fiction-bridges/loki-the-lie-that-tells-the-truth.md:71 | P5, P6, P10, P19 | correct → wording | Loki learns of it from Frigg, whom he visits at Fensalir "in the likeness of a woman", and "pulled it up". No fashioning is described; he hands Höðr "this wand" (*vendi þessum*). Völuspá: "a harmful shaft" came from the branch. | correct → as proposed |
| C17 | Loki: "I will guide your hand. Here is something to throw — a dart." (Höðr synthesis: "*here, I will guide your hand.*") | fiction-bridges/balder-the-light-that-learned-the-dark.md:133; synthesis/grown/hodr-the-blind-hand.md:34 | P6, P10, S2 | correct → wording | Snorri: "I will direct thee where he stands; shoot at him with this wand"; Höðr shot "being guided by Loki" (*at tilvísun Loka*, by Loki's direction). "Guided" stands; the guided *hand* first appears in the fetched material in Bellows' 1923 retelling (S2). Runner: film 30:5 ("a guiding hand still resting at his wrist"). | correct → as proposed |
| C18 | "Balder is placed on Hringhorni — his ship, the greatest ship ever built. Nanna… her heart bursts… She is placed on the ship beside him." | fiction-bridges/balder-the-light-that-learned-the-dark.md:159 | P7 | stands | "Hringhorni is the name of Baldr's ship: it was greatest of all ships"; Nanna's heart bursts; she is "borne to the pyre". Hyrrokkin's launch is omitted. | stands |
| C19 | "Odin places the ring Draupnir on Balder's body… every nine nights, drips eight new rings of equal weight" | fiction-bridges/balder-the-light-that-learned-the-dark.md:161 | P7 | stands | "laid on the pyre"; "every ninth night there dropped from it eight gold rings of equal weight". The motive ("what's the point of infinite abundance…") is the bridge's. | stands |
| C20 | "Thor consecrates the pyre with Mjolnir." | fiction-bridges/balder-the-light-that-learned-the-dark.md:163 | P7 | stands | "hallowed the pyre with Mjöllnir". Thor's kick of the dwarf Litr into the fire is omitted. | stands |
| C21 | "The fire is lit. Hringhorni sails burning into the sea." | fiction-bridges/balder-the-light-that-learned-the-dark.md:165 | P7 | correct → wording | The gods cannot launch the ship; Hyrrokkin thrusts it out "so that fire burst from the rollers"; the body is borne on board and "fire was kindled". No sailing is described. Runners: film 29:9 ("burns into the sea"), film 29:214. | correct → as proposed |
| C22 | "Every being in creation weeps… the very substances that swore to protect Balder now weep for his death" (placed at the funeral) | fiction-bridges/balder-the-light-that-learned-the-dark.md:167 | P6, P9 | correct → wording | At the death "weeping broke out" among the Æsir. The weeping of all things comes later, as Hel's condition, after Hermóðr returns. Runner: film 29 header line 9 ("burns into the sea while all creation weeps"). | correct → as proposed |
| C23 | "Hermod… volunteers to ride to Hel… Odin gives him Sleipnir" | fiction-bridges/balder-the-light-that-learned-the-dark.md:179 | P6 | stands | Frigg asks for a rider; Hermóðr "undertook that embassy"; "Sleipnir was taken, Odin's steed". Sleipnir's birth from Loki (Gylfaginning XLII) was not excerpted and is not ruled. | stands |
| C24 | "Hermod rides for nine nights through valleys so deep and dark that he sees nothing." | fiction-bridges/balder-the-light-that-learned-the-dark.md:181 | P8 | stands | "nine nights through dark dales and deep, so that he saw not". | stands |
| C25 | Módguðr "tells him a remarkable thing: she heard more noise from Balder's single passage than from five troops of dead men riding over her bridge… Balder crossed with the sound of an army. His death disturbed the infrastructure of death itself." | fiction-bridges/balder-the-light-that-learned-the-dark.md:183 | P8, P10, P30 | pull | The source says the opposite. Five companies of dead crossed the day before, "but the bridge thunders no less under thee alone, and thou hast not the color of dead men": the noise is under Hermóðr, the living rider (*undir einum þér*). Baldr's crossing is reported without sound. Arnold's 1855 poem has it right. The paragraph's inference rests on the misreading. Runner: film 29:232. | pull |
| C26 | "Hermod finds Balder in Hel's hall. Not in torment — *seated in the place of honour*." | fiction-bridges/balder-the-light-that-learned-the-dark.md:185 | P8 | stands | "saw sitting there in the high-seat Baldr, his brother". | stands |
| C27 | "He sends back Draupnir — returning Odin's ring, refusing to keep the gift that was given in grief. He sends his wife Nanna's linen back to Frigg and her gold ring to the goddess Fulla." | fiction-bridges/balder-the-light-that-learned-the-dark.md:187 | P8 | correct → wording | Baldr sends Draupnir to Odin "for a remembrance" (*til minja*); Nanna, not Baldr, sends Frigg "a linen smock, and yet more gifts" and Fulla "a golden finger-ring". The refusal is not in the text. | correct → as proposed |
| C28 | "Hel — the goddess, the ruler of the dead, half-living and half-dead herself" (nine-realms: "Hel's literally split body — half alive, half dead") | fiction-bridges/balder-the-light-that-learned-the-dark.md:189; synthesis/cosmological/nine-realms-density-cosmology.md:204 | P4 | mark | Snorri gives colours: "half blue-black and half flesh-color". The living/dead gloss is common but is not the text. | mark |
| C29 | Hel's terms: "if every thing in the world weeps for Balder, he may return. If even one thing refuses to weep, he stays." | fiction-bridges/balder-the-light-that-learned-the-dark.md:189 | P8 | stands | "If all things in the world, quick and dead, weep for him… but he shall remain with Hel if any gainsay it or will not weep." | stands |
| C30 | "Hel is asking: *does creation actually love Balder, or did creation merely agree to protect him?*" | fiction-bridges/balder-the-light-that-learned-the-dark.md:191 | P8, P10 | stands | Snorri frames the condition as a test "whether Baldr were so all-beloved as had been said" (*hvárt Baldr var svá ástsæll sem sagt er*). | stands |
| C31 | Stones "weep the way you've seen frost weep off stones when coming out of cold into warmth" | fiction-bridges/balder-the-light-that-learned-the-dark.md:201 | P9 | stands | "even as thou must have seen that these things weep when they come out of frost and into the heat". | stands |
| C32 | Thökk's verse in marks: "Thokk will weep dry tears / for Balder's funeral. / Neither alive nor dead / did the old man's son do me any good. / Let Hel hold what she has." | fiction-bridges/balder-the-light-that-learned-the-dark.md:209–213 | P9, P10 | correct → wording | No translator named; matches no fetched translation. Brodeur: "Thökk will weep / waterless tears / For Baldr's bale-fare; / Living or dead, / I loved not the churl's son; / Let Hel hold to that she hath!" The bridge's "do me any good" is nearer the Old Norse *nautk-a ek* than Brodeur's "loved not", so the sense is defensible; the quotation needs a named source. | correct → as proposed |
| C33 | "The Prose Edda adds: 'It is presumed that this was Loki Laufeyarson, who did the most evil among the Aesir.'" | fiction-bridges/balder-the-light-that-learned-the-dark.md:217 | P9, P10 | correct → wording | Brodeur: "And men deem that she who was there was Loki Laufeyarson, who hath wrought most ill among the Æsir." Sense stands; name the translation. | correct → as proposed |
| C34 | "Thokk is Loki." | fiction-bridges/balder-the-light-that-learned-the-dark.md:219 | P9, P10, S12 | correct → wording | Snorri reports a supposition (*þess geta menn*, people guess). He is the only fetched source to make the identification. Suggested: "Snorri reports that people supposed Thökk was Loki." | correct → as proposed |
| C35 | "This is not malice. This is *truth*. Balder's light… never reached the cave where Thokk lives." | fiction-bridges/balder-the-light-that-learned-the-dark.md:225 | P9, P10 | mark | A reading. The verse's stated reason is personal: Baldr did her no good, alive or dead (Old Norse), or she "loved not the churl's son" (Brodeur), a contemptuous phrase. Nothing in the source concerns light or reach. Label it as the corpus's reading. | mark |
| C36 | "Thokk's cave — the deepest, coldest, most hidden place in creation" | fiction-bridges/balder-the-light-that-learned-the-dark.md:229 | P9, P10 | correct → wording | "in a certain cave" (*í helli nökkurum*). | correct → as proposed |
| C37 | "Christ dies and returns in three days. Osiris… in a season. Adonis… annually. Tammuz… In every other death-and-return myth, the return is *swift*." | fiction-bridges/balder-the-light-that-learned-the-dark.md:241 | S8, P27 | mark | Frazer's category, rejected as a general class by Smith and much later work (S8). Saxo's Balderus dies "when three days had passed" from his wound (P27). | mark |
| C38 | "The Völuspá, the most ancient and authoritative of the Norse prophetic poems" | fiction-bridges/balder-the-light-that-learned-the-dark.md:263 | S1 | correct → wording | Bellows: "the most famous and important, as it is likewise the most debated, of all the Eddic poems"; dated by him to the mid-tenth century, with "evidences of Christian influence… sufficiently striking". "Most ancient" is not supported. | correct → as proposed |
| C39 | Völuspá in marks: "Unsown shall the fields bear fruit, / all evil shall be healed, / Balder shall come." | fiction-bridges/balder-the-light-that-learned-the-dark.md:265–267 | P22, P22b | correct → wording | No translator named. Bellows: "Then fields unsowed bear ripened fruit, / All ills grow better, and Baldr comes back"; Old Norse *böls mun alls batna*. | correct → as proposed |
| C40 | "*all evil shall be healed*. Not punished… The Norse tradition resolves evil through *healing*… a radical departure from almost every apocalyptic tradition, which resolves evil through judgment and separation." | fiction-bridges/balder-the-light-that-learned-the-dark.md:273 | P13, P20, P22 | correct → wording | Völuspá itself has Nastrond, where "Treacherous men and murderers too" wade venom rivers, and Gimle, where "the righteous rulers dwell". Snorri puts these in the world after the burning: "the good abodes shall be many, and many the ill", with oath-breakers and murderers in Nástrand. The sources do judge and separate. Völuspá 62's line stands; the contrast does not. | correct → as proposed |
| C41 | "What the sources describe instead is a Balder who *reconciles*. He dwells in peace with Hodr… They share the renewed hall." | fiction-bridges/balder-the-light-that-learned-the-dark.md:277 | P14, P22, P22b, S2, S7 | correct → wording | Völuspá 62: "Baldr and Hoth dwell in Hropt's battle-hall". Gylfaginning 53: they come from Hel and "all shall sit down together and hold speech". No source says "reconciled" or "in peace". The reading is Bellows' note ("their union being a symbol of the new age of peace") and Lindow's, where reconciliation follows revenge. Runner: film 29 header line 9 ("dwells in peace with the blind brother"). | correct → as proposed |
| C42 | "The reconciliation with Hodr is the proof that Thokk's cave has been reached." | fiction-bridges/balder-the-light-that-learned-the-dark.md:281 | — | mark | The corpus's inference; no source joins Thökk to the return. | mark |
| C43 | "The Balder-Christ parallel is not analogy. It is structural identity — two mythological systems encoding the same consciousness technology through different cultural containers." | fiction-bridges/balder-the-light-that-learned-the-dark.md:287 | S1, S6, S9, S14, S15, S20 | mark | A copula on a checkable claim (2026-06-24 clause). "Identity" through independent encoding needs independence, and derivation is not excluded: the fullest Baldr story was written in Christian Iceland (S6, S17); Christian influence on Völuspá is argued (S1, S14); Bugge's derivation thesis was rejected but has had influence (S9). The cycle's own thread note concedes the bridge argues "pattern rather than derivation" (threads/norse-anamnesis-cycle.md:28). State it as an analogy and name derivation as the rival explanation. | mark; the film states the Christ parallel as an analogy and names derivation as the rival explanation |
| C44 | "Both are killed through an instrument that shouldn't be lethal — a mistletoe twig, a wooden cross." | fiction-bridges/balder-the-light-that-learned-the-dark.md:289 | — | mark | A cross is an instrument of execution. Minor. | mark |
| C45 | Epigraph in marks, "Gylfaginning, the Prose Edda": "Thökk will weep dry tears for Balder's death. Let Hel hold what she has." (Seed: same words.) | synthesis/grown/thokk-the-cave-the-light-never-reached.md:11; seeds/thokk-the-cave-the-light-never-reached.md:9 | P9, P10 | correct → wording | Two lines of a six-line verse joined without an ellipsis; "death" stands for *bálfarar*, the funeral burning (Brodeur "bale-fare"); translator unnamed. | correct → as proposed |
| C46 | "Ragnarök is now inevitable." | synthesis/grown/thokk-the-cave-the-light-never-reached.md:20 | P9, P11 | mark | Not stated at this point in any source; Snorri turns next to Loki's punishment. | mark |
| C47 | "The myth strongly hints that Thökk is Loki in disguise" | synthesis/grown/thokk-the-cave-the-light-never-reached.md:20 | P9, P10 | correct → wording | The story does not hint; the narrator reports what people suppose (*þess geta menn*). | correct → as proposed |
| C48 | "the single most unanimous moment in all of Norse myth, the one time gods and giants and stones and beasts agree on anything" | synthesis/grown/thokk-the-cave-the-light-never-reached.md:36 | P9 | correct → wording | Snorri's weepers are "all men… and quick things, and the earth, and stones, and trees, and all metals". Giants are not among them; the one who refuses is a giantess. | correct → as proposed |
| C49 | "The myth itself winks: *men hafa þat fyrir satt at þar hafi verit Loki* — 'people hold it for true that this was Loki.'" | synthesis/grown/thokk-the-cave-the-light-never-reached.md:38 | P10 | pull | The Old Norse of the fetched edition reads "En þess geta menn, at þar hafi verit Loki Laufeyjarson": people guess, or suppose. The quoted Old Norse does not occur, and its gloss turns a guess into a held truth. Remove the invented Old Norse and quote the edition. Runner: film 08:83. | pull |
| C50 | "The being who arranged the death, who guided the blind brother's hand, who alone knew mistletoe was unsworn" | synthesis/grown/thokk-the-cave-the-light-never-reached.md:38 | P5 | correct → wording | Frigg knew it and told him. | correct → as proposed |
| C51 | "the texts are explicit… that a flower is named for the whiteness of his brow" | synthesis/grown/thokk-the-cave-the-light-never-reached.md:52 | P1, P2 | correct → wording | "A certain herb is so white that it is likened to Baldr's brow" (*jafnat er til Baldrs brár*). The text likens; it does not name. | correct → as proposed |
| C52 | "dwelling in the bright hall Breiðablik into which nothing unclean may come" | synthesis/grown/thokk-the-cave-the-light-never-reached.md:68 | P1 | stands | "in that place may nothing unclean be". | stands |
| C53 | "the Balder who returns is **not the Balder who died**." | synthesis/grown/thokk-the-cave-the-light-never-reached.md:90; also fiction-bridges/balder-the-light-that-learned-the-dark.md:233, fiction-bridges/loki-the-lie-that-tells-the-truth.md:83, synthesis/cosmological/post-ragnarok-cycles.md:12, fiction-bridges/thor-the-hammer-and-the-walking-stick.md:199 | P14, P22 | mark | No source describes a changed Baldr: "Baldr comes back" (Völuspá); he comes from Hel and sits and talks (Gylfaginning 53). The change is the corpus's construction; label it so. | mark |
| C54 | "For a thousand years the world looked at the giantess in the cave and saw a villain." | synthesis/grown/thokk-the-cave-the-light-never-reached.md:160 (also :18) | S17, S20 | mark | No reception history is cited. The one telling is Snorri's, dated c. 1220 (S20), surviving in manuscripts written more than half a century after his death (S17). | mark |
| C55 | Epigraph in marks, "after Snorri Sturluson, Gylfaginning": "Höðr was blind. The gods stood in a ring and threw at Balder for sport, and nothing harmed him, and Höðr stood apart because he had nothing to throw and could not see to throw it." | synthesis/grown/hodr-the-blind-hand.md:11 | P5, P6 | correct → wording | A paraphrase in marks (2026-09-08 clause). Snorri: Baldr stood up in the Thing while the others shot, hewed and threw stones; "Hödr stood outside the ring of men, because he was blind." | correct → as proposed |
| C56 | "Loki comes with one fact nobody else has — that the mistletoe was too young to swear the oath" | synthesis/grown/hodr-the-blind-hand.md:34 | P5 | correct → wording | Frigg had the fact and gave it to him. | correct → as proposed |
| C57 | Dialogue in marks: "*'Why do you not shoot at Balder?'* Loki asks. *'Because I am blind,'* says Höðr, *'and I have no weapon.'*" | synthesis/grown/hodr-the-blind-hand.md:34 | P6, P10 | correct → wording | Brodeur: "'Why dost thou not shoot at Baldr?' He answered: 'Because I see not where Baldr is; and for this also, that I am weaponless.'" Höðr does not call himself blind; the narrator does. | correct → as proposed |
| C58 | "Höðr only wanted, for once, to be included in the joy." | synthesis/grown/hodr-the-blind-hand.md:36 | P6 | mark | Interiority the source does not give. The nearest words are Loki's: "show Baldr honor as the other men do." | mark |
| C59 | Höðr throws "without knowing the dart is deadly, without bearing his brother any malice at all" | synthesis/grown/hodr-the-blind-hand.md:20 | P6, P4 | mark | Snorri states no motive for Höðr. The gods "were of one mind as to him who had wrought the work" and would wish the god never named. Innocence is a fair inference from the deception, not a statement of the text. | mark |
| C60 | "the myth says they are reconciled" (synthesis); "the myth says they are *reconciled*" (seed) | synthesis/grown/hodr-the-blind-hand.md:76; seeds/hodr-the-blind-hand.md:21; seeds/the-green-world-after-ragnarok.md:19; synthesis/grown/the-green-world-after-ragnarok.md:82; synthesis/capstones/the-tree-inside-which-the-gods-run.md:130 | P14, P22, P22b, S2, S7 | correct → wording | As C41. "Dwell together" stands; "reconciled" is Bellows' and Lindow's reading, not the myth's word. | correct → as proposed |
| C61 | "This is not what a justice-myth would do. A justice-myth would punish Höðr — exile him from the renewal, mark him… The Norse cosmology does the opposite, and the opposite is the teaching." | synthesis/grown/hodr-the-blind-hand.md:78 | P18b, P19, P15, P6, S2, S4, S6, S7, S10 | pull | The sources make Höðr's killing in vengeance a fixed part of the story. Baldrs draumar: "Rind bears Vali in Vestrsalir, / And one night old fights Othin's son; / … / Till the slayer of Baldr he brings to the flames." Völuspá: "Till he bore to the bale-blaze Baldr's foe." Skáldskaparmál: Váli is "Baldr's Avenger, Foe and Slayer of Hödr". Saxo's Bous kills Hother. Snorri's gods hold back only because "so great a sanctuary was in that place". Höðr is in Hel to come back from because he was killed. Runner: film 30:124. | pull; the film tells Váli |
| C62 | "The resolution is not the *punishment* of Höðr, because Höðr was never guilty in the punishable sense" | synthesis/grown/hodr-the-blind-hand.md:78–80 | P6, P18b, P19 | correct → wording | As C61: the sources record a vengeance killing. Whether a modern reader calls Höðr guilty is the corpus's question, not the myth's answer. | correct → as proposed |
| C63 | "In the green world, Höðr is presumably *no longer blind*" | synthesis/grown/hodr-the-blind-hand.md:82 (also :84) | P14, P22, S20 | mark | No source mentions sight restored. Choe reads a healed Höðr as the patristic idea of the body perfected at the resurrection: the reading belongs to a Christian frame. Runner: film 30:128. | mark |
| C64 | "The green world is the world in which that channel is closed: Höðr can see" | synthesis/grown/hodr-the-blind-hand.md:128 | — | mark | Asserted without the "presumably" of line 82. Runners: film 30:11 ("where Hodr returns able to see"), film 30:174. | mark |
| C65 | "Höðr's blindness was literal and total… That is innocence of a pure kind, and the myth grants it." | synthesis/grown/hodr-the-blind-hand.md:94 | P4, P15, P18, P19, P26, S4, S10, S20 | mark | The blindness is Snorri's (Gylfaginning 28 and 49; "the Blind God" in Skáldskaparmál). The fetched Völuspá and Baldrs draumar do not mention it; Saxo's Hother is sighted; skalds use Höðr in warrior-kennings. The older poems grant no innocence; they record his killing. | mark |
| C66 | "They hunt the trickster down after he engineers the death of Balder. They turn his own son into a wolf to disembowel another son, and from those entrails they forge the chains" | synthesis/grown/sigyn-staying-with-the-trickster.md:18 | P11, P24, S3 | stands | Gylfaginning 50. The Lokasenna prose reverses the sons ("bound with the bowels of his son Vali, but his son Narfi was changed to a wolf") and does not tie the binding to Baldr (S3). | stands |
| C67 | "They fix him beneath a serpent set to drip venom on his face forever" (Loki bridge: "for eternity") | synthesis/grown/sigyn-staying-with-the-trickster.md:18; fiction-bridges/loki-the-lie-that-tells-the-truth.md:93, :171 | P11 | correct → wording | "There he lies in bonds till the Weird of the Gods." Skaði fastens the serpent. Runner: film 07 header line 9. | correct → as proposed |
| C68 | "and then — having done justice, or vengeance, or both — *they leave.* The gods of action act, and then they go home." | synthesis/grown/sigyn-staying-with-the-trickster.md:18, :42; synthesis/grown/the-binding-of-loki-chaining-the-exhale.md:18 | P11, P24 | mark | Neither prose account says the gods leave; the scene ends on the binding. Runner: film 07 header line 9 ("they went home"). | mark |
| C69 | Sigyn "has no illusions about what her husband did, no enabling story, no plea of innocence"; "She knows exactly what he did — that the venom… is, in a real sense, *deserved.*" | synthesis/grown/sigyn-staying-with-the-trickster.md:22, :40; seeds/sigyn-staying-with-the-trickster.md:15 | P19, P19b, P11, P24 | mark | No source gives Sigyn a view of his guilt. The one line on her state is Völuspá 35: she sits by him "nor is glad / To see her mate" (*þeygi of sínum ver vel glýjuð*). The three refusals are the corpus's construction; offer them as such. | mark |
| C70 | "she holds a bowl over his face to catch the venom before it falls. And when the bowl fills and she must turn to empty it, the venom strikes, and Loki convulses, and the writhing… is what the old stories called the earthquake." | synthesis/grown/sigyn-staying-with-the-trickster.md:22, :70 | P11, P24 | stands | Gylfaginning 50 ("basin") and the Lokasenna prose ("shell"). These two prose passages are the only attestations of the bowl; Völuspá 35 has Sigyn without it (S3, S11). | stands |
| C71 | Loki "will one day break free and steer the ship of the dead to Ragnarök" | synthesis/grown/sigyn-staying-with-the-trickster.md:34 | P21, P12 | stands | Völuspá: a ship "With the people of Hel, at the helm stands Loki". Snorri's prose gives Naglfar to Hrymr and has "All the champions of Hel follow Loki". | stands |
| C72 | "Frigga knew Balder would die. She knew the means, perhaps. And she did not — could not, would not — break the silence that the structure of fate required." (True-mirror: "Frigga knew Baldr's death and did not speak it") | synthesis/grown/sigyn-staying-with-the-trickster.md:86; synthesis/grown/the-true-mirror-wager.md:128; seeds/frigga-the-one-who-knew-and-did-not-tell.md:11 | P3, P23, P5 | correct → wording | Her general foreknowledge is attested: "The fate of all does Frigg know well, / Though herself she says it not." But in Gylfaginning 49 she acts (takes oaths) and she speaks: she tells the disguised Loki that the mistletoe is unsworn because she "thought it too young". The means was the one thing she did not treat as a threat, and the one thing she told. | correct → as proposed |
| C73 | "This is Ragnarök's Loki: the trickster who, after an age bound and abandoned beneath the serpent, breaks his chains and steers the ship of the dead against the gods who left him." | synthesis/grown/sigyn-staying-with-the-trickster.md:110 | P11, P19, P24, P12 | correct → wording | No source abandons Loki: Sigyn "stands near him", "By his side does Sigyn sit", "Sigyn… sat there". He still leads Hel's champions, and he and Heimdallr kill each other. | correct → as proposed |
| C74 | "**the only bound thing that can ever be safely released is one that was never abandoned in its binding.**" | synthesis/grown/sigyn-staying-with-the-trickster.md:114 | P11, P12, P19 | mark | On the myth's own sequence the bound Loki who was not abandoned returns as an enemy and dies fighting. The claim is the corpus's proposal, and the myth it cites runs against it. Offer it as a proposal with the counter-case named. Runner: film 07 header line 9. | mark |
| C75 | Sigyn "maintains the possibility that what comes after Ragnarok includes Loki rather than excludes him" (Feeding-the-wolf: "an eventual integration that the myth defers to after Ragnarök") | fiction-bridges/loki-the-lie-that-tells-the-truth.md:235; synthesis/grown/feeding-the-wolf.md:70 | P12, P14 | mark | Loki and Heimdallr each kill the other; no source returns Loki or defers his integration. | mark |
| C76 | "the entrails of his own son Narfi — killed before Loki's eyes" | fiction-bridges/loki-the-lie-that-tells-the-truth.md:171 | P11 | correct → wording | The place of the killing relative to Loki is not stated. | correct → as proposed |
| C77 | Heimdall "watches Loki engineer Balder's death… watches the most beautiful god die and does not intervene." | fiction-bridges/heimdall-the-god-who-watched.md:213 | P5, P6, P7, P16 | mark | Heimdallr appears in the Baldr story only at the funeral, riding Gold-Top (P7, P16). | mark |
| C78 | "The Old Norse Völuspá and Snorri's account give us… *böls mun alls batna*… If this were victory, Höðr would be the villain, punished or erased." | synthesis/grown/the-green-world-after-ragnarok.md:86 | P22b, P14, P18b, P19 | correct → wording | The phrase is Völuspá 62's; Snorri's chapter LIII does not contain it. Höðr was punished, killed by Váli, before the renewal. | correct → as proposed |
| C79 | Völuspá in marks: "Höðr and Balder, the gods of slaughter, will live happily together / in the wise gods' dwelling-places." | synthesis/traditions/norse-cosmology.md:167–170 | P22, P22b | mark | Translation unnamed and not traced. Bellows: "Baldr and Hoth dwell in Hropt's battle-hall"; the fetched Old Norse: "búa þeir Höðr ok Baldr / Hrofts sigtoftir, / vé valtíva". "Happily" depends on a reading the fetched edition does not print. | mark |
| C80 | "Baldur returns to rule a renewed world" | synthesis/archetypal/set.md:111 | P14, P22 | correct → wording | He returns and dwells; rule is not stated. | correct → as proposed |
| C81 | "An old woman, Þökk, refusing to weep for Baldur" | synthesis/archetypal/loki-catalyst.md:99 | P9, P10 | correct → wording | A giantess (*gýgr*). The disguise before Frigg is "a woman"; Thökk is a giantess. | correct → as proposed |
| C82 | "The myth's deepest teaching is her *restraint* afterward"; "Frigga, after Balder, looked at the future and saw something to be left *unknown*" | synthesis/grown/the-cabal-prediction-that-kills-itself.md:42, :174 | P6, P19 | mark | No source tells of Frigg after the death beyond her call for a rider and her weeping in Fensalir. | mark |
| C83 | Node essence: "why her dry tears were not malice but the most accurate testimony in the cosmos" | constellation/constellation.json, node `thokk_the_cave_the_light_never_reached` | P9 | mark | The corpus's reading stated as fact in the graph. Outside `corpus/`; listed for `/weed`'s blast radius. | mark; a constellation node, outside corpus/, for /weed's blast radius and Sam's hand |

**Count.** 83 rows: 14 *stands*, 41 *correct → wording*, 25 *mark*, 3 *pull*. By document: Balder bridge 44 rows (10 stand); Thökk 10 (1 stands); Höðr 11 (none stands); Sigyn 9 (3 stand); neighbours 9 (none stands). Of the 74 rows on the four v1 documents, 60 (about 81 per cent) are corrections, marks or pulls. The rows were chosen by an adversarial read, not by extracting every checkable claim, so the figure is not the per-document failure rate the 2026-09-08 log asks for.

## 6. The strongest objection

The objection is John Lindow's method, sharpened by the Christian-influence question and by Saxo. Stated at its strongest:

The death of Baldr survives as a thirteenth-century Icelandic text. Snorri wrote it down around 1220, two centuries after Iceland's conversion around 1000 (S20); the manuscripts that carry it were "written more than half a century after Snorri's death" and "differ from each other considerably" (S17). Lindow's book reads the story "in the context of its thirteenth century recording by paying close attention to the texts themselves rather than to hypothetical background in cult or ritual" (S6), and Siikala's review says his interest is the myth "in forms in which we have it and the meaning it might have borne for those who knew it in those forms" (S7). On that standard the four v1 documents fail twice over. They read Snorri's prose as if it were the myth's oldest layer, and they read the myth as if it were a pre-Christian contemplative technology addressed to a modern reader.

The first failure shows in what the documents build on. Every element they make load-bearing is Snorri's, or later. The blind Höðr is Snorri's: the poems do not mention the blindness, Saxo's Hother can see and is a skilled archer and harper, and skalds use Höðr's name for warriors (P18, P19, P26, S10, S20). Loki's part in the shot is Snorri's; the fetched Book III of Saxo does not name Loki at all. The sport of throwing at the invulnerable god, Frigg's oaths, the unsworn sprout, Hermóðr's ride, the weeping of all things and Thökk are Snorri's prose alone. The identification of Thökk with Loki is Snorri's report of a supposition (P10). Sigyn's bowl is in two prose passages, one of them the closing note of Lokasenna, which Bellows judged a compiler's addition attached to "the wrong incident" (S3). The guided hand and the reconciliation are later still: in the fetched material the first appears only in Bellows' 1923 retelling of Snorri (S2), the second in Bellows' note (S2) and in modern scholarship (S7). When the documents say "the myth says", they usually mean Snorri, sometimes Bellows, and sometimes nobody.

The second failure shows in what the documents find there. The Baldr bridge calls the Baldr–Christ parallel "structural identity — two mythological systems encoding the same consciousness technology". That needs two systems. The parsimonious account has one: a Christian-era author shaping inherited material, with Christian elements visible in Völuspá too (S1, S14) and a long line of scholars, from Bugge on, arguing for Christian and classical sources (S9, S15). The corpus's own convergence method says a resemblance counts as evidence only when the witnesses are independent; here independence is the open question, and the cycle's thread note concedes the bridge argues "pattern rather than derivation" without testing derivation (threads/norse-anamnesis-cycle.md:28). The moral reading has the same shape. The v1 documents find a myth in which the blind killer is not punished, evil is "healed, not conquered", and Höðr returns healed of his blindness. That is close to Christian redemption, and Choe argues that the healed Höðr is a patristic resurrection idea entering Snorri's account (S20). The older poems tell a feud. Baldrs draumar has Odin ask "Who shall vengeance win for the evil work"; Váli is born for the purpose, "one night old", and "brings to the flames" the slayer (P18b); Snorri's gods hold back only because of the sanctuary (P6); Skáldskaparmál names Váli "Foe and Slayer of Hödr" (P15); Saxo's Bous kills Hother (S4). Lindow's reading follows the sources through "Conflict, Climax, Revenge and Reconciliation" (S7). The v1 documents keep the last stage and delete the third.

So the objection does not say that the corpus's readings are worthless. It says that they are readings of a Christian-era literary text and of its modern retellings, offered as the meaning of a pre-Christian myth, and that the parts most useful to the readings (the innocent blind instrument, the light that never reached the cave, the bowl as non-abandonment, the healing instead of judgment) are the parts least attested and most open to a Christian explanation.

**Where the objection is weaker.** Bugge's general thesis was "generally vehemently rejected" (S9), and Bellows held the Völuspá poet "heathen and not Christian" (S1). Baldr's death and return are in Völuspá, and his funeral was pictured in a hall and described by a skald whose stanzas Snorri quotes (P16, S19), so the core is not Snorri's invention. Choe, who argues for Christian reworking in Snorri, herself cites Vésteinn Ólason's caution that a Christian parallel is easily found by Christian readers and may have meant nothing of the kind to a poem's first audience, and writes that claiming explicit Christian parallels in the Norse material carries a danger (S20, paraphrased). Sigyn by the bound Loki is in a skaldic kenning of the ninth century (P17, S11). A medieval Icelandic text is still a myth received by people who knew it, and a modern reading of it is a legitimate kind of work. The objection does not forbid the readings. It requires that they be labelled as readings of Snorri, that "the myth says" be kept for what a source says, and that Váli be told.

## 7. Negative space

What the outside sources show matters and the v1 documents do not have:

1. **Váli and the vengeance.** The single largest absence. Baldrs draumar asks who will avenge Baldr and answers with Váli, born to Rindr, "one night old", unwashed and uncombed until he burns the slayer (P18b); Völuspá repeats it (P19); Skáldskaparmál names Váli "Baldr's Avenger, Foe and Slayer of Hödr" (P15); Snorri lists Váli as "daring in fights, and a most fortunate marksman" (P4); Saxo has Odin beget Bous on Rinda for the purpose (S4). Lindow's reading is built on it (S6, S7). None of the four documents mentions Váli as Höðr's killer; the Höðr synthesis asserts the opposite (C61).
2. **The sanctuary.** The gods know who did it but "none might take vengeance, so great a sanctuary was in that place" (P6). Vengeance is deferred by the sacredness of the place, not refused.
3. **Saxo's whole version.** A human Hother, sighted and accomplished; a demigod Balder who sees Nanna bathing and resolves to kill his rival; wood-maidens; a sword of Miming that can pierce a body "proof even against steel"; a sea-battle in which Hother cuts off Thor's club; snake-venom stirred into Balder's food; a litter; Proserpine in a dream; death after three days; a barrow that floods when robbed (P26, P26b, P27, S4). The invulnerability motif is here too, with a sword as the exception. The edition's introduction asks whether Miming's sword is the mistletoe (S4).
4. **Loki's boast in Lokasenna.** "Mine is the blame that Baldr no more / Thou seest ride home to the hall" (P23). The only place in the poems where Loki claims the killing, and it is said to Frigg's face, after she wishes for "a son like Baldr".
5. **Frigg told.** In Gylfaginning she is not a silent seeress in this story: she acts, and the one fact that kills Baldr is one she tells a stranger (P5). The Frigga seed's frame ("She tells none") meets the one telling that matters (C72).
6. **Baldr's judgments.** Snorri's portrait ends on a clause about his judgments that translators render in opposite senses (P1, P2), and he gives the best seat of judgment to Baldr's son Forseti (P4). The v1 documents quote the portrait without the clause (C6).
7. **The Völuspá mistletoe.** Völuspá's mistletoe stands "Full grown in strength", higher than the fields, "slender and fair" (P19, P19b): not the young sprout of Snorri. The documents' "too small, too young" depends on Snorri alone. Snorri calls it a *viðarteinungr*, a shoot of wood (P10). A sword named Mistilteinn exists in Icelandic saga (S16). Kaplan reads "too young" as legal: the young could not swear oaths (S13).
8. **Thökk's answer to Hel's formula.** Hel's condition is that all things "quick and dead" weep (*kykvir ok dauðir*); Thökk answers "living or dead" (*kyks né dauðs*) (P8, P10). The refusal is phrased as a reply to the condition. Her name means "thanks" (S12). Brodeur's "churl's son" is contempt (P9).
9. **The funeral's detail.** Hyrrokkin on a wolf with a viper bridle; four berserks who have to fell the wolf; fire from the rollers and all lands trembling; Thor's anger at her; the dwarf Litr kicked into the fire; the attendance of Frigg, valkyries, ravens, Freyr's boar, Heimdallr's horse, Freyja's cats, and frost- and hill-giants; Baldr's horse on the pyre (P7, P16). The bridge keeps none of these; it keeps the ship, Nanna, Draupnir and Thor's hallowing.
10. **Odin's word in Baldr's ear.** Vafþrúðnismál ends on "What spake Othin himself in the ears of his son, / Ere in the bale-fire he burned?", a question no one but Odin can answer (P25). The most cinematic unknown in the cycle, absent from all four documents.
11. **The seeress's own close.** Baldrs draumar ends with the seeress refusing further questions "Till Loki wanders loose from his bonds" (P18b), tying Baldr's death to the end.
12. **Judgment after Ragnarök.** Nastrond and Gimle, in Völuspá and in Snorri's description of the world after the burning (P13, P20, P22). The v1 documents say the Norse end has no judgment (C40).
13. **Divergent eschatology.** Vafþrúðnismál lists the surviving gods as Viðarr, Váli, Móði and Magni, with no Baldr or Höðr (S10).
14. **Sigyn's one line.** "nor is glad / To see her mate" (P19); in the Old Norse, not at all glad about her husband (P19b). The only textual window on her, unused.
15. **The Christian-influence debate itself.** Named in §6; the Baldr bridge raises the Christ parallel and does not mention that the parallel is a classic argument for derivation.
16. **Frazer as prior art.** Frazer opens his Balder chapter on a god whose life is "neither in heaven nor on earth but between the two", reads the mistletoe as the seat of that life, and builds the dying god who must return (S5). The bridge's betweenness reading and its dying-and-rising comparison follow him without naming him.
17. **No Loki at the shot in the poems.** Völuspá and Baldrs draumar have Höðr shoot or bear the branch with no Loki present (P18b, P19); Loki's part in the killing is in Snorri's prose and in Loki's own boast in Lokasenna (P23). Choe cites the view that Loki's part is a late development (S20, paraphrased).
18. **Baldr outside Scandinavia.** The Merseburg charm's "Balder" and the Old English *Bældæg* (Wikipedia "Baldr", fetched but not excerpted) are not in the corpus.

## 8. What the sources show

Literal things the sources name, with the excerpt that names them. Nothing here is a metaphor.

- **Baldr's face and hall.** Light shining from him; a white herb likened to his brow; the hall Breiðablik in heaven (P1).
- **The council of gods** on Baldr's dreams (P5, P18).
- **Odin's ride.** Sleipnir saddled; the descent to Niflhel; a hound "Bloody… on his breast"; the eastern door; the seeress's grave; her rising "snowed on with snow, and smitten with rain, / And drenched with dew"; benches "bright with rings", platforms "bedecked with gold"; mead brewed for Baldr with a shield laid over it (P18).
- **Frigg's oaths** from fire, water, iron, metals, stones, earth, trees, sicknesses, beasts, birds, venom, serpents (P5).
- **The sport.** Baldr standing in the Thing while the others shoot at him, hew at him and beat him with stones, and nothing harms him (P5).
- **Fensalir.** Loki in the likeness of a woman questioning Frigg (P5); Frigg weeping there later (P19).
- **The mistletoe.** A sprout westward of Valhall, pulled up by Loki (P5); in Völuspá, standing full grown and higher than the fields, slender and fair (P19).
- **The shot.** Höðr outside the ring of men; Loki directing him; the wand; the shaft flying through Baldr; Baldr falling dead (P6). The speechless gods, unable to lay hands on him; the weeping (P6).
- **Hringhorni.** The greatest ship, which will not move off its rollers (P7).
- **Hyrrokkin.** A giantess riding a wolf with a viper for a bridle; four berserks felling the wolf; her one push; fire bursting from the rollers; all lands trembling; Thor gripping his hammer (P7).
- **Nanna.** Her heart bursting at the sight of the body; borne to the pyre (P7).
- **The pyre.** Thor hallowing it with Mjöllnir; the dwarf Litr kicked into the fire; Odin with Frigg, valkyries and ravens; Freyr in a chariot drawn by the boar Gold-Mane; Heimdallr on Gold-Top; Freyja's cats; frost-giants and hill-giants; the gold ring Draupnir laid on the pyre, dropping eight rings every ninth night; Baldr's horse with all its trappings led to the fire (P7, P16).
- **Odin speaking into his dead son's ear** before the burning (P25).
- **Hermóðr's ride.** Nine nights through dark, deep dales; the river Gjöll; the bridge thatched with glittering gold; Módguðr at the bridge, the thundering under one living rider, five companies of dead the day before; the road "down and north"; Hel-gate leapt by Sleipnir; Baldr in the high-seat (P8).
- **The gifts sent back.** The ring Draupnir to Odin; a linen smock from Nanna to Frigg; a gold finger-ring to Fulla (P8).
- **The weeping.** Men, living things, earth, stones, trees and metals weeping as things do when they come out of frost into heat (P9).
- **The cave and Thökk.** A giantess sitting in a cave; her "waterless tears" (P9, P10).
- **Váli.** A child one night old who does not wash his hands or comb his hair until he brings Baldr's slayer to the fire (P18b, P19).
- **Loki's hiding.** A house with four doors on a mountain; a salmon in Fránangr's falls; a net of linen twine burned in the fire, its white ash read by Kvasir; the gods' net; Thor catching the salmon by the tail (Gylfaginning L, in the chapter of P11; the hiding passage was fetched but not excerpted).
- **The binding.** A cave; three flat stones set on edge, each drilled with a hole; Váli changed into a wolf tearing his brother Narfi; the entrails as bonds, turned to iron; Skaði fastening a venomous serpent above Loki's face (P11; the sons reversed in P24).
- **Sigyn.** Standing (P11) or sitting (P19, P24) by him; a basin (P11) or shell (P24) under the venom; going to pour it out; the venom dripping on his face meanwhile; his writhing; the earth trembling (P11, P24). In Völuspá, the bound one in "wet woods" (Bellows) or under the grove of hot springs (P19b), and Sigyn not glad.
- **Loki at the end.** At the helm of a ship carrying the people of Hel (P21); Hel's champions following him; Loki and Heimdallr killing each other (P12).
- **After the burning.** The earth rising green from the sea; waterfalls; an eagle catching fish below the cliffs; the gods at Iðavöllr; golden tables or chess-pieces in the grass; unsown fields bearing fruit; Baldr and Höðr coming from Hel, sitting down with the others and talking; the two dwelling in Odin's victory-halls (P14, P22). Gimle, a hall roofed with gold; Nástrand, a hall woven of serpents' backs with venom running through it and oath-breakers and murderers wading the streams (P13, P20, P22).
- **Saxo's Balder.** Nanna bathing; wood-maidens in a lodge that vanishes; Miming's sword and bracelet; a reindeer-drawn car over frozen ridges; three snakes dripping venom into the food that strengthens Balder; Hother playing the lyre; a sword in Balder's side; a litter carried into battle; Proserpine standing by him in a dream; death after three days; a barrow, and a flood bursting from it when robbers dig (P26, P26b, P27, S4).
- **Pliny's druids.** A white-robed priest climbing an oak; a golden sickle; mistletoe falling into a white cloth; two white bulls; the sixth day of the moon (P28).

## 9. Sources

**Method.** Every excerpt in §3 and §4 was fetched on 2026-10-14 and copied verbatim by script from the fetched text, not typed from memory. The brief asks for WebFetch. WebFetch was tried first: it returned HTTP 403 for sacred-texts.com and britannica.com and 405 or 429 for Open Book Publishers, and where it did return text it capped quotations at 125 characters, which rules it out for verbatim excerpts of 50–300 words. The excerpts were therefore fetched over HTTP from the same public sources (the Wikisource and Wikipedia APIs, heimskringla.no, Project Gutenberg, folklorefellows.fi) with `curl` and Python `urllib`, and cut from the saved files by start and end markers; the cutting script is the gatherer's scratch tool and is not in the repo. Only Choe (S20) came through WebFetch, and it is paraphrased. The writing hand can re-fetch any excerpt from the URL given.

| ID | source | URL | retrieved | status |
|---|---|---|---|---|
| P1, P3–P9, P11–P14 | Snorri Sturluson, *Gylfaginning*, tr. A. G. Brodeur, *The Prose Edda* (1916), Wikisource | https://en.wikisource.org/wiki/The_Prose_Edda_(1916_translation_by_Arthur_Gilchrist_Brodeur)/Gylfaginning | 2026-10-14 | fetched |
| P15–P17 | *Skáldskaparmál* (with *Húsdrápa* and *Haustlöng* stanzas), tr. Brodeur (1916), Wikisource | https://en.wikisource.org/wiki/The_Prose_Edda_(1916_translation_by_Arthur_Gilchrist_Brodeur)/Skáldskaparmál | 2026-10-14 | fetched |
| P2, P10 | *Gylfaginning*, Old Norse, ed. Guðni Jónsson, *Edda Snorra Sturlusonar*, heimskringla.no | https://heimskringla.no/wiki/Gylfaginning | 2026-10-14 | fetched |
| P19b, P22b | *Völuspá*, Old Norse, ed. Guðni Jónsson, *Eddukvæði*, heimskringla.no | https://heimskringla.no/wiki/Völuspá | 2026-10-14 | fetched |
| P18, P18b, S3 | *Baldrs draumar*, tr. H. A. Bellows, *The Poetic Edda* (1923), Wikisource | https://en.wikisource.org/wiki/The_Poetic_Edda_(tr._Bellows)/Baldrs_Draumar | 2026-10-14 | fetched |
| P19–P22, S1, S2 | *Völuspá*, tr. Bellows (1923), Wikisource | https://en.wikisource.org/wiki/The_Poetic_Edda_(tr._Bellows)/Voluspo | 2026-10-14 | fetched |
| P23, P24, S3 | *Lokasenna*, tr. Bellows (1923), Wikisource | https://en.wikisource.org/wiki/The_Poetic_Edda_(tr._Bellows)/Lokasenna | 2026-10-14 | fetched |
| P25 | *Vafþrúðnismál*, tr. Bellows (1923), Wikisource | https://en.wikisource.org/wiki/The_Poetic_Edda_(tr._Bellows)/Vafthruthnismol | 2026-10-14 | fetched |
| P26, P26b, P27, S4 | Saxo Grammaticus, *The Danish History, Books I–IX*, tr. Oliver Elton, Project Gutenberg eBook #1150 | https://www.gutenberg.org/cache/epub/1150/pg1150.txt | 2026-10-14 | fetched |
| P28, S5 | J. G. Frazer, *The Golden Bough* (abridged, 1922), Project Gutenberg eBook #3623 (includes Frazer's translation of Pliny, *NH* 16.95) | https://www.gutenberg.org/cache/epub/3623/pg3623.txt | 2026-10-14 | fetched |
| P29 | H. W. Longfellow, "Tegnér's Death", *The Seaside and the Fireside* (1850), Wikisource | https://en.wikisource.org/wiki/The_Seaside_and_the_Fireside/Tegnér's_Death | 2026-10-14 | fetched |
| P30 | Matthew Arnold, "Balder Dead", *Poetical Works*, Wikisource | https://en.wikisource.org/wiki/The_poetical_works_of_Matthew_Arnold/Balder_Dead | 2026-10-14 | fetched |
| S6 | Folklore Fellows, publisher's description of Lindow, *Murder and Vengeance among the Gods* (FFC 262, 1997) | https://www.folklorefellows.fi/?p=171 | 2026-10-14 | fetched |
| S7 | A.-L. Siikala, review of Lindow (1997), *FF Network* 15 (1998) | https://www.folklorefellows.fi/?p=1157 | 2026-10-14 | fetched |
| S8 | Wikipedia, "Dying-and-rising god", rev. 1370695398 | https://en.wikipedia.org/wiki/Dying-and-rising_god | 2026-10-14 | fetched |
| S9 | Wikipedia, "Sophus Bugge", rev. 1320167341 | https://en.wikipedia.org/wiki/Sophus_Bugge | 2026-10-14 | fetched |
| S10 | Wikipedia, "Höðr", rev. 1346894239 | https://en.wikipedia.org/wiki/Höðr | 2026-10-14 | fetched |
| S11 | Wikipedia, "Sigyn", rev. 1282676327 | https://en.wikipedia.org/wiki/Sigyn | 2026-10-14 | fetched |
| S12 | Wikipedia, "Þökk", rev. 1302913557 | https://en.wikipedia.org/wiki/Þökk | 2026-10-14 | fetched |
| S13 | Wikipedia, "Baldr", rev. 1376572028 | https://en.wikipedia.org/wiki/Baldr | 2026-10-14 | fetched |
| S14 | Wikipedia, "Völuspá", rev. 1315226517 | https://en.wikipedia.org/wiki/Völuspá | 2026-10-14 | fetched |
| S15 | Wikipedia, "Loki", rev. 1373790847 | https://en.wikipedia.org/wiki/Loki | 2026-10-14 | fetched |
| S16 | Wikipedia, "Weapons of Norse mythology", rev. 1371559745 | https://en.wikipedia.org/wiki/Weapons_of_Norse_mythology | 2026-10-14 | fetched |
| S17 | Wikipedia, "Prose Edda", rev. 1367985894 | https://en.wikipedia.org/wiki/Prose_Edda | 2026-10-14 | fetched |
| S18 | Wikipedia, "Frigg", rev. 1372114178 | https://en.wikipedia.org/wiki/Frigg | 2026-10-14 | fetched |
| S19 | Wikipedia, "Húsdrápa", rev. 1273392099 | https://en.wikipedia.org/wiki/Húsdrápa | 2026-10-14 | fetched |
| S20 | S. Choe, "'Hann var blindr'", *Mirator* 20:2 (2021), 5–20 | https://journal.fi/mirator/article/view/91899 ; PDF https://journal.fi/mirator/article/download/91899/60267/187125 | 2026-10-14 | fetched (WebFetch); text layer partial; paraphrased only |
| — | Brodeur's *Prose Edda* and Bellows' *Poetic Edda* (1936 printing) on sacred-texts.com | https://sacred-texts.com/neu/pre/pre04.htm | 2026-10-14 | not fetched (HTTP 403; Cloudflare challenge). Same translations used from Wikisource. |
| — | Britannica, "Balder" | https://www.britannica.com/topic/Balder | 2026-10-14 | not fetched (HTTP 403) |
| — | E. Pettit, *The Poetic Edda: A Dual-Language Edition* (Open Book Publishers, 2023), Baldrs draumar chapter | https://books.openbookpublishers.com/10.11647/obp.0308.33.pdf | 2026-10-14 | not fetched (bot check; HTTP 405/429) |
| — | J. Lindow, *Murder and Vengeance among the Gods* (1997), full text | — | — | not fetched |
| — | A. Liberman, "Some Controversial Aspects of the Myth of Baldr", *Alvíssmál* 11 (2004), 17–54 | — | — | not fetched (no copy found) |
| — | Review of Liberman, *In Prayer and Laughter*, *Scandinavica* 57:2 (2018) | https://www.scandinavica.net/article/11022.pdf | 2026-10-14 | fetched; text unreadable (encoded font); not used |
| — | J. Crawford, review of Liberman, *Scandinavian-Canadian Studies* 27 (2020) | https://scancan.net/index.php/scancan/article/download/184/367?inline=1 | 2026-10-14 | fetched; names the Baldr chapter only; not used |
| — | A. Faulkes (tr.), Snorri Sturluson, *Edda* (Everyman, 1987) | — | — | not fetched |
| — | J. Z. Smith, "Dying and Rising Gods", *Encyclopedia of Religion* (1987) | — | — | not fetched (quoted at second hand in S8) |
| — | T. Mettinger, *The Riddle of Resurrection* (2001) | — | — | not fetched (named in S8) |
| — | S. Bugge, *Studier over de nordiske Gude- og Heltesagns Oprindelse* (1881–89) | — | — | not fetched (named in S9) |
| — | M. Kaplan on oath-age and the mistletoe | — | — | not fetched (named in S13) |
| — | *Húsdrápa*, Hyrrokkin stanza (Skaldic Project edition) | — | — | not fetched |
