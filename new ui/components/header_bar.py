"""
UNI//POD — Header Bar Component
Classic iPod-style screen title bar with optional back arrow.
"""

import pygame
from tokens import (
    SCREEN_HEADER_BG, NORMAL_TEXT, DIM_TEXT, DIVIDER,
    SCREEN_W, HEADER_H, FONT_UI
)


class HeaderBar:
    def __init__(self):
        self._font_cache: dict = {}
        self._surf_cache: dict = {}    # keyed by (title, show_back)

    def _font(self, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in self._font_cache:
            for name in ("helvetica", "sans", "monospace"):
                try:
                    self._font_cache[key] = pygame.font.SysFont(name, size, bold=bold)
                    break
                except Exception:
                    continue
        return self._font_cache[(size, bold)]

    def draw(self, surface: pygame.Surface,
             title: str, show_back: bool = False) -> pygame.Rect:
        cache_key = (title, show_back)
        if cache_key not in self._surf_cache:
            surf = pygame.Surface((SCREEN_W, HEADER_H + 1))
            surf.fill(SCREEN_HEADER_BG)

            # Bottom divider
            pygame.draw.line(surf, DIVIDER, (0, HEADER_H), (SCREEN_W, HEADER_H))

            # Back arrow
            if show_back:
                bx, by = 12, HEADER_H // 2
                pts = [(bx + 4, by - 5), (bx + 4, by + 5), (bx - 2, by)]
                pygame.draw.polygon(surf, DIM_TEXT, pts)

            # Title centered
            title_font = self._font(FONT_UI, bold=True)
            title_t    = title_font.render(title, True, NORMAL_TEXT)
            tx = (SCREEN_W - title_t.get_width()) // 2
            ty = (HEADER_H - title_t.get_height()) // 2
            surf.blit(title_t, (tx, ty))

            self._surf_cache[cache_key] = surf

        surface.blit(self._surf_cache[cache_key], (0, 0))
        return pygame.Rect(0, 0, SCREEN_W, HEADER_H + 1)
