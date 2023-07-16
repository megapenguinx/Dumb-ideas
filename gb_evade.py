import pygame
import random

# Initialize pygame  
pygame.init()

# Set up screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Load graphics
player_img = pygame.image.load('player.png')
ball_img = pygame.image.load('ball.png') 

# Set up clock for frame rate
clock = pygame.time.Clock()

# Set up font for scoring
pygame.font.init()
font = pygame.font.Font(None, 36)

# User-defined event for adding a new ball
ADD_BALL_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_BALL_EVENT, 7000)

class Player:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.speed = 5

  def move(self, dx, dy):
    # Keep the player within screen bounds
    if 0 <= self.y + dy <= screen_height - player_img.get_height():
      self.y += dy
    if 0 <= self.x + dx <= screen_width - player_img.get_width():
      self.x += dx

class Ball:
  def __init__(self, x, y, speed_x, speed_y):
    self.x = x
    self.y = y
    self.speed_x = speed_x
    self.speed_y = speed_y

  def move(self):
    self.x += self.speed_x
    self.y += self.speed_y

  def bounce(self):
    if self.y > screen_height - ball_img.get_height() or self.y < 0:
      self.speed_y *= -1
    if self.x > screen_width - ball_img.get_width() or self.x < 0:
      self.speed_x *= -1

# Initialize player and balls
player = Player(400, 300)
balls = [Ball(random.randint(0, screen_width), random.randint(0, screen_height), random.choice([-5, 5]), random.choice([-5, 5])) for _ in range(3)]

score = 0
game_over = False

def draw():
  screen.fill((0,0,0))
  
  # Draw player
  screen.blit(player_img, (player.x, player.y))
  
  # Draw balls 
  for ball in balls:
    screen.blit(ball_img, (ball.x, ball.y))

  # Draw score
  score_text = font.render(f"Score: {score}", True, (255, 255, 255))
  screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))
  
  if game_over:
    game_over_text = font.render("Game Over! Press R to retry.", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, screen_height//2))

  pygame.display.flip()
  
def reset_game():
  global score, game_over, player, balls
  player = Player(400, 300)
  balls = [Ball(random.randint(0, screen_width), random.randint(0, screen_height), random.choice([-5, 5]), random.choice([-5, 5])) for _ in range(3)]
  score = 0
  game_over = False

def reset_ball(ball):
  # Reset ball to a random position
  ball.x = random.randint(0, screen_width - ball_img.get_width())
  ball.y = random.randint(0, screen_height - ball_img.get_height())
  
# Main game loop
running = True
while running:

  # input handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r and game_over:
        reset_game()

    if event.type == ADD_BALL_EVENT and not game_over:
      balls.append(Ball(random.randint(0, screen_width), random.randint(0, screen_height), random.choice([-5, 5]), random.choice([-5, 5])))

  if game_over:
    continue

  # Check for continuous key presses
  keys = pygame.key.get_pressed()
  dx, dy = 0, 0
  if keys[pygame.K_UP]:
    dy -= 5
  if keys[pygame.K_DOWN]:  
    dy += 5
  if keys[pygame.K_LEFT]:
    dx -= 5
  if keys[pygame.K_RIGHT]:
    dx += 5
  player.move(dx, dy)

  # Get player rectangle
  player_rect = player_img.get_rect(topleft=(player.x, player.y))

  # Move and bounce balls
  for ball in balls:
    ball.move()
    ball.bounce()
    
    # Get ball rectangle
    ball_rect = ball_img.get_rect(topleft=(ball.x, ball.y))
    
    # Check for collision
    if player_rect.colliderect(ball_rect):
      game_over = True
    
  if not game_over:
    # Add score
    score += len(balls)
    
  # Draw graphics
  draw()
  
  # Limit to 60 frames per second
  clock.tick(60)

pygame.quit()
