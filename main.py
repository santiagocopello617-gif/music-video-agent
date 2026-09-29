from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from src.music_video_agent.orchestrator import Orchestrator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a beat-synced music video from a song.")
    parser.add_argument("--song", type=str, help="Path to the local audio file.")
    parser.add_argument("--song-url", type=str, help="URL to the audio file.")
    parser.add_argument("--avatar", type=str, help="Optional avatar image path.")
    parser.add_argument("--output", type=str, default="output/music_video.mp4", help="Output MP4 path.")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second for the final render.")
    parser.add_argument("--width", type=int, default=1280, help="Output video width.")
    parser.add_argument("--height", type=int, default=720, help="Output video height.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.song and not args.song_url:
        print("You must provide either --song or --song-url.")
        return 1

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    orchestrator = Orchestrator()
    orchestrator.run(
        song_path=args.song,
        song_url=args.song_url,
        avatar_path=args.avatar,
        output_path=str(output_path),
        fps=args.fps,
        width=args.width,
        height=args.height,
    )
    print(f"Video created at: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
