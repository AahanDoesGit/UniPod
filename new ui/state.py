"""
UNI//POD — State Management
Global application state singleton.
"""

from enum import Enum, auto


class ScreenID(Enum):
    BOOT = auto()
    MENU = auto()
    MUSIC = auto()
    NOW_PLAYING = auto()
    SETTINGS = auto()


class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.current_screen: ScreenID = ScreenID.BOOT
        self.selected_index: int = 0
        self.scroll_offset: int = 0
        self.current_track_idx: int = 0
        self.current_track: str = "NEON GHOST"
        self.is_playing: bool = False
        self.transition_active: bool = False
        self.transition_alpha: int = 0
        self.transition_target: ScreenID = ScreenID.MENU
        self.pending_screen_change: ScreenID | None = None

    def request_screen(self, target: ScreenID):
        """Request a screen transition — handled by main loop."""
        self.pending_screen_change = target

    def clear_pending(self):
        self.pending_screen_change = None
