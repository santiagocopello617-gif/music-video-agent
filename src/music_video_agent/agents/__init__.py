from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

from .audio_agent import AudioAnalysis
from .visual_agent import VisualAgent


class RenderAgent:
    def __init__(self) -> None:
        pass

    def render(
        self,
        song_path: str,
        audio_analysis: AudioAnalysis,
        output_path: str,
        avatar_path: Optional[str] = None,
        fps: int = 30,
        width: int = 1280,
        height: int = 720,
    ) -> str:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        visual_agent = VisualAgent(width=width, height=height)

        codec = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(output), codec, fps, (width, height))

        if not writer.isOpened():
            raise RuntimeError("Could not initialize the video writer. Verify OpenCV and FFmpeg installation.")

        avatar_image = None
        if avatar_path and os.path.exists(avatar_path):
            avatar_image = cv2.imread(avatar_path, cv2.IMREAD_UNCHANGED)
            if avatar_image is not None:
                avatar_image = cv2.cvtColor(avatar_image, cv2.COLOR_RGBA2BGRA) if avatar_image.shape[2] == 4 else avatar_image

        total_frames = int(audio_analysis.duration * fps)
        if total_frames <= 0:
            total_frames = max(int(10 * fps), 1)

        for frame_index in range(total_frames):
            t = frame_index / fps
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            frame = visual_agent.draw_frame(frame, t, audio_analysis.beats, avatar_path=avatar_path, bpm=audio_analysis.tempo)

            if avatar_image is not None:
                avatar_h, avatar_w = avatar_image.shape[:2]
                scale = min((height * 0.45) / avatar_h, (width * 0.26) / avatar_w)
                new_w = max(1, int(avatar_w * scale))
                new_h = max(1, int(avatar_h * scale))
                resized = cv2.resize(avatar_image, (new_w, new_h), interpolation=cv2.INTER_AREA)

                x = int((width - new_w) / 2)
                y = int(height * 0.6 - new_h / 2)
                if resized.shape[2] == 4:
                    alpha = resized[:, :, 3:4] / 255.0
                    frame[y : y + new_h, x : x + new_w] = (
                        alpha * resized[:, :, :3] + (1.0 - alpha) * frame[y : y + new_h, x : x + new_w]
                    ).astype(np.uint8)
                else:
                    frame[y : y + new_h, x : x + new_w] = resized

            writer.write(frame)

        writer.release()
        return str(output)
