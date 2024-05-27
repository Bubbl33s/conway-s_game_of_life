import dearpygui.dearpygui as dpg
from typing import Any
from .grid import Grid
from .theme import apply_theme
from .custom_color_edit import CustomColorEdit

# VIEWPORT
# +20 for the window and +20~ for the viewport I think
V_WIDTH: int = 1272
V_HEIGHT: int = 672


class Interface:
    def __init__(self) -> None:
        self.grid: Grid = Grid()
        self.cell_colors: CustomColorEdit = CustomColorEdit(self.grid)

    def show(self) -> None:
        dpg.create_context()
        dpg.create_viewport(
            title="Conway's Game of Life",
            resizable=False,
            max_width=V_WIDTH,
            max_height=V_HEIGHT,
            large_icon="../assets/cgl.ico"
        )
        dpg.setup_dearpygui()

        with dpg.window(tag="main_window", autosize=True):
            with dpg.group(horizontal=True):
                with dpg.child_window(tag="controls_container", width=226, height=616):
                    dpg.add_spacer(height=1)
                    dpg.add_text("Conway's Game of Life", tag="txt_title")
                    dpg.add_spacer(height=2)

                    dpg.add_text("  Generation: ", tag="txt_generation")
                    dpg.add_text("  Alive cells:", tag="txt_alive_cells")
                    dpg.add_text("  Dead cells:", tag="txt_dead_cells")
                    dpg.add_text(f"  {"Total cells":<15} {self.grid.total_cells:>6}", tag="txt_total_cells")

                    dpg.add_spacer(height=1)
                    dpg.add_separator()
                    dpg.add_spacer(height=1)

                    with dpg.group():
                        dpg.add_text("Controls", tag="txt_controls")

                        with dpg.group(horizontal=True):
                            dpg.add_text("Speed")

                            dpg.add_slider_float(
                                default_value=.1,
                                min_value=.1,
                                max_value=1.,
                                format="%.1f seconds",
                                width=163,
                                callback=self.grid.set_update_speed
                            )

                        # Default horizontal spacing -> 8px ???
                        with dpg.group(horizontal=True, horizontal_spacing=7):
                            dpg.add_button(
                                label="Play",
                                tag="play_pause_button",
                                width=102,
                                callback=self.grid.play_pause_game
                            )

                            dpg.add_button(
                                label="Clear",
                                tag="clear_button",
                                width=102,
                                callback=self.grid.reset_grid
                            )

                        dpg.add_spacer(height=1)
                        dpg.add_separator()
                        dpg.add_spacer(height=1)

                        with dpg.group():
                            dpg.add_text("Paint random cells", tag="txt_random_cells")

                            with dpg.group(horizontal=True):
                                random_cells_input: Any = dpg.add_input_int(
                                    default_value=600,
                                    min_value=1,
                                    max_value=self.grid.total_cells,
                                    min_clamped=True,
                                    max_clamped=True,
                                    step=10,
                                    step_fast=50,
                                    width=150
                                )

                                dpg.add_button(
                                    label="Go",
                                    width=53,
                                    callback=lambda: self.grid.paint_random_cells(None, dpg.get_value(random_cells_input)
                                    )
                                )

                        dpg.add_spacer(height=1)
                        dpg.add_separator()
                        dpg.add_spacer(height=1)

                        with dpg.group():
                            self.cell_colors.render()

                # child_window padding -> 8 ???
                with dpg.child_window(
                        width=(self.grid.width*self.grid.cell_size + 16),
                        height=616,
                        tag="grid_container"
                ) as grid_container:
                    with dpg.drawlist(width=(self.grid.width*self.grid.cell_size), height=600) as grid_drawlist:
                        self.grid.initialize_grid(grid_drawlist)

            apply_theme()

        with dpg.handler_registry() as handler_registry_id:
            self.grid.mouse_handler(handler_registry_id)

        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)

        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            self.grid.mainloop()

        dpg.destroy_context()
