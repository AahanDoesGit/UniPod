"""
UNI//POD — Now Playing Screen
Album art box, track info, progress bar, play state indicator.

Wheel routing:
  TOP    → MENU (go home)
  BOTTOM → play/pause toggle
  LEFT   → back (pop to music list)
  RIGHT  → next track flash (prototype)
  CENTER → play/pause toggle
"""

import pygame
from tokens import (
    SCREEN_BG, SCREEN_HEADER_BG, NORMAL_TEXT, DIM_TEXT,
    DIVIDER, PROGRESS_BG, PROGRESS_FILL,
    SCREEN_W, CONTENT_Y, FONT_TRACK, FONT_BODY, FONT_UI
)
from state import AppState, ScreenID
from touch import GestureType
from components.click_wheel import ClickWheel, WheelZone

# Album art box
ART_W  = 80
ART_H  = 80
ART_X  = (SCREEN_W - ART_W) // 2   # 80
ART_Y  = 10

# Progress bar
PROG_W = 180
PROG_H = 3
PROG_X = (SCREEN_W - PROG_W) // 2  # 30
PROG_Y = 136

# Dot handle size
DOT_R  = 3


class NowPlayingScreen:
    def __init__(self, wheel: ClickWheel):
        self._wheel       = wheel
        self._font_cache: dict = {}

    def _font(self, size, bold=False):
        key = (size, bold)
        if key not in self._font_cache:
            for name in ("helvetica", "sans", "monospace"):
                try:
                    self._font_cache[key] = pygame.font.SysFont(name, size, bold=bold)
                    break
                except Exception:
                    continue
        return self._font_cache[(size, bold)]

    def on_enter(self):
        pass

    def _toggle_play(self):
        AppState().is_playing = not AppState().is_playing
        self._wheel.trigger_flash(WheelZone.BOTTOM)

    def handle_gesture(self, gesture):
        t = gesture.type

        if t == GestureType.SWIPE_LEFT:
            AppState().pop_screen()
            return

        if t == GestureType.TAP:
            zone = self._wheel.get_zone(gesture.x, gesture.y)

            if zone == WheelZone.TOP:
                AppState().go_home()
                self._wheel.trigger_flash(WheelZone.TOP)

            elif zone in (WheelZone.BOTTOM, WheelZone.CENTER):
                self._toggle_play()

            elif zone == WheelZone.LEFT:
                AppState().pop_screen()
                self._wheel.trigger_flash(WheelZone.LEFT)

            elif zone == WheelZone.RIGHT:
                self._wheel.trigger_flash(WheelZone.RIGHT)

    def update(self, dt: int):
        self._wheel.update(dt)

    def _draw_content(self, surface: pygame.Surface):
        state = AppState()

        pygame.draw.rect(surface, SCREEN_HEADER_BG, (ART_X, ART_Y, ART_W, ART_H))
        pygame.draw.rect(surface, DIVIDER,          (ART_X, ART_Y, ART_W, ART_H), 1)
        # Draw a simple music note shape
        nc = (ART_X + ART_W // 2, ART_Y + ART_H // 2)
        pygame.draw.rect(surface, DIM_TEXT, (nc[0] - 2, nc[1] - 10, 3, 14))
        pygame.draw.rect(surface, DIM_TEXT, (nc[0] - 2, nc[1] - 10, 8, 2))
        pygame.draw.ellipse(surface, DIM_TEXT, (nc[0] - 7, nc[1] + 2, 8, 5))

        # ── Track title ───────────────────────────────────────────────────
        title = state.current_track
        if len(title) > 20:
            title = title[:19] + "…"
        t = self._font(FONT_TRACK, bold=True).render(title, True, NORMAL_TEXT)
        surface.blit(t, t.get_rect(center=(SCREEN_W // 2, 100)))

        # ── Artist ────────────────────────────────────────────────────────
        a = self._font(FONT_BODY).render("Unknown Artist", True, DIM_TEXT)
        surface.blit(a, a.get_rect(center=(SCREEN_W // 2, 118)))

        # ── Progress bar ──────────────────────────────────────────────────
        pygame.draw.rect(surface, PROGRESS_BG,   (PROG_X, PROG_Y, PROG_W, PROG_H))
        fill_w = int(PROG_W * 0.38)              # static 38%
        pygame.draw.rect(surface, PROGRESS_FILL, (PROG_X, PROG_Y, fill_w, PROG_H))
        # Dot handle at progress head
        dot_x = PROG_X + fill_w
        dot_y = PROG_Y + PROG_H // 2
        pygame.draw.circle(surface, PROGRESS_FILL, (dot_x, dot_y), DOT_R)

        # ── Time labels ───────────────────────────────────────────────────
        tf = self._font(FONT_BODY)
        t_left  = tf.render("0:00", True, DIM_TEXT)
        t_right = tf.render("3:45", True, DIM_TEXT)
        surface.blit(t_left,  (PROG_X, PROG_Y + 6))
        surface.blit(t_right, (PROG_X + PROG_W - t_right.get_width(), PROG_Y + 6))

        # Draw play/pause indicator with shapes
        px = SCREEN_W // 2
        py = 162
        if state.is_playing:
            pts = [(px - 6, py - 7), (px - 6, py + 7), (px + 7, py)]
            pygame.draw.polygon(surface, NORMAL_TEXT, pts)
        else:
            pygame.draw.rect(surface, DIM_TEXT, (px - 6, py - 7, 4, 14))
            pygame.draw.rect(surface, DIM_TEXT, (px + 2, py - 7, 4, 14))

        # ── Bottom divider ────────────────────────────────────────────────
        pygame.draw.line(surface, DIVIDER, (0, 176), (SCREEN_W, 176))

    def draw(self, surface: pygame.Surface) -> list:
        pygame.draw.rect(surface, SCREEN_BG, (0, 0, SCREEN_W, 198))
        self._draw_content(surface)
        return [
            pygame.Rect(0, 0, SCREEN_W, 198),
            self._wheel.draw(surface),
        ]
