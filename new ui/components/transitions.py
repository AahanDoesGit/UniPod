"""
UNI//POD — CrossFade Transition
Blends between two screen surface captures over TRANSITION_MS.
"""

import pygame
from tokens import SCREEN_W, SCREEN_H, TRANSITION_MS


class CrossFade:
    def __init__(self):
        self._old:     pygame.Surface | None = None
        self._new:     pygame.Surface | None = None
        self._elapsed: int                   = 0
        self._active:  bool                  = False

    @property
    def active(self) -> bool:
        return self._active

    def start(self, old_surf: pygame.Surface, new_surf: pygame.Surface):
        self._old     = old_surf.copy()
        self._new     = new_surf.copy()
        self._elapsed = 0
        self._active  = True

    def update(self, dt: int) -> bool:
        """Advance fade. Returns True when complete."""
        if not self._active:
            return True
        self._elapsed += dt
        if self._elapsed >= TRANSITION_MS:
            self._active = False
            return True
        return False

    def draw(self, surface: pygame.Surface):
        if not self._active or self._old is None or self._new is None:
            return
        progress  = min(1.0, self._elapsed / TRANSITION_MS)
        alpha     = int(255 * progress)
        surface.blit(self._old, (0, 0))
        new_copy = self._new.copy()
        new_copy.set_alpha(alpha)
        surface.blit(new_copy, (0, 0))
