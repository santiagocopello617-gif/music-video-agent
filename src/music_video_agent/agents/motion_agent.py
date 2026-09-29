from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class SubtitleLine:
    start: float
    end: float
    text: str
    style: str = "cinematic"


class LyricAgent:
    def __init__(self) -> None:
        self.templates = {
            "intro": ["Let the rhythm build the night.", "A new pulse begins here."],
            "verse": ["Follow the beat, feel the motion.", "Every line moves with the sound."],
            "chorus": ["This is the moment.", "Rise with the drop."],
            "bridge": ["Turn the lights low.", "Hold the breath for the next wave."],
            "outro": ["The final glow fades softly.", "We leave the melody in the air."]
        }

    def generate_lyrics(self, scene_plan: List[dict], duration: float) -> List[SubtitleLine]:
        subtitle_lines: List[SubtitleLine] = []
        for idx, scene in enumerate(scene_plan):
            lines = self.templates.get(scene["section_name"], self.templates["verse"])
            start = scene["start"]
            end = scene["end"]
            step = (end - start) / max(len(lines), 1)
            for i, line in enumerate(lines):
                subtitle_lines.append(
                    SubtitleLine(
                        start=start + i * step,
                        end=min(start + (i + 1) * step, duration),
                        text=line,
                        style="neon" if scene["section_name"] == "chorus" else "cinematic",
                    )
                )
        return subtitle_lines
