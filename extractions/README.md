# Extractions

Raw transcripts extracted from external sources (YouTube, podcasts, lectures).

**Source material** - unprocessed, verbatim captures awaiting synthesis.

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

- `cli/youtube_ingest.py` - YouTube transcript extraction

## Usage

```bash
# Single video (saves to extractions root)
python cli/youtube_ingest.py https://www.youtube.com/watch?v=VIDEO_ID

# Harvest entire channel (auto-creates subdirectory)
python cli/youtube_ingest.py --channel https://www.youtube.com/@ChannelName

# List channel videos first
python cli/youtube_ingest.py --channel URL --list-only

# Custom tags
python cli/youtube_ingest.py --channel URL --tags philosophy consciousness
```

See `/translated` for consciousness-synthesized versions.
