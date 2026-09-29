from __future__ import annotations

import colorsys
import math
from typing import List, Tuple

import numpy as np


class VisualAgent:
    def __init__(self, width: int = 1280, height: int = 720) -> None:
        self.width = width
        self.height = height
        self.palette = [
            (18, 16, 48),
            (39, 42, 88),
            (86, 49, 109),
            (31, 82, 115),
            (24, 77, 77),
        ]

    def choose_background_color(self, t: float, beat_times: List[float]) -> Tuple[int, int, int]:
        if not beat_times:
            return self.palette[0]

        time_in_cycle = t % max(beat_times[-1] if beat_times[-1] > 0 else 1.0, 1.0)
        cycle_index = int((time_in_cycle / max(beat_times[-1], 1.0)) * len(self.palette)) % len(self.palette)
        return self.palette[cycle_index]

    def get_effect_strength(self, t: float, beat_times: List[float]) -> float:
        if not beat_times:
            return 0.0

        strength = 0.0
        for beat in beat_times:
            delta = abs(t - beat)
            if delta < 0.25:
                strength = max(strength, 1.0 - delta / 0.25)
        return strength

    def draw_frame(
        self,
        frame: np.ndarray,
        t: float,
        beat_times: List[float],
        avatar_path: str | None = None,
        bpm: float = 120,
    ) -> np.ndarray:
        base_color = self.choose_background_color(t, beat_times)
        effect_strength = self.get_effect_strength(t, beat_times)

        # Fluido de fondo
        for y in range(0, self.height, 8):
            wave = 20 * math.sin((y / 60.0) + t * 2.0)
            r = int(np.clip(base_color[0] + wave * (0.5 + effect_strength), 0, 255))
            g = int(np.clip(base_color[1] + wave * 0.7, 0, 255))
            b = int(np.clip(base_color[2] + wave * 1.0, 0, 255))
            color = (b, g, r)
            frame[y : y + 8, :] = color

        # Pulses synchronized to beat
        if effect_strength > 0.05:
            radius = int(80 + effect_strength * 220)
            center = (self.width // 2, self.height // 2)
            alpha = int(255 * effect_strength)
            pulse_color = (255, 255, 255) if effect_strength > 0.6 else (120, 200, 255)
            cv2_circle = __import__("cv2").circle
            cv2_circle(frame, center, radius, pulse_color, thickness=8)

        # Moving particles
        for i in range(32):
            angle = t * (0.7 + i * 0.05) + i * 1.3
            x = int(self.width / 2 + math.cos(angle) * (180 + i * 8))
            y = int(self.height / 2 + math.sin(angle * 1.5) * (120 + i * 6))
            radius = int(8 + (i % 5) * 3)
            color = tuple(int(c * (0.5 + effect_strength)) for c in colorsys.hsv_to_rgb((i % 10) / 10.0, 0.9, 1.0))
            color = tuple(int(channel * 255) for channel in color)
            color = (color[2], color[1], color[0])
            __import__("cv2").circle(frame, (x, y), radius, color, -1)

        # subtle top text hint
        text_color = (255, 255, 255)
        __import__("cv2").putText(
            frame,
            f"BPM {bpm:.1f}",
            (30, 60),
            __import__("cv2").FONT_HERSHEY_SIMPLEX,
            1.2,
            text_color,
            2,
            __import__("cv2").LINE_AA,
        )

        return frame
