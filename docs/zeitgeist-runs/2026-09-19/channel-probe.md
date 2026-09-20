<!--
Provenance: Channel probe: 27 candidate endpoints tested for reachability. /zeitgeist run of 19 September 2026.
Final report of an isolated subagent, extracted byte-exact from the session
transcript and not edited. It is model output built from web search and page
fetches (which pass through a summarising model): unverified except where
3a-verifier.md says otherwise. Headline-level register throughout.
-->

Reachability test, 27 endpoints, 19 Sep 2026. No files written. One WebFetch call each; #3 got a second call after a 301. WebFetch answers through a small summarising model, so the "verbatim" titles are as that model relayed them.

**A. Wikipedia**
1. REACHABLE — 200 — 10 of 10 — "Lizzie_Borden", "Duncan_Sheik", "Resident_Evil_(2026_film)" — View counts present; dated yesterday (18 Sep). Needs a filter: Main_Page, Special:Search and Wikipedia:Featured_pictures take ranks 1, 3 and 4.
2. REACHABLE — 200 — 10 of 10 — "Chicxulub_crater", "Macklemore", "Hugh_Jackman_filmography_and_discography" — Counts present; dated 17 Sep. It needs the same filter. Fetching two days lets you compare movement.
3. BLOCKED — 301 redirect to the no-slash URL, which returned 200 but only a JS shell showing "Loading…" — 0 entries — Unusable. It renders the same API data as #1.
4. REACHABLE — 200 — 10 of 10 — "Elizabeth Holmes", "Ben Shelton", "Hanuman Ansh" — Weekly counts present and the list is curated, so no namespace noise. It covers 6–12 Sep, a week behind.

**B. Google Trends RSS**
5. IN — REACHABLE — 200 — 10 — "raphinha", "salman khan", "rohit sharma" — Approximate traffic present as bucketed floors (100+ to 2000+); first item dated today, 14:00 −0700.
6. ID — REACHABLE — 200 — 10 — "roma vs inter", "flashscore", "dortmund" — Counts present, dated today. All ten are European football and none is in Bahasa. That may just be Saturday night, but there is little local signal.
7. BR — REACHABLE — 200 — 10 — "sport recife x juventude", "remo x santos", "atlético-mg x chapecoense" — Counts present (up to 20,000+), dated today. Four entries read as US English ("nfl schedule this week", "best shows on hbo max"), so either the feed is contaminated or the summariser drifted. Check the raw XML before trusting it.
8. NG — REACHABLE — 200 — 10 — "barcelona", "nottingham forest", "galatasaray" — Counts present (up to 10000+), dated today. All football.
9. JP — REACHABLE — 200 — 10 — "台風情報", "トヨタ", "しぐれうい 炎上" — Counts present, dated today. This feed had the most genuinely local content of the six.
10. DE — REACHABLE — 200 — 10 — "the international", "the masked singer", "sandra bullock" — Counts present, dated today.

All six feeds are fetchable and current. The counts are coarse floors. On a match day, football saturates every territory.

**C. X aggregators**
11. REACHABLE — 200 — 10 — "#SalmanKhan", "Rahul Gandhi", "Pedri" — No tweet counts came back. Timestamp today, 20:52 UTC.
12. REACHABLE — 200 — 10 — "#CORTIS_2ND_DAESANG", "#MrFanboyEP4", "PERTHSANTA NIHON ICHINICHI" — No counts. Today, 21:21 UTC. The fandom hashtags are clearly local, which the Google ID feed was not.
13. REACHABLE — 200 — 10 — "#DrinkWithJin", "Danilo Pereira", "Arthur Cabral" — No counts. Today, 21:21 UTC.
14. REACHABLE — 200 — 10 — "#okanburukistifa", "NC State", "رافينيا" — A worldwide list with no counts and no explicit timestamp (the page refers to the "last 8 hours"). Looks current.

**D. Discourse**
15. BLOCKED — tool-level refusal: "unable to fetch from www.reddit.com" — 0 entries. This is not an HTTP error, so retrying will not help.
16. BLOCKED — same refusal for old.reddit.com — 0 entries.
17. REACHABLE — 200 — 10 — "Trump creates AI Force and appoints AI czar to oversee artificial intelligence", "The Last of Us Part II", "She is still unemployed" — Dated today. No scores. Each item carries a source label, and about half the items are Reddit, so this works as the Reddit substitute. The general news items include conflict headlines; take titles only.
18. REACHABLE — 200 — 10 — "Only AI gets to work remotely", "Pilot project", "Dog Love" — Scores, community names and publish dates present, 13–18 Sep. Clean JSON. The content skews heavily to memes, shitposts and anti-AI sentiment.
19. BLOCKED — 200 but a JS shell containing only the word "Bluesky" — 0 entries.
20. REACHABLE — 200 — 10 — "Cregger's Resident Evil earns praise", "Fans celebrate Batman Day", "Pete Alonso hits 3-run homer" — No counts and no dates in the payload. The topics are evidently current and are phrased as short headlines. The `suggested` field was empty. US-centric.
21. REACHABLE — 200 — 10 — "Typst makes big strides", "I don't like passkeys", "CSS-Tricks could be a co-op" — Score, comment count and timestamps present, 18–19 Sep. A niche developer surface.
22. REACHABLE — 200 — 10 — "Former DraftKings employees detail how it uses ML to target likely losers…", "Raindrop … raised a $35M Series A led by CRV", "ING: India's software services exports have risen to ~5.2% of GDP…" — Dated today, 5:50 PM. Sources present, no counts. The top cluster is AI-security stories; take headlines only.
23. REACHABLE — 200 — 10 — "AI-generated posters don't have to be horrible", "Cloudflare Quick Tunnels", "How to Write with an LLM" — Points, comment counts and age present. Current, from 11 hours to 1 day old.

**E. Meme surfaces**
24. BLOCKED — HTTP 404 — 0 entries. The path does not exist.
25. PARTIAL — 200 — 10 — "Verity (Minecraft ARG)", "What's The 'Parent Split-Face Trend'?", "What Is The 'Mitch McConnell Car' Meme?" — No counts. Relative dates run from 3 hours to 11 days, so it mixes ranked entries with editorial and video items and the ranking is blurry. The explainer titles are still usable.
26. PARTIAL — 200 — 5 (the rest sit behind "Load more") — "How Verity became the new Skibidi Toilet", "They want you to be scared of AI in a very specific way", "AI is still boring and also bad and also expensive" — Dated, latest 18 Sep. Titles only, but it is a good interpretive signal, and it corroborates #25 on Verity.
27. BLOCKED — DNS `ENOTFOUND tokboard.com` — 0 entries. The domain appears dead.

**Use these**
- A: #1, with a namespace filter. Add #2 only if you want day-on-day deltas. #4 as a weekly curated cross-check.
- B: JP first, then DE, IN and BR (BR only after the raw-XML check). NG and ID are fetchable but added almost nothing local on this sample.
- C: #12, #13 and #11 (trends24, timestamped and territorial). #14 as a single worldwide call.
- D: #23, #22, #17 (Reddit by proxy), #20, #18. Add #21 only if the developer niche is wanted.
- E: #26, then #25. Neither carries counts. No fetchable short-form video surface turned up.

**Drop these**
- #3 and #19: JS shells with no content.
- #15 and #16: Reddit is refused by the tool itself.
- #24: 404.
- #27: DNS failure.
- #2: optional, since it duplicates #1's shape.
- #6 and #8: low marginal signal on match days. Run them again on a weekday before deciding.

---

## The prompt this agent was given

> Today's date is 19 September 2026. You are testing which public endpoints a WebFetch tool can actually read, so they can be added as channels to a recurring news-reading pipeline. Do NOT write any files. This is a reachability test, not a news digest.
>
> **Register rules (hard):** if any fetched content touches security, conflict, weapons or crime, give headline-level titles only. No operational or technical detail of any kind.
>
> For EACH endpoint below, call WebFetch once (twice at most if the first attempt errors transiently) with a prompt asking for "the top 10 entries exactly as listed, with any counts shown". Report one row per endpoint:
> `N. REACHABLE | PARTIAL | BLOCKED — [HTTP/error if any] — [how many entries came back] — [3 sample entries, verbatim titles only] — [one line on data quality: are counts present? is it current (dated today/yesterday)? is it clearly stale?]`
>
> A. Wikipedia most-viewed articles (collective look-ups):
> 1. https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2026/09/18
> 2. https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2026/09/17
> 3. https://pageviews.wmcloud.org/topviews/?project=en.wikipedia.org&platform=all-access&date=yesterday
> 4. https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report
>
> B. Google Trends public RSS by territory (search intent beyond the US/UK):
> 5. https://trends.google.com/trending/rss?geo=IN
> 6. https://trends.google.com/trending/rss?geo=ID
> 7. https://trends.google.com/trending/rss?geo=BR
> 8. https://trends.google.com/trending/rss?geo=NG
> 9. https://trends.google.com/trending/rss?geo=JP
> 10. https://trends.google.com/trending/rss?geo=DE
>
> C. X trend aggregator by territory:
> 11. https://trends24.in/india/
> 12. https://trends24.in/indonesia/
> 13. https://trends24.in/brazil/
> 14. https://getdaytrends.com/
>
> D. Reddit substitutes and other discourse surfaces:
> 15. https://www.reddit.com/r/popular/top.json?t=week&limit=15
> 16. https://old.reddit.com/r/popular/top/?t=week
> 17. https://upstract.com/
> 18. https://lemmy.world/api/v3/post/list?sort=TopWeek&limit=15
> 19. https://bsky.app/ (looking for any public trending list)
> 20. https://public.api.bsky.app/xrpc/app.bsky.unspecced.getTrendingTopics
> 21. https://lobste.rs/hottest.json
> 22. https://www.techmeme.com/
> 23. https://news.ycombinator.com/best
>
> E. Short-form / meme surfaces:
> 24. https://knowyourmeme.com/memes/trending
> 25. https://trending.knowyourmeme.com/
> 26. https://www.garbageday.email/archive
> 27. https://tokboard.com/
>
> Finish with two short lists:
> - "Use these" — endpoints that returned current, structured data, best first within each group A–E.
> - "Drop these" — blocked, stale, or too noisy to be worth a call.
> Keep the whole report under 900 words.
