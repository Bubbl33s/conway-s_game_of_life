import dearpygui.dearpygui as dpg
from typing import Any
from grid import Grid

# CONSTANTS AND VARIABLES ---------------------------------------------
# VIEWPORT
# +20 for the window and +20 for the viewport I think
V_HEIGHT: int = 680
V_WIDTH: int = 1300

# GRID
GRID_POS: list[int] = [250, 0]
grid_width: int = 100
grid_height: int = 60
cell_size: int = 10
# ---------------------------------------------------------------------

dpg.create_context()
dpg.create_viewport(
    title="Conway's Game of Life",
    max_width=V_WIDTH,
    max_height=V_HEIGHT,
    resizable=False,
    large_icon="../assets/cgl.ico")
dpg.setup_dearpygui()

grid: Grid = Grid(grid_width, grid_height, cell_size, pos_offset=GRID_POS)


def set_update_speed(sender) -> None:
    grid.set_update_speed(dpg.get_value(sender))


def reset_grid(sender) -> None:
    grid.clear_grid()
    grid.update_grid()


def paint_random_cells(sender, cells_quantity) -> None:
    grid.paint_random_cells(cells_quantity)


with dpg.window(tag="main_window"):
    with dpg.group(tag="controls_container", horizontal_spacing=10):

        dpg.add_text("Conway's Game of Life", tag="title")
        dpg.add_text("Generation: ", tag="txt_generation")
        dpg.add_text("Alive cells:", tag="txt_alive_cells")
        dpg.add_text("Dead cells:", tag="txt_dead_cells")
        dpg.add_text("Total cells:", tag="txt_total_cells")

        with dpg.group():
            speed_slider: Any = dpg.add_slider_float(
                default_value=.1,
                min_value=.1,
                max_value=1.,
                format="%.2f",
                width=200,
                callback=set_update_speed
            )

            # Default horizontal spacing -> 8px ???
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Play",
                    tag="play_pause_button",
                    width=100,
                    callback=grid.play_pause_game
                )
                dpg.add_button(
                    label="Clear",
                    tag="clear_button",
                    width=100,
                    callback=reset_grid
                )

            dpg.add_separator()

            with dpg.group():
                # TODO: UPDATE ATTS WHEN RESIZING GRID
                random_cells_input: Any = dpg.add_input_int(
                    default_value=grid.total_cells//5,
                    min_value=1,
                    max_value=grid.total_cells,
                    min_clamped=True,
                    step=10,
                    step_fast=50,
                    width=200
                )

                dpg.add_button(
                    label="Go",
                    width=100,
                    callback=lambda: paint_random_cells(None, dpg.get_value(random_cells_input))
                )

            # TODO: CHANGE GRID SIZE
            # DELETE AND RE INIT GRID INSTANCE?

    # HEIGHT MUST BE CELL_SIZE divisor + 20 (TOTAL PADDING I GUESS) ???
    with dpg.group(width=1020, height=620, pos=GRID_POS, tag="grid_container"):
        with dpg.drawlist(width=1000, height=600, tag="grid") as drawlist_id:
            grid.initialize_grid(drawlist_id)

with dpg.handler_registry() as handler_registry_id:
    grid.mouse_handler(handler_registry_id)

dpg.show_viewport()
dpg.set_primary_window("main_window", True)

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    grid.mainloop()

dpg.destroy_context()
