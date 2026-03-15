"""
UNI//POD — Button Component
Simple rectangular buttons for Unihiker touchscreen.
"""

import pygame
from tokens import BG_SURFACE, NEON_PRIMARY, TEXT_BRIGHT, SCREEN_W, SCREEN_H
from enum import Enum, auto


class ButtonID(Enum):
    BACK = auto()
    UP = auto()
    DOWN = auto()
    OK = auto()


class Buttons:
    def __init__(self):
        self.buttons = {
            ButtonID.BACK: pygame.Rect(10, SCREEN_H - 90, 100, 30),
            ButtonID.UP: pygame.Rect(120, SCREEN_H - 90, 100, 30),
            ButtonID.DOWN: pygame.Rect(10, SCREEN_H - 50, 100, 30),
            ButtonID.OK: pygame.Rect(120, SCREEN_H - 50, 100, 30),
        }
        self.labels = {
            ButtonID.BACK: "BACK",
            ButtonID.UP: "UP",
            ButtonID.DOWN: "DOWN",
            ButtonID.OK: "OK",
        }
        self.font = pygame.font.SysFont("monospace", 14, bold=True)

    def get_button(self, x, y):
        """Return which button was tapped, or None."""
        for btn_id, rect in self.buttons.items():
            if rect.collidepoint(x, y):
                return btn_id
        return None

    def draw(self, surface):
        """Draw all buttons."""
        for btn_id, rect in self.buttons.items():
            pygame.draw.rect(surface, BG_SURFACE, rect, border_radius=15)
            pygame.draw.rect(surface, NEON_PRIMARY, rect, 2, border_radius=15)
            label = self.font.render(self.labels[btn_id], True, TEXT_BRIGHT)
            surface.blit(label, label.get_rect(center=rect.center))
        return pygame.Rect(0, SCREEN_H - 100, SCREEN_W, 100)
