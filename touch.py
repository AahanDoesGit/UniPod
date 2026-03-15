"""
UNI//POD — Touch / Gesture Detection
"""

import pygame
from enum import Enum, auto
from tokens import SCREEN_W, SCREEN_H


class GestureType(Enum):
    TAP        = auto()
    SWIPE_UP   = auto()
    SWIPE_DOWN = auto()
    SWIPE_LEFT = auto()


class Gesture:
    __slots__ = ("type", "x", "y")

    def __init__(self, gtype: GestureType, x: int = 0, y: int = 0):
        self.type = gtype
        self.x    = x
        self.y    = y


SWIPE_THRESHOLD  = 28
TAP_MAX_MOVE     = 10
TAP_MAX_DURATION = 220   # ms


class TouchHandler:
    def __init__(self):
        self._down_x    = 0
        self._down_y    = 0
        self._down_time = 0
        self._active    = False

    def handle_event(self, event) -> "Gesture | None":
        # Mouse events (desktop testing)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._down_x    = event.pos[0]
            self._down_y    = event.pos[1]
            self._down_time = pygame.time.get_ticks()
            self._active    = True
            return None

        if event.type == pygame.MOUSEBUTTONUP and self._active:
            self._active = False
            dx = event.pos[0] - self._down_x
            dy = event.pos[1] - self._down_y
            dt = pygame.time.get_ticks() - self._down_time
            adx, ady = abs(dx), abs(dy)

            if adx < TAP_MAX_MOVE and ady < TAP_MAX_MOVE and dt < TAP_MAX_DURATION:
                return Gesture(GestureType.TAP, self._down_x, self._down_y)
            if dx < -SWIPE_THRESHOLD and ady < 22:
                return Gesture(GestureType.SWIPE_LEFT)
            if dy < -SWIPE_THRESHOLD and adx < 22:
                return Gesture(GestureType.SWIPE_UP)
            if dy > SWIPE_THRESHOLD and adx < 22:
                return Gesture(GestureType.SWIPE_DOWN)

        # Touch events (Unihiker)
        if event.type == pygame.FINGERDOWN:
            self._down_x    = int(event.x * SCREEN_W)
            self._down_y    = int(event.y * SCREEN_H)
            self._down_time = pygame.time.get_ticks()
            self._active    = True
            return None

        if event.type == pygame.FINGERUP and self._active:
            self._active = False
            up_x = int(event.x * SCREEN_W)
            up_y = int(event.y * SCREEN_H)
            dx = up_x - self._down_x
            dy = up_y - self._down_y
            dt = pygame.time.get_ticks() - self._down_time
            adx, ady = abs(dx), abs(dy)

            if adx < TAP_MAX_MOVE and ady < TAP_MAX_MOVE and dt < TAP_MAX_DURATION:
                return Gesture(GestureType.TAP, self._down_x, self._down_y)
            if dx < -SWIPE_THRESHOLD and ady < 22:
                return Gesture(GestureType.SWIPE_LEFT)
            if dy < -SWIPE_THRESHOLD and adx < 22:
                return Gesture(GestureType.SWIPE_UP)
            if dy > SWIPE_THRESHOLD and adx < 22:
                return Gesture(GestureType.SWIPE_DOWN)

        return None
