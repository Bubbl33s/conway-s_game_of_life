import dearpygui.dearpygui as dpg
from typing import Any


class CustomColorEdit:
    def __init__(self, default_value: tuple[int, ...], grid: Any) -> None:
        self.default_value = default_value
        self.grid = grid
        self.selected_radio: str = "Alive cell"

    def update_color_picker(self, sender) -> None:
        self.selected_radio = dpg.get_value(sender)

        color_mapping = {
            "Alive cell": self.grid.alive_color.get_int(),
            "Dead cell": self.grid.dead_color.get_int(),
            "Cell border": self.grid.cell_border_color.get_int()
        }

        dpg.set_value("cell_color_picker", color_mapping[self.selected_radio])

    def update_grid_colors(self, sender) -> None:
        color = [int(x) for x in dpg.get_value(sender)][:3]

        color_mapping = {
            "Alive cell": ("alive_color_edit", self.grid.alive_color),
            "Dead cell": ("dead_color_edit", self.grid.dead_color),
            "Cell border": ("border_color_edit", self.grid.cell_border_color)
        }

        tag, color_obj = color_mapping[self.selected_radio]
        color_obj.set_color(*color)
        dpg.set_value(tag, color_obj.get_int())

        if self.selected_radio == "Cell border":
            self.grid.update_border_color()

    def render(self) -> None:
        dpg.add_text("Color scheme:")
        with dpg.group(horizontal=True):
            dpg.add_radio_button(
                items=("Alive cell", "Dead cell", "Cell border"),
                callback=self.update_color_picker,
                tag="color_radio"
            )

            with dpg.group():
                color_data = {
                    "alive_color_edit": self.grid.alive_color.get_int(),
                    "dead_color_edit": self.grid.dead_color.get_int(),
                    "border_color_edit": self.grid.cell_border_color.get_int()
                }

                for tag, default_value in color_data.items():
                    dpg.add_color_edit(
                        tag=tag,
                        default_value=default_value,
                        no_inputs=True,
                        no_picker=True,
                    )

        # Color picker
        dpg.add_color_picker(
            default_value=self.grid.alive_color.get_int(),
            no_alpha=True,
            no_side_preview=True,
            no_small_preview=True,
            tag="cell_color_picker",
            callback=self.update_grid_colors
        )
