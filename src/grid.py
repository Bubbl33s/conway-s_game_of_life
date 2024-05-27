import dearpygui.dearpygui as dpg
import numpy as np
import time

from colors import *


class Grid:
    width: int
    height: int
    cell_size: int
    pos_offset: list[int]
    is_running: bool
    update_speed: float
    last_update_time: float
    total_cells: int
    alive_cells: int
    dead_cells: int
    generation: int
    grid: np.ndarray

    alive_color: Color
    dead_color: Color
    cell_border_color: Color

    def __init__(self, width: int, height: int, cell_size: int) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cursor_offset = [8, 8]
        self.is_running = False
        self.update_speed = .1
        self.last_update_time = time.time()
        self.total_cells = self.width*self.height
        self.alive_cells = 0
        self.dead_cells = self.total_cells

        self.alive_color = WHITE
        self.dead_color = BLACK
        self.cell_border_color = GRAY_CELL_BORDER

    def initialize_grid(self, parent: int) -> None:
        self.clear_grid()

        for i in range(self.width):
            for j in range(self.height):
                current_cell_tag: str = f"cellx{i}y{j}"

                pmin: tuple[int, int] = (i*self.cell_size, j*self.cell_size)
                pmax: tuple[int, int] = (pmin[0] + self.cell_size, pmin[1] + self.cell_size)

                dpg.draw_rectangle(
                    pmin,
                    pmax,
                    color=self.cell_border_color.get_int(),
                    fill=self.dead_color.get_int(),
                    tag=current_cell_tag,
                    parent=parent
                )

    def clear_grid(self) -> None:
        # Reset attributes and UI texts
        self.is_running = False
        dpg.set_item_label("play_pause_button", "Play")
        self.grid = np.zeros((self.width, self.height), dtype=bool)
        self.generation = 1
        self.update_cells_count()

    def toggle_cell_color(self, sender, app_data) -> None:
        # CHECK IF THE MOUSE IS OVER THE GRID, FIX MULTIPLE CHILD WINDOWS BUG
        if dpg.get_active_window() != dpg.get_alias_id("grid_container"):
            return None

        mouse_button: int = dpg.get_item_configuration(sender)["button"]

        x: int
        y: int
        x, y = dpg.get_mouse_pos()

        cell_x: int = int((x - self.cursor_offset[0])//self.cell_size)
        cell_y: int = int((y - self.cursor_offset[1])//self.cell_size)
        cell_tag: str = f"cellx{cell_x}y{cell_y}"

        if dpg.does_item_exist(cell_tag):
            current_fill: list[float] = dpg.get_item_configuration(cell_tag)["fill"]
            """
            NOTE
            
            Colors are provided on a 0-1 scale list, but must be set using a 0-255 scale
            """
            # PAINT CELL
            if mouse_button == 0 and current_fill == self.dead_color.get_normalized():
                dpg.configure_item(cell_tag, fill=self.alive_color.get_float())
                self.grid[cell_x][cell_y] = True

            # UNPAINT CELL
            elif mouse_button == 1 and current_fill == self.alive_color.get_normalized():
                dpg.configure_item(cell_tag, fill=self.dead_color.get_float())
                self.grid[cell_x][cell_y] = False

            self.update_cells_count()

    def count_alive_neighbors(self, x, y):
        alive_neighbors: int = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    if 0 <= x + i < self.width and 0 <= y + j < self.height:
                        if self.grid[x + i][y + j]:
                            alive_neighbors += 1

        return alive_neighbors

    def update_grid(self) -> None:
        new_grid = np.zeros((self.width, self.height), dtype=bool)

        for i in range(self.width):
            for j in range(self.height):
                alive_neighbors = self.count_alive_neighbors(i, j)
                if self.grid[i, j]:
                    if alive_neighbors in [2, 3]:
                        new_grid[i, j] = True
                else:
                    if alive_neighbors == 3:
                        new_grid[i, j] = True

        self.grid = new_grid
        self.render_grid()

    def update_cells_count(self) -> None:
        self.alive_cells = np.count_nonzero(self.grid)
        self.dead_cells = self.total_cells - self.alive_cells

        dpg.set_value("txt_generation", f"Generation: {self.generation}")
        dpg.set_value("txt_alive_cells", f"Alive cells: {self.alive_cells}")
        dpg.set_value("txt_dead_cells", f"Dead cells: {self.dead_cells}")

    def render_grid(self) -> None:
        self.update_cells_count()

        for i in range(self.width):
            for j in range(self.height):
                cell_tag: str = f"cellx{i}y{j}"
                new_fill: list[float] | tuple[float, ...] = self.alive_color.get_float() if self.grid[i, j] \
                    else self.dead_color.get_float()
                dpg.configure_item(cell_tag, fill=new_fill)

    def play_pause_game(self) -> None:
        self.is_running = not self.is_running
        self.last_update_time = time.time() if self.is_running else 0
        dpg.set_item_label("play_pause_button", "Pause" if self.is_running else "Play")

    def paint_random_cells(self, cells_quantity: int) -> None:
        self.clear_grid()
        self.update_grid()

        painted_cells: set = set()

        while len(painted_cells) < cells_quantity:
            x: int = np.random.randint(0, self.width)
            y: int = np.random.randint(0, self.height)

            if (x, y) not in painted_cells:
                cell_tag: str = f"cellx{x}y{y}"
                # I think this here is better than call render_grid() after the loop
                dpg.configure_item(cell_tag, fill=self.alive_color.get_float())
                self.grid[x][y] = True
                painted_cells.add((x, y))

        self.update_cells_count()

    def update_border_color(self) -> None:
        for i in range(self.width):
            for j in range(self.height):
                cell_tag: str = f"cellx{i}y{j}"
                dpg.configure_item(cell_tag, color=self.cell_border_color.get_int())

    def set_update_speed(self, new_update_speed: float) -> None:
        self.update_speed = new_update_speed

    def mouse_handler(self, parent: int) -> None:
        dpg.add_mouse_down_handler(
            button=0,
            callback=self.toggle_cell_color,
            parent=parent
        )

        dpg.add_mouse_down_handler(
            button=1,
            callback=self.toggle_cell_color,
            parent=parent
        )

    def mainloop(self) -> None:
        current_time: float = time.time()

        # Update the grid only if there any alive cells
        if self.is_running and (current_time - self.last_update_time) >= self.update_speed and self.alive_cells > 0:
            self.generation += 1
            self.update_grid()
            self.last_update_time = current_time
