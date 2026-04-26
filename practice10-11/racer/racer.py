import pygame
import sys
import random
import time
from pygame.locals import *

# Initialize pygame modules
pygame.init()

# Frames per second (game speed)
FPS = 60
FramePerSec = pygame.time.Clock()

# Color definitions (RGB)
BLUE   = (0,   0,   255)
RED    = (255, 0,   0)
GREEN  = (0,   255, 0)
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
YELLOW = (255, 220, 0)

# Screen size
SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600

# Game variables
SPEED  = 5    # Enemy speed
SCORE  = 0    # Score for dodging enemies
COINS  = 0    # Collected coins

# Fonts for UI
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# Game Over text
game_over_text = font.render("Game Over", True, BLACK)

# Create game window
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer")

# Function to load image or fallback to colored rectangle if missing
def load_image_or_rect(path, fallback_size, fallback_color):
    try:
        return pygame.image.load(path).convert_alpha()
    except FileNotFoundError:
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf

# Load images (with fallback)
background   = load_image_or_rect("background.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT), (80, 80, 80))
enemy_image  = load_image_or_rect("Enemy.jpg", (60, 80), RED)
player_image = load_image_or_rect("Player.jpg", (50, 70), BLUE)

# Resize background if needed
if background.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


# ================= ENEMY CLASS =================
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image.copy()
        self.rect  = self.image.get_rect()
        # Spawn enemy at random x position at top
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        # Move enemy down
        self.rect.move_ip(0, SPEED)

        # If enemy leaves screen → respawn and increase score
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1  # Player dodged enemy
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)


# ================= PLAYER CLASS =================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image.copy()
        self.rect  = self.image.get_rect()
        # Initial player position
        self.rect.center = (160, 520)

    def move(self):
        pressed = pygame.key.get_pressed()

        # Move left
        if self.rect.left > 0 and pressed[K_LEFT]:
            self.rect.move_ip(-5, 0)

        # Move right
        if self.rect.right < SCREEN_WIDTH and pressed[K_RIGHT]:
            self.rect.move_ip(5, 0)


# ================= COIN CLASS =================
class Coin(pygame.sprite.Sprite):
    RADIUS = 12  # coin radius

    def __init__(self):
        super().__init__()

        # Create circular coin surface
        size = self.RADIUS * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)

        # Draw coin (yellow circle + border)
        pygame.draw.circle(self.image, YELLOW, (self.RADIUS, self.RADIUS), self.RADIUS)
        pygame.draw.circle(self.image, (200, 160, 0), (self.RADIUS, self.RADIUS), self.RADIUS, 2)

        self.rect = self.image.get_rect()
        self._respawn()

    def _respawn(self):
        """Spawn coin above the screen at random position"""
        self.rect.center = (
            random.randint(20, SCREEN_WIDTH - 20),
            random.randint(-SCREEN_HEIGHT, -20)
        )

    def move(self):
        """Move coin downward"""
        self.rect.move_ip(0, max(2, SPEED // 2))

        # Respawn if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self._respawn()


# Create player and enemy
P1 = Player()
E1 = Enemy()

# Create initial coins
coins_group = pygame.sprite.Group()
for _ in range(3):
    coins_group.add(Coin())

# Sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, *coins_group)

# Event: increase speed every second
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Event: spawn new coins every 4 seconds
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 4000)


# ================= GAME LOOP =================
while True:

    # -------- HANDLE EVENTS --------
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Increase enemy speed over time
        if event.type == INC_SPEED:
            SPEED += 0.5

        # Randomly spawn new coin
        if event.type == SPAWN_COIN:
            if random.random() < 0.6:  # 60% chance
                new_coin = Coin()
                coins_group.add(new_coin)
                all_sprites.add(new_coin)

    # -------- DRAW BACKGROUND --------
    DISPLAYSURF.blit(background, (0, 0))

    # -------- MOVE & DRAW OBJECTS --------
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # -------- COIN COLLECTION --------
    collected = pygame.sprite.spritecollide(P1, coins_group, False)
    for coin in collected:
        COINS += 1              # increase coin count
        coin._respawn()         # move coin back above screen

    # -------- DRAW SCORE --------
    score_surf = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(score_surf, (10, 10))

    # -------- DRAW COINS --------
    coins_surf = font_small.render(f"Coins: {COINS}", True, YELLOW)
    coin_x = SCREEN_WIDTH - coins_surf.get_width() - 10
    DISPLAYSURF.blit(coins_surf, (coin_x, 10))

    # -------- COLLISION (GAME OVER) --------
    if pygame.sprite.spritecollideany(P1, enemies):

        # Play crash sound (if exists)
        try:
            pygame.mixer.Sound("crash.wav").play()
            time.sleep(0.5)
        except Exception:
            pass

        # Show Game Over screen
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (30, 250))

        # Show final score
        final_score = font_small.render(f"Score: {SCORE}   Coins: {COINS}", True, BLACK)
        DISPLAYSURF.blit(final_score, (80, 340))

        pygame.display.update()

        # Remove all sprites
        for entity in all_sprites:
            entity.kill()

        # Pause and exit
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # -------- UPDATE SCREEN --------
    pygame.display.update()
    FramePerSec.tick(FPS)