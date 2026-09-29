from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class MotionState:
    time: float
    x_offset: float
    y_offset: float
    scale: float
    pose: str
    intensity: float


class MotionAgent:
    def __init__(self) -> None:
        pass

    def generate_motion_plan(self, audio_analysis, scene_plan: List[dict]) -> List[MotionState]:
        motions: List[MotionState] = []
        for i, beat in enumerate(audio_analysis.beats):
            time = float(beat)
            section = self._section_for_time(time, scene_plan)
            intensity = float(sum(1 for b in audio_analysis.beats if abs(b - time) < 0.25) / max(len(audio_analysis.beats), 1))
            x_offset = (i % 5 - 2) * 12.0 * (0.5 + intensity)
            y_offset = (1 if i % 2 == 0 else -1) * 18.0 * (0.5 + intensity)
            scale = 1.0 + (0.08 if section == "chorus" else 0.02) * (1.0 + intensity)
            pose = "drop" if section == "chorus" and intensity > 0.8 else "sway" if section == "verse" else "idle"
            motions.append(MotionState(time=time, x_offset=x_offset, y_offset=y_offset, scale=scale, pose=pose, intensity=intensity))
        return motions

    def _section_for_time(self, time: float, scene_plan: List[dict]) -> str:
        for scene in scene_plan:
            if scene["start"] <= time <= scene["end"]:
                return scene["section_name"]
        return "verse"
