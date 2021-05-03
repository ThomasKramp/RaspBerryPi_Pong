from functools import partial
import tkinter as tk
from Paddle import Paddle
from Ball import Ball

scrHeight = 500
scrWidth = scrHeight*5/3

root = tk.Tk()
canvas = tk.Canvas( root, height = scrHeight, width = scrWidth)

Pad1 = Paddle(canvas, (scrHeight, scrWidth), True, "red")
Pad2 = Paddle(canvas, (scrHeight, scrWidth), False, "green")
Ball = Ball(canvas, (scrHeight, scrWidth))
# Start de functie opnieuw op
canvas.pack()

root.bind('<Key>', func=Pad1.movePaddle)
# root.bind('<Key>', func=Pad2.movePaddle)
button = tk.Button ( root, text = "Start", command = lambda:Ball.moveBall(Pad1.id, Pad2.id))
button.pack()

root.mainloop()