# Zeitgeist threads — draft taxonomy for review (D5 gate)

**Status: draft. Nothing here is live.** The registry the site reads (`apparatus/site/src/data/zeitgeist-threads.json`) still holds only the nine July threads. The proposed assignment is `zeitgeist-threads-draft.json`, beside this file. Strike, rename, merge or split below; on your word it lands.

What was checked, independently of the drafter: the draft passes the site's own schema and validator (no slug claimed twice, no dangling member, no new id colliding with an item slug, no existing member lost, no title that is a sentence). Swapped in as a dry run: all 194 tests pass, including the contract that every item URL live on 20 Sep 2026 stays a page or a redirect; the build emits 151 thread-or-item pages and 326 redirects. Index would read 31 active, 42 dormant, 78 once, against today's 402 ids of which 9 recur.

## Editor's flags (Claude, reading the draft before you do)

1. **Author's position.** `anthropic-ascent`, "Anthropic's Trillion-Dollar Ascent", is a thread about the maker of the model that drafted this list, under a triumphal noun. Proposed: `anthropic-valuation`, "Anthropic's Valuation". The id is new, so it is free to change now and not after.
2. **`ai-substrate-shift`, "AI as Substrate"** is the entry closest to a theme and furthest from a thing in the world; the drafter says so too. Candidate for dissolving back into residue.
3. **The withdrawal cluster is the real naming question.** `social-exit` was the tip of a 59-item domain, now seven threads: social-exit, return-to-familiar, cozy-web-migration, subculture-revival, shared-internet-ending, analogue-turn, human-made-premium (plus quiet-flex). Seven things, or one thing described seven ways across seven months. This is your archive's most persistent cultural signal and the split decides how it reads. My lean: the split is right in kind but `return-to-familiar` (13) is nearer a mood than a thing and deserves your eye first.
4. **"The Inference Economy"** is your coinage; the drafter proposes "The AI Capex Trade". Plainer, but it is your title and its id cannot move. Keep unless you prefer otherwise.
5. **Seven one-week pairs** (winter-olympics-2026, march-madness, world-environment-day, correspondents-dinner-shooting, ai-scare-trade, quiet-flex, forest-decline): one event read twice in adjacent readings, no sequel. My lean is to keep them: they are accurate merges, the alternative is two near-duplicate pages each, and `dormant` says honestly what they are. Striking all seven leaves 50 threads over 316 items.
6. **`cascade-structure`** is, as the drafter says, a way of reading and not a thing. Its id is a live URL, so it cannot simply go; it stays as a one-item thread unless you name a thread for it to redirect into.
7. **The war is five threads** (iran-war, strait-of-hormuz, oil-shock, iran-ceasefire-talks, wartime-markets; 70 items) under a price rule: the barrel and everything downstream is oil-shock even when the title names the Strait. Consequence worth knowing: `strait-of-hormuz` stops on 8 June and survives afterwards only as a straddler. If you would rather the Strait ran to September, the rule is the thing to change, not individual items.
8. **A finding, not a flag:** `iran-war` reads SURFACE, CURRENT, SURFACE, DEEP, SURFACE, DEEP, SURFACE, TECTONIC… across sixteen readings. It never settles at a scale. That oscillation is the series' own difficulty with the war, now visible.
9. **One archive fault surfaced:** `the-diagnostic-moment` is one slug for two different items (12 and 27 April). They already share a page, wrongly. Fixing it needs date-qualified members in the registry, since past readings are not rewritten; left for later.
10. On approval, one inherited member moves: `gas-prices-are-52-higher-than-before-the-iran-war` from iran-war to oil-shock, by the price rule.

Everything below this line is the drafter's document, unedited.

---

# Zeitgeist threads — draft taxonomy (v2) for editorial mark-up

This draft proposes 57 threads — the nine existing ids plus 48 new — covering 330 of the 426 items (77.5%). Ninety-six items remain outside any thread: 94 ids, of which 92 are true singletons and two (`the-diagnostic-moment`, `the-sea-is-rising-faster-than-the-models-predicted`) already recur under their own slug. Ids that recur rise from 9 of 402 (2.2%) to 58 of 151 (38.4%); items sitting under a recurring id rise from 33 (7.7%) to 333 (78.2%).

Reading notes. Dates are 2026, MM-DD; the bracketed figure is the number of distinct readings the thread appears in. Scales are listed in order of first appearance. Where an item's gap column was blank or its title opaque, the assignment was checked against the reading itself in `corpus/synthesis/zeitgeist/` (read only). Nothing here adds detail beyond the headline level of the source.

## Threads

| id | title | items | dates (first → last) | scales touched | scope |
|---|---|---|---|---|---|
| iran-war | The Iran War | 22 | 03-03 → 09-19 (16) | SURFACE → CURRENT → DEEP → TECTONIC | The fighting and how it is attended to: strikes, leaders killed and succeeded, domestic dissent, the war's duration, its silence in the feed. Not: any pause, truce or deal (iran-ceasefire-talks). |
| oil-shock | The Oil Shock | 14 | 03-03 → 09-10 (13) | CURRENT → SURFACE → TECTONIC | The barrel price and what it does downstream: pump prices, rationing, demand forecasts, the risk premium. Not: the physical state of the waterway (strait-of-hormuz). |
| social-exit | The Social Exit | 14 | 03-10 → 09-19 (13) | CURRENT → DEEP | People leaving public platforms: the withdrawal itself, Gen Z's retreat, the exit becoming a place. Not: the small rooms they arrive in (cozy-web-migration). |
| strait-of-hormuz | The Strait of Hormuz | 14 | 03-03 → 06-08 (10) | SURFACE → DEEP → CURRENT → TECTONIC | The waterway itself: closure, the dual blockade, naval incidents, shipping, the chokepoint read at depth. Not: the price it sets (oil-shock). |
| inference-economy | The Inference Economy | 13 | 02-23 → 06-08 (8) | CURRENT → DEEP → SURFACE | AI capital expenditure and its pricing: capex, the inference pivot, venture concentration, the June chip rout. Not: AI's change of status from product to background (ai-substrate-shift). |
| return-to-familiar | The Return to the Familiar | 13 | 03-03 → 09-10 (12) | CURRENT → SURFACE → DEEP | Nostalgia and re-anchoring as mass taste: 2016, Bob Ross, remakes, resale, tradition. Not: deliberately offline objects and media (analogue-turn). |
| ai-cyber-offence | AI-Driven Cyberattacks | 12 | 02-23 → 06-04 (9) | CURRENT → DEEP → SURFACE | AI finding and exploiting vulnerabilities, and defending with the same tools: attack surfaces, the patch window, the first AI-built zero-day. Not: the decision to withhold such a model (ai-pacing-debate). |
| cozy-web-migration | The Cozy Web Migration | 12 | 02-22 → 08-13 (11) | CURRENT → DEEP | The destination: micro-communities, the living-room internet, the cozy web, rooms. Not: the departure (social-exit) nor the platforms closing the common page (shared-internet-ending). |
| iran-ceasefire-talks | The Iran Ceasefire Talks | 11 | 03-24 → 07-28 (9) | SURFACE → TECTONIC | Every pause, truce, memo, negotiation and interim deal, and each collapse. Not: statements about the war's end made with no talks under way (iran-war). |
| rate-cycle | The Rate Cycle | 10 | 02-22 → 09-19 (9) | CURRENT → SURFACE → DEEP | The price of money: Fed decisions, the new chair, the killed cut, then the September bond repricing. Not: the inflation prints themselves (second-inflation-wave). |
| ai-pacing-debate | The AI Pacing Debate | 9 | 04-12 → 09-19 (5) | CURRENT → DEEP → TECTONIC → SURFACE | Whether and when frontier capability reaches the public: the withheld model, the government release gate, the resignation, the case for pacing, the brake. Not: statute and regulators' calendars (ai-governance-gap). |
| wartime-markets | The Wartime Stock Market | 9 | 03-03 → 07-07 (9) | SURFACE → CURRENT | Equity indices during the war: the first shock, record highs against sentiment, narrow leadership. Not: cash on the sidelines (retreat-to-cash) or yields (rate-cycle). |
| ai-labour-substitution | The AI Labour Substitution | 8 | 02-26 → 05-10 (5) | DEEP → CURRENT → TECTONIC | Layoffs and workforce replacement attributed to AI. Not: the market's fear trade in software stocks (ai-scare-trade). |
| ai-substrate-shift | AI as Substrate | 8 | 02-22 → 06-01 (7) | TECTONIC → CURRENT → DEEP | AI's change of status: from product and headline to infrastructure, substrate, economic base. Not: the money behind it (inference-economy). The nearest of all threads to a theme — see Hardest calls. |
| federal-hollowing | The Hollowing of Federal Capacity | 8 | 02-26 → 04-09 (4) | SURFACE → CURRENT → DEEP | The DHS shutdown, TSA attrition, the DOGE aftermath, EPA withdrawal. Not: the constitutional argument over who may do it (executive-power-confrontation). |
| subculture-revival | The Subculture Revival | 8 | 02-23 → 06-08 (8) | CURRENT | Named subcultures returning, small and offline: the countermovement, the metasthetic, cyberdecking. Not: generic micro-communities (cozy-web-migration). |
| ukraine-war | The Ukraine War | 8 | 04-12 → 06-22 (7) | SURFACE → CURRENT | Strikes, the ritual ceasefires (Easter, Victory Day), the turn to fuel and logistics. Not: Europe's airspace and alliances under strain (postwar-settlement). |
| ai-governance-gap | The AI Governance Gap | 6 | 04-29 → 09-04 (6) | DEEP → CURRENT | Rules and regulators running behind deployment: capability past containment, the EU delay, the compliance filing, behavioural remedies. Not: the labs' own brake (ai-pacing-debate). |
| data-centre-backlash | The Data-Centre Power Backlash | 6 | 04-27 → 09-19 (5) | CURRENT → DEEP | AI's electricity demand meeting the public: bills, terawatt-hours, the neighbourhood, substations. Not: capex as a market story (inference-economy). |
| frontier-model-flood | The Frontier Model Flood | 6 | 03-10 → 09-04 (5) | SURFACE → CURRENT → TECTONIC | The cadence of closed frontier releases, from the model avalanche to the general-intelligence claim. Not: open weights and sovereign models (open-weights-sovereignty). |
| shared-internet-ending | The End of the Shared Internet | 6 | 05-14 → 08-13 (4) | CURRENT → DEEP → TECTONIC | Platforms dismantling the common surface: Reddit walling itself, the front page dissolving, the mass internet ending. Not: users choosing to leave (social-exit). |
| warming-acceleration | The Warming Acceleration | 6 | 03-10 → 09-04 (5) | DEEP → TECTONIC | The measured heat signal: acceleration, ocean heat, the energy the planet keeps, 1.5°C. Not: El Niño's overlay (el-nino-2026) nor single weather events (residue). |
| anthropic-ascent | Anthropic's Trillion-Dollar Ascent | 5 | 05-12 → 06-06 (3) | CURRENT → SURFACE → TECTONIC | One company's revenue, S-1 and valuation. Not: the sector's capex trade (inference-economy). |
| hantavirus-outbreak | The Hondius Hantavirus Outbreak | 5 | 05-07 → 05-14 (5) | SURFACE | The cruise-ship outbreak across five readings in one week. Not: Ebola (singleton). |
| orbital-buildout | The Orbital Buildout | 5 | 05-14 → 06-22 (2) | SURFACE → DEEP → TECTONIC | Compute and capital leaving the planet: orbital data centres, the rocket-company listing. Not: Artemis II or the lunar impact (singletons). |
| planetary-overshoot | Planetary Overshoot | 5 | 06-01 → 06-06 (3) | TECTONIC → DEEP | The carrying-capacity finding across three June readings. Not: temperature (warming-acceleration). |
| synthetic-media-trust | Synthetic Media and Trust | 5 | 04-29 → 09-04 (3) | TECTONIC → SURFACE → DEEP | Fabricated personas, images and warnings eroding shared evidence, and trust withdrawing in response. Not: press access (press-freedom-erosion). |
| analogue-turn | The Analogue Turn | 4 | 04-29 → 05-07 (3) | CURRENT → DEEP | Going offline through objects and practice: the "year of analog", going analogue. Not: nostalgia for content (return-to-familiar). |
| executive-power-confrontation | The Constitutional Confrontation | 4 | 02-22 → 03-03 (4) | DEEP | The US separation-of-powers confrontation, always at DEEP: the ruling's structure, the confrontation named, war without authorisation. Not: tariffs as trade policy (tariff-regime). |
| open-weights-sovereignty | Open Weights and AI Sovereignty | 4 | 04-29 → 07-28 (4) | CURRENT | Capability diffusing: DeepSeek V4, capability seeping underground, "sovereignty", the open-weights argument. Not: the closed frontier's release cadence (frontier-model-flood). |
| postwar-settlement | The Postwar Settlement | 4 | 07-07 → 09-10 (3) | SURFACE → DEEP → TECTONIC | The post-1945 order under test: the NATO rift, three settlements in one week, Europe's sky as a front. Not: the Ukraine fighting itself (ukraine-war). |
| species-turnover-slowdown | Species Turnover Slowdown | 4 | 03-18 → 03-24 (3) | TECTONIC → DEEP | One finding — the biosphere's self-renewal slowing — across three readings in a week. Not: gene-edited coral (coral-reef-collapse). |
| tariff-regime | The Tariff Regime | 4 | 02-22 → 06-20 (4) | SURFACE → CURRENT | Tariffs as policy: the IEEPA ruling, the 15% global tariff, the next tariff, the trade order fragmenting. Not: the constitutional reading (executive-power-confrontation). |
| agentic-ai | The Arrival of Agents | 3 | 03-31 → 05-14 (3) | CURRENT → DEEP | Agents as the working frame: arrival, deployment, "agentic" as official vocabulary. Not: agents proving theorems (residue pair). |
| ai-self-improvement | AI Self-Improvement | 3 | 05-14 → 09-19 (3) | TECTONIC → DEEP | AI doing the work of making AI: recursion at the substrate, the machine writing itself, a quarter of the next mind's making. Not: machine-proved mathematics (residue pair). |
| coral-reef-collapse | The Coral Reef Collapse | 3 | 02-22 → 04-27 (3) | DEEP | Reef condition and the gene-edited rescue. Not: ocean oxygen (ocean-deoxygenation). |
| cuba-crisis | The Cuba Crisis | 3 | 03-19 → 07-07 (3) | SURFACE | Cuba's grid collapses, March and July. Not: Venezuela (singleton). |
| freshwater-fish-collapse | The Freshwater Fish Collapse | 3 | 04-27 → 05-08 (3) | CURRENT → DEEP | The 81% decline finding across three readings. Not: the oceans (ocean-deoxygenation). |
| human-made-premium | The Human-Made Premium | 3 | 07-28 → 09-10 (3) | CURRENT | "Made by humans" as a price signal and a feature, including software that sells by refusing AI. Not: planning objections to data centres (data-centre-backlash). |
| press-freedom-erosion | The Erosion of Press Freedom | 3 | 05-01 → 09-19 (2) | SURFACE → TECTONIC | The press-freedom low, the degrading means of knowing, newsrooms shut out. Not: synthetic fakes (synthetic-media-trust). |
| second-inflation-wave | Inflation's Second Act | 3 | 05-14 → 08-13 (3) | CURRENT → SURFACE | Inflation re-accelerating, its second act, then cooling. Not: what central banks do about it (rate-cycle). |
| trump-xi-summit | The Trump–Xi Summit | 3 | 05-12 → 06-01 (3) | SURFACE | The Beijing summit: approach, meeting, close. Not: tariffs (tariff-regime). |
| uk-realignment | The UK Party Realignment | 3 | 05-09 → 06-22 (3) | SURFACE | The two-party system breaking: the May elections to the June seat. Not: other countries' ballots (singletons). |
| world-cup-2026 | The 2026 World Cup | 3 | 06-08 → 06-20 (3) | SURFACE | The tournament as the feed's ritual. Not: the wedding it shares a title with (residue). |
| ai-scare-trade | The AI Scare Trade | 2 | 02-22 → 02-26 (2) | CURRENT → SURFACE | The February sell-off in software and services on AI fear. Not: layoffs (ai-labour-substitution). Short-span pair. |
| correspondents-dinner-shooting | The Correspondents' Dinner Shooting | 2 | 04-27 → 04-29 (2) | SURFACE | The shooting and the arraignment. Short-span pair. |
| el-nino-2026 | The 2026 El Niño | 2 | 06-20 → 09-19 (2) | DEEP → TECTONIC | El Niño's return and its near-certain persistence. Not: the underlying trend (warming-acceleration). |
| forest-decline | Forest Decline | 2 | 02-22 → 02-23 (2) | DEEP | Forests becoming uniform; forests dying of chronic stress. Short-span pair. |
| gulf-stream-drift | The Gulf Stream Drift | 2 | 03-16 → 06-08 (2) | DEEP → TECTONIC | The Atlantic overturning: the Gulf Stream drifting, then the decline confirmed as its instruments are switched off. Not: ocean heat (warming-acceleration). |
| march-madness | March Madness | 2 | 03-16 → 03-19 (2) | SURFACE | The tournament, seen twice. Short-span pair. |
| multi-cancer-blood-test | The Multi-Cancer Blood Test | 2 | 05-14 → 06-04 (2) | CURRENT → DEEP | The fifty-cancer blood test, anticipated then arrived. Not: the general science round-ups (residue). |
| ocean-deoxygenation | Ocean Deoxygenation | 2 | 05-10 → 08-13 (2) | DEEP | The ocean losing its breath, May and August. Not: freshwater (freshwater-fish-collapse). |
| quiet-flex | The Quiet Flex | 2 | 02-23 → 02-26 (2) | CURRENT | The quiet-flex aesthetic. Short-span pair. |
| retreat-to-cash | The Retreat to Cash | 2 | 03-31 → 06-06 (2) | CURRENT | Record money-market balances, March and June. Not: equities (wartime-markets). |
| winter-olympics-2026 | The Milan-Cortina Winter Olympics | 2 | 02-22 → 02-23 (2) | SURFACE | The Games as clean ritual. Short-span pair. |
| world-environment-day | World Environment Day | 2 | 06-01 → 06-06 (2) | SURFACE | The day announced, then the day as hashtag. Short-span pair. |
| cascade-structure | The Cascade | 1 | 03-19 (1) | DEEP | One item. A way of reading, not a thing in the world — see Existing threads, assessed. |

## Where the lines fall

**Three rules applied throughout.** (1) Assignment follows the title's subject; where the title is a metaphor, the lead fact of the item decides. (2) Two items in the *same* reading (a CURRENT and its DEEP echo) do not make a thread: there is no movement in time to show. Six such pairs sit in residue — the glacier-for-lithium trade (04-12), the mind that burns less (04-09), the suicide figure (05-14), the planetary thermostat (05-09), the desalination bloom (09-10), machine-proved mathematics (09-10). (3) The series' own devices — the mismatch, the thermostat, the substitution, the pause, the unholdable whole — are never threads, however often they recur.

**The war cluster (iran-war · iran-ceasefire-talks · strait-of-hormuz · oil-shock · wartime-markets; 70 items).**
- *iran-war* holds the fighting and how it is attended to — strikes, leaders killed and succeeded, domestic dissent, duration, the war's absence from the feed — and any title whose subject is simply "the war".
- *strait-of-hormuz* holds the waterway as a physical thing — closed, blockaded, fired across, stranding ships, read as a chokepoint — and nothing whose subject is a price.
- *oil-shock* holds the barrel price and everything downstream of it — pump prices, rationing in Asia, demand forecasts, the risk premium — even when the title names the Strait as the cause.
- *iran-ceasefire-talks* (new) holds every pause, truce, memo, negotiation and interim deal and each collapse; a presidential end-date given with no talks under way stays in iran-war.
- *wartime-markets* (new) holds equity indices only; yields go to rate-cycle, parked cash to retreat-to-cash, the barrel to oil-shock.

Without the talks split iran-war would hold 33 items and read as a domain; with it, the diplomacy reads as its own sequence (five-day pause → two-week pause → Islamabad → the memo → life support → interim deal → the July pause). A further split is available and not taken: four SURFACE items (`the-split-screen`, `three-iranian-leaders-killed-in-twenty-four-hours`, `the-son-replaces-the-father`, `mojtaba-khamenei-breaks-silence-invisibly`) would make a succession thread. One inherited member sits on the wrong side of the oil line: `gas-prices-are-52-higher-than-before-the-iran-war` is in iran-war and has been kept there as instructed; by the rule above it is oil-shock.

A consequence worth knowing: under the price rule the Strait is never again a title's subject after 8 June. It persists as a clause — in ten straddlers, five of them after that date, the last on 19 September. An `also` field would carry the thread to the end of the archive; the partition cannot.

**The "dual blockade" and the "chokepoint economy".** The dual-blockade items (04-29 → 05-08) are a phase of the Hormuz story, not a separate thing, and sit in strait-of-hormuz. "The chokepoint civilisation" (06-01) and "The chokepoint economy" (06-08) are the DEEP reading of the same strait — the second is almost wholly about Hormuz — so they join it rather than founding a theme thread. "The chokepoint we will not watch" (06-10) is about the ocean, not the strait, and is left in residue. "Narrow leadership everywhere" (06-08) is equity breadth and goes to wartime-markets.

**Money (rate-cycle · second-inflation-wave · retreat-to-cash).** rate-cycle merges the Fed's decisions (February to July) with the September bond repricing, on the ground that both are the price of money and the second is what the first became. An editor who wants the long end kept apart can split off four items (`the-price-of-beef…`, `the-bond-market-is-repricing…`, `the-price-of-money-is-going-up…`, `the-price-of-time-went-through…`) as a bond-repricing thread. Inflation prints are kept separate from what central banks do about them.

**AI: money, status, company (inference-economy · ai-substrate-shift · anthropic-ascent · ai-scare-trade).** inference-economy is money and hardware: capex, chips, inference cost, the AI trade's repricing in June. ai-substrate-shift is a claim about status — AI ceasing to be a product or a headline and becoming a layer. The two March CURRENT items ("AI becomes infrastructure, not product"; "AI as infrastructure, not spectacle") were the hardest to place: their titles say status, part of their content says racks and power. They go with status so that they sit beside their June twin ("AI has stopped being a headline and become substrate"). anthropic-ascent is one company; the sector stays in inference-economy. (Position note, after the series' own practice: this draft was made by an Anthropic model. The thread is proposed because five titles name the company; weigh it accordingly.) ai-scare-trade is a market event about displacement and could be folded into ai-labour-substitution as its SURFACE prelude.

**AI: release, brake, rules (frontier-model-flood · open-weights-sovereignty · ai-pacing-debate · ai-governance-gap · agentic-ai).** frontier-model-flood is the closed labs' cadence; open-weights-sovereignty is capability escaping them — the two June items whose titles name both go with the second, because their commentary says the undercurrent is the signal. ai-pacing-debate is the gate on release and the argument about slowing (the withheld model, the state as release valve, the resignation, the pacing essay, the brake filed as a cartel); ai-governance-gap is statute, regulators and remedies. They could be merged into one fifteen-item thread; they are kept apart because "what happened to the rules?" and "what happened to the brake?" are different questions with different answers. agentic-ai is thin (three items) and takes `ai-agents-are-being-deployed-faster…` by its title's subject, leaving that item's next-day twin (`ai-governance-is-lagging…`) in governance — the one place the title rule separates two near-identical items.

**AI: harm and cost (ai-cyber-offence · data-centre-backlash · ai-labour-substitution · human-made-premium).** ai-cyber-offence includes defence, since the series treats them as one substrate. The Mythos items are split by title: the withheld model goes to pacing, the vulnerability it found goes to cyber. data-centre-backlash is demand for electricity meeting the public, from the midterm energy question to substations; it takes "The thermal bill for abstraction" on the word *abstraction*, though that item opens with a heatwave. human-made-premium takes the LibreOffice item ("Refusal has become a feature") as the same market signal one step on.

**The withdrawal cluster (social-exit · cozy-web-migration · shared-internet-ending · analogue-turn · return-to-familiar · subculture-revival · quiet-flex; 59 items).** As one thread this is a domain, and social-exit was on course to become it. The split follows the titles' own vocabulary: *exit/withdrawal/retreat* (the act of leaving) · *micro-community/cozy web/rooms* (where they go) · *front page/shared surface/mass internet* (platforms removing the common page) · *analog/analogue* (objects and practice) · *re-anchoring/familiar/nostalgia/2016* (taste turning backward) · *subculture* (named scenes returning). The weakest boundary is social-exit ↔ cozy-web-migration: departure and destination are one movement, and `the-great-withdrawal-social-exit-the-cozy-web-the-intentiona` names both in its title. Merge those two and the result is 26 items — large but under the ceiling. return-to-familiar is the loosest of the seven: five of its thirteen members (`bob-ross…`, `realism-over-romanticism…`, `spending-turns-deliberate…`, `the-turn-toward-weight…`, `the-pause-is-nostalgic…`) are there on the commentary rather than the title.

**Ecology.** Split by system, as instructed: species turnover, coral, freshwater fish, ocean oxygen, the Atlantic overturning, measured warming, El Niño, overshoot, forests. What is deliberately *not* threaded is the ecological round-up — DEEP items that list five findings under a device title ("The ecological acceleration", "The planetary thermostat is failing", "The earth is changing in ways the news cycle cannot photograph", "The atmosphere is being inventoried", "The chokepoint we will not watch", "The Antarctic surrenders its keystone"). Each touches two or three systems and belongs to none. Weather events (nor'easter, severe weather, March burned, the European fire, the Indonesian fire) are left alone: different events, no sequel.

**The US state (executive-power-confrontation · tariff-regime · federal-hollowing).** The Supreme Court tariff ruling appears twice on 02-22: the SURFACE item goes to tariffs, the DEEP item ("a constitutional phase transition") to the confrontation. federal-hollowing merges the DHS shutdown (a named event, four items) with its DEEP reading (the hollowing, the DOGE aftermath, the EPA) because the merged thread shows the migration SURFACE → CURRENT → DEEP in six weeks; split, neither half shows anything.

**ukraine-war · postwar-settlement.** The Ukraine items are strikes and ritual ceasefires. The September "sky" items concern Europe's airspace described as a front and are titled as a settlement ending, which ties them to "Three postwar settlements" a week earlier and to the NATO rift in July. An editor who distrusts postwar-settlement as too interpretive should send the two sky items to ukraine-war and return the other two to residue.

**Short-span pairs.** Seven threads are the same thing caught by two readings less than a week apart and never again: ai-scare-trade, quiet-flex, forest-decline, winter-olympics-2026, march-madness, correspondents-dinner-shooting, world-environment-day. They are unmistakable, which is why they are here; they show no movement, which is why they are flagged as a block. Striking all seven costs 14 items and leaves 50 threads over 316.

## Existing threads, assessed

- **iran-war** — sound; now the largest thread (22) and the only one touching all four scales; stays a thread rather than a domain only because the talks are split off; one inherited member (`gas-prices-are-52…`) belongs by rule to oil-shock.
- **oil-shock** — sound; its three original members were one item re-titled over four days; extended, it runs to 10 September and reaches TECTONIC.
- **social-exit** — sound as a thing, but it was the visible tip of a 59-item domain; confined here to the act of leaving, with six siblings carrying the rest.
- **strait-of-hormuz** — sound; the cleanest scale-migrator in the archive; goes silent as a title after 8 June (see above).
- **inference-economy** — sound as a thing, weak as a title: the phrase is the series' coinage, and the existing June member shows the thread already means capex-and-its-pricing. Proposed title: "The AI Capex Trade".
- **gulf-stream-drift** — one item as found, two now; the thing is the Atlantic overturning, and the id slightly misnames it. Proposed title: "The Atlantic Overturning".
- **species-turnover-slowdown** — sound but a burst, not an arc: one finding across three readings in a week. Proposed title: "The Species Turnover Slowdown" (article, for consistency).
- **cuba-crisis** — empty in the registry; three items found, all grid collapses. Proposed title: "The Cuba Blackouts".
- **cascade-structure** — badly conceived: a way of reading ("it is all one cascade"), not a thing in the world, and a single member. Its natural siblings are the TECTONIC weavings (`the-convergence-of-four-accelerating-systems`, `the-substitution`, `the-chokepoint-civilisation…`), which would make it a mood thread. Not grown; recommend retiring the page or leaving it as a titled singleton.

## Straddlers

Sixty-one items, assigned by title, each touching one other thread. strait-of-hormuz is the second thread in ten of them; inference-economy and ai-cyber-offence in five each.

| date, scale | item slug | assigned | also touches |
|---|---|---|---|
| 02-22 S | `the-supreme-court-struck-down-trump-s-ieepa-tariffs-6-3` | tariff-regime | executive-power-confrontation |
| 02-23 C | `subculture-revival-and-micro-community-formation` | subculture-revival | cozy-web-migration |
| 02-26 S | `nvidia-beats-software-falls` | ai-scare-trade | inference-economy |
| 03-03 C | `ai-becomes-infrastructure-not-product` | ai-substrate-shift | inference-economy |
| 03-03 D | `executive-war-without-congressional-authorisation` | executive-power-confrontation | iran-war |
| 03-10 C | `ai-as-infrastructure-not-spectacle` | ai-substrate-shift | inference-economy |
| 03-24 T | `the-biosphere-s-self-repair-mechanism-is-failing-at-the-same` | species-turnover-slowdown | ai-cyber-offence |
| 03-31 D | `the-biosphere-is-being-edited` | coral-reef-collapse | species-turnover-slowdown |
| 04-09 S | `the-pause-that-markets-called-peace` | iran-ceasefire-talks | wartime-markets |
| 04-09 T | `the-ceasefire-revealed-the-machine` | iran-ceasefire-talks | wartime-markets |
| 04-12 C | `the-model-too-capable-to-release` | ai-pacing-debate | ai-cyber-offence |
| 04-12 D | `the-intelligence-that-sees-what-we-couldn-t` | ai-cyber-offence | ai-pacing-debate |
| 04-27 S | `iran-talks-stall-hormuz-remains-closed` | iran-ceasefire-talks | strait-of-hormuz |
| 04-27 C | `the-ai-acceleration-paradox` | frontier-model-flood | ai-labour-substitution |
| 04-29 D | `ai-is-crossing-a-threshold-where-capability-exceeds-containm` | ai-governance-gap | ai-cyber-offence |
| 05-01 D | `ai-capability-has-crossed-the-threshold-where-discovery-outp` | ai-governance-gap | ai-cyber-offence |
| 05-07 S | `gas-prices-are-52-higher-than-before-the-iran-war` | iran-war (inherited) | oil-shock |
| 05-07 D | `ai-agents-are-being-deployed-faster-than-governance-can-trac` | agentic-ai | ai-governance-gap |
| 05-08 C | `markets-holding-pattern-during-dual-blockade` | wartime-markets | strait-of-hormuz |
| 05-09 C | `oil-markets-remain-paralysed-by-hormuz-closure` | oil-shock | strait-of-hormuz |
| 05-09 T | `the-human-ai-economic-transition-has-begun-and-no-governance` | ai-labour-substitution | ai-governance-gap |
| 05-10 C | `oil-at-95-the-strait-nearly-closed-and-no-one-is-panicking` | oil-shock | strait-of-hormuz |
| 05-10 D | `ai-is-becoming-the-economic-base-not-the-superstructure` | ai-substrate-shift | ai-labour-substitution |
| 05-10 D | `the-oceans-are-forgetting-how-to-breathe` | ocean-deoxygenation | freshwater-fish-collapse |
| 05-10 T | `a-war-is-being-waged-over-the-planet-s-chokepoint-and-normal` | iran-war | strait-of-hormuz |
| 06-01 D | `re-anchoring-is-not-nostalgia-it-is-the-body-s-correct-respo` | return-to-familiar | ai-cyber-offence |
| 06-04 T | `a-single-privately-held-company-is-approaching-one-trillion-` | anthropic-ascent | ai-self-improvement |
| 06-06 S | `anthropic-nears-a-trillion-as-chips-lose-one` | anthropic-ascent | inference-economy |
| 06-06 T | `two-trillion-dollar-quantities-are-being-measured-this-week-` | planetary-overshoot | inference-economy |
| 06-08 T | `we-are-switching-off-the-instruments-as-the-readings-go-red` | gulf-stream-drift | federal-hollowing |
| 06-10 C | `the-front-page-dissolves` | shared-internet-ending | cozy-web-migration |
| 06-10 C | `the-war-that-is-read-through-its-valve` | iran-war | strait-of-hormuz |
| 06-17 S | `the-risk-premium-returns-to-the-strait` | oil-shock | strait-of-hormuz |
| 06-17 C | `the-frontier-races-on-the-surface-while-capability-seeps-und` | open-weights-sovereignty | frontier-model-flood |
| 06-17 T | `two-accelerations-are-crossing-thresholds-at-once-and-neithe` | warming-acceleration | frontier-model-flood |
| 06-22 S | `a-rocket-company-becomes-worth-more-than-a-nation-and-a-stra` | orbital-buildout | strait-of-hormuz |
| 06-22 C | `the-frontier-models-keep-landing-and-sovereignty-becomes-the` | open-weights-sovereignty | frontier-model-flood |
| 06-22 C | `markets-exhale-central-banks-refuse-to` | wartime-markets | rate-cycle |
| 06-22 T | `the-species-is-reaching-two-escape-velocities-at-once-in-opp` | orbital-buildout | social-exit |
| 07-07 S | `nato-summit-in-ankara-over-a-rift-it-can-t-name` | postwar-settlement | iran-war |
| 07-07 S | `markets-close-at-records-while-the-ground-says-no` | wartime-markets | data-centre-backlash |
| 07-07 C | `the-great-withdrawal-social-exit-the-cozy-web-the-intentiona` | social-exit | cozy-web-migration |
| 07-07 C | `the-turn-toward-weight-tradition-wisdom-flexing-physical-med` | return-to-familiar | analogue-turn |
| 07-07 D | `the-thermal-bill-for-abstraction-is-coming-due-in-bodies-and` | data-centre-backlash | warming-acceleration |
| 07-07 D | `the-mass-internet-is-ending-and-no-one-is-holding-a-funeral-` | shared-internet-ending | social-exit |
| 07-28 C | `government-becomes-the-release-valve-on-frontier-intelligenc` | ai-pacing-debate | ai-governance-gap |
| 07-28 C | `inflation-s-second-act-filed-as-a-rate-decision-preview` | second-inflation-wave | rate-cycle |
| 07-28 D | `the-small-room-and-the-small-model-are-one-migration` | cozy-web-migration | open-weights-sovereignty |
| 07-28 D | `who-holds-the-key-is-now-the-central-political-question-at-e` | ai-pacing-debate | open-weights-sovereignty |
| 08-13 C | `made-by-humans-hardens-from-a-complaint-into-infrastructure` | human-made-premium | data-centre-backlash |
| 08-13 D | `trust-has-stopped-scaling-and-every-organ-is-solving-it-loca` | synthetic-media-trust | shared-internet-ending |
| 08-13 T | `the-withdrawal-of-trust-at-the-exact-moment-the-problems-bec` | synthetic-media-trust | cozy-web-migration |
| 09-04 C | `the-bond-market-is-repricing-the-century-and-it-is-the-only-` | rate-cycle | iran-war |
| 09-10 S | `a-king-is-buried-while-the-continent-s-sky-is-described-as-a` | postwar-settlement | ukraine-war |
| 09-10 C | `the-price-of-money-is-going-up-and-the-reason-is-the-sky` | rate-cycle | iran-war |
| 09-10 D | `the-war-has-been-given-a-date-and-the-price-has-been-given-n` | iran-war | oil-shock |
| 09-10 T | `the-peaceful-sky-was-the-settlement-and-the-sky-is-now-descr` | postwar-settlement | ukraine-war |
| 09-19 C | `every-sentence-about-the-war-now-comes-in-pairs` | iran-war | strait-of-hormuz |
| 09-19 C | `the-pause-that-is-actually-happening-is-made-of-substations` | data-centre-backlash | ai-pacing-debate |
| 09-19 D | `the-brake-was-filed-as-a-cartel` | ai-pacing-debate | ai-governance-gap |
| 09-19 D | `the-price-of-time-went-through-its-old-ceiling-and-a-strait-` | rate-cycle | strait-of-hormuz |

One collision the partition cannot fix: `the-diagnostic-moment` is a single slug for two different items — a weekly weaving on 04-12 and the Project Glasswing item on 04-27. The second belongs in ai-cyber-offence; the first belongs nowhere. Left unthreaded; one of the two needs a new slug.

## Scale migration worth seeing

- **iran-war** — SURFACE on day three, DEEP by 18 March ("the war without a name"), TECTONIC by 10 May, and DEEP again in September as "the war has become weather" while its SURFACE items turn into reports of its absence from the feed.
- **strait-of-hormuz** — SURFACE (03-03) → DEEP (03-16) → TECTONIC (05-07) in nine weeks, then nothing titled after 8 June: the chokepoint stops being news and becomes a clause in other stories.
- **iran-ceasefire-talks** — ten of eleven items SURFACE, one TECTONIC: diplomacy is only ever processed as an event.
- **ukraine-war** — eight items, seven SURFACE: the older war never leaves the surface, the contrast case to iran-war.
- **ai-substrate-shift** — opens at TECTONIC in February, appears at CURRENT in March, returns at DEEP and TECTONIC in mid-May and ends at CURRENT on 1 June: a thing announced as an epoch marker ends as a weekly trend and is then not titled again.
- **ai-labour-substitution** — DEEP in February, then seven items in four days (05-07 → 05-10) across CURRENT, DEEP and TECTONIC, then silence through September.
- **ai-governance-gap** — four of six items are DEEP; the two CURRENT items are the EU delay and the September remedies: the structural worry reaches the weekly scale only as a compliance calendar.
- **rate-cycle** — CURRENT (February, April) → SURFACE (four meeting-week items, June–July) → CURRENT → DEEP on 19 September ("the price of time"): a trend becomes an event series and then deepens.
- **federal-hollowing** — SURFACE → CURRENT → DEEP in six weeks (02-26 → 04-09), then gone; the only later trace is a straddler in June.
- **planetary-overshoot** — TECTONIC on 1 June, DEEP and TECTONIC on both 4 and 6 June, then never again; the 06-06 item itself remarks that the finding had already sunk.

## Hardest calls

1. **`the-chokepoint-civilisation-is-becoming-legible` → strait-of-hormuz.** Its title generalises across commodities; assigned to the strait because the item opens from Hormuz and its 06-08 sequel is almost wholly about it. The alternative, a "chokepoint economy" thread, would be a theme.
2. **`the-risk-premium-returns-to-the-strait` → oil-shock.** The title names the Strait; the item is about a price. The price rule won; it is the assignment most likely to be reversed, and reversing it extends strait-of-hormuz to 17 June.
3. **`one-civilisation-running-two-energy-systems-at-full-speed-in` → oil-shock.** A TECTONIC weaving of record renewables against depleting oil stocks; placed with oil because no renewables thread exists and the item continues the "energy thermostat" line of March. Could as easily be residue.
4. **`a-quarterback-s-hip-is-the-largest-single-spike-of-attention` → oil-shock.** The title's grammatical subject is the quarterback; the recurring thing is oil crossing a hundred dollars.
5. **`signals-from-the-deep-scarcely-a-ripple` → cuba-crisis.** Half the item is a submarine missile launch; assigned for Cuba's third island-wide blackout, which is the sequel the thread needs. Without it cuba-crisis is a five-day pair.
6. **`trust-has-stopped-scaling…` and `the-withdrawal-of-trust…` → synthetic-media-trust.** Both weave the rooms, the labels and the closed front page; they could sit in residue as weavings. Placed because the 08-13 reading's central story is that images can no longer be trusted and these are its DEEP and TECTONIC.
7. **`the-thermal-bill-for-abstraction…` → data-centre-backlash.** Opens with heatwave deaths, turns to megawatts; the same reading's TECTONIC ("The planetary heat mismatch") carries the heat, so this one carries the grid.
8. **`mercury-returns-to-the-air` → federal-hollowing.** A deregulation, not a loss of capacity; included because the same reading's DEEP item names it as the hollowing's latest instance.
9. **ai-substrate-shift as a thread at all.** "AI becoming substrate" is close to the series' own thesis. Kept because its items are about a change in the world rather than a way of reading it, and because its path from TECTONIC to CURRENT is worth seeing. If struck, its two March items go to inference-economy and the rest to residue.
10. **The residue pair `the-mind-that-burns-less` / `the-intelligence-that-reasons-versus-the-intelligence-that-b`.** Both are framed against the capex buildout and could be inference-economy's counter-signal; left out under the same-reading rule rather than forced.

Also uncertain, briefly: `the-biosphere-is-being-edited` → coral (its second half is species turnover); `the-mismatch` (02-22) is arguably the first appearance of species-turnover-slowdown under a device title; `a-wedding-two-deaths…` (06-20) and `the-art-world-buries-two…` (06-22) are the same two deaths and were left apart because the first title straddles three things.

## Residue

Ninety-six items (94 ids) are outside any thread. By scale: SURFACE 45 of 147, CURRENT 18 of 144, DEEP 15 of 84, TECTONIC 18 of 51. TECTONIC has the highest unthreaded share (35%) because a TECTONIC item is usually the week's weaving of several threads, not a thing in itself; CURRENT has the lowest (12.5%) because CURRENT is where the series re-titles the same trend every week. The residue falls into five kinds: one-off events; the series' own devices (four "mismatch" items, four "thermostat" items, the substitution, the unholdable whole); same-reading pairs; ecological round-ups; science round-ups.

A sample of fifteen:

| date | scale | title |
|---|---|---|
| 02-23 | CURRENT | US withdrawal from Syria completing |
| 02-26 | SURFACE | El Mencho killed; Mexico burns |
| 02-26 | TECTONIC | The great mismatch |
| 03-03 | DEEP | The High Seas Treaty enters a wartime ocean |
| 03-24 | SURFACE | Sudan's invisible hospital |
| 03-31 | TECTONIC | The substitution |
| 04-12 | SURFACE | Hungary votes |
| 04-27 | SURFACE | Artemis II Astronauts Return from the Moon |
| 05-09 | SURFACE | Canvas hacked—30 million students exposed |
| 05-14 | SURFACE | The CDC reports suicide has replaced COVID as the tenth leading cause of death in the United States |
| 06-06 | SURFACE | Ebola's quiet arithmetic in central Africa |
| 06-17 | DEEP | The world's largest living network was always under our feet, and we just drew the map |
| 07-07 | CURRENT | The friendship recession, named out loud |
| 08-13 | SURFACE | Half a million people travel to stand under something that cannot be faked |
| 09-19 | SURFACE | The Moon was hit in the spring of 2024 and the news arrived this week |
