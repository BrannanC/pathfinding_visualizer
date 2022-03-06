import pygame as pg

from colors import COLORS
from a_star import A_Star
from visualizer import Visualizer

WINDOW_HEIGHT = 980
WINDOW_WIDTH = 900
GRID_WIDTH = 800
ROWS = 40 # GRID_WIDTH must be divisible by ROWS or it's wonky


parent = pg.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
grid_rect = pg.Rect(0, 0, GRID_WIDTH, GRID_WIDTH )
center_x, center_y = parent.get_rect().center
grid_rect.center = (center_x, center_y + 40)
screen = parent.subsurface(grid_rect)
pg.display.set_caption("Path Finding Algorithm Visualizer")


if __name__ == "__main__":
    vs = Visualizer(parent, screen, ROWS, GRID_WIDTH)
    vs.algorithm = A_Star()
    
    running = True
    while running:
        vs.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            left, middle, right = pg.mouse.get_pressed()
            if left: # left click
                pos = pg.mouse.get_pos()
                vs.click_bottons(pos)
                cell = vs.get_cell_from_click(pos)
                if cell:
                    pressed = vs.button_pressed
                    vs.clear_if_start_or_end(cell, pressed)
                    cell.set_status(pressed)
                    if pressed == "START":
                        vs.start = cell
                    elif pressed == "END":
                        vs.end = cell
            elif right: # right click
                pos = pg.mouse.get_pos()
                cell = vs.get_cell_from_click(pos)
                if cell:
                    cell.reset()
                    if cell == vs.start:
                        vs.start = None
                    if cell == vs.end:
                        vs.end = None
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and vs.start and vs.end:
                    vs.run()
                if event.key == pg.K_c:
                    vs.clear()
                    
    pg.quit()