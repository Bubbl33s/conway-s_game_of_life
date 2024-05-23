import dearpygui.dearpygui as dpg
from grid import Grid
import time

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


with dpg.window(tag="main_window"):
    with dpg.group(tag="controls_container", horizontal_spacing=10):

        dpg.add_text("Conway's Game of Life", tag="title")
        dpg.add_text("Generation: ", tag="txt_generation")
        dpg.add_text("Alive cells:", tag="txt_alive_cells")
        dpg.add_text("Dead cells:", tag="txt_dead_cells")
        dpg.add_text("Total cells:", tag="txt_total_cells")

        with dpg.group():
            speed_slider: int | str = dpg.add_slider_float(
                default_value=.1,
                min_value=.1,
                max_value=1.,
                format="%.2f",
                width=200,
                callback=set_update_speed
            )
            dpg.add_button(
                label="Play",
                tag="play_pause_button",
                width=100,
                callback=grid.play_pause_game
            )

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
