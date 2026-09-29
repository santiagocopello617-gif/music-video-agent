from __future__ import annotations

import math
from typing import List

import numpy as np
import cv2


class VisualAgent:
    def __init__(self, width: int = 1280, height: int = 720) -> None:
        self.width = width
        self.height = height

    def draw_background(self, frame: np.ndarray, palette: List[int], t: float, beat_strength: float) -> np.ndarray:
        for y in range(0, self.height, 6):
            wave = 20 * math.sin((y / 40.0) + t * 2.5)
            color = np.clip(np.array(palette, dtype=float) + wave, 0, 255).astype(np.uint8)
            frame[y : y + 6, :] = color
        if beat_strength > 0.1:
            cv2.circle(frame, (self.width // 2, self.height // 2), int(80 + beat_strength * 200), (255, 255, 255), 2)
        return frame

    def draw_particles(self, frame: np.ndarray, t: float, beat_strength: float) -> np.ndarray:
        for i in range(34):
            angle = t * (0.8 + i * 0.04) + i * 0.8
            x = int(self.width / 2 + math.cos(angle) * (180 + i * 8))
            y = int(self.height / 2 + math.sin(angle * 1.5) * (130 + i * 7))
            radius = int(4 + i % 4)
            cv2.circle(frame, (x, y), radius, (120, 200, 255), -1)
        return frame

    def draw_text_hint(self, frame: np.ndarray, text: str) -> np.ndarray:
        cv2.putText(frame, text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
        return frame
