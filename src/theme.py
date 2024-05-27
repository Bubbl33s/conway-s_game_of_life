import dearpygui.dearpygui as dpg

FONT_PATHS = {
    "default": "../assets/MonaspaceKrypton-Medium.otf",
    "title": "../assets/MonaspaceKrypton-Bold.otf",
    "subtitle": "../assets/MonaspaceKrypton-Bold.otf"
}

FONT_SIZES = {
    "default": 13,
    "title": 16,
    "subtitle": 14
}


def apply_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(0):
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)

    with dpg.font_registry():
        default_font = dpg.add_font(FONT_PATHS["default"], FONT_SIZES["default"])
        title_font = dpg.add_font(FONT_PATHS["title"], FONT_SIZES["title"])
        subtitle_font = dpg.add_font(FONT_PATHS["subtitle"], FONT_SIZES["subtitle"])

    dpg.bind_font(default_font)
    dpg.bind_item_font("txt_title", title_font)
    dpg.bind_item_font("txt_controls", subtitle_font)
    dpg.bind_item_font("txt_random_cells", subtitle_font)
    dpg.bind_item_font("txt_color_scheme", subtitle_font)

    dpg.bind_theme(global_theme)
