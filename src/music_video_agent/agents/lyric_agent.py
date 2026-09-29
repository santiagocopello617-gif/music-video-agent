from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict

from .audio_agent import AudioAnalysis, SongSection


@dataclass
class ScenePlan:
    section_name: str
    start: float
    end: float
    transition: str
    background_type: str
    palette: List[int]
    camera_motion: str
    effect_strength: float


class SceneAgent:
    def __init__(self) -> None:
        self.theme_map = {
            "intro": {"transition": "fade", "background_type": "neon-glow", "camera_motion": "slow-zoom", "palette": [12, 18, 46]},
            "verse": {"transition": "dissolve", "background_type": "city-wave", "camera_motion": "sway", "palette": [23, 72, 102]},
            "chorus": {"transition": "pulse", "background_type": "energy-rings", "camera_motion": "beat-pan", "palette": [118, 68, 144]},
            "bridge": {"transition": "flash", "background_type": "deep-space", "camera_motion": "orbit", "palette": [52, 112, 92]},
            "outro": {"transition": "fade-out", "background_type": "soft-vignette", "camera_motion": "slow-drift", "palette": [16, 18, 28]},
        }

    def build_scene_plan(self, audio_analysis: AudioAnalysis) -> List[ScenePlan]:
        plans = []
        for s in audio_analysis.sections:
            config = self.theme_map.get(s.name, self.theme_map["verse"])
            plans.append(
                ScenePlan(
                    section_name=s.name,
                    start=s.start,
                    end=s.end,
                    transition=config["transition"],
                    background_type=config["background_type"],
                    palette=s.palette or config["palette"],
                    camera_motion=config["camera_motion"],
                    effect_strength=float(s.energy),
                )
            )
        return plans
