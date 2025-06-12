import pygame
import sys
import random
import asyncio

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Game settings
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_MARGIN = 1

# Calculate board position to center it
BOARD_WIDTH = GRID_WIDTH * (GRID_SIZE + GRID_MARGIN) + GRID_MARGIN
BOARD_HEIGHT = GRID_HEIGHT * (GRID_SIZE + GRID_MARGIN) + GRID_MARGIN
BOARD_X = (width - BOARD_WIDTH) // 2
BOARD_Y = (height - BOARD_HEIGHT) // 2

# Tetromino shapes
SHAPES = [
    # I piece
    [
        ['.....',
         '.....',
         'IIII.',
         '.....',
         '.....'],
        ['..I..',
         '..I..',
         '..I..',
         '..I..',
         '.....']
    ],
    # J piece
    [
        ['.....',
         '.J...',
         '.JJJ.',
         '.....',
         '.....'],
        ['.....',
         '..JJ.',
         '..J..',
         '..J..',
         '.....'],
        ['.....',
         '.....',
         '.JJJ.',
         '...J.',
         '.....'],
        ['.....',
         '..J..',
         '..J..',
         '.JJ..',
         '.....']
    ],
    # L piece
    [
        ['.....',
         '...L.',
         '.LLL.',
         '.....',
         '.....'],
        ['.....',
         '..L..',
         '..L..',
         '..LL.',
         '.....'],
        ['.....',
         '.....',
         '.LLL.',
         '.L...',
         '.....'],
        ['.....',
         '.LL..',
         '..L..',
         '..L..',
         '.....']
    ],
    # O piece
    [
        ['.....',
         '.....',
         '.OO..',
         '.OO..',
         '.....']
    ],
    # S piece
    [
        ['.....',
         '.....',
         '..SS.',
         '.SS..',
         '.....'],
        ['.....',
         '..S..',
         '..SS.',
         '...S.',
         '.....']
    ],
    # T piece
    [
        ['.....',
         '..T..',
         '.TTT.',
         '.....',
         '.....'],
        ['.....',
         '..T..',
         '..TT.',
         '..T..',
         '.....'],
        ['.....',
         '.....',
         '.TTT.',
         '..T..',
         '.....'],
        ['.....',
         '..T..',
         '.TT..',
         '..T..',
         '.....']
    ],
    # Z piece
    [
        ['.....',
         '.....',
         '.ZZ..',
         '..ZZ.',
         '.....'],
        ['.....',
         '...Z.',
         '..ZZ.',
         '..Z..',
         '.....']
    ]
]

# Colors for each shape
SHAPE_COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

# Game variables
score = 0
level = 1
lines_cleared = 0
game_over = False
paused = False
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 48)

# Create the game grid (0 means empty)
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

class Tetromino:
    def __init__(self):
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_index]
        self.color = SHAPE_COLORS[self.shape_index]
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0
        
    def get_shape(self):
        return self.shape[self.rotation % len(self.shape)]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        if not self.is_valid_position():
            self.rotation = (self.rotation - 1) % len(self.shape)

    def is_valid_position(self):
        shape = self.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell != '.':
                    pos_x = self.x + x
                    pos_y = self.y + y
                    
                    if (pos_x < 0 or pos_x >= GRID_WIDTH or 
                        pos_y >= GRID_HEIGHT or 
                        (pos_y >= 0 and grid[pos_y][pos_x] != 0)):
                        return False
        return True
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if not self.is_valid_position():
            self.x -= dx
            self.y -= dy
            return False
        return True
    
    def draw(self):
        shape = self.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell != '.':
                    draw_x = BOARD_X + (self.x + x) * (GRID_SIZE + GRID_MARGIN) + GRID_MARGIN
                    draw_y = BOARD_Y + (self.y + y) * (GRID_SIZE + GRID_MARGIN) + GRID_MARGIN
                    pygame.draw.rect(screen, self.color, (draw_x, draw_y, GRID_SIZE, GRID_SIZE))

def create_new_tetromino():
    return Tetromino()

def draw_grid():
    # Draw the background
    pygame.draw.rect(screen, WHITE, (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT))
    
    # Draw the grid cells
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            draw_x = BOARD_X + x * (GRID_SIZE + GRID_MARGIN) + GRID_MARGIN
            draw_y = BOARD_Y + y * (GRID_SIZE + GRID_MARGIN) + GRID_MARGIN
            
            if grid[y][x] == 0:
                pygame.draw.rect(screen, BLACK, (draw_x, draw_y, GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen, SHAPE_COLORS[grid[y][x] - 1], (draw_x, draw_y, GRID_SIZE, GRID_SIZE))

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    lines_text = font.render(f"Lines: {lines_cleared}", True, WHITE)
    
    screen.blit(score_text, (BOARD_X + BOARD_WIDTH + 20, BOARD_Y))
    screen.blit(level_text, (BOARD_X + BOARD_WIDTH + 20, BOARD_Y + 40))
    screen.blit(lines_text, (BOARD_X + BOARD_WIDTH + 20, BOARD_Y + 80))

def draw_game_over():
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    game_over_text = big_font.render("GAME OVER", True, RED)
    restart_text = font.render("Press R to restart", True, WHITE)
    
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 20))

def draw_pause():
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    pause_text = big_font.render("PAUSED", True, YELLOW)
    continue_text = font.render("Press P to continue", True, WHITE)
    
    screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - 50))
    screen.blit(continue_text, (width // 2 - continue_text.get_width() // 2, height // 2 + 20))

def check_lines():
    global grid, score, level, lines_cleared
    
    lines_to_clear = []
    for y in range(GRID_HEIGHT):
        if all(grid[y][x] != 0 for x in range(GRID_WIDTH)):
            lines_to_clear.append(y)
    
    if lines_to_clear:
        # Update score
        num_lines = len(lines_to_clear)
        score += [100, 300, 500, 800][min(num_lines - 1, 3)] * level
        lines_cleared += num_lines
        level = lines_cleared // 10 + 1
        
        # Remove the lines
        for line in lines_to_clear:
            for y in range(line, 0, -1):
                grid[y] = grid[y - 1][:]
            grid[0] = [0] * GRID_WIDTH

def lock_tetromino(tetromino):
    shape = tetromino.get_shape()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell != '.':
                if tetromino.y + y >= 0:  # Only add to grid if it's visible
                    grid[tetromino.y + y][tetromino.x + x] = tetromino.shape_index + 1

def reset_game():
    global grid, score, level, lines_cleared, game_over, current_tetromino, next_tetromino
    
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    score = 0
    level = 1
    lines_cleared = 0
    game_over = False
    
    current_tetromino = create_new_tetromino()
    next_tetromino = create_new_tetromino()

# Initialize game
current_tetromino = create_new_tetromino()
next_tetromino = create_new_tetromino()
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 0.5  # seconds

# Key repeat settings
pygame.key.set_repeat(200, 100)  # Delay, interval in milliseconds

async def main():
    global current_tetromino, next_tetromino, fall_time, game_over, paused, score, level, lines_cleared
    
    running = True
    while running:
        # Calculate fall speed based on level
        fall_speed = max(0.05, 0.5 - (level - 1) * 0.05)
        
        dt = clock.tick(60) / 1000  # Convert to seconds
        fall_time += dt
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not game_over and not paused:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_tetromino.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        current_tetromino.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        current_tetromino.move(0, 1)
                    elif event.key == pygame.K_UP:
                        current_tetromino.rotate()
                    elif event.key == pygame.K_SPACE:
                        # Hard drop
                        while current_tetromino.move(0, 1):
                            pass
                        
                        lock_tetromino(current_tetromino)
                        check_lines()
                        current_tetromino = next_tetromino
                        next_tetromino = create_new_tetromino()
                        
                        if not current_tetromino.is_valid_position():
                            game_over = True
                        
                        fall_time = 0
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    reset_game()
        
        # Game logic
        if not game_over and not paused:
            if fall_time >= fall_speed:
                if not current_tetromino.move(0, 1):
                    # Can't move down, lock the tetromino in place
                    lock_tetromino(current_tetromino)
                    check_lines()
                    current_tetromino = next_tetromino
                    next_tetromino = create_new_tetromino()
                    
                    if not current_tetromino.is_valid_position():
                        game_over = True
                
                fall_time = 0
        
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw the game
        draw_grid()
        if not game_over and not paused:
            current_tetromino.draw()
        draw_score()
        
        # Draw game over or pause screen
        if game_over:
            draw_game_over()
        elif paused:
            draw_pause()
        
        # Update the display
        pygame.display.flip()
        
        # Required for Pygbag
        await asyncio.sleep(0)

    # Quit Pygame
    pygame.quit()
    sys.exit()

# Pygbag requires this structure
asyncio.run(main())
