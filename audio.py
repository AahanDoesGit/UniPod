"""
UNI//POD — Audio Manager
Handles music playback via pygame.mixer.
Auto-detects USB audio (Type-C adapter / earbuds) on Linux/UniHiker.
"""

import os
import pygame
from typing import Optional


def _find_usb_audio_card() -> Optional[int]:
    """Return ALSA card index of first USB/headset device, or None."""
    try:
        if not os.path.exists("/proc/asound/cards"):
            return None
        with open("/proc/asound/cards") as f:
            content = f.read()
        for line in content.splitlines():
            low = line.lower()
            if any(kw in low for kw in ("usb", "headset", "headphone", "earphone")):
                parts = line.strip().split()
                if parts:
                    try:
                        return int(parts[0])
                    except ValueError:
                        pass
    except Exception:
        pass
    return None


_usb_card = _find_usb_audio_card()
if _usb_card is not None:
    os.environ.setdefault("SDL_AUDIODRIVER", "alsa")
    os.environ["AUDIODEV"] = f"hw:{_usb_card},0"
    print(f"[audio] USB card {_usb_card} → AUDIODEV=hw:{_usb_card},0")
else:
    print("[audio] No USB audio, using default device")

pygame.mixer.pre_init(44100, -16, 2, 2048)



class AudioManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self._is_playing: bool = False
        self._volume: float = 1.0
        self._pause_position: float = 0.0
        self._play_start_time: Optional[float] = None
        self._initialized = True

    def load_and_play(self, filepath: str, start_pos: float = 0.0):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self._volume)
            pygame.mixer.music.play(start=start_pos)
            self._is_playing = True
            self._pause_position = start_pos
            import time
            self._play_start_time = time.time() - start_pos
            return True
        except Exception as e:
            print(f"[audio] Error: {e}")
            return False

    def pause(self):
        if self._is_playing:
            pygame.mixer.music.pause()
            import time
            self._pause_position = time.time() - (self._play_start_time or 0)
            self._is_playing = False

    def resume(self):
        if not self._is_playing:
            pygame.mixer.music.unpause()
            import time
            self._play_start_time = time.time() - self._pause_position
            self._is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self._is_playing = False
        self._pause_position = 0.0
        self._play_start_time = None

    def set_volume(self, volume: float):
        self._volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._volume)

    def is_playing(self) -> bool:
        return self._is_playing and pygame.mixer.music.get_busy()

    def get_progress(self, duration: float) -> float:
        if not self._play_start_time or duration <= 0:
            return 0.0
        import time
        return min((time.time() - self._play_start_time) / duration, 1.0)

    def get_elapsed(self) -> float:
        if not self._play_start_time:
            return 0.0
        import time
        return time.time() - self._play_start_time
