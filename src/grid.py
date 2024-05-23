import dearpygui.dearpygui as dpg
import numpy as np
import time


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

    def __init__(self, width: int, height: int, cell_size: int, pos_offset: list[int]) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.pos_offset = pos_offset
        self.is_running = False
        self.update_speed = .1
        self.last_update_time = time.time()
        self.total_cells = self.width*self.height
        self.alive_cells = 0
        self.dead_cells = self.total_cells
        self.generation = 0

    def initialize_grid(self, parent: int) -> None:
        # Reset attributes and UI texts
        self.is_running = False
        dpg.set_item_label("play_pause_button", "Play")
        self.grid = np.zeros((self.width, self.height), dtype=bool)
        dpg.set_value("txt_total_cells", f"Total cells: {self.total_cells}")
        self.update_cells_count()

        for i in range(self.width):
            for j in range(self.height):
                current_cell_tag: str = f"cellx{i}y{j}"

                # WEIRD VERTICAL OFFSET
                w_offset = 20
                pmin: tuple[int, int] = (i*self.cell_size, j*self.cell_size + w_offset)
                pmax: tuple[int, int] = (pmin[0] + self.cell_size, pmin[1] + self.cell_size)

                dpg.draw_rectangle(
                    pmin,
                    pmax,
                    color=(30, 30, 30),
                    fill=(0, 0, 0),
                    tag=current_cell_tag,
                    parent=parent
                )

    def toggle_cell_color(self, sender, app_data) -> None:
        mouse_button: int = dpg.get_item_configuration(sender)["button"]

        x: int
        y: int
        x, y = dpg.get_mouse_pos()

        cell_x: int = int((x - self.pos_offset[0])//self.cell_size)
        cell_y: int = int((y - self.pos_offset[1])//self.cell_size)
        cell_tag: str = f"cellx{cell_x}y{cell_y}"

        if dpg.does_item_exist(cell_tag):
            current_fill: list = dpg.get_item_configuration(cell_tag)["fill"]

            # PAINT CELL
            """
            NOTE
            
            Colors are provided on a 0-1 scale, but must be set using a 0-255 scale
            That's why I'm not using color constants
            """
            if mouse_button == 0 and current_fill == [0.0, 0.0, 0.0, 1.0]:
                dpg.configure_item(cell_tag, fill=[255.0, 255.0, 255.0, 255.0])
                self.grid[cell_x][cell_y] = True
                self.alive_cells += 1
            # UNPAINT CELL
            elif mouse_button == 1 and current_fill == [1.0, 1.0, 1.0, 1.0]:
                dpg.configure_item(cell_tag, fill=[0.0, 0.0, 0.0, 255.0])
                self.grid[cell_x][cell_y] = False

            self.dead_cells = self.total_cells - self.alive_cells

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
        self.generation += 1
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
                new_fill: list = [255.0, 255.0, 255.0, 255.0] if self.grid[i, j] else [0.0, 0.0, 0.0, 255.0]
                dpg.configure_item(cell_tag, fill=new_fill)

    def play_pause_game(self) -> None:
        self.is_running = not self.is_running
        self.last_update_time = time.time() if self.is_running else 0
        dpg.set_item_label("play_pause_button", "Pause" if self.is_running else "Play")

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

    def set_update_speed(self, new_update_speed: float) -> None:
        self.update_speed = new_update_speed

    def mainloop(self) -> None:
        current_time: float = time.time()

        # Update the grid only if there any alive cells
        if self.is_running and (current_time - self.last_update_time) >= self.update_speed and self.alive_cells > 0:
            self.update_grid()
            self.last_update_time = current_time
