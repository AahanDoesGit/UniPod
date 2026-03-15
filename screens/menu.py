"""
UNI//POD — Main Menu Screen
"""

import pygame
from tokens import SCREEN_BG, SCREEN_W, CONTENT_Y, ITEM_H
from state import AppState, ScreenID
from touch import GestureType
from components.header_bar import HeaderBar
from components.list_view import ListView
from components.click_wheel import ClickWheel, WheelZone

MENU_ITEMS = ["Music", "Playlists", "Settings", "About"]

_DEST = {
    0: ScreenID.MUSIC,
    1: ScreenID.MUSIC,
    2: ScreenID.SETTINGS,
    3: ScreenID.SETTINGS,
}


class MainMenuScreen:
    def __init__(self, header: HeaderBar, listview: ListView, wheel: ClickWheel):
        self._header   = header
        self._listview = listview
        self._wheel    = wheel
        self._sel      = 0

    def on_enter(self):
        self._sel = 0

    def _scroll_up(self):
        self._sel = max(0, self._sel - 1)

    def _scroll_down(self):
        self._sel = min(len(MENU_ITEMS) - 1, self._sel + 1)

    def _select(self):
        AppState().push_screen(_DEST[self._sel])
        self._wheel.trigger_flash(WheelZone.CENTER)

    def handle_gesture(self, gesture):
        t = gesture.type

        if t == GestureType.SWIPE_UP:
            self._scroll_up()
            return
        if t == GestureType.SWIPE_DOWN:
            self._scroll_down()
            return

        if t == GestureType.TAP:
            zone = self._wheel.get_zone(gesture.x, gesture.y)

            if zone == WheelZone.TOP:
                self._scroll_up()
                self._wheel.trigger_flash(WheelZone.TOP)
            elif zone == WheelZone.BOTTOM:
                self._scroll_down()
                self._wheel.trigger_flash(WheelZone.BOTTOM)
            elif zone in (WheelZone.CENTER, WheelZone.RIGHT):
                self._select()
            elif zone == WheelZone.LEFT:
                self._wheel.trigger_flash(WheelZone.LEFT)
            elif zone == WheelZone.NONE:
                row_y = gesture.y - CONTENT_Y
                if 0 <= row_y < len(MENU_ITEMS) * ITEM_H:
                    self._sel = row_y // ITEM_H
                    self._select()

    def update(self, dt: int):
        self._wheel.update(dt)

    def draw(self, surface: pygame.Surface) -> list:
        pygame.draw.rect(surface, SCREEN_BG, (0, 0, SCREEN_W, 198))
        return [
            self._header.draw(surface, "iPod", show_back=False),
            self._listview.draw(surface, MENU_ITEMS, self._sel, 0,
                                y_start=CONTENT_Y, show_chevron=True),
            self._wheel.draw(surface),
        ]
