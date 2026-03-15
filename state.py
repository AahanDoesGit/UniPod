"""
UNI//POD — Application State
"""

from enum import Enum, auto


class ScreenID(Enum):
    BOOT        = auto()
    MENU        = auto()
    MUSIC       = auto()
    NOW_PLAYING = auto()
    SETTINGS    = auto()


class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.current_screen:        ScreenID       = ScreenID.BOOT
        self.screen_history:        list           = []
        self.selected_index:        int            = 0
        self.scroll_offset:         int            = 0
        self.current_track:         str            = "Neon Ghost"
        self.is_playing:            bool           = False
        self.pending_screen_change: ScreenID | None = None


    def push_screen(self, target: ScreenID):

        """Navigate forward; push current screen onto history stack."""
        if self.pending_screen_change is not None:
            return
        self.screen_history.append(self.current_screen)
        self.pending_screen_change = target

    def pop_screen(self):
        """Navigate back one screen."""
        if self.pending_screen_change is not None:
            return
        if self.screen_history:
            self.pending_screen_change = self.screen_history.pop()
        else:
            self.pending_screen_change = ScreenID.MENU

    def go_home(self):
        """Jump directly to Main Menu, clear history."""
        if self.pending_screen_change is not None:
            return
        self.screen_history.clear()
        self.pending_screen_change = ScreenID.MENU

    def clear_pending(self):
        self.pending_screen_change = None
