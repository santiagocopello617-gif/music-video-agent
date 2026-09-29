# Music Video Agent 2.0

A refined music video generation pipeline designed to build beat-synced visuals from a song using multiple specialized agents.

This version introduces:
- scene segmentation by musical sections
- richer visual transitions and dynamic palettes
- avatar motion synchronized to beat intensity
- subtitle generation with cinematic overlays
- preset-based exports for cinematic, vertical, square, and story formats

## Architecture

- Audio Agent: analyzes tempo, beats, onset energy and section structure
- Scene Agent: maps each song section to a visual style and transition
- Lyric Agent: builds subtitle timeline markers
- Motion Agent: computes avatar positions and pose changes based on beats and intensity
- Preset Agent: resolves output presets for different aspect ratios
- Render Agent: composes frames and exports the final MP4
- Orchestrator: coordinates the whole pipeline

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --song path/to/song.mp3 --output output/final_video.mp4 --preset cinematic
```

Optional avatar:

```bash
python main.py --song path/to/song.mp3 --avatar path/to/avatar.png --output output/final_video.mp4 --preset vertical
```

## Available presets

- cinematic
- vertical
- square
- story

## Example roadmap

```text
Song input
  ↓
Audio analysis (BPM, beat grid, intensity)
  ↓
Scene planning (intro, verse, chorus, bridge, outro)
  ↓
Motion planning (avatar + effects + camera movement)
  ↓
Subtitle timeline
  ↓
Rendered MP4 export
```

## Notes

This project remains a generator framework, but the 2.0 version is much closer to a real music video pipeline than the MVP. It is suitable as a foundation for production upgrades like AI-generated backgrounds, lip-sync animation, or cloud rendering.

## Future enhancements

- AI avatar generation / synthetic performers
- advanced lyric alignment from actual lyrics
- cinematic camera systems
- lip-sync + mouth motion
- multi-scene template libraries
- adaptive transitions from drop detection
- parallel rendering tasks for faster exports

## Project structure

```text
music-video-agent/
├── README.md
├── requirements.txt
├── main.py
└── src/
    └── music_video_agent/
        ├── __init__.py
        ├── orchestrator.py
        └── agents/
            ├── __init__.py
            ├── audio_agent.py
            ├── scene_agent.py
            ├── lyric_agent.py
            ├── motion_agent.py
            ├── preset_agent.py
            └── render_agent.py
```

