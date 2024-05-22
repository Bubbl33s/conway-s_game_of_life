import dearpygui.dearpygui as dpg
from grid import Grid

dpg.create_context()
dpg.create_viewport(title="Conway's Game of Life", width=1200, height=800)
dpg.setup_dearpygui()

grid: Grid = Grid(30, 20, 30)

with dpg.window(label="Game"):
    with dpg.drawlist(width=1200, height=700, tag="table") as drawlist_id:
        grid.render_grid(drawlist_id)

with dpg.handler_registry() as handler_registry_id:
    grid.mouse_handler(handler_registry_id)

dpg.show_viewport()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()
