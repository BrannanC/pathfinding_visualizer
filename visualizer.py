
import pygame as pg

from colors import COLORS

pg.init()
header1 = pg.font.Font('freesansbold.ttf', 32)
header2 = pg.font.Font('freesansbold.ttf', 22)

class Cell:
    def __init__(cls, row, col, w) -> None:
        cls.row = row
        cls.col = col
        cls.x = w * row
        cls.y = w * col
        cls.color = COLORS["DEFAULT"]
        cls.width = w
        cls.neighbors = []
        cls.status = None
        cls.weight = 2
        cls.rect = None

    @property
    def pos(cls):
        return (cls.row, cls.col)

    def reset(cls):
        cls.status = None
        cls.weight = 2
        cls.color = COLORS["DEFAULT"]
    
    def set_color(cls, color):
        cls.color = COLORS[color] if color in COLORS else COLORS["DEFAULT"]

    def set_status(cls, status):
        cls.status = status
        cls.set_color(status)
        if status == None:
            cls.weight = 2
        elif status == "ROAD":
            cls.weight = 1
        elif status == "MUD":
            cls.weight = 3

    def draw(cls, screen):
        cls.rect = pg.draw.rect(screen, cls.color, (cls.x, cls.y, cls.width, cls.width))

    def update_neighbors(cls, grid):
        cls.neighbors.clear()
        coords = ( (0,1), (1,0), (-1, 0), (0, -1) )
        for dy, dx in coords:
            ny = cls.row + dy
            nx = cls.col + dx
            if is_valid_cell(ny, nx, grid):
                cls.neighbors.append(grid[ny][nx])

    def is_barrier(cls):
        return cls.status == "BARRIER"

def is_valid_cell(y, x, grid):
    return (
        0 <= y < len(grid)
        and 0 <= x < len(grid[0])
        and not grid[y][x].is_barrier()
    )


class Button:
    def __init__(cls, vs, text, i):
        cls.button = header2.render(text, True, COLORS["START"])
        cls.rect = cls.button.get_rect(center=(150 * i + 100,  100))
        cls.vs = vs
        cls.text = text
        cls.i = i
        cls.show()
        
    def show(cls):
        cls.vs.parent.blit(cls.button, cls.rect)

    def click(cls, pos):
        if cls.rect.collidepoint(pos):
            cls.button.fill(COLORS["BACKGROUND"])
            cls.button = header2.render(cls.text, True, COLORS["LINE"])
            cls.rect = cls.button.get_rect(center=(150 * cls.i + 100,  100))
            cls.show()
            cls.vs.button_pressed = cls.text
            return True

    def unclick(cls):
        cls.button.fill(COLORS["BACKGROUND"])
        cls.button = header2.render(cls.text, True, COLORS["START"])
        cls.rect = cls.button.get_rect(center=(150 * cls.i + 100,  100))
        cls.show()       


class Visualizer:
    def __init__(cls, parent, screen, rows, width) -> None:
        cls.rows = rows
        cls.width = width
        cls.grid = cls.make_grid()
        cls.screen = screen
        cls.parent = parent
        cls.algorithm = None
        cls.start = None
        cls.end = None
        cls.button_pressed = "START"
        cls.buttons = [
            Button(cls, button_type, i) for i, button_type in enumerate([
                "START", "END", "BARRIER", "ROAD", "MUD"
                ])
        ]
        cls.buttons[0].click(cls.buttons[0].rect.center)
    
    @property
    def cell_width(cls):
        return cls.width // cls.rows

    def click_bottons(cls, pos):
        clicked = None
        for button in cls.buttons:
            if button.click(pos):
                clicked = button
        if clicked:
            for button in cls.buttons:
                if button != clicked:
                    button.unclick()

    def make_grid(cls):
        grid = []

        for i in range(cls.rows):
            grid.append([])
            for j in range(cls.rows):
                cell = Cell(i, j, cls.cell_width)
                grid[i].append(cell)
        return grid

    def get_cell_from_click(cls, pos):
        ox, oy = cls.screen.get_offset()
        x, y = pos
        x -= ox
        y -= oy
        for row in cls.grid:
            for cell in row:
                if cell.rect.collidepoint( (x,y) ):
                    return cell

    def clear(cls):
        cls.start = None
        cls.end = None
        cls.grid = cls.make_grid()
    
    def clear_if_start_or_end(cls, cell, pressed):
        if cell == cls.start:
            cls.start.reset()
            cls.start = None
        elif cell == cls.end:
            cls.end.reset()
            cls.end = None
        if pressed == "START" and cls.start:
            cls.start.reset()
            cls.start = None
        elif pressed == "END" and cls.end:
            cls.end.reset()
            cls.end = None

    def run(cls):
        cls.algorithm.run(cls.start, cls.end, cls.grid, cls.draw)

# ******** DRAWS **********
    def draw_grid(cls):
        for i in range(cls.rows):
            pg.draw.line(
                cls.screen, COLORS["LINE"], 
                (0, i * cls.cell_width), 
                (cls.width, i * cls.cell_width)
            )
            for j in range(cls.rows):
                pg.draw.line(
                    cls.screen,
                    COLORS["LINE"],
                    (j * cls.cell_width, 0),
                    (j * cls.cell_width, cls.width)
                )

    def draw_header(cls):
        title = header1.render(cls.algorithm.title, True, COLORS["START"])
        title_rect = title.get_rect(center=(cls.parent.get_width()/2, 40))
        cls.parent.blit(title, title_rect)


    def draw(cls):
        cls.screen.fill(COLORS["BACKGROUND"])
        cls.draw_header()

        for row in cls.grid:
            for cell in row:
                cell.draw(cls.screen)
        cls.draw_grid()
        pg.display.update()
