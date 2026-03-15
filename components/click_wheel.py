"""
UNI//POD — ClickWheel Component
"""

import math
import pygame
from enum import Enum, auto
from tokens import (
    SHELL_WHITE, SHELL_MID, SHELL_DARK,
    WHEEL_FACE, WHEEL_RING,
    WHEEL_CENTER_BTN, WHEEL_CENTER_RIM,
    WHEEL_LABEL, WHEEL_PRESSED,
    SCREEN_W, SCREEN_H,
    WHEEL_AREA_TOP, WHEEL_AREA_H,
    WHEEL_CX, WHEEL_CY,
    WHEEL_R_OUTER, WHEEL_R_INNER,
    FONT_WHEEL, DIVIDER_BAND_Y, DIVIDER_BAND_H, SHELL_LIGHT
)


class WheelZone(Enum):
    NONE   = auto()
    TOP    = auto()    # MENU
    BOTTOM = auto()    # PLAY / PAUSE
    LEFT   = auto()    # PREV / BACK
    RIGHT  = auto()    # NEXT
    CENTER = auto()    # SELECT


FLASH_ALPHA_FULL = 178    # 70% of 255
FLASH_DURATION   = 150    # ms


class ClickWheel:
    def __init__(self):
        self._font_cache:   dict          = {}
        self._base_surf:    pygame.Surface | None = None
        self._flash_zone:   WheelZone     = WheelZone.NONE
        self._flash_alpha:  int           = 0
        self._center_down:  bool          = False

    def _font(self, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in self._font_cache:
            for name in ("helvetica", "sans", "monospace"):
                try:
                    f = pygame.font.SysFont(name, size, bold=bold)
                    self._font_cache[key] = f
                    break
                except Exception:
                    continue
        return self._font_cache[(size, bold)]

    def get_zone(self, tx: int, ty: int) -> WheelZone:
        dx   = tx - WHEEL_CX
        dy   = ty - WHEEL_CY
        dist = math.hypot(dx, dy)

        if dist > WHEEL_R_OUTER:
            return WheelZone.NONE
        if dist <= WHEEL_R_INNER:
            return WheelZone.CENTER

        angle = math.degrees(math.atan2(dy, dx))
        if -135 <= angle < -45:
            return WheelZone.TOP
        if 45 <= angle < 135:
            return WheelZone.BOTTOM
        if -45 <= angle < 45:
            return WheelZone.RIGHT
        return WheelZone.LEFT

    def trigger_flash(self, zone: WheelZone):
        self._flash_zone  = zone
        self._flash_alpha = FLASH_ALPHA_FULL

    def set_center_down(self, down: bool):
        if self._center_down != down:
            self._center_down = down
            self._base_surf   = None

    def update(self, dt: int):
        if self._flash_alpha > 0:
            decay             = max(1, int(FLASH_ALPHA_FULL * dt / FLASH_DURATION))
            self._flash_alpha = max(0, self._flash_alpha - decay)
            if self._flash_alpha == 0:
                self._flash_zone = WheelZone.NONE

    def _build_base(self) -> pygame.Surface:
        surf = pygame.Surface((SCREEN_W, SCREEN_H - WHEEL_AREA_TOP))
        surf.fill(SHELL_WHITE)

        cx = WHEEL_CX
        cy = WHEEL_CY - WHEEL_AREA_TOP

        pygame.draw.circle(surf, WHEEL_RING,       (cx, cy), WHEEL_R_OUTER)
        pygame.draw.circle(surf, WHEEL_FACE,       (cx, cy), WHEEL_R_OUTER - 3)
        pygame.draw.circle(surf, SHELL_MID,        (cx, cy), WHEEL_R_OUTER - 3, 1)

        # MENU label (top) — ASCII safe
        font = self._font(FONT_WHEEL)
        menu_t = font.render("MENU", True, WHEEL_LABEL)
        surf.blit(menu_t, menu_t.get_rect(center=(cx, cy - 35)))

        # BOTTOM: draw play triangle + two pause bars
        bx, by = cx, cy + 35
        # small play triangle
        tri = [(bx - 7, by - 4), (bx - 7, by + 4), (bx - 2, by)]
        pygame.draw.polygon(surf, WHEEL_LABEL, tri)
        # two pause bars
        pygame.draw.rect(surf, WHEEL_LABEL, (bx,     by - 4, 2, 8))
        pygame.draw.rect(surf, WHEEL_LABEL, (bx + 4, by - 4, 2, 8))

        # LEFT: << (prev) — two left triangles
        lx2, ly2 = cx - 38, cy
        for dx in (0, 5):
            pts = [(lx2 - dx + 5, ly2 - 4), (lx2 - dx + 5, ly2 + 4), (lx2 - dx, ly2)]
            pygame.draw.polygon(surf, WHEEL_LABEL, pts)

        # RIGHT: >> (next) — two right triangles
        rx2, ry2 = cx + 33, cy
        for dx in (0, 5):
            pts = [(rx2 + dx, ry2 - 4), (rx2 + dx, ry2 + 4), (rx2 + dx + 5, ry2)]
            pygame.draw.polygon(surf, WHEEL_LABEL, pts)

        center_color = WHEEL_CENTER_RIM if self._center_down else WHEEL_CENTER_BTN
        pygame.draw.circle(surf, center_color,     (cx, cy), WHEEL_R_INNER)
        pygame.draw.circle(surf, WHEEL_CENTER_RIM, (cx, cy), WHEEL_R_INNER, 1)

        return surf

    def _draw_zone_flash(self, surface: pygame.Surface):
        zone  = self._flash_zone
        alpha = self._flash_alpha
        if zone == WheelZone.NONE or alpha <= 0:
            return

        cx = WHEEL_CX
        cy = WHEEL_CY

        flash_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)

        if zone == WheelZone.CENTER:
            pygame.draw.circle(flash_surf,
                               (*WHEEL_PRESSED, alpha), (cx, cy), WHEEL_R_INNER)
        else:
            angle_map = {
                WheelZone.TOP:    (-135, -45),
                WheelZone.BOTTOM: (45,   135),
                WheelZone.RIGHT:  (-45,   45),
                WheelZone.LEFT:   (135,   225),
            }
            a_start, a_end = angle_map[zone]
            pts = [(cx, cy)]
            for i in range(21):
                a  = math.radians(a_start + (a_end - a_start) * i / 20)
                pts.append((
                    int(cx + (WHEEL_R_OUTER - 3) * math.cos(a)),
                    int(cy + (WHEEL_R_OUTER - 3) * math.sin(a))
                ))
            if len(pts) >= 3:
                pygame.draw.polygon(flash_surf, (*WHEEL_PRESSED, alpha), pts)
            pygame.draw.circle(flash_surf,
                                (0, 0, 0, 0), (cx, cy), WHEEL_R_INNER + 1)

        surface.blit(flash_surf, (0, 0))

    def draw(self, surface: pygame.Surface) -> pygame.Rect:
        pygame.draw.rect(surface, SHELL_DARK,
                         (0, DIVIDER_BAND_Y, SCREEN_W, DIVIDER_BAND_H))

        if self._base_surf is None:
            self._base_surf = self._build_base()
        surface.blit(self._base_surf, (0, WHEEL_AREA_TOP))

        if self._flash_alpha > 0:
            self._draw_zone_flash(surface)

        return pygame.Rect(0, DIVIDER_BAND_Y, SCREEN_W,
                           SCREEN_H - DIVIDER_BAND_Y)
