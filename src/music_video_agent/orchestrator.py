from __future__ import annotations

from pathlib import Path
from typing import Optional

from .agents.audio_agent import AudioAgent
from .agents.avatar_agent import AvatarAgent
from .agents.render_agent import RenderAgent


class Orchestrator:
    def __init__(self) -> None:
        self.audio_agent = AudioAgent()
        self.avatar_agent = AvatarAgent()
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
    ) -> str:
        song_source = self.audio_agent.prepare_audio(song_path=song_path, song_url=song_url)
        audio_analysis = self.audio_agent.analyze(song_source)
        avatar_file = self.avatar_agent.prepare_avatar(avatar_path)
        self.render_agent.render(
            song_path=song_source,
            audio_analysis=audio_analysis,
            output_path=output_path,
            avatar_path=avatar_file,
            fps=fps,
            width=width,
            height=height,
        )
        return output_path
