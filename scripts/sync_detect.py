#!/usr/bin/env python3
"""
Find the time offset between two video recordings of the same event.

Uses ffmpeg to extract audio, then FFT-based cross-correlation to find
the point where recording 2 aligns with recording 1.

Output tells you: how many seconds into recording 2 corresponds to the
start of recording 1 (or vice versa), so you can align them in Kdenlive.

Usage:
    python3 sync_detect.py <recording1.mp4> <recording2.mp4>
"""

import subprocess
import sys
import numpy as np
from scipy.signal import fftconvolve

SAMPLE_RATE = 8000   # Hz — low enough to be fast, high enough for sync accuracy
DURATION = 300       # seconds of audio to analyse (first 5 minutes)


def extract_audio(path, sample_rate=SAMPLE_RATE, duration=DURATION):
    print(f"  Extracting audio: {path}")
    cmd = [
        "ffmpeg", "-i", path,
        "-vn",              # no video
        "-ac", "1",         # mono
        "-ar", str(sample_rate),
        "-t", str(duration),
        "-f", "s16le",      # raw signed 16-bit PCM
        "-loglevel", "error",
        "-"
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"ffmpeg error:\n{result.stderr.decode()}", file=sys.stderr)
        sys.exit(1)
    samples = np.frombuffer(result.stdout, dtype=np.int16).astype(np.float32)
    # Normalise to [-1, 1]
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples /= peak
    return samples


def find_offset(a, b, sample_rate=SAMPLE_RATE):
    """
    Cross-correlate a and b using FFT.
    Returns offset in samples: positive means b starts later than a.
    """
    print("  Cross-correlating...")
    correlation = fftconvolve(a, b[::-1], mode="full")
    peak_idx = int(np.argmax(correlation))
    offset_samples = peak_idx - (len(b) - 1)
    return offset_samples


def format_timecode(seconds):
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    if h > 0:
        return f"{sign}{h}:{m:02d}:{s:06.3f}"
    return f"{sign}{m}:{s:06.3f}"


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 sync_detect.py <recording1.mp4> <recording2.mp4>")
        sys.exit(1)

    rec1, rec2 = sys.argv[1], sys.argv[2]

    print(f"\nAnalysing first {DURATION}s of each recording at {SAMPLE_RATE} Hz...\n")

    a = extract_audio(rec1)
    b = extract_audio(rec2)

    offset_samples = find_offset(a, b)
    offset_seconds = offset_samples / SAMPLE_RATE

    print(f"\n--- RESULT ---")
    print(f"Offset: {offset_seconds:+.3f} seconds  ({format_timecode(offset_seconds)})\n")

    if offset_seconds > 0:
        print(f"Recording 2 starts {abs(offset_seconds):.3f}s LATER than recording 1.")
        print(f"In Kdenlive: place recording 1 at 0:00, then shift recording 2 RIGHT by {format_timecode(offset_seconds)}.")
    elif offset_seconds < 0:
        print(f"Recording 2 starts {abs(offset_seconds):.3f}s EARLIER than recording 1.")
        print(f"In Kdenlive: place recording 1 at 0:00, then shift recording 2 LEFT by {format_timecode(abs(offset_seconds))}.")
    else:
        print("Recordings appear to be already in sync.")

    print(f"\nConfidence check: verify by finding a sharp sound (clap, laugh, word start)")
    print(f"at a known point and confirming both tracks hit it at the same timeline position.")


if __name__ == "__main__":
    main()
