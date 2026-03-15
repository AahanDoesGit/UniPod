"""
UNI//POD — Main Entry Point
pygame 240×320, 30 FPS, non-blocking loop, dirty-rect updates.

Run:  python main.py
"""

import sys
import pygame

from tokens import SCREEN_W, SCREEN_H
from state import AppState, ScreenID
from touch import TouchHandler
from components.click_wheel import ClickWheel, WheelZone
from components.header_bar import HeaderBar
from components.list_view import ListView
from components.transitions import CrossFade

from screens.boot import BootScreen
from screens.menu import MainMenuScreen
from screens.music_list import MusicListScreen
from screens.now_playing import NowPlayingScreen
from screens.settings import SettingsScreen

FPS = 30


def _render_to_surf(screen_obj) -> pygame.Surface:
    """Render a screen to an offscreen surface for cross-fade capture."""
    surf = pygame.Surface((SCREEN_W, SCREEN_H))
    screen_obj.draw(surf)
    return surf


def main():
    pygame.init()
    display = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("UNI//POD")
    clock = pygame.time.Clock()

    # ── Shared components (one instance each) ────────────────────────────────
    wheel    = ClickWheel()
    header   = HeaderBar()
    listview = ListView()
    fader    = CrossFade()
    touch    = TouchHandler()
    state    = AppState()

    # ── Build screen registry ─────────────────────────────────────────────────
    boot_scr  = BootScreen()
    menu_scr  = MainMenuScreen(header, listview, wheel)
    music_scr = MusicListScreen(header, listview, wheel)
    play_scr  = NowPlayingScreen(wheel)
    sett_scr  = SettingsScreen(header, listview, wheel)

    screens = {
        ScreenID.BOOT:        boot_scr,
        ScreenID.MENU:        menu_scr,
        ScreenID.MUSIC:       music_scr,
        ScreenID.NOW_PLAYING: play_scr,
        ScreenID.SETTINGS:    sett_scr,
    }

    # ── Start on boot screen ──────────────────────────────────────────────────
    active_id     = ScreenID.BOOT
    active_screen = screens[active_id]
    boot_scr.reset()

    # Track MOUSEBUTTONDOWN for wheel center press-hold visual
    def _check_center_press(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if wheel.get_zone(event.pos[0], event.pos[1]) == WheelZone.CENTER:
                wheel.set_center_down(True)
        if event.type == pygame.MOUSEBUTTONUP:
            wheel.set_center_down(False)

    # ── Main loop ─────────────────────────────────────────────────────────────
    while True:
        dt = clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            _check_center_press(event)

            if not fader.active:
                gesture = touch.handle_event(event)
                if gesture:
                    active_screen.handle_gesture(gesture)

        # Update active screen
        if not fader.active:
            active_screen.update(dt)

        # Check for pending screen change
        if state.pending_screen_change is not None and not fader.active:
            target_id     = state.pending_screen_change
            target_screen = screens[target_id]
            state.clear_pending()
            state.current_screen = target_id

            # Capture frames for cross-fade
            old_surf = display.copy()
            new_surf = _render_to_surf(target_screen)

            fader.start(old_surf, new_surf)

            # Switch active
            active_id     = target_id
            active_screen = target_screen
            if hasattr(active_screen, "on_enter"):
                active_screen.on_enter()

        # Draw
        if fader.active:
            done = fader.update(dt)
            fader.draw(display)
            pygame.display.flip()
            if done:
                # Final clean frame after fade completes
                active_screen.draw(display)
                pygame.display.flip()
        else:
            dirty = active_screen.draw(display)
            if dirty:
                pygame.display.update(dirty)
            else:
                pygame.display.flip()


if __name__ == "__main__":
    main()
