import tkinter as tk

class Label(object):
    def __init__(self, canvas, coords, text):
        self.canvas = canvas
        self.text = tk.StringVar()
        self.text.set(text)
        self.label = tk.Label(canvas,textvariable=self.text)
        self.label.place(x=coords[0], y=coords[1])
    
    def changeText(self, pre, item):
        if( __name__ == "__main__"):
            global points
        self.text.set(pre + str(item))

if( __name__ == "__main__"):
    def up():
        global points, label
        points = points +1
        label.changeText()

    points = 0  
    root = tk.Tk()
    root.geometry('480x480')
    var = tk.StringVar()
    label = Label( root, (100,20), "Hallo")
    label = Label( root, (50,100), "BRB")

    button = tk.Button(root,text="Click to change text below", command=up)
    button.pack()

    root.mainloop()