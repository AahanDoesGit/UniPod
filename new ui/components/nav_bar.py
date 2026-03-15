"""
UNI//POD — NavBar Component
Persistent top status bar.
"""

import pygame
from tokens import (
    BG_SURFACE, DIVIDER, NEON_PRIMARY, TEXT_MID,
    SCREEN_W, NAVBAR_H, FONT_SMALL, FONT_TINY
)


class NavBar:
    def __init__(self):
        self._font_brand   = None
        self._font_context = None
        self._last_context = None
        self._cached_surf  = None

    def _ensure_fonts(self):
        if self._font_brand is None:
            self._font_brand   = pygame.font.SysFont("monospace", FONT_SMALL, bold=True)
            self._font_context = pygame.font.SysFont("monospace", FONT_TINY,  bold=False)

    def draw(self, surface: pygame.Surface, context_label: str) -> pygame.Rect:
        self._ensure_fonts()
        rect = pygame.Rect(0, 0, SCREEN_W, NAVBAR_H)

        if context_label != self._last_context or self._cached_surf is None:
            surf = pygame.Surface((SCREEN_W, NAVBAR_H))
            surf.fill(BG_SURFACE)

            # Bottom border
            pygame.draw.line(surf, DIVIDER, (0, NAVBAR_H - 1), (SCREEN_W, NAVBAR_H - 1))

            # Brand
            brand_t = self._font_brand.render("UNI//POD", True, NEON_PRIMARY)
            surf.blit(brand_t, (14, (NAVBAR_H - brand_t.get_height()) // 2))

            # Context label right-aligned
            ctx_t = self._font_context.render(context_label, True, TEXT_MID)
            cx = SCREEN_W - 14 - ctx_t.get_width()
            surf.blit(ctx_t, (cx, (NAVBAR_H - ctx_t.get_height()) // 2))

            self._cached_surf  = surf
            self._last_context = context_label

        surface.blit(self._cached_surf, (0, 0))
        return rect
