"""
UNI//POD — Music List Screen
Scrollable song list — 10 tracks, 5 visible at once.

Wheel routing:
  TOP    → MENU (go home)
  BOTTOM → scroll down
  LEFT   → back (pop screen)
  RIGHT  → open selected track
  CENTER → open selected track
"""

import pygame
from tokens import SCREEN_BG, SCREEN_W, CONTENT_Y, ITEM_H, VISIBLE_ROWS
from state import AppState, ScreenID
from touch import GestureType
from components.header_bar import HeaderBar
from components.list_view import ListView
from components.click_wheel import ClickWheel, WheelZone

TRACKS = [
    "Neon Ghost",
    "Electric Rain",
    "Void Walker",
    "Circuit Pulse",
    "Dark Signal",
    "Ultraviolet",
    "Synthetic Dawn",
    "Broken Grid",
    "Phase Drift",
    "Null City",
]


class MusicListScreen:
    def __init__(self, header: HeaderBar, listview: ListView, wheel: ClickWheel):
        self._header   = header
        self._listview = listview
        self._wheel    = wheel
        self._sel      = 0
        self._scroll   = 0

    def on_enter(self):
        self._sel    = 0
        self._scroll = 0

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _clamp_scroll(self):
        if self._sel < self._scroll:
            self._scroll = self._sel
        elif self._sel >= self._scroll + VISIBLE_ROWS:
            self._scroll = self._sel - VISIBLE_ROWS + 1
        max_scroll   = max(0, len(TRACKS) - VISIBLE_ROWS)
        self._scroll = max(0, min(self._scroll, max_scroll))

    def _scroll_up(self):
        self._sel = max(0, self._sel - 1)
        self._clamp_scroll()

    def _scroll_down(self):
        self._sel = min(len(TRACKS) - 1, self._sel + 1)
        self._clamp_scroll()

    def _open_track(self):
        AppState().current_track = TRACKS[self._sel]
        AppState().push_screen(ScreenID.NOW_PLAYING)
        self._wheel.trigger_flash(WheelZone.CENTER)

    # ── Public API ────────────────────────────────────────────────────────────

    def handle_gesture(self, gesture):
        t = gesture.type

        if t == GestureType.SWIPE_LEFT:
            AppState().pop_screen()
            return
        if t == GestureType.SWIPE_UP:
            self._scroll_up()
            return
        if t == GestureType.SWIPE_DOWN:
            self._scroll_down()
            return

        if t == GestureType.TAP:
            zone = self._wheel.get_zone(gesture.x, gesture.y)

            if zone == WheelZone.TOP:
                # MENU → home
                AppState().go_home()
                self._wheel.trigger_flash(WheelZone.TOP)

            elif zone == WheelZone.BOTTOM:
                self._scroll_down()
                self._wheel.trigger_flash(WheelZone.BOTTOM)

            elif zone == WheelZone.LEFT:
                # PREV / BACK
                AppState().pop_screen()
                self._wheel.trigger_flash(WheelZone.LEFT)

            elif zone in (WheelZone.CENTER, WheelZone.RIGHT):
                self._open_track()

            elif zone == WheelZone.NONE:
                # Direct tap on a list row
                row_y = gesture.y - CONTENT_Y
                if 0 <= row_y < VISIBLE_ROWS * ITEM_H:
                    tapped = self._scroll + row_y // ITEM_H
                    if tapped < len(TRACKS):
                        self._sel = tapped
                        self._open_track()

    def update(self, dt: int):
        self._wheel.update(dt)

    def draw(self, surface: pygame.Surface) -> list:
        pygame.draw.rect(surface, SCREEN_BG, (0, 0, SCREEN_W, 198))
        dirty = [
            self._header.draw(surface, "Songs", show_back=True),
            self._listview.draw(surface, TRACKS, self._sel, self._scroll,
                                y_start=CONTENT_Y,
                                show_chevron=False,
                                show_scrollbar=True),
            self._wheel.draw(surface),
        ]
        return dirty
