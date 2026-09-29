from __future__ import annotations

from typing import Optional

from .agents.audio_agent import AudioAgent
from .agents.lyric_agent import LyricAgent
from .agents.motion_agent import MotionAgent
from .agents.render_agent import RenderAgent
from .agents.scene_agent import SceneAgent


class Orchestrator:
    def __init__(self) -> None:
        self.audio_agent = AudioAgent()
        self.scene_agent = SceneAgent()
        self.lyric_agent = LyricAgent()
        self.motion_agent = MotionAgent()
        self.render_agent = RenderAgent()

    def run(
        self,
        song_path: Optional[str] = None,
        song_url: Optional[str] = None,
        avatar_path: Optional[str] = None,
        output_path: str = "output/music_video.mp4",
        fps: int = 30,
        width: int = 1280,
        height: int = 720,
        preset_name: str = "cinematic",
    ) -> str:
        source = self.audio_agent.prepare_audio(song_path=song_path, song_url=song_url)
        audio_analysis = self.audio_agent.analyze(source)

        scene_plan = self.scene_agent.build_scene_plan(audio_analysis)
        motion_plan = self.motion_agent.generate_motion_plan(audio_analysis, scene_plan)
        subtitle_lines = self.lyric_agent.generate_lyrics(scene_plan, audio_analysis.duration)

        return self.render_agent.render(
            song_path=source,
            audio_analysis=audio_analysis,
            output_path=output_path,
            avatar_path=avatar_path,
            fps=fps,
            width=width,
            height=height,
            preset_name=preset_name,
            scene_plan=scene_plan,
            motion_plan=motion_plan,
            subtitle_lines=subtitle_lines,
        )
