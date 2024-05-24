import dearpygui.dearpygui as dpg


def apply_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(0):
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 0)

    dpg.bind_theme(global_theme)
