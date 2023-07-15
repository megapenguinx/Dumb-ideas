import random
import importlib

# Check if Pygame is installed
try:
    importlib.import_module('pygame')
except ImportError:
    print("Pygame not found. Installing...")
    try:
        import pip
        pip.main(['install', 'pygame'])
        print("Pygame has been successfully installed.")
    except Exception as e:
        print("Failed to install Pygame:", str(e))
        exit(1)

# Proceed with importing Pygame
import pygame

# Initial setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Blocky Bird")

# Player
player_width = 50
player_height = 50
player = pygame.Rect(50, 275, player_width, player_height)

# Obstacle
obstacles = []
spawn_time = pygame.time.get_ticks()

# Score
score = 0
font = pygame.font.Font(None, 36)
score_text = font.render(str(score), 1, (10, 10, 10))

# Game over
game_over_font = pygame.font.Font(None, 72)
game_over_text = game_over_font.render("Game Over", 1, (255, 0, 0))
play_again_text = font.render("Press SPACE to play again", 1, (10, 10, 10))

# Game states
playing = True
game_over = False

# Game loop
while playing:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and game_over:
        # Reset game
        player.y = 275
        obstacles.clear()
        spawn_time = pygame.time.get_ticks()
        score = 0
        score_text = font.render(str(score), 1, (10, 10, 10))
        game_over = False

    if not game_over:
        if keys[pygame.K_SPACE]:
            player.y -= 5
        else:
            player.y += 5

        if pygame.time.get_ticks() - spawn_time > 1000:
            gap_height = random.randint(100, 200)
            obstacle_height = player_height * 3  # Three times the player height
            obstacles.append(pygame.Rect(800, 0, player_width, 600 - gap_height - obstacle_height))
            obstacles.append(pygame.Rect(800, 600 - gap_height, player_width, gap_height))
            spawn_time = pygame.time.get_ticks()

            score += 1
            score_text = font.render(str(score), 1, (10, 10, 10))

        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, (255, 0, 0), player)

        for obstacle in obstacles:
            obstacle.x -= 5
            pygame.draw.rect(screen, (0, 255, 0), obstacle)

            if player.colliderect(obstacle):
                game_over = True

        screen.blit(score_text, (50, 50))

    if game_over:
        screen.blit(game_over_text, (250, 200))
        screen.blit(score_text, (375, 300))
        screen.blit(play_again_text, (275, 350))

    pygame.display.update()

    obstacles = [obstacle for obstacle in obstacles if obstacle.x + obstacle.width > 0]

pygame.quit()
