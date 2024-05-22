import dearpygui.dearpygui as dpg
import numpy as np
from typing import cast


class Grid:
    def __init__(self, width: int, height: int, cell_size: int) -> None:
        self.width: int = width
        self.height: int = height
        self.cell_size: int = cell_size

        self.last_cell_tag: str = ""
        self.grid: np.ndarray = np.zeros((self.width, self.height), dtype=bool)

    def render_grid(self, parent: int):
        for i in range(self.width):
            for j in range(self.height):
                current_cell_tag: str = f"cellx{i}y{j}"

                pmin = (i * self.cell_size, j * self.cell_size)
                pmax = (pmin[0] + self.cell_size, pmin[1] + self.cell_size)

                dpg.draw_rectangle(
                    pmin,
                    pmax,
                    color=(90, 90, 90),
                    fill=(0, 0, 0),
                    tag=current_cell_tag,
                    parent=parent
                )

    def toggle_cell_color(self, sender, app_data) -> None:

        x, y = cast(tuple[int, int], dpg.get_mouse_pos())

        cursor_offset: int = 8
        cell_x: int = int((x - cursor_offset)//self.cell_size)
        cell_y: int = int((y - cursor_offset)//self.cell_size)
        cell_tag: str = f"cellx{cell_x}y{cell_y}"

        if cell_tag != self.last_cell_tag:
            current_fill = dpg.get_item_configuration(cell_tag)["fill"]

            new_fill: tuple[float, float, float, float] = (255.0, 255.0, 255.0, 255.0) \
                if current_fill == [0.0, 0.0, 0.0, 1.0] \
                else (0.0, 0.0, 0.0, 255.0)

            dpg.configure_item(cell_tag, fill=new_fill)

            # Update last modified cell
            self.last_cell_tag = cell_tag

    def mouse_handler(self, parent: int):
        dpg.add_mouse_down_handler(button=0, callback=self.toggle_cell_color, parent=parent)
