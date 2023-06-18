import customtkinter as ctk
from PIL import Image
from graphviz import Graph, Digraph
import main
from customtkinter import filedialog

# TODO: show DP Table
# TODO: Going from point other than start
# TODO: Add Comments
# TODO: Check if route is possible

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Route Finder")
# full screen
# app.attributes('-fullscreen', True)
app.geometry("1680x920")
# sizing disabled
app.resizable(False, False)

main_frame = ctk.CTkFrame(master=app)
main_frame.pack(padx=20, pady=20)

left_side_frame = ctk.CTkFrame(master=main_frame)
left_side_frame.pack(side=ctk.LEFT, padx=20, pady=5, anchor="n")

file_frame = ctk.CTkFrame(master=left_side_frame)
file_frame.pack(side=ctk.TOP, padx=20, pady=5)
file_lb = ctk.CTkLabel(master=file_frame, text="File: ")
file_lb.pack(side=ctk.LEFT, padx=20, pady=5)
file_path_lb = ctk.CTkEntry(master=file_frame, state="readonly")
file_path_lb.pack(side=ctk.LEFT, padx=20, ipadx=100, pady=5)
file_browse_bt = ctk.CTkButton(master=file_frame, text="Browse")
file_browse_bt.pack(side=ctk.LEFT, padx=20, pady=5)

city_choose_frame = ctk.CTkFrame(master=left_side_frame)
city_choose_frame.pack(side=ctk.TOP, padx=20, pady=5)

start_city_lb = ctk.CTkLabel(master=city_choose_frame, text="Start City: ")
start_city_lb.pack(side=ctk.LEFT, padx=20, pady=5)

start_city_entry = ctk.CTkOptionMenu(master=city_choose_frame)
start_city_entry.set("Select:")
start_city_entry.pack(side=ctk.LEFT, padx=20, pady=5)
start_city_entry.configure(state="disabled")

end_city_lb = ctk.CTkLabel(master=city_choose_frame, text="End City: ")
end_city_lb.pack(side=ctk.LEFT, padx=20, pady=5)

end_city_entry = ctk.CTkOptionMenu(master=city_choose_frame, state="disabled")
end_city_entry.set("Select:")
end_city_entry.pack(side=ctk.LEFT, padx=20, pady=5)
# end_city_entry.configure(state="disabled")

show_dp_table_bt = ctk.CTkButton(master=left_side_frame, text="Show DP Table", state="disabled")
show_dp_table_bt.pack(side=ctk.TOP, padx=20, pady=5)
button_frame = ctk.CTkFrame(master=left_side_frame)
button_frame.pack(side=ctk.BOTTOM, padx=20, pady=5, anchor="s")
# find_route_bt = ctk.CTkButton(master=button_frame, text="Find Routes", state="disabled")
# find_route_bt.pack(side=ctk.LEFT, padx=20, pady=20)
prev_route_bt = ctk.CTkButton(master=button_frame, text="Previous Route", state="disabled")
prev_route_bt.pack(side=ctk.LEFT, padx=20, pady=5)
next_route_bt = ctk.CTkButton(master=button_frame, text="Next Route", state="disabled")
next_route_bt.pack(side=ctk.RIGHT, padx=20, pady=5)

map_canvas = ctk.CTkCanvas(master=left_side_frame, height=500)
# map_canvas.pack(side=ctk.BOTTOM, padx=20, pady=20, fill=ctk.BOTH, expand=True)
img = ctk.CTkImage(light_image=Image.open("default.png"), size=(930, 690))
img_lb = ctk.CTkLabel(master=left_side_frame, image=img, text="")
img_lb.pack(side=ctk.BOTTOM, padx=20, pady=5, fill=ctk.BOTH, expand=True)

right_side_frame = ctk.CTkFrame(master=main_frame)
right_side_frame.pack(side=ctk.LEFT, padx=20, pady=5, ipadx=200, ipady=200)
# canvas_frame = ctk.CTkFrame(master=right_side_frame)
# canvas_frame.pack(side=ctk.TOP, padx=20, pady=20, ipadx=200, ipady=200)

canvas = ctk.CTkCanvas(master=right_side_frame, height=600)
vbar = ctk.CTkScrollbar(right_side_frame, orientation="vertical")
vbar.pack(side="right", fill="y")
vbar.configure(command=canvas.yview)
canvas.configure(yscrollcommand=vbar.set)
canvas.pack(padx=20, pady=5, fill=ctk.BOTH, expand=True)  # frame to view 2d matrix content
pointer = canvas.create_polygon(10, 80, 10, 110, 30, 95, fill="white")
# hover_pointer = canvas.create_polygon(10, 80, 10, 110, 30, 95, outline="" , dash=(4, 4), fill='')
export_img_bt = ctk.CTkButton(master=right_side_frame, text="Export Image", state="disabled")
export_img_bt.pack(side=ctk.TOP, padx=20, pady=5)

g = Graph('G', filename='process.gv', engine='sfdp', format='png')

start_city_list = []
end_city_list = []
city_list = None
num_of_cities = None
default_src = None
default_dest = None
best_paths = None
max_num_of_paths = 100
current_path_indx = 0


def get_start_list():
    global start_city_list
    start_city_list = []
    for city_info in city_list[:-1]:
        start_city_list.append(city_info[0])


def get_end_city_list(start_city):
    global end_city_list
    # assert city_list != None
    very_end_city = city_list[-1][0]
    end_city_list.clear()
    start_city_index = start_city_list.index(start_city)
    for i in range(start_city_index + 1, len(start_city_list)):
        end_city_list.append(start_city_list[i])
    end_city_list.append(very_end_city)
    end_city_entry.set("Select:")
    end_city_entry.configure(values=end_city_list, state="enabled")


def color_selected_path_map(selected_path, city_list):
    global g
    g = Graph('G', filename='process.gv', engine='sfdp', format='png')
    # g.attr('node', shape='circle')
    # g.graph_attr['bgcolor'] = 'white'
    g.edge_attr['dir'] = 'forward'
    g.node_attr['style'] = 'filled'

    for city in city_list:
        if city[0] == selected_path[0]:
            g.node(city[0], fillcolor="green")
        elif city[0] == selected_path[-1]:
            g.node(city[0], fillcolor="red")
        elif city[0] in selected_path:
            g.node(city[0], fillcolor="lightblue")
        selected_path_pairs = []
        for i in range(len(selected_path) - 1):
            selected_path_pairs.append(selected_path[i] + selected_path[i + 1])
        for i in range(1, len(city)):
            if str(city[0] + city[i][0]) in selected_path_pairs:
                g.edge(city[0], city[i][0], label=str(city[i][1] + city[i][2]), color="darkgreen", penwidth="3")
            else:
                g.edge(city[0], city[i][0])  # , label=str(city[i][1] + city[i][2]))
    g.render()
    img.configure(light_image=Image.open("process.gv.png"))


def select_next_route():
    global best_paths, current_path_indx, max_num_of_paths, pointer
    canvas.move(pointer, 0, 70)
    # if canvas.coords(pointer)[1] > 770:
    #     canvas.yview_scroll(1, "pages")
    pointer_pos = canvas.bbox(pointer)[1]
    if ((pointer_pos - 9) / 70) % 11 == 0:
        canvas.yview_scroll(1, "pages")
    current_path_indx += 1
    next_route_bt.configure(state="enabled")
    prev_route_bt.configure(state="enabled")
    color_selected_path_map(best_paths[current_path_indx][:-1], city_list)
    if current_path_indx == min(max_num_of_paths - 1, len(best_paths) - 2):
        # 22 is the max number of routes that can be displayed on the canvas
        next_route_bt.configure(state="disabled")
    # if current_path_indx % 10 == 0:
    #     # canvas.yview_moveto(0.5)
    #     canvas.yview_scroll(1, "pages")


def select_prev_route():
    global best_paths, current_path_indx, max_num_of_paths, pointer
    page_size = len(best_paths)
    canvas.move(pointer, 0, -70)
    pointer_pos = canvas.bbox(pointer)[1]
    if pointer_pos not in range(int(canvas.yview()[0] * page_size * 70), int(canvas.yview()[1] * page_size * 70)):
        canvas.yview_scroll(-1, "pages")

    current_path_indx -= 1
    prev_route_bt.configure(state="enabled")
    color_selected_path_map(best_paths[current_path_indx][:-1], city_list)
    if current_path_indx == 0:
        prev_route_bt.configure(state="disabled")
    next_route_bt.configure(state="enabled")


def export_img():
    global g
    g.view()


def browse_file():
    # reading file of type txt setting the filepath entry to be non editiable
    filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
    if file_path != '':
        file_path_lb.configure(state="normal")
        file_path_lb.delete(0, "end")
        file_path_lb.insert(-1, str(file_path))
        file_path_lb.configure(state="readonly")
    else:
        return
    file = open(file_path, "r")
    global city_list, num_of_cities, default_src, default_dest, current_path_indx
    current_path_indx = 0
    city_list, num_of_cities, default_src, default_dest = main.process_file(file)
    global best_paths
    best_paths = main.global_find_route(city_list, default_src, default_dest)
    color_selected_path_map(best_paths[0][:-1], city_list)
    canvas.delete("all")
    global pointer
    pointer = canvas.create_polygon(10, 80, 10, 110, 30, 95, fill="white")
    canvas.configure(scrollregion=(0, 0, 0, min(len(best_paths), max_num_of_paths) * 70))
    list_all_routes(best_paths)
    end_city_entry.configure(state="disabled")
    show_dp_table_bt.configure(state="enabled")
    next_route_bt.configure(state="disabled")
    prev_route_bt.configure(state="disabled")
    get_start_list()
    start_city_entry.configure(state="enabled", values=start_city_list, command=get_end_city_list)
    start_city_entry.set(default_src)
    end_city_entry.set(default_dest)
    next_route_bt.configure(state="enabled", command=lambda: select_next_route())
    prev_route_bt.configure(command=lambda: select_prev_route())
    export_img_bt.configure(state="enabled", command=lambda: export_img())


file_browse_bt.configure(command=browse_file)


def create_city_map(city_list):
    global g
    g = Graph('G', filename='process.gv', engine='sfdp', format='png')
    # g.attr('node', shape='circle')
    # g.graph_attr['bgcolor'] = 'white'
    g.edge_attr['dir'] = 'forward'

    for route in city_list:
        for i in range(1, len(route)):
            g.edge(route[0], route[i][0], label=str(route[i][1] + route[i][2]))
    g.render()
    img.configure(light_image=Image.open("process.gv.png"))


def list_all_routes(best_routes):
    # canvas.delete(pointer)
    initial_y = 0
    for route in best_routes[:max_num_of_paths]:
        num = len(route) - 1
        width = 400
        unit_width = 50
        node_space = unit_width * num
        line_length = (width - node_space) / (num - 1)
        initial_y += 70
        for i in range(num):
            if i == 0:
                canvas.create_oval(50 + i * (line_length + unit_width), initial_y, 100 + i * (line_length + unit_width),
                                   initial_y + unit_width, fill="green")
                canvas.create_text(75 + i * (line_length + unit_width), initial_y + 25, text=route[i])
                canvas.create_line(100 + i * (line_length + unit_width), initial_y + unit_width / 2,
                                   100 + (i + 1) * (line_length + unit_width), initial_y + unit_width / 2, fill="white",
                                   width=3)
            elif i == num - 1:
                canvas.create_oval(50 + i * (line_length + unit_width), initial_y, 100 + i * (line_length + unit_width),
                                   initial_y + unit_width, fill="red")
                canvas.create_text(75 + i * (line_length + unit_width), initial_y + 25, text=route[i])
            else:
                canvas.create_oval(50 + i * (line_length + unit_width), initial_y, 100 + i * (line_length + unit_width),
                                   initial_y + unit_width, fill="dark blue")
                canvas.create_text(75 + i * (line_length + unit_width), initial_y + 25, text=route[i])
                canvas.create_line(100 + i * (line_length + unit_width), initial_y + unit_width / 2,
                                   100 + (i + 1) * (line_length + unit_width), initial_y + unit_width / 2, fill="white",
                                   width=3)
        canvas.create_rectangle(475, initial_y, 525, initial_y + 50, fill="orange", outline="white")
        canvas.create_line(450, initial_y + 25, 475, initial_y + 25, fill="white", width=3)
        canvas.create_text(500, initial_y + 25, text=f"{route[-1]}")
        # global hover_pointer
        # canvas.delete(hover_pointer)
        # hover_pointer = canvas.create_polygon(10, 80, 10, 110, 30, 95, outline="black" , dash=(4, 4), fill='')


# def color_start_end_map(routes, start, end):
#     g = Graph('G', filename='process.gv', engine='sfdp', format='png')
#     # g.attr('node', shape='circle')
#     # g.graph_attr['bgcolor'] = 'white'
#     g.edge_attr['dir'] = 'forward'
#     g.node_attr['style'] = 'filled'
#
#     for route in routes:
#         if route[0] == start:
#             g.node(route[0], fillcolor="green")
#         elif route[0] == end:
#             g.node(route[0], fillcolor="red")
#         for i in range(1, len(route)):
#             g.edge(route[0], route[i][0], label=str(route[i][1] + route[i][2]))
#     g.render()
#     img.configure(light_image=Image.open("process.gv.png"))
#     img_lb = ctk.CTkLabel(master=left_side_frame, image=img, text="")
#     img_lb.pack(side=ctk.BOTTOM, padx=20, pady=20, fill=ctk.BOTH, expand=True)


def list_and_color_best_path(start, end):
    global best_paths, current_path_indx
    current_path_indx = 0
    best_paths = main.global_find_route(city_list, start, end)
    canvas.delete("all")
    global pointer
    pointer = canvas.create_polygon(10, 80, 10, 110, 30, 95, fill="white")
    canvas.configure(scrollregion=(0, 0, 0, min(len(best_paths), max_num_of_paths) * 70))
    list_all_routes(best_paths)
    color_selected_path_map(best_paths[0][:-1], city_list)
    next_route_bt.configure(state="enabled", command=lambda: select_next_route())
    show_dp_table_bt.configure(state="enabled")


end_city_entry.configure(command=lambda x: list_and_color_best_path(start_city_entry.get(), end_city_entry.get()))


def open_table_window():
    # route = best_paths[current_path_indx]
    table_window = ctk.CTkToplevel(app)
    table_window.title("Dynamic Programming Table")
    table_window.geometry("600x800")
    table_window.resizable(False, False)

    # table_canvas = ctk.CTkCanvas(table_window, width=800, height=600)
    # table_canvas.pack()

    # table_canvas.create_text(200, 20, text="Dynamic Programming Table", font=("Arial", 20))
    # dp_table = ctk.CTkTabview(table_canvas, width=800, height=600)
    # dp_table.pack()

    table_area = ctk.CTkLabel(master=table_window, text=main.table)
    table_area.pack(side=ctk.TOP, padx=20, pady=20, fill=ctk.BOTH, expand=True)

    # table_text_area = ctk.CTkTextbox(master=table_window, text=main.table)
    # table_text_area.pack(side=ctk.TOP, padx=20, pady=20, fill=ctk.BOTH, expand=True)
    # table_text_area.insert(index=0.0, text=main.table)

    label_vector_lb = ctk.CTkLabel(master=table_window, text=main.label_vector_interface)
    label_vector_lb.pack(side=ctk.TOP, padx=20, pady=20, fill=ctk.BOTH, expand=True)



show_dp_table_bt.configure(command=lambda: open_table_window())

# def get_coor(event):
#     # print(event.x, event.y)
#     if event.y < 95:
#         canvas.moveto(hover_pointer, 10, 80)
#     else:
#         index = int((event.y- 80)/60)  +1
#         # distance = int(event.y/80)
#         canvas.moveto(hover_pointer, 10, index * 60 + 70)
#     print(event.y, index)
# canvas.bind("<Motion>", get_coor)

app.mainloop()
