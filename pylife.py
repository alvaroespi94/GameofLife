import time
import pygame
import numpy as np
import random

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)
BUTTON_BG = (50, 50, 50)
BUTTON_TEXT = (200, 200, 200)
BUTTON_HOVER = (70, 70, 70)
BUTTON_RED = (200, 50, 50)
BUTTON_GREEN = (50, 200, 50)
FONT_SIZE = 24

CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 80, 60
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + 50

def draw_button(screen, rect, text, hover, bg_color=None):
    if bg_color:
        color = bg_color
    else:
        color = BUTTON_HOVER if hover else BUTTON_BG
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros(cells.shape, dtype=int)

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()

    cells = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    screen.fill(COLOR_GRID)
    running = False
    drawing = False

    buttons = {
        "Start/Stop": pygame.Rect(10, SCREEN_HEIGHT - 40, 100, 30),
        "Clear": pygame.Rect(120, SCREEN_HEIGHT - 40, 100, 30),
        "Randomize": pygame.Rect(230, SCREEN_HEIGHT - 40, 100, 30),
        "Quit": pygame.Rect(340, SCREEN_HEIGHT - 40, 100, 30)
    }

    while True:
        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, CELL_SIZE, with_progress=True)
        else:
            update(screen, cells, CELL_SIZE)

        mouse_pos = pygame.mouse.get_pos()
        for text, rect in buttons.items():
            hover = rect.collidepoint(mouse_pos)
            
            if text == "Start/Stop":
                draw_button(screen, rect, text, hover, BUTTON_RED if running else BUTTON_GREEN)
            else:
                draw_button(screen, rect, text, hover)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[1] < SCREEN_HEIGHT - 50:
                        drawing = True
                        cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1

                    for text, rect in buttons.items():
                        if rect.collidepoint(mouse_pos):
                            if text == "Start/Stop":
                                running = not running
                            elif text == "Clear":
                                cells = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
                            elif text == "Randomize":
                                cells = np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH), p=[0.8, 0.2])
                            elif text == "Quit":
                                pygame.quit()
                                return
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    pos = pygame.mouse.get_pos()
                    if pos[1] < SCREEN_HEIGHT - 50:
                        cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running

        clock.tick(30)

if __name__ == '__main__':
    main()
