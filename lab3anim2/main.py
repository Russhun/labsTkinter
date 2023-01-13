import random
import time
from tkinter import *
from PIL import ImageGrab, Image

class Cell:
    def __init__(self, parent: Canvas, x, y):
        self.c = parent
        self.x = x
        self.y = y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False
        self.is_start_cell = False
        self.is_last_cell = False

    def check_cell(self, x, y, grid_cells):
        find_index = lambda x, y: x+y*cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        neighbors = []
        top = self.check_cell(self.x, self.y-1, grid_cells)
        right = self.check_cell(self.x+1, self.y, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, grid_cells)
        left = self.check_cell(self.x-1, self.y, grid_cells)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return random.choice(neighbors) if neighbors else False

    def draw_current_cell(self):
        x = self.x * tile
        y = self.y * tile
        self.c.create_rectangle(x+3, y+3, x+tile-3, y+tile-3, fill="orange")

    def draw(self):
        x = self.x * tile
        y = self.y * tile
        color = "#424242"
        if self.is_start_cell:
            color = "green"
        if self.is_last_cell:
            color = "red"
        if self.visited:
            self.c.create_rectangle(x, y, x+tile, y+tile, fill=color, outline="")

        if self.walls["top"]:
            self.c.create_line(x, y, x+tile, y, fill="blue", width=5)
        if self.walls["right"]:
            self.c.create_line(x+tile, y, x+tile, y+tile, fill="blue", width=5)
        if self.walls["bottom"]:
            self.c.create_line(x+tile, y+tile, x, y+tile, fill="blue", width=5)
        if self.walls["left"]:
            self.c.create_line(x, y+tile, x, y, fill="blue", width=7)

    def draw_start_point(self):
        x = self.x * tile
        y = self.y * tile
        self.c.create_rectangle(x + 3, y + 3, x + tile - 3, y + tile - 3, fill="green")


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls["left"] = False
        next.walls["right"] = False
    elif dx == -1:
        current.walls["right"] = False
        next.walls["left"] = False

    dy = current.y - next.y
    if dy == 1:
        current.walls["top"] = False
        next.walls["bottom"] = False
    if dy == -1:
        current.walls["bottom"] = False
        next.walls["top"] = False



class MainApplication(Canvas):
    def __init__(self, parent: Tk, *args, **kwargs):
        Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    def draw_labyrinth(self):
        grid_cells = [Cell(self, col, row) for row in range(rows) for col in range(cols)]
        current_cell = grid_cells[0]
        current_cell.walls["left"] = False
        current_cell.is_start_cell = True
        visited_cells = []
        colors, color = [], 40
        max_visited = {}
        while True:
            for i in grid_cells:
                i.draw()

            current_cell.visited = True
            current_cell.draw_current_cell()

            for i, cell in enumerate(visited_cells[1:]):
                self.create_rectangle(cell.x*tile+5, cell.y*tile+5, cell.x*tile+tile-10, cell.y*tile+tile-10,
                                      fill=f'#{colors[i][0]:02x}{colors[i][1]:02x}{colors[i][2]:02x}')

            self.parent.after(100, self.parent.update())
            next_cell = current_cell.check_neighbors(grid_cells)
            if next_cell:
                next_cell.visited = True
                visited_cells.append(current_cell)
                colors.append((min(color, 255), 10, 100))
                color += 1
                remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif visited_cells:
                if visited_cells[0].is_start_cell and (visited_cells[-1].x in (0, cols) or
                                                       visited_cells[-1].y in (0, rows)):
                    if str(len(visited_cells)) in max_visited:
                        max_visited[str(len(visited_cells))].append(visited_cells[-1])
                    else:
                        max_visited[str(len(visited_cells))] = [visited_cells[-1]]
                current_cell = visited_cells.pop()
            if len(visited_cells) == 0:
                m = random.choice(max_visited[str(max(map(int, max_visited.keys())))])
                m.is_last_cell = True
                for i in grid_cells:
                    i.draw()
                break


def save_labyrinth(event: Event, canvas, file_name="lab"):
    # save postscipt image
    if event.keysym == "s":
        canvas.postscript(file=file_name + '.eps')


if __name__ == '__main__':
    cols = 5
    rows = 5
    tile = 100
    WINDOW_WIDTH = cols * tile
    WINDOW_HEIGHT = rows * tile
    root = Tk()
    root.geometry(f"{WINDOW_WIDTH+5}x{WINDOW_HEIGHT+5}")
    c = MainApplication(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
    c.place(x=1, y=1)
    c.focus_set()
    c.draw_labyrinth()
    c.bind("<KeyPress>", lambda event, canvas=c: save_labyrinth(event, canvas))
    root.mainloop()

