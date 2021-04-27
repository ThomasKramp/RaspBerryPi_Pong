import tkinter as tk

screenW = 500
screenH = 500


def startBounce():
    canvas.move(bol, 1 ,1)
    canvas.after(50, startBounce)


root = tk.Tk()
root.geometry('500x530')    #instellen van window size
root.resizable(False, False)    #instellen dat width en height niet kan veranderd worden
root.config(bg='goldenrod')
canvas = tk.Canvas(root, width=screenW, height=screenH,bg="sky blue")

#een bol maken
bol = canvas.create_oval(10,10,20,20,fill="black")

canvas.pack()


startButton = tk.Button(root, text="Switch player", command=startBounce)    #zal Hello printen in de button en bij drukken knop -> naar event methode
startButton.pack(side="bottom")


# set window title
root.wm_title("Pong Game")

print("Startup Pong")

# show window
root.mainloop()