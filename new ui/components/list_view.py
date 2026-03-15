"""
UNI//POD — ListView Component
Classic iPod row list: blue selection bar, chevrons, hairline dividers.
"""

import pygame
from tokens import (
    SCREEN_BG, SELECTION_BAR, SELECTION_TEXT,
    NORMAL_TEXT, CHEVRON, DIVIDER,
    SCREEN_W, ITEM_H, CONTENT_Y, VISIBLE_ROWS,
    FONT_UI, DIM_TEXT
)


class ListView:
    def __init__(self):
        self._font_cache: dict = {}

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

    def draw(self,
             surface: pygame.Surface,
             items: list,
             selected_index: int,
             scroll_offset: int,
             y_start: int = CONTENT_Y,
             show_chevron: bool = True,
             show_scrollbar: bool = False) -> pygame.Rect:

        area_h    = ITEM_H * VISIBLE_ROWS
        list_rect = pygame.Rect(0, y_start, SCREEN_W, area_h)

        # Fill list background
        pygame.draw.rect(surface, SCREEN_BG, list_rect)

        visible = items[scroll_offset : scroll_offset + VISIBLE_ROWS]
        fn      = self._font(FONT_UI)

        for i, item in enumerate(visible):
            abs_idx = scroll_offset + i
            row_y   = y_start + i * ITEM_H
            is_sel  = (abs_idx == selected_index)

            if is_sel:
                pygame.draw.rect(surface, SELECTION_BAR,
                                 (0, row_y, SCREEN_W, ITEM_H))
                text_color = SELECTION_TEXT
                chev_color = SELECTION_TEXT
            else:
                text_color = NORMAL_TEXT
                chev_color = CHEVRON

            # Row label
            label = fn.render(str(item), True, text_color)
            surface.blit(label, (14, row_y + (ITEM_H - label.get_height()) // 2))

            # Chevron
            if show_chevron:
                cx_pos, cy_pos = 228, row_y + ITEM_H // 2
                pts = [(cx_pos - 3, cy_pos - 4), (cx_pos - 3, cy_pos + 4), (cx_pos + 2, cy_pos)]
                pygame.draw.polygon(surface, chev_color, pts)

            # Hairline divider (below each row)
            if i < len(visible) - 1:
                dy = row_y + ITEM_H - 1
                pygame.draw.line(surface, DIVIDER, (0, dy), (SCREEN_W, dy))

        # Scrollbar
        if show_scrollbar and len(items) > VISIBLE_ROWS:
            total    = len(items)
            bar_h    = area_h
            thumb_h  = max(16, bar_h * VISIBLE_ROWS // total)
            max_off  = total - VISIBLE_ROWS
            thumb_y  = y_start + (bar_h - thumb_h) * scroll_offset // max(1, max_off)
            pygame.draw.rect(surface, DIVIDER,
                             (SCREEN_W - 3, y_start, 2, bar_h))
            pygame.draw.rect(surface, DIM_TEXT,
                             (SCREEN_W - 3, thumb_y, 2, thumb_h))

        return list_rect
