import pygame
import sys

# Parameters
b = 1.65 
play_color = (251, 234, 235) # Pastel Pink
pause_color = (0, 0, 0) # Black
background_color = (47, 60, 126) # Blue
grid_color = (0, 0, 0) # Black
cell_size = 10
width, height = 610, 610
tick_rate = 50

pygame.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Prisoners Dilemma Cellular Automaton')

COOPERATE = 0
DEFECT = 1

# Grid dimensions
grid_width = width // cell_size
grid_height = height // cell_size

# Cell states array
cell_states = [[0] * grid_height for _ in range(grid_width)]
cell_states[grid_width // 2][grid_height // 2] = 1

paused = True
states = 2

def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if cell_states[x][y] == 1:
                color = play_color
                if paused:
                    color = pause_color
                pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, grid_color, rect, 1)  # Grid line color

def handle_click(pos):
    x, y = pos
    grid_x = x // cell_size
    grid_y = y // cell_size
    cell_states[grid_x][grid_y] = (cell_states[grid_x][grid_y] + 1) % states

def get_score(x, y):
    score = 0
    cell_state = cell_states[x][y]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < grid_width and 0 <= y + j < grid_height:
                if i == 0 and j == 0:
                    continue
                if cell_states[x + i][y + j] == COOPERATE:
                    if cell_state == COOPERATE:
                        score += 1
                    else:
                        score += b
    return score

def update_cell(x, y, scores):
    max_score = 0
    max_state = COOPERATE
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < grid_width and 0 <= y + j < grid_height:
                if scores[x + i][y + j] > max_score:
                    max_score = scores[x + i][y + j]
                    max_state = cell_states[x + i][y + j]
    return max_state

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_c:
                cell_states = [[0] * grid_height for _ in range(grid_width)]
                cell_states[grid_width // 2][grid_height // 2] = 1
    screen.fill(background_color)
    draw_grid()
    if not paused:
        next_states = [[0] * grid_height for _ in range(grid_width)]
        scores = [[0] * grid_height for _ in range(grid_width)]
        for x in range(grid_width):
            for y in range(grid_height):
                scores[x][y] = get_score(x, y)
        for x in range(grid_width):
            for y in range(grid_height):
                next_states[x][y] = update_cell(x, y, scores)
        cell_states = next_states
    pygame.display.flip()
    pygame.time.delay(tick_rate)

pygame.quit()
sys.exit()