import pygame
import sys
import json
from config import *

LEADERBOARD_FILE = "leaderboard.json"


def get_fonts():
    if not pygame.font.get_init():
        pygame.font.init()
    return (
        pygame.font.SysFont(None, 36),
        pygame.font.SysFont("comicsansms", 72),
        pygame.font.SysFont("comicsansms", 48),
    )

def main_menu():
    menu_running = True
    while menu_running:
        font, _, menu_font = get_fonts()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(BLACK)
        title_text = menu_font.render("Most Wanted UFO", True, WHITE)
        start_text = font.render("Start Game", True, GREEN)
        exit_text = font.render("Exit", True, RED)
        fullscreen_text = font.render("Full Screen", True, GREEN)

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(fullscreen_text, (SCREEN_WIDTH // 2 - fullscreen_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if SCREEN_WIDTH // 2 - start_text.get_width() // 2 < mouse_x < SCREEN_WIDTH // 2 + start_text.get_width() // 2 and \
                        SCREEN_HEIGHT // 2 < mouse_y < SCREEN_HEIGHT // 2 + start_text.get_height():
                    menu_running = False
                if SCREEN_WIDTH // 2 - exit_text.get_width() // 2 < mouse_x < SCREEN_WIDTH // 2 + exit_text.get_width() // 2 and \
                        SCREEN_HEIGHT // 2 + 100 < mouse_y < SCREEN_HEIGHT // 2 + 100 + exit_text.get_height():
                    pygame.quit()
                    sys.exit()
                if SCREEN_WIDTH // 2 - fullscreen_text.get_width() // 2 < mouse_x < SCREEN_WIDTH // 2 + fullscreen_text.get_width() // 2 and \
                        SCREEN_HEIGHT // 2 + 50 < mouse_y < SCREEN_HEIGHT // 2 + 50 + fullscreen_text.get_height():
                    pygame.display.toggle_fullscreen()

def pause_menu():
    paused = True
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font, _, menu_font = get_fonts()
    while paused:
        screen.fill(BLACK)
        pause_text = menu_font.render("Paused", True, WHITE)
        resume_text = font.render("Press R to Resume", True, GREEN)
        restart_text = font.render("Press Enter to Restart", True, GREEN)
        quit_text = font.render("Press Esc to Quit", True, RED)

        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "resume"
                if event.key == pygame.K_RETURN:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_end_game_message(message, score=0):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font, end_game_font, _ = get_fonts()
    screen.fill(BLACK)
    end_game_text = end_game_font.render(message, True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press any key to restart", True, GREEN)
    continue_text = font.render("Press C to Continue", True, GREEN)
    quit_text = font.render("Press Esc to Quit", True, RED)

    screen.blit(end_game_text, (SCREEN_WIDTH // 2 - end_game_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    waiting_for_input = False  # Continue the game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    waiting_for_input = False

def enter_initials(score=0):
    initials = ""
    enter_initials_running = True
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    _, _, menu_font = get_fonts()
    while enter_initials_running:
        screen.fill(BLACK)
        enter_initials_text = menu_font.render("Enter Initials:", True, WHITE)
        initials_text = menu_font.render(initials, True, GREEN)
        screen.blit(enter_initials_text, (SCREEN_WIDTH // 2 - enter_initials_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(initials_text, (SCREEN_WIDTH // 2 - initials_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) == 3:
                    enter_initials_running = False
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]
                elif len(initials) < 3 and event.unicode.isalpha():
                    initials += event.unicode.upper()

    update_leaderboard(initials, score)
    show_leaderboard(after_initials=True)

def update_leaderboard(initials, score):
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            leaderboard = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = []

    leaderboard.append({"initials": initials, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file)

def show_leaderboard(after_initials=False):
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            leaderboard = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = []

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font, _, menu_font = get_fonts()
    screen.fill(BLACK)
    title_text = menu_font.render("Leaderboard", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 16))
    for i, entry in enumerate(leaderboard):
        entry_text = font.render(f"{i + 1}. {entry['initials']} - {entry['score']}", True, GREEN)
        screen.blit(entry_text, (SCREEN_WIDTH // 2 - entry_text.get_width() // 2, SCREEN_HEIGHT // 10 + 60 + i * 30))

    pygame.display.flip()
    pygame.time.wait(5000)
