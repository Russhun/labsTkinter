from tkinter import *
from math import cos, sin, radians


root = Tk()
root.geometry("600x600")

c = Canvas(root, width=600, height=600, bg='white')
c.pack()

ball = c.create_oval(100, 100, 500, 500, fill='green')
dot = c.create_oval(295, 295, 305, 305, fill='red')


def motion(angle: float = 0,
           clockwise: bool = True) -> None:
    if angle >= 360:
        angle = 0
    x = 210*cos(radians(angle))
    y = 210*sin(radians((1 if clockwise else -1)*angle))
    angle += 1
    c.coords(dot, x+295, y+295, x+305, y+305)
    root.after(10, motion, angle, clockwise)


root.after(10, motion, 0, True)

root.mainloop()

