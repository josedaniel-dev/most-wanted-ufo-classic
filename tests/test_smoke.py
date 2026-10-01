import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


class ClassicSmokeTests(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_game_manager_initializes_assets_and_state(self):
        from game_manager import GameManager

        manager = GameManager()
        manager.game_initialize()

        self.assertEqual(manager.screen.get_size(), (800, 600))
        self.assertEqual(len(manager.enemies), 10)
        self.assertEqual(manager.lives, 5)
        self.assertEqual(manager.score, 0)
        self.assertEqual(manager.player_speed, 10)

    def test_menu_quit_event_exits_cleanly(self):
        from game_manager import GameManager

        manager = GameManager()
        pygame.event.post(pygame.event.Event(pygame.QUIT))

        with self.assertRaises(SystemExit):
            manager.main_menu()

    def test_main_menu_f_key_toggles_fullscreen(self):
        from game_manager import GameManager

        manager = GameManager()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))

        with patch("pygame.display.toggle_fullscreen") as toggle_fullscreen:
            manager.main_menu()

        toggle_fullscreen.assert_called_once()

    def test_pause_menu_resume_and_restart_keys(self):
        from game_manager import GameManager

        manager = GameManager()
        manager.game_initialize()

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
        manager.pause_menu()

        manager.score = 90
        manager.lives = 1
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        manager.pause_menu()

        self.assertEqual(manager.score, 0)
        self.assertEqual(manager.lives, 5)

    def test_boss_warp_methods_exist_and_update_state(self):
        from game_manager import GameManager

        manager = GameManager()
        manager.game_initialize()
        manager.show_warp_speed_message("Warp speed activated!", duration_ms=1)
        manager.boss_appeared = True
        manager.boss_bullets.append([1, 2])
        manager.start_warp_speed_level()

        self.assertFalse(manager.boss_appeared)
        self.assertEqual(manager.boss_bullets, [])
        self.assertGreaterEqual(manager.background_speed, 6)

    def test_end_game_continue_keeps_legacy_reset_behavior(self):
        from game_manager import GameManager

        manager = GameManager()
        manager.game_initialize()
        manager.score = 120
        manager.lives = 2
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c))

        manager.show_end_game_message("Game Over")

        self.assertEqual(manager.score, 0)
        self.assertEqual(manager.lives, 5)

    def test_auxiliary_entities_instantiate(self):
        from entities import Boss, Enemy, Player

        player = Player()
        Enemy()
        boss = Boss()
        boss.update()

        self.assertEqual(player.speed, 10)

    def test_ui_leaderboard_writes_json(self):
        import ui

        with tempfile.TemporaryDirectory() as directory:
            previous_cwd = Path.cwd()
            try:
                os.chdir(directory)
                ui.update_leaderboard("AAA", 10)
                self.assertTrue(Path("leaderboard.json").exists())
            finally:
                os.chdir(previous_cwd)

    def test_ui_leaderboard_recovers_from_corrupt_json(self):
        import ui

        with tempfile.TemporaryDirectory() as directory:
            previous_cwd = Path.cwd()
            try:
                os.chdir(directory)
                Path("leaderboard.json").write_text("not json")
                ui.update_leaderboard("BUG", 20)
                self.assertIn('"BUG"', Path("leaderboard.json").read_text())
            finally:
                os.chdir(previous_cwd)

    def test_ui_main_menu_f_key_toggles_fullscreen(self):
        import ui

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f))
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))

        with patch("pygame.display.toggle_fullscreen") as toggle_fullscreen:
            ui.main_menu()

        toggle_fullscreen.assert_called_once()

    def test_ui_pause_menu_resume_and_restart_keys_match_prompt(self):
        import ui

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
        self.assertEqual(ui.pause_menu(), "resume")

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        self.assertEqual(ui.pause_menu(), "restart")

    def test_main_loop_processes_quit_event_without_traceback(self):
        code = """
import os
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
import main as main_module

pygame.init()
pygame.event.clear()
pygame.event.post(pygame.event.Event(pygame.QUIT))

with patch.object(main_module.GameManager, "main_menu", return_value=None):
    main_module.main()
"""
        env = os.environ.copy()
        env.update({
            "SDL_VIDEODRIVER": "dummy",
            "SDL_AUDIODRIVER": "dummy",
            "PYGAME_HIDE_SUPPORT_PROMPT": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        })

        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parents[1],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_main_loop_routes_gameplay_key_events(self):
        code = """
import os
from unittest.mock import Mock, patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
import main as main_module

pygame.init()
manager = main_module.GameManager()
manager.game_initialize()
manager.main_menu = Mock(return_value=None)
manager.pause_menu = Mock(return_value=None)

pygame.event.clear()
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_f))
pygame.event.post(pygame.event.Event(pygame.QUIT))

with patch.object(main_module, "GameManager", return_value=manager):
    main_module.main()

assert manager.pause_menu.called
assert len(manager.bullets) == 1
"""
        env = os.environ.copy()
        env.update({
            "SDL_VIDEODRIVER": "dummy",
            "SDL_AUDIODRIVER": "dummy",
            "PYGAME_HIDE_SUPPORT_PROMPT": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        })

        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parents[1],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_main_loop_routes_arrow_key_state(self):
        code = """
import os
from unittest.mock import Mock, patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
import main as main_module

class PressedKeys:
    def __getitem__(self, key):
        return key == pygame.K_RIGHT

pygame.init()
manager = main_module.GameManager()
manager.game_initialize()
manager.main_menu = Mock(return_value=None)
start_x = manager.player_x

pygame.event.clear()
pygame.event.post(pygame.event.Event(pygame.QUIT))

with patch.object(main_module, "GameManager", return_value=manager), \
        patch("pygame.key.get_pressed", return_value=PressedKeys()):
    main_module.main()

assert manager.player_x > start_x
assert manager.player_x - start_x == manager.player_speed
"""
        env = os.environ.copy()
        env.update({
            "SDL_VIDEODRIVER": "dummy",
            "SDL_AUDIODRIVER": "dummy",
            "PYGAME_HIDE_SUPPORT_PROMPT": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        })

        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=Path(__file__).resolve().parents[1],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
