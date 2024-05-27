import dearpygui.dearpygui as dpg
from .grid import Grid
from .colors import Color


class CustomColorEdit:

    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.selected_radio: str = "Alive cell"
        self.color_mapping: dict[str, tuple[str, Color]] = {
            "Alive cell": ("alive_color_edit", self.grid.alive_color),
            "Dead cell": ("dead_color_edit", self.grid.dead_color),
            "Cell border": ("border_color_edit", self.grid.cell_border_color)
        }

    def update_color_picker(self, sender) -> None:
        self.selected_radio = dpg.get_value(sender)
        color = self.color_mapping[self.selected_radio][1].get_int()
        dpg.set_value("cell_color_picker", color)

    def update_grid_colors(self, sender) -> None:
        color = [int(x) for x in dpg.get_value(sender)][:3]
        tag, color_obj = self.color_mapping[self.selected_radio]
        color_obj.set_color(*color)
        dpg.set_value(tag, color_obj.get_int())

        if self.selected_radio == "Cell border":
            self.grid.update_border_color()

        self.grid.render_grid()

    def render(self) -> None:
        dpg.add_text("Color scheme", tag="txt_color_scheme")

        with dpg.group(horizontal=True):
            dpg.add_radio_button(
                items=list(self.color_mapping.keys()),
                callback=self.update_color_picker,
                tag="color_radio"
            )

            with dpg.group():
                for tag, (edit_tag, color_obj) in self.color_mapping.items():
                    dpg.add_color_edit(
                        tag=edit_tag,
                        default_value=color_obj.get_int(),
                        no_inputs=True,
                        no_picker=True,
                    )

        dpg.add_spacer(height=5)

        # Color picker
        dpg.add_color_picker(
            default_value=self.grid.alive_color.get_int(),
            no_alpha=True,
            no_side_preview=True,
            no_small_preview=True,
            display_rgb=True,
            width=210,
            tag="cell_color_picker",
            callback=self.update_grid_colors
        )
