"""
UNI//POD — Boot Screen
iPod startup logo, loading bar, fade into Main Menu.
"""

import pygame
from tokens import (
    SCREEN_BG, NORMAL_TEXT, DIM_TEXT,
    PROGRESS_BG, PROGRESS_FILL, DIVIDER,
    SCREEN_W, SCREEN_H,
    FONT_BOOT, FONT_UI, FONT_BODY,
    SHELL_WHITE, WHEEL_AREA_TOP, DIVIDER_BAND_Y, DIVIDER_BAND_H, SHELL_DARK
)
from state import AppState, ScreenID


FADE_IN_MS  = 400
HOLD_MS     = 2000     # total before transitioning
BAR_W_FULL  = 80
BAR_H       = 4
BAR_X       = (SCREEN_W - BAR_W_FULL) // 2
BAR_Y       = 178


class BootScreen:
    def __init__(self):
        self._elapsed    = 0
        self._fade_alpha = 0
        self._done       = False
        self._fonts: dict = {}

    def _font(self, size, bold=False):
        key = (size, bold)
        if key not in self._fonts:
            for name in ("helvetica", "sans", "monospace"):
                try:
                    self._fonts[key] = pygame.font.SysFont(name, size, bold=bold)
                    break
                except Exception:
                    continue
        return self._fonts[key]

    def reset(self):
        self._elapsed    = 0
        self._fade_alpha = 0
        self._done       = False

    def update(self, dt: int):
        if self._done:
            return
        self._elapsed   += dt
        progress         = min(1.0, self._elapsed / FADE_IN_MS)
        self._fade_alpha = int(255 * progress)
        if self._elapsed >= HOLD_MS:
            self._done = True
            AppState().go_home()

    def draw(self, surface: pygame.Surface) -> list:
        # Shell and wheel area (always visible, no fade)
        surface.fill(SHELL_WHITE, (0, WHEEL_AREA_TOP, SCREEN_W, SCREEN_H - WHEEL_AREA_TOP))
        pygame.draw.rect(surface, SHELL_DARK,
                         (0, DIVIDER_BAND_Y, SCREEN_W, DIVIDER_BAND_H))

        # Screen area content on fading layer
        content = pygame.Surface((SCREEN_W, WHEEL_AREA_TOP))
        content.fill(SCREEN_BG)

        # Large logo glyph
        logo_font = self._font(FONT_BOOT, bold=True)
        logo_t    = logo_font.render("◉", True, NORMAL_TEXT)
        lx        = (SCREEN_W - logo_t.get_width())  // 2
        content.blit(logo_t, (lx, 120))

        # Sub-brand text
        sub_font  = self._font(FONT_UI)
        sub_t     = sub_font.render("UNI//POD", True, DIM_TEXT)
        sx        = (SCREEN_W - sub_t.get_width()) // 2
        content.blit(sub_t, (sx, 162))

        # Loading bar
        pygame.draw.rect(content, PROGRESS_BG,    (BAR_X, BAR_Y, BAR_W_FULL, BAR_H))
        fill_w = int(BAR_W_FULL * min(1.0, self._elapsed / HOLD_MS))
        if fill_w > 0:
            pygame.draw.rect(content, PROGRESS_FILL, (BAR_X, BAR_Y, fill_w, BAR_H))

        content.set_alpha(self._fade_alpha)
        surface.blit(content, (0, 0))

        return [pygame.Rect(0, 0, SCREEN_W, SCREEN_H)]
