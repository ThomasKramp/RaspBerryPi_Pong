import tkinter as tk

class Button(object):
    def __init__(self, canvas, coords, fill, text, command):
        self.canvas = canvas
        self.button = tk.Button(canvas, text=text,command=command)
        self.button.place(x=175, y=100)




if __name__  == "__main__":
    def x():
        global xb
        print(xb)
        xb = xb + 1
    
    xb = 0
    scrHeight = 500
    scrWidth = 500

    root = tk.Tk()
    canvas = tk.Canvas(root, height=scrHeight, width=scrWidth)

    button = Button(canvas, (10, 50), "green","Start", x)

    canvas.pack()

    root.mainloop()