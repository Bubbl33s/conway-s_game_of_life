import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Conway's Game of Life", width=1200, height=800)
dpg.setup_dearpygui()


with dpg.window(label="Game"):

    with dpg.drawlist(width=1200, height=700, tag="table"):
        for i in range(0, 1200, 30):
            for j in range(0, 700, 30):
                current_cell_tag = f"cell{i}{j}"
                dpg.draw_rectangle((i, j), (i + 30, j + 30), color=(90, 90, 90), fill=(0, 0, 0), tag=current_cell_tag)


def get_mouse_pos(sender, app_data):
    x, y = dpg.get_mouse_pos()

    # Mouse cursor offset lmao
    cursor_offset = 8
    pmin_x = int(((x - cursor_offset)//30)*30)
    pmin_y = int(((y - cursor_offset)//30)*30)

    print(x, y)

    cell_tag = f"cell{pmin_x}{pmin_y}"
    print()
    print(cell_tag)
    print(dpg.get_item_configuration(cell_tag))

    # dpg.draw_rectangle((pmin_x, pmin_y), (pmin_x + 30, pmin_y + 30), color=(90, 90, 90), fill=(255, 255, 255), parent="table")

    current_fill = dpg.get_item_configuration(cell_tag)["fill"]
    new_fill = (255.0, 255.0, 255.0, 255.0) if current_fill == [0.0, 0.0, 0.0, 1.0] else (0.0, 0.0, 0.0, 255.0)
    dpg.configure_item(cell_tag, fill=new_fill)



with dpg.handler_registry():
    dpg.add_mouse_click_handler(button=0, callback=get_mouse_pos)

dpg.show_viewport()

while dpg.is_dearpygui_running():

    dpg.render_dearpygui_frame()

dpg.destroy_context()
