from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import librosa
import numpy as np
import requests


@dataclass
class AudioAnalysis:
    path: str
    duration: float
    tempo: float
    beats: List[float]
    sample_rate: int


class AudioAgent:
    def __init__(self) -> None:
        self.temp_dir = Path(tempfile.gettempdir()) / "music_video_agent"
        self.temp_dir.mkdir(exist_ok=True)

    def prepare_audio(self, song_path: Optional[str] = None, song_url: Optional[str] = None) -> str:
        if song_path:
            return song_path

        if not song_url:
            raise ValueError("Either a local song path or a song URL is required.")

        target = self.temp_dir / (song_url.split("/")[-1] or "downloaded_song.wav")
        response = requests.get(song_url, timeout=60)
        response.raise_for_status()
        target.write_bytes(response.content)
        return str(target)

    def analyze(self, song_path: str) -> AudioAnalysis:
        if not os.path.exists(song_path):
            raise FileNotFoundError(f"Audio file not found: {song_path}")

        y, sr = librosa.load(song_path, sr=None, mono=True)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        if len(beat_times) == 0:
            beat_times = np.linspace(0.0, max(float(len(y) / sr), 1.0), 10)

        duration = float(len(y) / sr)
        return AudioAnalysis(
            path=song_path,
            duration=duration,
            tempo=float(tempo),
            beats=[float(t) for t in beat_times],
            sample_rate=int(sr),
        )
