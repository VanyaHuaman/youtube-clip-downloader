#!/usr/bin/env python3
"""
YouTube Clip Downloader
A simple CLI tool to download YouTube videos and clips using yt-dlp
"""

import argparse
import sys
import subprocess
import shutil
import json
from pathlib import Path


def check_ytdlp_installed():
    """Check if yt-dlp is installed"""
    if shutil.which("yt-dlp") is None:
        print("❌ yt-dlp is not installed!")
        print("\nInstall it with:")
        print("  pip install yt-dlp")
        print("\nor:")
        print("  brew install yt-dlp")
        sys.exit(1)


def check_clip_availability(url):
    """
    Check if a clip is from a live stream and warn user

    Returns: (is_available, warning_message)
    """
    try:
        # Get metadata without downloading
        result = subprocess.run(
            ["yt-dlp", "-j", url],
            capture_output=True,
            text=True,
            check=True
        )

        metadata = json.loads(result.stdout)
        is_live = metadata.get("is_live", False)
        live_status = metadata.get("live_status", "")
        section_start = metadata.get("section_start")

        # Check if this is a clip from a live stream
        if (is_live or live_status == "is_live") and section_start is not None:
            duration = metadata.get("duration", 0)
            return False, (
                f"⚠️  WARNING: This clip is from a LIVE STREAM that is currently broadcasting.\n"
                f"   Clip timestamp: {section_start:.1f}s into the stream\n"
                f"   Current issue: yt-dlp cannot download past segments from active live streams.\n"
                f"   \n"
                f"   Options:\n"
                f"   1. Wait for the stream to end and be archived, then try again\n"
                f"   2. Download will proceed but may only capture recent stream content\n"
                f"   \n"
                f"   Continue anyway? (y/n): "
            )

        return True, None

    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
        # If we can't check, just proceed
        return True, None


def download_clip(url, output_dir=".", quality="best", format_type="mp4"):
    """
    Download a YouTube video or clip

    Args:
        url: YouTube URL (video or clip)
        output_dir: Directory to save the download
        quality: Video quality (best, worst, or specific like 1080p)
        format_type: Output format (mp4, webm, mkv, etc.)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Check if clip is available for download
    is_available, warning = check_clip_availability(url)
    if not is_available and warning:
        print(warning, end='', flush=True)
        response = input().strip().lower()
        if response != 'y':
            print("\n❌ Download cancelled")
            return False

    # Build yt-dlp command
    cmd = [
        "yt-dlp",
        url,
        "-o", str(output_path / "%(title)s.%(ext)s"),
        "--restrict-filenames",  # Remove special characters from filename
    ]

    # Handle quality and format
    # Use HLS format 301 for best quality (1080p60) - works better for clips than DASH
    if quality == "best":
        cmd.extend(["-f", "301/300/299+140/bestvideo+bestaudio/best"])
    else:
        cmd.extend(["-f", f"bestvideo[height<={quality.replace('p', '')}]+bestaudio/best"])

    # Merge to specified format
    cmd.extend(["--merge-output-format", format_type])

    print(f"\n📥 Downloading from: {url}")
    print(f"📁 Saving to: {output_path.absolute()}")
    print(f"🎬 Quality: {quality}, Format: {format_type}\n")

    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Download complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Download failed with error code {e.returncode}")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelled by user")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos and clips easily",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://youtube.com/watch?v=VIDEO_ID
  %(prog)s https://youtube.com/clip/CLIP_ID -o ~/Downloads
  %(prog)s URL -q 720p -f webm
        """
    )

    parser.add_argument(
        "url",
        help="YouTube video or clip URL"
    )

    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Output directory (default: current directory)"
    )

    parser.add_argument(
        "-q", "--quality",
        default="best",
        choices=["best", "worst", "2160p", "1440p", "1080p", "720p", "480p", "360p"],
        help="Video quality (default: best)"
    )

    parser.add_argument(
        "-f", "--format",
        default="mp4",
        choices=["mp4", "webm", "mkv"],
        help="Output format (default: mp4)"
    )

    args = parser.parse_args()

    # Check if yt-dlp is installed
    check_ytdlp_installed()

    # Download the clip
    success = download_clip(
        url=args.url,
        output_dir=args.output,
        quality=args.quality,
        format_type=args.format
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
