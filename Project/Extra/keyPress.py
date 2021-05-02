from tkinter import *

root = Tk()
root.title("Show Key Output")
root.geometry("400x400")

def showKey(event):
    print("Button Clicked: " + event.char)
    label = Label(root, text="Button Clicked: " + event.char)
    label.pack()
# def quit(event):                           
#     print("Double Click, so let's stop") 
#     import sys; sys.exit() 

button = Button(None, text='Click Me')
root.bind('<Key>', showKey)
#widget.bind('<Double-1>', quit)
button.pack()
root.mainloop()