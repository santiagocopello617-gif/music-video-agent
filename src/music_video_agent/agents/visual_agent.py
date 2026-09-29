from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw


class AvatarAgent:
    def __init__(self) -> None:
        self.temp_dir = Path(tempfile.gettempdir()) / "music_video_agent"
        self.temp_dir.mkdir(exist_ok=True)

    def prepare_avatar(self, avatar_path: Optional[str] = None) -> Optional[str]:
        if avatar_path and os.path.exists(avatar_path):
            return avatar_path

        if avatar_path and avatar_path.startswith("http"):
            import requests

            target = self.temp_dir / "remote_avatar.png"
            response = requests.get(avatar_path, timeout=60)
            response.raise_for_status()
            target.write_bytes(response.content)
            return str(target)

        fallback = self.temp_dir / "fallback_avatar.png"
        self._generate_placeholder(fallback)
        return str(fallback)

    def _generate_placeholder(self, target: Path) -> None:
        width, height = 512, 512
        image = Image.new("RGBA", (width, height), (20, 20, 30, 255))
        draw = ImageDraw.Draw(image)

        # Background glow
        for r in range(180, 0, -20):
            alpha = int(60 * (r / 180))
            draw.ellipse((256 - r, 256 - r, 256 + r, 256 + r), outline=(120, 195, 255, alpha))

        # Face circle
        draw.ellipse((170, 150, 340, 330), fill=(240, 220, 180, 255))
        # Hair
        draw.ellipse((165, 120, 345, 210), fill=(38, 40, 50, 255))
        # Eyes
        draw.ellipse((205, 210, 225, 225), fill=(24, 24, 28, 255))
        draw.ellipse((285, 210, 305, 225), fill=(24, 24, 28, 255))
        draw.arc((210, 235, 302, 285), start=200, end=340, fill=(24, 24, 28, 255), width=5)

        image.save(target)
