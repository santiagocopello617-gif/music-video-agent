# Music Video Agent

A starter project for building an automation pipeline that turns a song into a beat-synced music video using specialized agents:

- Audio Agent: analyzes the song (BPM, beats, duration)
- Avatar Agent: prepares or generates avatar assets
- Visual Agent: composes scenes, effects, transitions and beat-synced motion
- Render Agent: exports the final MP4
- Orchestrator: coordinates the full workflow

This MVP supports:
- local audio files
- remote URLs to audio files
- beat detection with librosa
- dynamic background pulses and shapes synchronized to the music
- avatar overlay support (optional)

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
            ├── avatar_agent.py
            ├── visual_agent.py
            └── render_agent.py
```

## Quick start

1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the generator

```bash
python main.py --song path/to/your/song.mp3 --output output/music_video.mp4
```

Or with a remote URL:

```bash
python main.py --song-url "https://example.com/song.mp3" --output output/music_video.mp4
```

Optional avatar:

```bash
python main.py --song path/to/song.mp3 --avatar path/to/avatar.png --output output/music_video.mp4
```

## Architecture

### 1. Audio Agent
- loads the song from a local file or URL
- extracts BPM, beat times and duration
- returns a structured analysis object

### 2. Avatar Agent
- validates optional avatar
- creates a fallback placeholder if no avatar is provided

### 3. Visual Agent
- defines a palette and motion style per beat
- picks effect intensity and background transitions based on beat timings

### 4. Render Agent
- creates the video frames
- renders beat-synced motion, overlays and effects
- writes the final MP4 file

### 5. Orchestrator
- coordinates the full pipeline in a single call

## Notes

This project is intentionally an MVP. It is designed to be extended with:
- AI avatar generation
- generative background scenes
- automatic lyric captions
- style transfer and cinematic transitions
- cloud orchestration with queues and workers

## Future enhancements

- support for YouTube / Spotify / SoundCloud URLs
- voice-aware animation synchronization
- multiple avatar personas and scene templates
- automatic text-to-speech intro/outro narration
- local or cloud rendering pipeline

## Example roadmap

```text
Song input
  ↓
Audio Agent (beat + BPM)
  ↓
Avatar Agent (avatar/or placeholder)
  ↓
Visual Agent (scene plan + effects)
  ↓
Render Agent (MP4 export)
```
