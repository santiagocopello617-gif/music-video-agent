from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, List

import cv2
import numpy as np

from .audio_agent import AudioAnalysis
from .lyric_agent import SubtitleLine
from .motion_agent import MotionState
from .preset_agent import PresetAgent
from .scene_agent import ScenePlan


class RenderAgent:
    def __init__(self) -> None:
        self.preset_agent = PresetAgent()

    def render(
        self,
        song_path: str,
        audio_analysis: AudioAnalysis,
        output_path: str,
        avatar_path: Optional[str] = None,
        fps: int = 30,
        width: int = 1280,
        height: int = 720,
        preset_name: str = "cinematic",
        scene_plan: Optional[List[ScenePlan]] = None,
        motion_plan: Optional[List[MotionState]] = None,
        subtitle_lines: Optional[List[SubtitleLine]] = None,
    ) -> str:
        preset = self.preset_agent.resolve(preset_name)
        width = width if width > 0 else preset.width
        height = height if height > 0 else preset.height

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        codec = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(output), codec, fps, (width, height))
        if not writer.isOpened():
            raise RuntimeError("Could not initialize the video writer. Verify OpenCV and FFmpeg installation.")

        avatar_image = None
        if avatar_path and os.path.exists(avatar_path):
            avatar_image = cv2.imread(avatar_path, cv2.IMREAD_UNCHANGED)

        total_frames = max(int(audio_analysis.duration * fps), 1)

        for frame_index in range(total_frames):
            t = frame_index / fps
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            scene = self._get_scene_for_time(t, scene_plan or [])
            if scene:
                frame[:] = np.array(scene.palette, dtype=np.uint8)
            else:
                frame[:] = (12, 16, 32)

            # Background glow and beat pulses
            beat_strength = self._beat_strength(t, audio_analysis.beats)
            pulse_radius = int(120 + beat_strength * 240)
            center = (width // 2, height // 2)
            cv2.circle(frame, center, pulse_radius, (120, 200, 255), 2 + int(beat_strength * 6), lineType=cv2.LINE_AA)

            # camera motion / waves
            for y in range(0, height, 8):
                wave = 18 * np.sin((y / 45.0) + t * 2.5)
                rgb = tuple(np.clip(np.array(scene.palette if scene else [18, 16, 48], dtype=np.int16) + wave, 0, 255).astype(int).tolist())
                frame[y : y + 8, :] = np.array(rgb, dtype=np.uint8)

            if avatar_image is not None:
                frame = self._add_avatar(frame, avatar_image, t, motion_plan or [], preset)

            if subtitle_lines:
                self._add_subtitles(frame, t, subtitle_lines, preset)

            writer.write(frame)

        writer.release()
        return str(output)

    def _beat_strength(self, t: float, beat_times: list[float]) -> float:
        strength = 0.0
        for beat in beat_times:
            delta = abs(t - beat)
            if delta < 0.25:
                strength = max(strength, 1.0 - delta / 0.25)
        return strength

    def _get_scene_for_time(self, time: float, scene_plan: List[ScenePlan]) -> Optional[ScenePlan]:
        for scene in scene_plan:
            if scene.start <= time <= scene.end:
                return scene
        return scene_plan[0] if scene_plan else None

    def _add_avatar(self, frame: np.ndarray, avatar_image: np.ndarray, t: float, motion_plan: List[MotionState], preset) -> np.ndarray:
        motion = None
        for m in motion_plan:
            if abs(m.time - t) < 0.25:
                motion = m
                break
        if motion is None:
            motion = motion_plan[0] if motion_plan else None

        avatar = avatar_image.copy()
        if avatar.shape[2] == 4:
            alpha = avatar[:, :, 3:4] / 255.0
            avatar_rgb = avatar[:, :, :3]
        else:
            alpha = np.ones((avatar.shape[0], avatar.shape[1], 1), dtype=np.float32)
            avatar_rgb = avatar

        h, w = avatar_rgb.shape[:2]
        scale_factor = preset.avatar_scale * (1.0 + (motion.scale - 1.0) if motion else 1.0)
        new_w = max(80, int(w * scale_factor))
        new_h = max(100, int(h * scale_factor))
        resized = cv2.resize(avatar_rgb, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        resized_alpha = cv2.resize(alpha, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        x = int((frame.shape[1] - new_w) / 2 + (motion.x_offset if motion else 0))
        y = int(frame.shape[0] * 0.62 + (motion.y_offset if motion else 0))

        # apply small sway motion
        if motion:
            x += int(np.sin(t * 6.0 + motion.time) * 18)
            y += int(np.cos(t * 5.0 + motion.time) * 8)

        overlay = frame[y : y + new_h, x : x + new_w].copy()
        composite = np.array(overlay, dtype=np.float32)
        resized_float = resized.astype(np.float32)
        alpha_float = resized_alpha.astype(np.float32)
        composite = (1.0 - alpha_float) * composite + alpha_float * resized_float
        frame[y : y + new_h, x : x + new_w] = composite.astype(np.uint8)
        return frame

    def _add_subtitles(self, frame: np.ndarray, t: float, subtitle_lines: List[SubtitleLine], preset) -> None:
        for line in subtitle_lines:
            if line.start <= t <= line.end:
                cv2.putText(
                    frame,
                    line.text,
                    (preset.subtitle_x, preset.subtitle_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    frame,
                    line.text,
                    (preset.subtitle_x + 2, preset.subtitle_y + 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.1,
                    (80, 220, 255),
                    2,
                    cv2.LINE_AA,
                )
                break
