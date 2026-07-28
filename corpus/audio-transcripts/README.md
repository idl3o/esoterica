# Audio Transcripts

Transcriptions of audio files — voice notes, recordings, lectures, conversations.

## Quick Start

```bash
# From repo root
python apparatus/cli/audio_ingest.py path/to/audio.mp3

# With timestamps
python apparatus/cli/audio_ingest.py recording.m4a --timestamps

# Better accuracy (slower)
python apparatus/cli/audio_ingest.py lecture.mp3 --model medium

# Custom title and tags
python apparatus/cli/audio_ingest.py voice-note.m4a --title "Session Notes" --tags personal reflection
```

## Requirements

```bash
pip install faster-whisper
```

## Workflow

1. Drop audio file in `raw/`
2. Run: `python apparatus/cli/audio_ingest.py audio-transcripts/raw/your-file.mp3`
3. Transcript saved to `transcripts/[filename]-transcript.md`
4. Optional: digest/synthesis saved as `digests/[filename]-digest.md`

## Supported Formats

`.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`, `.opus`, `.webm`, `.mp4`, `.mkv`, `.avi`

## Model Sizes

| Model  | Speed    | Accuracy | Use Case |
|--------|----------|----------|----------|
| tiny   | Fastest  | Basic    | Quick drafts |
| base   | Fast     | Good     | Default, voice notes |
| small  | Medium   | Better   | Lectures, interviews |
| medium | Slow     | High     | Important recordings |
| large  | Slowest  | Best     | Critical accuracy needed |

## Structure

```
audio-transcripts/
├── raw/          # Original audio files — local only, not in git
├── transcripts/  # Raw transcriptions
└── digests/      # Synthesized/processed versions
```

`raw/` is gitignored. Source audio ran to ~165 MB and every clone paid for it
forever, while the transcripts beside it already carry the content. Drop audio in
`raw/` to transcribe it; keep the originals wherever you keep originals. What
belongs in the library is the text.
