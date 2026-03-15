"""
UNI//POD — Settings Screen
Display / Sound / About — prototype, no sub-navigation.

Wheel routing:
  TOP    → MENU (go home)
  BOTTOM → scroll down
  LEFT   → back (pop screen)
  CENTER → flash (no sub-nav, prototype)
  RIGHT  → flash alias
"""

import pygame
from tokens import SCREEN_BG, SCREEN_W, CONTENT_Y, ITEM_H
from state import AppState
from touch import GestureType
from components.header_bar import HeaderBar
from components.list_view import ListView
from components.click_wheel import ClickWheel, WheelZone

SETTINGS_ITEMS = ["Display", "Sound", "About"]


class SettingsScreen:
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
        self._sel = min(len(SETTINGS_ITEMS) - 1, self._sel + 1)

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
                AppState().go_home()
                self._wheel.trigger_flash(WheelZone.TOP)

            elif zone == WheelZone.BOTTOM:
                self._scroll_down()
                self._wheel.trigger_flash(WheelZone.BOTTOM)

            elif zone == WheelZone.LEFT:
                AppState().pop_screen()
                self._wheel.trigger_flash(WheelZone.LEFT)

            elif zone in (WheelZone.CENTER, WheelZone.RIGHT):
                self._wheel.trigger_flash(WheelZone.CENTER)

            elif zone == WheelZone.NONE:
                row_y = gesture.y - CONTENT_Y
                if 0 <= row_y < len(SETTINGS_ITEMS) * ITEM_H:
                    self._sel = row_y // ITEM_H
                self._wheel.trigger_flash(WheelZone.CENTER)

    def update(self, dt: int):
        self._wheel.update(dt)

    def draw(self, surface: pygame.Surface) -> list:
        pygame.draw.rect(surface, SCREEN_BG, (0, 0, SCREEN_W, 198))
        return [
            self._header.draw(surface, "Settings", show_back=True),
            self._listview.draw(surface, SETTINGS_ITEMS, self._sel, 0,
                                y_start=CONTENT_Y, show_chevron=True),
            self._wheel.draw(surface),
        ]
