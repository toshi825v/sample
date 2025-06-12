import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Pygame Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player properties
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
player_speed = 5

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < height - player_size:
        player_y += player_speed
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Draw the player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
