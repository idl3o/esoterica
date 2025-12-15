#!/usr/bin/env python3
"""
CONSCIOUSNESS HARVEST RUNNER
Extracts high-value consciousness interviews from curated YouTube channels.

Run this script when YouTube rate limit has reset (15-30 min after hitting 429).

Usage:
    python cli/run-consciousness-harvest.py
    python cli/run-consciousness-harvest.py --channel lex-fridman
    python cli/run-consciousness-harvest.py --test  # Test one video first
"""

import subprocess
import sys
from pathlib import Path

# Channel configurations
CHANNELS = {
    'lex-fridman': {
        'tags': ['lex-fridman', 'consciousness', 'philosophy', 'interview'],
        'videos': [
            'P-2P3MSZrBM',  # Joscha Bach
            'hXgqik6HXc0',  # Roger Penrose
            'reYdQYZ9Rj4',  # Donald Hoffman
            'NwzuibY5kUs',  # Karl Friston
            'qfKyNxfyWbo',  # Sheldon Solomon
            'p3lsYlod5OU',  # Michael Levin
            'cMscNuSUy0I',  # Noam Chomsky
            'rfKiTGj-zeQ',  # Nick Bostrom
            'yImlXr5Tr8g',  # John Vervaeke
            'BqHrpBPdtSI',  # Annaka Harris
        ]
    },
    'after-skool': {
        'tags': ['after-skool', 'philosophy', 'animation', 'wisdom'],
        'videos': [
            'mMRrCYPxD0I',  # Alan Watts - The Real You
            '4-tY6hmKcms',  # Terence McKenna
            'khOaAHK7efc',  # Alan Watts - Money
            'caCkMX6YdYU',  # Aldous Huxley
        ]
    },
    'theories-of-everything': {
        'tags': ['theories-of-everything', 'physics', 'consciousness'],
        'videos': [
            'dd6CQCbk2ro',  # Donald Hoffman
        ]
    },
    # ========== GURU TEACHINGS (All Require Whisper) ==========
    # Spiritual/guru channels don't expose transcripts - Whisper required
    # Use: python cli/run-consciousness-harvest.py --channel [name]
    # Auto-enables whisper for channels marked requires_whisper=True

    'sadhguru': {
        'tags': ['sadhguru', 'yoga', 'consciousness', 'guru', 'isha'],
        'requires_whisper': True,
        'videos': [
            # Verified working videos from @Sadhguru channel
            'LjCYRWCPwHs',  # Dark Side of Misusing Telepathy
            'hCXrdYi6KO4',  # Power of Kundalini Yoga
            'x5WunaqToGQ',  # Unplug from the Mental Matrix
            '8bVzuYeqi7U',  # Karma, Enlightenment, Devotion & Sadhana
        ]
    },
    'eckhart-tolle': {
        'tags': ['eckhart-tolle', 'presence', 'consciousness', 'guru', 'now'],
        'requires_whisper': True,
        'videos': [
            # Verified working videos from @EckhartTolle channel
            'JYq4BmFfT50',  # Stop Trying to Get There
            'cLq6NGlLTaA',  # How to Stop Feeling Irritated
            '9ArnkFERuqA',  # Stop Letting Overthinking Control You
        ]
    },
    'mooji': {
        'tags': ['mooji', 'advaita', 'consciousness', 'guru', 'nondual'],
        'requires_whisper': True,
        'videos': [
            # Need to scan @Molojiw channel for working IDs
        ]
    },
    'alan-watts': {
        'tags': ['alan-watts', 'zen', 'consciousness', 'philosophy', 'tao'],
        'requires_whisper': True,
        'videos': [
            # Alan Watts Organization uploads
            'mMRrCYPxD0I',  # The Real You (After Skool)
            '4-tY6hmKcms',  # (check availability)
        ]
    },
    'swami-sarvapriyananda': {
        'tags': ['swami-sarvapriyananda', 'vedanta', 'consciousness', 'advaita', 'guru'],
        'requires_whisper': True,
        'videos': [
            # Verified working from @VedantaNY channel
            'emKyPG0k4MU',  # Sam Harris headless way
            'q3uAxRYxgW4',  # Karma: What It Is
            'KJo1YaXW2Aw',  # Is Pure Consciousness God?
        ]
    },
    'batgap': {
        'tags': ['batgap', 'nondual', 'consciousness', 'awakening', 'interview'],
        'requires_whisper': True,
        'videos': [
            # Buddha at the Gas Pump interviews
            'Mq-em6kP6Wc',  # Kundalini - Michael Bradford
            'CXK_Itq6iH4',  # Awakening to True Source - Karyn O'Beirne
        ]
    },
}


def run_extraction(channel: str, test_mode: bool = False, use_whisper: bool = False):
    """Run extraction for a channel."""
    config = CHANNELS[channel]

    # Auto-enable whisper for channels that require it
    requires_whisper = config.get('requires_whisper', False)
    effective_whisper = use_whisper or requires_whisper

    # Use base channel name for output (strip -whisper suffix)
    output_name = channel.replace('-whisper', '')
    output_dir = Path(__file__).parent.parent / 'extractions' / output_name
    output_dir.mkdir(parents=True, exist_ok=True)

    videos = config['videos'][:1] if test_mode else config['videos']

    urls = [f'https://www.youtube.com/watch?v={vid}' for vid in videos]

    print(f"\n{'='*60}")
    print(f"  Extracting {len(videos)} videos from {channel}")
    print(f"  Output: {output_dir}")
    if effective_whisper:
        if requires_whisper:
            print(f"  Whisper: REQUIRED (channel has no native transcripts)")
        else:
            print(f"  Whisper: ENABLED (fallback for missing transcripts)")
    print(f"{'='*60}\n")

    cmd = [
        sys.executable,
        str(Path(__file__).parent / 'youtube_ingest.py'),
        *urls,
        '-o', str(output_dir),
        '--tags', *config['tags']
    ]

    if effective_whisper:
        cmd.append('--whisper')

    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Consciousness Harvest Runner')
    parser.add_argument('--channel', choices=list(CHANNELS.keys()),
                        help='Extract specific channel only')
    parser.add_argument('--test', action='store_true',
                        help='Test mode - extract one video per channel')
    parser.add_argument('--whisper', action='store_true',
                        help='Use Whisper for transcription fallback')
    args = parser.parse_args()

    print("""
================================================================
       CONSCIOUSNESS HARVEST - Wisdom Extraction Pipeline
   ~~ Academic + Guru teachings -> synthesis documentation ~~
================================================================
    """)

    channels = [args.channel] if args.channel else list(CHANNELS.keys())

    total_videos = sum(len(CHANNELS[c]['videos']) for c in channels)
    if args.test:
        total_videos = len(channels)

    print(f"  Channels: {', '.join(channels)}")
    print(f"  Total videos: {total_videos}")
    print(f"  Mode: {'TEST (1 per channel)' if args.test else 'FULL'}")
    if args.whisper:
        print(f"  Whisper: ENABLED (fallback for missing transcripts)")

    successes = 0
    for channel in channels:
        if run_extraction(channel, args.test, args.whisper):
            successes += 1

    print(f"\n{'='*60}")
    print(f"  Complete: {successes}/{len(channels)} channels")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
