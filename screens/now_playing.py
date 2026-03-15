"""
UNI//POD — Now Playing Screen
"""

import math
import pygame
from tokens import (
    SCREEN_BG, SCREEN_HEADER_BG, NORMAL_TEXT, DIM_TEXT,
    DIVIDER, PROGRESS_BG, PROGRESS_FILL,
    SCREEN_W, CONTENT_Y, FONT_TRACK, FONT_BODY, FONT_UI
)
from state import AppState, ScreenID
from touch import GestureType
from components.click_wheel import ClickWheel, WheelZone

ART_W  = 80
ART_H  = 80
ART_X  = (SCREEN_W - ART_W) // 2
ART_Y  = 10

PROG_W = 180
PROG_H = 3
PROG_X = (SCREEN_W - PROG_W) // 2
PROG_Y = 136
DOT_R  = 3


class NowPlayingScreen:
    def __init__(self, wheel: ClickWheel, library=None, audio=None):
        self._wheel       = wheel
        self._library     = library
        self._audio       = audio
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
        state = AppState()
        if self._audio:
            if state.is_playing:
                self._audio.pause()
                state.is_playing = False
            else:
                self._audio.resume()
                state.is_playing = True
        else:
            state.is_playing = not state.is_playing
        self._wheel.trigger_flash(WheelZone.BOTTOM)

    def _next_track(self):
        if not self._library or not self._audio:
            return
        state = AppState()
        n = len(self._library.tracks)
        if n > 0:
            state.current_track_idx = (state.current_track_idx + 1) % n
            track = self._library.get_track(state.current_track_idx)
            if track:
                state.current_track = track.title
                self._audio.load_and_play(track.filepath)
                state.is_playing = True

    def _prev_track(self):
        if not self._library or not self._audio:
            return
        state = AppState()
        n = len(self._library.tracks)
        if n > 0:
            state.current_track_idx = (state.current_track_idx - 1) % n
            track = self._library.get_track(state.current_track_idx)
            if track:
                state.current_track = track.title
                self._audio.load_and_play(track.filepath)
                state.is_playing = True

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
                self._prev_track()
                self._wheel.trigger_flash(WheelZone.LEFT)
            elif zone == WheelZone.RIGHT:
                self._next_track()
                self._wheel.trigger_flash(WheelZone.RIGHT)

    def update(self, dt: int):
        self._wheel.update(dt)
        # Auto-advance when track ends
        state = AppState()
        if self._audio and self._library and state.is_playing:
            if not self._audio.is_playing():
                self._next_track()

    def _get_progress(self):
        state = AppState()
        if self._library and self._audio:
            track = self._library.get_track(state.current_track_idx)
            if track and track.duration > 0:
                return self._audio.get_progress(track.duration)
        return 0.38   # static demo

    def _get_times(self):
        state = AppState()
        if self._library and self._audio:
            track = self._library.get_track(state.current_track_idx)
            if track:
                elapsed  = self._audio.get_elapsed()
                duration = track.duration
                def fmt(s): return f"{int(s)//60}:{int(s)%60:02d}"
                return fmt(elapsed), fmt(duration)
        return "0:00", "3:45"

    def _draw_content(self, surface: pygame.Surface):
        state = AppState()

        # Album art box
        pygame.draw.rect(surface, SCREEN_HEADER_BG, (ART_X, ART_Y, ART_W, ART_H))
        pygame.draw.rect(surface, DIVIDER,          (ART_X, ART_Y, ART_W, ART_H), 1)
        # Music note drawn as shapes
        nc = (ART_X + ART_W // 2, ART_Y + ART_H // 2)
        pygame.draw.rect(surface, DIM_TEXT, (nc[0] - 2, nc[1] - 10, 3, 14))
        pygame.draw.rect(surface, DIM_TEXT, (nc[0] - 2, nc[1] - 10, 8, 2))
        pygame.draw.ellipse(surface, DIM_TEXT, (nc[0] - 7, nc[1] + 2, 8, 5))

        # Track title
        title = state.current_track
        if len(title) > 20:
            title = title[:19] + "…"
        t = self._font(FONT_TRACK, bold=True).render(title, True, NORMAL_TEXT)
        surface.blit(t, t.get_rect(center=(SCREEN_W // 2, 100)))

        # Artist
        artist = "Unknown Artist"
        if self._library:
            track = self._library.get_track(state.current_track_idx)
            if track and track.artist:
                artist = track.artist
        if len(artist) > 22:
            artist = artist[:21] + "…"
        a = self._font(FONT_BODY).render(artist, True, DIM_TEXT)
        surface.blit(a, a.get_rect(center=(SCREEN_W // 2, 118)))

        # Progress bar
        progress = self._get_progress()
        pygame.draw.rect(surface, PROGRESS_BG,   (PROG_X, PROG_Y, PROG_W, PROG_H))
        fill_w = int(PROG_W * progress)
        if fill_w > 0:
            pygame.draw.rect(surface, PROGRESS_FILL, (PROG_X, PROG_Y, fill_w, PROG_H))
        dot_x = PROG_X + fill_w
        dot_y = PROG_Y + PROG_H // 2
        pygame.draw.circle(surface, PROGRESS_FILL, (dot_x, dot_y), DOT_R)

        # Time labels
        t_str, d_str = self._get_times()
        tf = self._font(FONT_BODY)
        t_left  = tf.render(t_str, True, DIM_TEXT)
        t_right = tf.render(d_str, True, DIM_TEXT)
        surface.blit(t_left,  (PROG_X, PROG_Y + 6))
        surface.blit(t_right, (PROG_X + PROG_W - t_right.get_width(), PROG_Y + 6))

        # Play/pause drawn as shapes
        px, py = SCREEN_W // 2, 162
        if state.is_playing:
            pts = [(px - 6, py - 7), (px - 6, py + 7), (px + 7, py)]
            pygame.draw.polygon(surface, NORMAL_TEXT, pts)
        else:
            pygame.draw.rect(surface, DIM_TEXT, (px - 6, py - 7, 4, 14))
            pygame.draw.rect(surface, DIM_TEXT, (px + 2, py - 7, 4, 14))

        # Bottom divider
        pygame.draw.line(surface, DIVIDER, (0, 176), (SCREEN_W, 176))

    def draw(self, surface: pygame.Surface) -> list:
        pygame.draw.rect(surface, SCREEN_BG, (0, 0, SCREEN_W, 198))
        self._draw_content(surface)
        return [
            pygame.Rect(0, 0, SCREEN_W, 198),
            self._wheel.draw(surface),
        ]
