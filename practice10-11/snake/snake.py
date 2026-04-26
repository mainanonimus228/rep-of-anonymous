"""
===================================================
  SNAKE GAME – Extended Version with File-Based Levels
  -------------------------------------------------------
  Уровни загружаются из файлов: level1.txt, level2.txt, ...
  Механики:
    - Еда обычная (+5)
    - Переход на следующий уровень после FOODS_PER_LEVEL съеденных едок
    - Экран "LEVEL CLEAR" между уровнями, ENTER пропускает его
    - Скорость растёт с каждым уровнем
    - Счёт сохраняется между уровнями
===================================================
"""
import pygame
import sys
import os
import random
import time
from pygame.locals import *

pygame.init()

# ================================================================
#  КОНСТАНТЫ
# ================================================================
CELL       = 20
COLS       = 30
ROWS       = 28
HUD_HEIGHT = 40
SCREEN_W = COLS * CELL
SCREEN_H = ROWS * CELL + HUD_HEIGHT

BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (0,   200, 0)
DARK_GREEN = (0,   140, 0)
RED        = (220, 0,   0)
GRAY       = (50,  50,  50)
LIGHT_GRAY = (120, 120, 120)
DARK_GRAY  = (80,  80,  80)
GOLD       = (255, 215, 0)
ORANGE     = (255, 140, 0)

UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

FOODS_PER_LEVEL = 3
BASE_FPS        = 8
FPS_INCREMENT   = 2
FOOD_POINTS     = 5

# ================================================================
#  ЗАГРУЗКА УРОВНЕЙ
# ================================================================
def load_level(level_number):
    filename = f"level{level_number}.txt"
    walls = set()
    if not os.path.exists(filename):
        return walls
    with open(filename, "r") as f:
        lines = f.readlines()
    for row_idx, line in enumerate(lines):
        if row_idx >= ROWS:
            break
        for col_idx, ch in enumerate(line.rstrip("\n")):
            if col_idx >= COLS:
                break
            if ch == "#":
                walls.add((col_idx, row_idx))
    return walls

def border_walls():
    walls = set()
    for c in range(COLS):
        walls.add((c, 0))
        walls.add((c, ROWS - 1))
    for r in range(1, ROWS - 1):
        walls.add((0, r))
        walls.add((COLS - 1, r))
    return walls

def all_walls_for_level(n):
    return border_walls() | load_level(n)

def level_file_exists(n):
    return os.path.exists(f"level{n}.txt")

# ================================================================
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ================================================================
def free_cells(walls):
    cells = set()
    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if (c, r) not in walls:
                cells.add((c, r))
    return cells

def spawn_food(snake_cells, walls):
    valid = free_cells(walls) - set(snake_cells)
    if not valid:
        return None
    return random.choice(list(valid))

def safe_start(walls):
    for dc in range(COLS // 2):
        col = COLS // 2 + dc
        row = ROWS // 2
        candidates = [(col - i, row) for i in range(3)]
        if all(c not in walls for c in candidates):
            return candidates
    return [(3, 1), (2, 1), (1, 1)]

# ================================================================
#  PYGAME: экран, шрифты
# ================================================================
screen     = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake")
clock      = pygame.time.Clock()
font_hud   = pygame.font.SysFont("Consolas", 22, bold=True)
font_large = pygame.font.SysFont("Consolas", 44, bold=True)

# ================================================================
#  ОТРИСОВКА
# ================================================================
def draw_cell(surface, col, row, color, shrink=2):
    rect = pygame.Rect(
        col * CELL + shrink,
        row * CELL + HUD_HEIGHT + shrink,
        CELL - shrink * 2,
        CELL - shrink * 2
    )
    pygame.draw.rect(surface, color, rect, border_radius=3)

def draw_text(surface, text, font, color, x, y):
    surf = font.render(text, True, color)
    surface.blit(surf, (x, y))

def draw_walls(surface, walls):
    border = border_walls()
    for (c, r) in walls:
        color = LIGHT_GRAY if (c, r) in border else DARK_GRAY
        draw_cell(surface, c, r, color, shrink=1)

def draw_snake(surface, snake):
    for i, (c, r) in enumerate(snake):
        draw_cell(surface, c, r, GREEN if i == 0 else DARK_GREEN)

def draw_food(surface, food_pos):
    if food_pos is None:
        return
    col, row = food_pos
    cx = col * CELL + CELL // 2
    cy = row * CELL + HUD_HEIGHT + CELL // 2
    radius = CELL // 2 - 2
    pygame.draw.circle(surface, RED, (cx, cy), radius)
    pygame.draw.circle(surface, (160, 0, 0), (cx, cy), radius, 2)

def draw_hud(surface, score, level, foods_eaten):
    surface.fill(GRAY, (0, 0, SCREEN_W, HUD_HEIGHT))
    draw_text(surface, f"Score: {score}", font_hud, WHITE, 10, 8)
    prog = f"Food: {foods_eaten}/{FOODS_PER_LEVEL}"
    ps   = font_hud.render(prog, True, ORANGE)
    surface.blit(ps, (SCREEN_W // 2 - ps.get_width() // 2, 8))
    ls = font_hud.render(f"Level: {level}", True, GOLD)
    surface.blit(ls, (SCREEN_W - ls.get_width() - 10, 8))

def draw_overlay(surface, lines, colors=None):
    ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 170))
    surface.blit(ov, (0, 0))
    total_h = len(lines) * 60
    start_y = (SCREEN_H - total_h) // 2
    for i, line in enumerate(lines):
        color = (colors[i] if colors and i < len(colors) else WHITE)
        surf  = font_large.render(line, True, color)
        surface.blit(surf, (SCREEN_W // 2 - surf.get_width() // 2, start_y + i * 60))

# ================================================================
#  СОСТОЯНИЕ ИГРЫ
# ================================================================
def new_game_state(level=1, score=0):
    walls = all_walls_for_level(level)
    snake = safe_start(walls)
    fps   = BASE_FPS + (level - 1) * FPS_INCREMENT
    return {
        "snake":     snake,
        "direction": RIGHT,
        "next_dir":  RIGHT,
        "walls":     walls,
        "food":      spawn_food(snake, walls),
        "score":     score,
        "level":     level,
        "foods_eaten_this_level": 0,
        "fps":       fps,
    }

# ================================================================
#  ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ
# ================================================================
def run_game():
    phase          = "playing"
    clear_deadline = 0.0
    pending_level  = 1
    pending_score  = 0

    state = new_game_state(level=1, score=0)

    while True:
        # ----------------------------------------------------------
        # СОБЫТИЯ
        # ----------------------------------------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if phase == "playing":
                    if   event.key in (K_UP,    K_w) and state["direction"] != DOWN:
                        state["next_dir"] = UP
                    elif event.key in (K_DOWN,  K_s) and state["direction"] != UP:
                        state["next_dir"] = DOWN
                    elif event.key in (K_LEFT,  K_a) and state["direction"] != RIGHT:
                        state["next_dir"] = LEFT
                    elif event.key in (K_RIGHT, K_d) and state["direction"] != LEFT:
                        state["next_dir"] = RIGHT
                elif phase == "level_clear":
                    if event.key in (K_RETURN, K_SPACE):
                        state = new_game_state(level=pending_level, score=pending_score)
                        phase = "playing"
                elif phase in ("game_over", "win"):
                    if event.key == K_RETURN:
                        state = new_game_state(level=1, score=0)
                        phase = "playing"

        # ----------------------------------------------------------
        # АВТОПЕРЕХОД МЕЖДУ УРОВНЯМИ
        # ----------------------------------------------------------
        if phase == "level_clear":
            if time.time() >= clear_deadline:
                state = new_game_state(level=pending_level, score=pending_score)
                phase = "playing"

        # ----------------------------------------------------------
        # ИГРОВАЯ ЛОГИКА
        # ----------------------------------------------------------
        if phase == "playing":
            state["direction"] = state["next_dir"]
            dx, dy = state["direction"]
            hc, hr = state["snake"][0]
            new_head = (hc + dx, hr + dy)

            if new_head in state["walls"]:
                phase = "game_over"
            elif new_head in state["snake"]:
                phase = "game_over"
            else:
                state["snake"].insert(0, new_head)
                if state["food"] is not None and new_head == state["food"]:
                    state["score"]                  += FOOD_POINTS
                    state["foods_eaten_this_level"] += 1
                    if state["foods_eaten_this_level"] >= FOODS_PER_LEVEL:
                        next_level = state["level"] + 1
                        if level_file_exists(next_level):
                            pending_level  = next_level
                            pending_score  = state["score"]
                            clear_deadline = time.time() + 2.0
                            phase          = "level_clear"
                        else:
                            phase = "win"
                    else:
                        state["food"] = spawn_food(state["snake"], state["walls"])
                else:
                    state["snake"].pop()

        # ----------------------------------------------------------
        # ОТРИСОВКА
        # ----------------------------------------------------------
        screen.fill(BLACK)
        draw_walls(screen, state["walls"])
        draw_snake(screen, state["snake"])
        draw_food(screen, state["food"] if phase == "playing" else None)
        draw_hud(screen, state["score"], state["level"], state["foods_eaten_this_level"])

        if phase == "level_clear":
            left = max(0.0, clear_deadline - time.time())
            draw_overlay(screen,
                [
                    "LEVEL CLEAR!",
                    f"Level {state['level']} done",
                    f"Score: {state['score']}",
                    f"-> Level {pending_level}",
                    f"ENTER  ({left:.1f}s)",
                ],
                [GREEN, LIGHT_GRAY, WHITE, GOLD, LIGHT_GRAY])
        elif phase == "game_over":
            draw_overlay(screen,
                ["GAME OVER", f"Score: {state['score']}", "ENTER - restart"],
                [RED, WHITE, LIGHT_GRAY])
        elif phase == "win":
            draw_overlay(screen,
                ["YOU WIN!", f"Score: {state['score']}", "ENTER - restart"],
                [GOLD, WHITE, LIGHT_GRAY])

        pygame.display.flip()
        clock.tick(state["fps"])

# ================================================================
#  ТОЧКА ВХОДА
# ================================================================
run_game()