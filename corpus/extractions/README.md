# Extractions

Raw transcripts extracted from external sources (YouTube, podcasts, lectures).

**Source material** - unprocessed, verbatim captures awaiting synthesis.

## Rights & licence — read before reuse

**This directory is not covered by the repository's CC BY 4.0 licence.** These are
verbatim (ASR) transcripts of talks by other people, mirrored here as raw input for
synthesis. **Copyright in the underlying words remains with the original speakers and
their publishers.** They are hosted with attribution, for study and transformation into
the project's own synthesized documents — not relicensed, not offered for redistribution.

- Attribution is by directory: each channel/speaker folder (`benjamin-davies/`,
  `eckhart-tolle/`, `sadhguru/`, `lex-fridman/`, `ted/`, `theories-of-everything`, …)
  names the source. `benjamin-davies/` is a fuller channel harvest — see its
  `channel-manifest.json`.
- **Double-derivative cases** (e.g. an Alan Watts clip already licensed to a third
  party before capture) are attribution-only and carry whatever restrictions the
  upstream licence imposes; treat them as most-restrictive.
- If you are a rights-holder and want your material removed, that is a valid request —
  it will be honored.

The project's own CC BY 4.0 grant (see the root `LICENSE`) applies to the *synthesized*
documents derived from this material, not to these raw captures.

## Structure

```
extractions/
├── benjamin-davies/     # Paraphilosophy channel (23 transcripts)
├── ted/                 # TED talks
├── [channel-name]/      # Auto-created per channel harvest
└── README.md
```

## Pipeline

```
External Source → /extractions/[channel]/ (raw) → /translated (synthesized)
```

## Tools

- `apparatus/cli/youtube_ingest.py` - YouTube transcript extraction

## Usage

```bash
# Single video (saves to extractions root)
python apparatus/cli/youtube_ingest.py https://www.youtube.com/watch?v=VIDEO_ID

# Harvest entire channel (auto-creates subdirectory)
python apparatus/cli/youtube_ingest.py --channel https://www.youtube.com/@ChannelName

# List channel videos first
python apparatus/cli/youtube_ingest.py --channel URL --list-only

# Custom tags
python apparatus/cli/youtube_ingest.py --channel URL --tags philosophy consciousness
```

See `/translated` for consciousness-synthesized versions.
