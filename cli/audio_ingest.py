#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESOTERICA: Audio Consciousness Extraction
~~ Transmuting voice into text ~~

Transcribes local audio files using Whisper and formats them
as synthesis-ready markdown documents.
"""

import sys
import io
import re
import argparse
import json
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Optional: faster-whisper for audio transcription
try:
    from faster_whisper import WhisperModel
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False

# Global whisper model (lazy loaded)
_whisper_model = None


BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║            AUDIO CONSCIOUSNESS EXTRACTION                    ║
║          ~~ Transmuting voice into wisdom ~~                 ║
╚══════════════════════════════════════════════════════════════╝
"""

SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.opus', '.webm', '.mp4', '.mkv', '.avi']


def get_whisper_model(model_size: str = "base"):
    """Lazy-load Whisper model."""
    global _whisper_model

    if not HAS_WHISPER:
        print("=" * 60)
        print("  DEPENDENCY REQUIRED: faster-whisper")
        print("=" * 60)
        print()
        print("  Install with:")
        print("    pip install faster-whisper")
        print()
        sys.exit(1)

    if _whisper_model is None or getattr(_whisper_model, '_model_size', None) != model_size:
        print(f"  Loading Whisper model ({model_size})...")
        _whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8")
        _whisper_model._model_size = model_size

    return _whisper_model


def transcribe_audio(audio_path: Path, model_size: str = "base") -> tuple:
    """Transcribe audio file using Whisper.

    Returns: (segments_list, detected_language)
    """
    model = get_whisper_model(model_size)

    print(f"  Transcribing with Whisper ({model_size})...")
    segments, info = model.transcribe(str(audio_path), beam_size=5)

    # Convert to list format
    transcript = []
    for segment in segments:
        transcript.append({
            'text': segment.text.strip(),
            'start': segment.start,
            'duration': segment.end - segment.start
        })

    print(f"  Detected language: {info.language} (probability: {info.language_probability:.2f})")

    return transcript, info.language


def format_transcript(transcript: list, include_timestamps: bool = False) -> str:
    """Format transcript entries into readable text."""

    if include_timestamps:
        lines = []
        for entry in transcript:
            timestamp = format_timestamp(entry['start'])
            text = entry['text'].replace('\n', ' ')
            lines.append(f"[{timestamp}] {text}")
        return '\n\n'.join(lines)
    else:
        # Combine into paragraphs (roughly every 5-7 sentences or natural breaks)
        full_text = ' '.join(entry['text'].replace('\n', ' ') for entry in transcript)

        # Clean up spacing
        full_text = re.sub(r'\s+', ' ', full_text).strip()

        # Break into paragraphs at sentence boundaries (roughly every 300 chars)
        paragraphs = []
        current = []
        char_count = 0

        for sentence in re.split(r'(?<=[.!?])\s+', full_text):
            current.append(sentence)
            char_count += len(sentence)

            if char_count > 300:
                paragraphs.append(' '.join(current))
                current = []
                char_count = 0

        if current:
            paragraphs.append(' '.join(current))

        return '\n\n'.join(paragraphs)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:60]


def get_audio_duration(audio_path: Path) -> str:
    """Get audio duration if possible."""
    try:
        # Try using mutagen for metadata
        from mutagen import File
        audio = File(str(audio_path))
        if audio and audio.info:
            duration = int(audio.info.length)
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            secs = duration % 60
            if hours > 0:
                return f"{hours}:{minutes:02d}:{secs:02d}"
            return f"{minutes}:{secs:02d}"
    except:
        pass
    return "Unknown"


def generate_markdown(audio_path: Path, transcript: str, language: str,
                      output_dir: Path, custom_tags: list = None,
                      custom_title: str = None,
                      model_size: str = "base") -> Path:
    """Generate markdown document from transcribed content."""

    title = custom_title or audio_path.stem.replace('-', ' ').replace('_', ' ').title()
    slug = slugify(title)
    filename = f"{slug}-transcript.md"

    # Build frontmatter tags
    tags = ['audio', 'transcript', 'whisper']
    if custom_tags:
        tags.extend(custom_tags)

    duration = get_audio_duration(audio_path)

    # Build the document
    doc = f"""---
title: "{title}"
source: audio
source_file: "{audio_path.name}"
transcript_type: whisper-{model_size}
language: {language}
extracted: {datetime.now().strftime('%Y-%m-%d')}
duration: {duration}
tags: {json.dumps(tags)}
---

# {title}

> **Source**: {audio_path.name}
> **Transcript**: Whisper ({model_size})
> **Language**: {language}
> **Duration**: {duration}

---

## Transcript

{transcript}

---

*Extracted via Esoterica Audio Consciousness Extraction Protocol*
*Source file: {audio_path.name}*
"""

    # Write to file
    output_path = output_dir / filename
    output_path.write_text(doc, encoding='utf-8')

    return output_path


def ingest_audio(audio_path: Path, output_dir: Path,
                 include_timestamps: bool = False,
                 custom_tags: list = None,
                 custom_title: str = None,
                 quiet: bool = False,
                 model_size: str = "base") -> Path:
    """Main ingestion pipeline for a single audio file."""

    if not quiet:
        print(f"\n  Processing: {audio_path.name}")

    # Validate file exists and is supported
    if not audio_path.exists():
        raise Exception(f"File not found: {audio_path}")

    if audio_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise Exception(f"Unsupported format: {audio_path.suffix}. Supported: {', '.join(SUPPORTED_FORMATS)}")

    # Transcribe
    transcript_data, language = transcribe_audio(audio_path, model_size)

    if not quiet:
        print(f"  Segments: {len(transcript_data)}")

    # Format transcript
    transcript_text = format_transcript(transcript_data, include_timestamps)

    # Generate markdown
    output_path = generate_markdown(
        audio_path, transcript_text, language,
        output_dir, custom_tags, custom_title, model_size
    )

    if not quiet:
        print(f"  Saved: {output_path.name}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe local audio files into synthesis-ready markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file
  python audio_ingest.py recording.mp3
  python audio_ingest.py voice-note.m4a --timestamps

  # Multiple files
  python audio_ingest.py *.mp3

  # With custom title and tags
  python audio_ingest.py lecture.mp3 --title "Consciousness Lecture" --tags philosophy awakening

  # Specify output directory
  python audio_ingest.py recording.mp3 -o ./transcripts/

  # Use larger model for better accuracy
  python audio_ingest.py recording.mp3 --model medium

Model sizes (speed vs accuracy):
  tiny   - Fastest, least accurate
  base   - Good balance (default)
  small  - Better accuracy
  medium - High accuracy
  large  - Best accuracy, slowest
        """
    )

    parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='Audio file(s) to transcribe'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output directory (default: ../audio-transcripts/transcripts/)'
    )

    parser.add_argument(
        '-t', '--timestamps',
        action='store_true',
        help='Include timestamps in transcript'
    )

    parser.add_argument(
        '--tags',
        nargs='+',
        help='Additional tags to add to the document'
    )

    parser.add_argument(
        '--title',
        type=str,
        help='Custom title for the transcript (only for single file)'
    )

    parser.add_argument(
        '-m', '--model',
        type=str,
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Whisper model size (default: base). Larger = more accurate but slower'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Minimal output'
    )

    args = parser.parse_args()

    if not args.quiet:
        print(BANNER)

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        repo_root = Path(__file__).parent.parent
        output_dir = repo_root / 'audio-transcripts' / 'transcripts'

    output_dir.mkdir(parents=True, exist_ok=True)

    if not args.quiet:
        print(f"  Output directory: {output_dir}")
        print(f"  Whisper model: {args.model}")
        print(f"  Files to process: {len(args.files)}")

    # Validate custom title only for single file
    if args.title and len(args.files) > 1:
        print("  Warning: --title ignored for multiple files")
        args.title = None

    # Process each file
    successful = []
    failed = []

    for audio_file in args.files:
        try:
            output_path = ingest_audio(
                audio_file,
                output_dir,
                include_timestamps=args.timestamps,
                custom_tags=args.tags,
                custom_title=args.title,
                quiet=args.quiet,
                model_size=args.model
            )
            successful.append((audio_file, output_path))
        except Exception as e:
            failed.append((audio_file, str(e)))
            if not args.quiet:
                print(f"  ERROR: {e}")

    # Summary
    if not args.quiet:
        print()
        print("=" * 60)
        print(f"  Completed: {len(successful)}/{len(args.files)} files")

        if successful:
            print()
            print("  Saved files:")
            for audio_file, path in successful:
                print(f"    {path.name}")

        if failed:
            print()
            print("  Failed:")
            for audio_file, error in failed:
                print(f"    {audio_file}: {error}")

        print("=" * 60)

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
