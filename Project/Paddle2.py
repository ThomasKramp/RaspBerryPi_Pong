import tkinter as tk
# from tk.Tk().Canvas as tkCanvas

class Paddle(object):
    def __init__(self, canvas, coords, fill):
        self.canvas = canvas
        self.fill = fill
        self.paddle = self.canvas.create_rectangle(coords, fill=self.fill)

    def movePaddle(self):
        self.canvas.move(self.paddle, 0, 3)
    

scrWidth = 750
scrHeight = 500

root = tk.Tk()
canvas = tk.Canvas( root, width = scrWidth, height = scrHeight)
r1 = Paddle(canvas, (50,50, 150, 150), "red")
r2 = Paddle(canvas, (100, 50, 150, 150), "green")
canvas.pack()

button1 = tk.Button ( root, text = "Start", command = r1.movePaddle )
button1.pack()
button2 = tk.Button ( root, text = "Start", command = r2.movePaddle )
button2.pack()

root.mainloop()