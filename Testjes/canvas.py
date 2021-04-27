#http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter color picker

import tkinter as tk
from time import sleep

screenW = 500
screenH = 500
padx0, pady0 ,padx1 , pady1 = 20, 0 ,30 ,60

start = False

def clickedStart():
    print("Start")
    global start
    start = True

def movePad(event):
    
    y=event.y - pady1/2

    print(y)

    if(y < screenH - pady1 and y > 0):
        canvas.coords(rect, padx0,pady0 + y,padx1,pady1 + y)
    elif (y > screenH - pady1):
        canvas.coords(rect, padx0,pady0 + (screenH - pady1),padx1,pady1 + (screenH - pady1))
    elif(y < 0):
        canvas.coords(rect, padx0,pady0,padx1,pady1)


def mouseOverEvent(event):
    print(event.y)

root = tk.Tk()
root.geometry('500x530')    #instellen van window size
root.resizable(False, False)    #instellen dat width en height niet kan veranderd worden
root.config(bg='goldenrod')
canvas = tk.Canvas(root, width=screenW, height=screenH,bg="sky blue")
#Een vierkant maken
rect = canvas.create_rectangle(padx0,pady0,padx1,pady1,fill="grey18")
canvas.pack()

print("Startup Pong")

#kader = tk.Canvas(root, width = screenW, height = screenH)
#kader.pack()

startButton = tk.Button(root, text="Hello",command=clickedStart)    #zal Hello printen in de button en bij drukken knop -> naar event methode
startButton.pack(side="bottom")

canvas.bind("<Motion>", movePad)

#if(start == True):
#    startButton

#startButton.bind("<Button-1>",clickedStart)     #Een event van linkermuisklik op de button

#kader.bind("<Button-1>",clickedL)   #Een event van linkermuisklik in de kader
#kader.bind("<Button-3>",clickedR)   #Een event van rechtermuisklik in de kader

# set window title
root.wm_title("Pong Game")

# tekstlabel.pack()

# show window
root.mainloop()