from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import os
import tempfile

import librosa
import numpy as np
import requests


@dataclass
class SongSection:
    name: str
    start: float
    end: float
    energy: float
    palette: List[int]


@dataclass
class AudioAnalysis:
    path: str
    duration: float
    tempo: float
    beats: List[float]
    sample_rate: int
    onset_env: np.ndarray = None
    sections: List[SongSection] = field(default_factory=list)
    intensity: List[float] = field(default_factory=list)


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
        duration = float(len(y) / sr)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        if len(beat_times) == 0:
            beat_times = np.linspace(0.0, max(duration, 1.0), 12)

        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onset_env_norm = librosa.util.normalize(onset_env)
        intensity = [float(v) for v in onset_env_norm.tolist()]

        sections = self._build_sections(duration, intensity)

        return AudioAnalysis(
            path=song_path,
            duration=duration,
            tempo=float(tempo),
            beats=[float(t) for t in beat_times],
            sample_rate=int(sr),
            onset_env=onset_env_norm,
            sections=sections,
            intensity=intensity,
        )

    def _build_sections(self, duration: float, intensity: List[float]) -> List[SongSection]:
        section_names = ["intro", "verse", "chorus", "bridge", "outro"]
        section_count = min(len(section_names), max(3, int(duration / 20)))
        window = duration / section_count
        sections = []

        palettes = {
            "intro": [18, 16, 48],
            "verse": [26, 76, 112],
            "chorus": [116, 58, 128],
            "bridge": [55, 120, 100],
            "outro": [14, 14, 20],
        }

        for i, name in enumerate(section_names[:section_count]):
            start = i * window
            end = (i + 1) * window if i < section_count - 1 else duration
            segment = intensity[int((start / duration) * len(intensity)): int((end / duration) * len(intensity))]
            energy = float(np.mean(segment)) if segment else 0.5
            sections.append(
                SongSection(
                    name=name,
                    start=start,
                    end=end,
                    energy=energy,
                    palette=palettes.get(name, [80, 80, 120]),
                )
            )

        return sections
