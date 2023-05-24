import turtle
import graphviz


import customtkinter as ctk
from turtle import *

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("Hello World!")
app.geometry("680x480")

file_lb = ctk.CTkLabel(app, text="File Name: ")
file_lb.pack(padx=10, pady=10)
file_entry = ctk.CTkEntry(app, width=300)
file_entry.pack(padx=10, pady=10)
file_browser = ctk.CTkButton(app, text="Browse")
file_browser.pack(padx=10, pady=10)
turtle_canvas = ctk.CTkCanvas(app, width=600, height=300)
turtle_canvas.pack(padx=10, pady=10)
# turtle_canvas.create_line(0, 0, 200, 100)
# turtle_canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
# turtle_canvas.create_rectangle(50, 25, 150, 75, fill="blue")
circle1 = turtle_canvas.create_oval(10, 10, 100, 100, fill="red")
#put text in in circle1
turtle_canvas.create_text(50, 50, text="circle1", fill="white")
# circle_bt = ctk.CTkButton(app, text="Circle", width=10, height=2)
# button in the canvas
# turtle_canvas.create_window(50, 50, window=circle_bt)


# increase circle1 size
# turtle_screen = TurtleScreen(turtle_canvas)
# tess = RawTurtle(turtle_canvas)
# tess.color('red', 'yellow')
# print(circle1_coor)

# def get_coor(event):
#     print(event.x, event.y)
#     # if 10 < event.x < 100 and event.y > 10 and event.y < 100:
#     #     print("circle1")
#     #     turtle_canvas.itemconfig(circle1, width=5, fill="blue")
#     # if circle1 is pressed then change color to blue
#     if circle1_coor[0] < event.x < circle1_coor[2] and circle1_coor[1] < event.y < circle1_coor[3]:
#         print("circle1")
#         turtle_canvas.itemconfig(circle1, width=5, fill="blue")
def select_object(object):
    # print(object)
    # coor = turtle_canvas.coords(object)
    # print(coor)
    turtle_canvas.itemconfig(object, width=5, fill="blue")

turtle_canvas.tag_bind(circle1, "<Button-1>", lambda x: select_object(circle1))

# turtle_canvas.bind("<Button-1>", get_coor)

app.mainloop()

# from tkinter import *
# from tkinter import ttk
# root = Tk()
# root.title("Hello World!")
# root.geometry("680x480")
#
#
# file_lb = Label(root, text="File Name: ")
# file_lb.pack(padx=10, pady=10)
# file_entry = Entry(root, width=200)
# file_entry.pack(padx=150, pady=10)
# file_browser = Button(root, text="Browse")
# file_browser.pack(padx=10, pady=10)
#
#
# root.mainloop()
