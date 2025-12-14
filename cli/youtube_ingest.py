#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESOTERICA: YouTube Consciousness Extraction
~~ Transmuting video streams into wisdom documents ~~

Extracts transcripts from YouTube videos and formats them
as synthesis-ready markdown documents.
"""

import sys
import io
import re
import argparse
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
except ImportError:
    print("=" * 60)
    print("  DEPENDENCY REQUIRED: youtube-transcript-api")
    print("=" * 60)
    print()
    print("  Install with:")
    print("    pip install youtube-transcript-api")
    print()
    sys.exit(1)

# Optional: yt-dlp for metadata (graceful degradation if not available)
try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False

# Optional: faster-whisper for audio transcription fallback
try:
    from faster_whisper import WhisperModel
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False

# Global whisper model (lazy loaded)
_whisper_model = None


BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║           YOUTUBE CONSCIOUSNESS EXTRACTION                   ║
║         ~~ Transmuting streams into wisdom ~~                ║
╚══════════════════════════════════════════════════════════════╝
"""


def get_channel_videos(channel_url: str, limit: int = None) -> tuple:
    """Extract all video URLs from a YouTube channel using yt-dlp.

    Returns: (videos_list, channel_slug)
    """

    if not HAS_YTDLP:
        raise Exception("yt-dlp is required for channel scraping. Install with: pip install yt-dlp")

    print(f"\n  Scanning channel: {channel_url}")
    print("  This may take a moment...")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Don't download, just get info
        'ignoreerrors': True,
    }

    videos = []
    channel_name = 'Unknown Channel'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Handle different channel URL formats
            # Ensure we're hitting the videos tab
            if '/videos' not in channel_url:
                if channel_url.endswith('/'):
                    channel_url = channel_url + 'videos'
                else:
                    channel_url = channel_url + '/videos'

            result = ydl.extract_info(channel_url, download=False)

            if result is None:
                raise Exception("Could not extract channel information")

            channel_name = result.get('channel', result.get('uploader', 'Unknown Channel'))

            # Get entries (videos)
            entries = result.get('entries', [])

            if not entries:
                raise Exception("No videos found in channel")

            for entry in entries:
                if entry is None:
                    continue

                video_id = entry.get('id')
                title = entry.get('title', 'Unknown')

                if video_id:
                    videos.append({
                        'id': video_id,
                        'title': title,
                        'url': f'https://www.youtube.com/watch?v={video_id}'
                    })

                if limit and len(videos) >= limit:
                    break

            print(f"  Channel: {channel_name}")
            print(f"  Videos found: {len(videos)}")

    except Exception as e:
        raise Exception(f"Failed to scrape channel: {e}")

    # Create channel slug for subdirectory
    channel_slug = slugify(channel_name)

    return videos, channel_slug


def list_channel_videos(channel_url: str) -> None:
    """List all videos from a channel without extracting."""

    videos, channel_slug = get_channel_videos(channel_url)

    print()
    print("=" * 60)
    print(f"  CHANNEL VIDEO INVENTORY ({len(videos)} videos)")
    print(f"  Output folder: extractions/{channel_slug}/")
    print("=" * 60)
    print()

    for i, video in enumerate(videos, 1):
        title = video['title'][:55] + '...' if len(video['title']) > 55 else video['title']
        print(f"  {i:3d}. {title}")
        print(f"       {video['url']}")
        print()

    print("=" * 60)
    print(f"  Total: {len(videos)} videos")
    print("=" * 60)


def generate_channel_manifest(output_dir: Path, channel_url: str, channel_slug: str,
                               successful: list, failed: list, tags: list = None) -> Path:
    """Generate a manifest file for channel extraction results."""

    manifest = {
        'channel': {
            'name': channel_slug.replace('-', ' ').title(),
            'slug': channel_slug,
            'url': channel_url,
        },
        'extraction': {
            'date': datetime.now().isoformat(),
            'total_found': len(successful) + len(failed),
            'successful': len(successful),
            'failed': len(failed),
            'tags': tags or [],
        },
        'videos': {
            'extracted': [
                {
                    'url': url,
                    'file': path.name,
                    'video_id': extract_video_id(url)
                }
                for url, path in successful
            ],
            'failed': [
                {
                    'url': url,
                    'video_id': extract_video_id(url) if 'watch?v=' in url else url,
                    'error': error
                }
                for url, error in failed
            ]
        }
    }

    manifest_path = output_dir / 'channel-manifest.json'

    # If manifest exists, merge with previous extractions
    if manifest_path.exists():
        try:
            existing = json.loads(manifest_path.read_text(encoding='utf-8'))

            # Merge extracted videos (avoid duplicates)
            existing_ids = {v['video_id'] for v in existing.get('videos', {}).get('extracted', [])}
            for video in manifest['videos']['extracted']:
                if video['video_id'] not in existing_ids:
                    existing['videos']['extracted'].append(video)

            # Update failed list (replace with latest)
            existing['videos']['failed'] = manifest['videos']['failed']

            # Update extraction metadata
            existing['extraction']['date'] = manifest['extraction']['date']
            existing['extraction']['total_found'] = len(existing['videos']['extracted']) + len(manifest['videos']['failed'])
            existing['extraction']['successful'] = len(existing['videos']['extracted'])
            existing['extraction']['failed'] = len(manifest['videos']['failed'])

            manifest = existing
        except:
            pass  # If merge fails, overwrite with new manifest

    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

    return manifest_path


def load_existing_video_ids(output_dir: Path) -> set:
    """Load video IDs that have already been extracted."""

    existing_ids = set()

    # Check manifest
    manifest_path = output_dir / 'channel-manifest.json'
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            for video in manifest.get('videos', {}).get('extracted', []):
                existing_ids.add(video.get('video_id'))
        except:
            pass

    # Also scan for existing files (fallback)
    for md_file in output_dir.glob('*.md'):
        try:
            content = md_file.read_text(encoding='utf-8')
            match = re.search(r'video_id:\s*(\S+)', content)
            if match:
                existing_ids.add(match.group(1))
        except:
            pass

    return existing_ids


# ====================================
# WHISPER TRANSCRIPTION (FALLBACK)
# ====================================

def get_whisper_model(model_size: str = "base"):
    """Lazy-load Whisper model."""
    global _whisper_model

    if not HAS_WHISPER:
        raise Exception("faster-whisper not installed. Install with: pip install faster-whisper")

    if _whisper_model is None:
        print(f"  Loading Whisper model ({model_size})...")
        _whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8")

    return _whisper_model


def download_audio(video_id: str, output_dir: Path) -> Path:
    """Download audio from YouTube video using yt-dlp."""

    if not HAS_YTDLP:
        raise Exception("yt-dlp required for audio download. Install with: pip install yt-dlp")

    # Check for any existing audio file
    for ext in ['mp3', 'm4a', 'webm', 'opus', 'wav']:
        existing = output_dir / f"{video_id}.{ext}"
        if existing.exists():
            return existing

    # Try with ffmpeg first (better quality), fall back to direct download
    import shutil
    has_ffmpeg = shutil.which('ffmpeg') is not None

    if has_ffmpeg:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(output_dir / f'{video_id}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
    else:
        # No ffmpeg - download audio in native format
        print("  Note: ffmpeg not found, downloading audio in native format")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(output_dir / f'{video_id}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
    except Exception as e:
        raise Exception(f"Failed to download audio: {e}")

    # Find the downloaded file
    for ext in ['mp3', 'm4a', 'webm', 'opus', 'wav']:
        audio_path = output_dir / f"{video_id}.{ext}"
        if audio_path.exists():
            return audio_path

    raise Exception("Audio download failed - no output file found")


def transcribe_with_whisper(audio_path: Path, model_size: str = "base") -> list:
    """Transcribe audio file using Whisper."""

    model = get_whisper_model(model_size)

    print(f"  Transcribing with Whisper ({model_size})...")
    segments, info = model.transcribe(str(audio_path), beam_size=5)

    # Convert to list format compatible with existing code
    transcript = []
    for segment in segments:
        transcript.append({
            'text': segment.text.strip(),
            'start': segment.start,
            'duration': segment.end - segment.start
        })

    print(f"  Detected language: {info.language} (probability: {info.language_probability:.2f})")

    return transcript


def get_transcript_with_whisper_fallback(video_id: str, output_dir: Path,
                                          use_whisper: bool = False,
                                          whisper_model: str = "base") -> tuple:
    """Try YouTube transcript first, fall back to Whisper if enabled."""

    # First try YouTube transcript API
    try:
        transcript, transcript_type = get_transcript(video_id)
        return transcript, transcript_type
    except Exception as yt_error:
        if not use_whisper:
            raise yt_error

        # Fall back to Whisper
        print(f"  No YouTube transcript, using Whisper fallback...")

        try:
            # Create temp directory for audio
            temp_dir = output_dir / '.audio_temp'
            temp_dir.mkdir(exist_ok=True)

            # Download audio
            print("  Downloading audio...")
            audio_path = download_audio(video_id, temp_dir)

            # Transcribe
            transcript = transcribe_with_whisper(audio_path, whisper_model)

            # Clean up audio file (optional - comment out to keep)
            try:
                audio_path.unlink()
            except:
                pass

            return transcript, f'whisper-{whisper_model}'

        except Exception as whisper_error:
            raise Exception(f"Both YouTube and Whisper failed. YT: {yt_error}, Whisper: {whisper_error}")


def extract_video_id(url_or_id: str) -> str:
    """Extract YouTube video ID from various URL formats or return as-is if already an ID."""

    # Already a video ID (11 characters, alphanumeric with - and _)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id

    # Parse URL
    parsed = urlparse(url_or_id)

    # youtube.com/watch?v=VIDEO_ID
    if 'youtube.com' in parsed.netloc:
        query = parse_qs(parsed.query)
        if 'v' in query:
            return query['v'][0]
        # youtube.com/embed/VIDEO_ID
        if '/embed/' in parsed.path:
            return parsed.path.split('/embed/')[1].split('/')[0]
        # youtube.com/v/VIDEO_ID
        if '/v/' in parsed.path:
            return parsed.path.split('/v/')[1].split('/')[0]

    # youtu.be/VIDEO_ID
    if 'youtu.be' in parsed.netloc:
        return parsed.path.lstrip('/')

    # Try to extract any 11-character sequence that looks like a video ID
    match = re.search(r'[a-zA-Z0-9_-]{11}', url_or_id)
    if match:
        return match.group()

    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def get_video_metadata(video_id: str) -> dict:
    """Get video metadata using yt-dlp if available, otherwise return minimal info."""

    metadata = {
        'title': f'YouTube Video {video_id}',
        'channel': 'Unknown Channel',
        'description': '',
        'upload_date': '',
        'duration': '',
        'url': f'https://www.youtube.com/watch?v={video_id}'
    }

    if not HAS_YTDLP:
        return metadata

    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)

            metadata['title'] = info.get('title', metadata['title'])
            metadata['channel'] = info.get('channel', info.get('uploader', metadata['channel']))
            metadata['description'] = info.get('description', '')[:500]  # Truncate long descriptions
            metadata['upload_date'] = info.get('upload_date', '')
            metadata['duration'] = info.get('duration_string', '')
            metadata['view_count'] = info.get('view_count', '')
            metadata['tags'] = info.get('tags', [])[:10]  # First 10 tags

    except Exception as e:
        print(f"  Note: Could not fetch full metadata ({e})")

    return metadata


def get_transcript(video_id: str, languages: list = None) -> list:
    """Fetch transcript for a video, trying multiple language options."""

    if languages is None:
        languages = ['en', 'en-US', 'en-GB']

    # Create API instance (new API style)
    api = YouTubeTranscriptApi()

    try:
        # Try to get manually created transcript first
        transcript_list = api.list(video_id)

        # Prefer manual transcripts over auto-generated
        try:
            transcript = transcript_list.find_manually_created_transcript(languages)
            fetched = transcript.fetch()
            return list(fetched), 'manual'
        except:
            pass

        # Fall back to auto-generated
        try:
            transcript = transcript_list.find_generated_transcript(languages)
            fetched = transcript.fetch()
            return list(fetched), 'auto-generated'
        except:
            pass

        # Last resort: get whatever is available and translate
        for transcript in transcript_list:
            try:
                if transcript.language_code.startswith('en'):
                    fetched = transcript.fetch()
                    return list(fetched), f'auto ({transcript.language_code})'
                else:
                    translated = transcript.translate('en')
                    fetched = translated.fetch()
                    return list(fetched), f'translated from {transcript.language_code}'
            except:
                continue

    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise Exception("No transcript found for this video")

    raise Exception("Could not retrieve any transcript")


def format_transcript(transcript: list, include_timestamps: bool = False) -> str:
    """Format transcript entries into readable text."""

    # Handle both dict entries (old API) and FetchedTranscriptSnippet objects (new API)
    def get_text(entry):
        return entry.text if hasattr(entry, 'text') else entry['text']

    def get_start(entry):
        return entry.start if hasattr(entry, 'start') else entry['start']

    if include_timestamps:
        lines = []
        for entry in transcript:
            timestamp = format_timestamp(get_start(entry))
            text = get_text(entry).replace('\n', ' ')
            lines.append(f"[{timestamp}] {text}")
        return '\n\n'.join(lines)
    else:
        # Combine into paragraphs (roughly every 5-7 sentences or natural breaks)
        full_text = ' '.join(get_text(entry).replace('\n', ' ') for entry in transcript)

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


def generate_markdown(video_id: str, metadata: dict, transcript: str,
                      transcript_type: str, output_dir: Path,
                      custom_tags: list = None) -> Path:
    """Generate markdown document from extracted content."""

    title = metadata['title']
    slug = slugify(title)
    filename = f"{slug}.md"

    # Build frontmatter tags
    tags = ['youtube', 'transcript', 'extracted']
    if custom_tags:
        tags.extend(custom_tags)
    if metadata.get('tags'):
        tags.extend(metadata['tags'][:5])

    # Format upload date if available
    upload_date = ''
    if metadata.get('upload_date'):
        try:
            d = metadata['upload_date']
            upload_date = f"{d[:4]}-{d[4:6]}-{d[6:8]}"
        except:
            pass

    # Build the document
    doc = f"""---
title: "{title}"
source: youtube
video_id: {video_id}
url: {metadata['url']}
channel: "{metadata['channel']}"
transcript_type: {transcript_type}
extracted: {datetime.now().strftime('%Y-%m-%d')}
upload_date: {upload_date}
duration: {metadata.get('duration', '')}
tags: {json.dumps(tags)}
---

# {title}

> **Source**: [{metadata['channel']}]({metadata['url']})
> **Transcript**: {transcript_type}
> **Duration**: {metadata.get('duration', 'Unknown')}

---

## Description

{metadata.get('description', '*No description available*')}

---

## Transcript

{transcript}

---

*Extracted via Esoterica YouTube Consciousness Extraction Protocol*
*Video ID: {video_id}*
"""

    # Write to file
    output_path = output_dir / filename
    output_path.write_text(doc, encoding='utf-8')

    return output_path


def ingest_video(url_or_id: str, output_dir: Path,
                 include_timestamps: bool = False,
                 custom_tags: list = None,
                 quiet: bool = False,
                 use_whisper: bool = False,
                 whisper_model: str = "base") -> Path:
    """Main ingestion pipeline for a single video."""

    if not quiet:
        print(f"\n  Processing: {url_or_id}")

    # Extract video ID
    video_id = extract_video_id(url_or_id)
    if not quiet:
        print(f"  Video ID: {video_id}")

    # Get metadata
    if not quiet:
        print("  Fetching metadata...")
    metadata = get_video_metadata(video_id)
    if not quiet:
        print(f"  Title: {metadata['title'][:50]}...")

    # Get transcript (with optional Whisper fallback)
    if not quiet:
        print("  Extracting transcript...")

    transcript_data, transcript_type = get_transcript_with_whisper_fallback(
        video_id, output_dir,
        use_whisper=use_whisper,
        whisper_model=whisper_model
    )

    if not quiet:
        print(f"  Transcript type: {transcript_type}")
        print(f"  Segments: {len(transcript_data)}")

    # Format transcript
    transcript_text = format_transcript(transcript_data, include_timestamps)

    # Generate markdown
    output_path = generate_markdown(
        video_id, metadata, transcript_text,
        transcript_type, output_dir, custom_tags
    )

    if not quiet:
        print(f"  Saved: {output_path.name}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Extract YouTube transcripts into synthesis-ready markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single video
  python youtube_ingest.py https://www.youtube.com/watch?v=VIDEO_ID
  python youtube_ingest.py VIDEO_ID --timestamps

  # Batch file
  python youtube_ingest.py --batch urls.txt --tags consciousness awakening

  # Entire channel (harvest all videos)
  python youtube_ingest.py --channel https://www.youtube.com/@ChannelName
  python youtube_ingest.py --channel https://www.youtube.com/channel/CHANNEL_ID

  # List channel videos without extracting
  python youtube_ingest.py --channel URL --list-only

  # Channel with limit
  python youtube_ingest.py --channel URL --limit 10

  # Use Whisper for videos without YouTube transcripts
  python youtube_ingest.py VIDEO_URL --whisper
  python youtube_ingest.py --channel URL --whisper --whisper-model small

  # Re-run channel with Whisper to get previously failed videos
  python youtube_ingest.py --channel URL --whisper --skip-existing
        """
    )

    parser.add_argument(
        'urls',
        nargs='*',
        help='YouTube URL(s) or video ID(s) to process'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output directory (default: ../extractions/)'
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
        '-b', '--batch',
        type=Path,
        help='File containing URLs (one per line)'
    )

    parser.add_argument(
        '-c', '--channel',
        type=str,
        help='YouTube channel URL to harvest all videos from'
    )

    parser.add_argument(
        '--list-only',
        action='store_true',
        help='List channel videos without extracting (use with --channel)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of videos to process from channel'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Minimal output'
    )

    parser.add_argument(
        '--skip-existing',
        action='store_true',
        help='Skip videos that have already been extracted'
    )

    parser.add_argument(
        '--whisper',
        action='store_true',
        help='Use Whisper to transcribe videos without YouTube transcripts'
    )

    parser.add_argument(
        '--whisper-model',
        type=str,
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Whisper model size (default: base). Larger = more accurate but slower'
    )

    args = parser.parse_args()

    # Handle channel mode
    if args.channel:
        print(BANNER)

        # List only mode
        if args.list_only:
            try:
                list_channel_videos(args.channel)
                return 0
            except Exception as e:
                print(f"Error: {e}")
                return 1

        # Harvest mode - get all videos from channel
        try:
            channel_videos, channel_slug = get_channel_videos(args.channel, limit=args.limit)
            urls = [v['url'] for v in channel_videos]

            # Set output to channel subdirectory
            if not args.output:
                repo_root = Path(__file__).parent.parent
                args.output = repo_root / 'extractions' / channel_slug
                print(f"  Output folder: extractions/{channel_slug}/")

            # Add channel name as tag if not provided
            if not args.tags:
                args.tags = ['channel-harvest', channel_slug]

        except Exception as e:
            print(f"Error: {e}")
            return 1
    else:
        # Collect all URLs from args and batch file
        urls = list(args.urls) if args.urls else []

        if args.batch:
            if args.batch.exists():
                urls.extend(line.strip() for line in args.batch.read_text().splitlines() if line.strip() and not line.startswith('#'))
            else:
                print(f"Error: Batch file not found: {args.batch}")
                return 1

    if not urls:
        print(BANNER)
        print("Usage: python youtube_ingest.py <youtube_url_or_id>")
        print()
        print("Examples:")
        print("  python youtube_ingest.py https://www.youtube.com/watch?v=VIDEO_ID")
        print("  python youtube_ingest.py VIDEO_ID --timestamps")
        print("  python youtube_ingest.py VIDEO_ID -o ./output/")
        print()
        print("Channel harvest:")
        print("  python youtube_ingest.py --channel https://www.youtube.com/@ChannelName")
        print("  python youtube_ingest.py --channel URL --list-only")
        print()
        print("For full options: python youtube_ingest.py --help")
        return 0

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        repo_root = Path(__file__).parent.parent
        output_dir = repo_root / 'extractions'

    output_dir.mkdir(parents=True, exist_ok=True)

    # Skip existing videos if requested
    skipped = []
    if args.skip_existing:
        existing_ids = load_existing_video_ids(output_dir)
        if existing_ids:
            original_count = len(urls)
            filtered_urls = []
            for url in urls:
                try:
                    vid_id = extract_video_id(url)
                    if vid_id in existing_ids:
                        skipped.append(url)
                    else:
                        filtered_urls.append(url)
                except:
                    filtered_urls.append(url)
            urls = filtered_urls
            if not args.quiet and skipped:
                print(f"  Skipping {len(skipped)} already extracted videos")

    if not args.quiet:
        if not args.channel:  # Banner already printed for channel mode
            print(BANNER)
        print(f"  Output directory: {output_dir}")
        print(f"  Videos to process: {len(urls)}")

    # Process each URL
    successful = []
    failed = []

    # Show Whisper status if enabled
    if args.whisper and not args.quiet:
        print(f"  Whisper fallback: ENABLED (model: {args.whisper_model})")

    for url in urls:
        try:
            output_path = ingest_video(
                url,
                output_dir,
                include_timestamps=args.timestamps,
                custom_tags=args.tags,
                quiet=args.quiet,
                use_whisper=args.whisper,
                whisper_model=args.whisper_model
            )
            successful.append((url, output_path))
        except Exception as e:
            failed.append((url, str(e)))
            if not args.quiet:
                print(f"  ERROR: {e}")

    # Generate manifest for channel harvests
    if args.channel and (successful or failed):
        channel_slug = output_dir.name  # Directory name is the channel slug
        manifest_path = generate_channel_manifest(
            output_dir, args.channel, channel_slug,
            successful, failed, args.tags
        )
        if not args.quiet:
            print(f"\n  Manifest saved: {manifest_path.name}")

    # Summary
    if not args.quiet:
        print()
        print("=" * 60)
        print(f"  Completed: {len(successful)}/{len(urls)} videos")

        if skipped:
            print(f"  Skipped (already extracted): {len(skipped)}")

        if successful:
            print()
            print("  Saved files:")
            for url, path in successful:
                print(f"    {path.name}")

        if failed:
            print()
            print("  Failed:")
            for url, error in failed:
                print(f"    {url}: {error}")

        print("=" * 60)

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
