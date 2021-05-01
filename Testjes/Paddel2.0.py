#!/usr/bin/python3
import tkinter as tk

screenW = 500
screenH = 500

class Paddle(object):
    def __init__ (self, canvas, coords, fill):
        self.canvas = canvas
        self.fill = fill
        self.paddle = self.canvas.create_rectangle(coords, fill=self.fill)
        #print(coords);
        self.x0 = coords[0]
        self.y0 = coords[1]
        self.x1 = coords[2]
        self.y1 = coords[3]
    
    def MovePad(self, y, screenH):
        if(y < screenH - self.y1 and y > 0):
            self.canvas.coords(self.paddle, self.x0,self.y0 + y,self.x1,self.y1 + y)
        elif (y > screenH - self.y1):
            self.canvas.coords(self.paddle, self.x0,self.y0 + (screenH - self.y1),self.x1,self.y1 + (screenH - self.y1))
        elif(y < 0):
            self.canvas.coords(self.paddle, self.x0,self.y0,self.x1,self.y1)

PlayerDefine = "R"

def clickedStart():
    global PlayerDefine
    print("Switch player")
    print(PlayerDefine)
    
    if(PlayerDefine == "R"):
        PlayerDefine = "L"
    else:
        PlayerDefine = "R"

def movePad(event):
    global PlayerDefine
    if(PlayerDefine == "L"):
        y=event.y - player1.y1/2
        player1.MovePad(y, screenH)
        print("Links")

    else:
        y=event.y - player1.y1/2
        player2.MovePad(y, screenH)
        print("Rechts")

def mouseOverEvent(event):
    print(event.y)

root = tk.Tk()
root.geometry('500x530')    #instellen van window size
root.resizable(False, False)    #instellen dat width en height niet kan veranderd worden
root.config(bg='goldenrod')
canvas = tk.Canvas(root, width=screenW, height=screenH,bg="sky blue")
#de paddles maken
player1 = Paddle(canvas, (20, 0, 30, 60),"grey18")
player2 = Paddle(canvas, (470, 0, 480, 60),"grey18")
canvas.pack()

startButton = tk.Button(root, text="Switch player",command=clickedStart)    #zal Hello printen in de button en bij drukken knop -> naar event methode
startButton.pack(side="bottom")

#event wanneer de muis erover gaat.
canvas.bind("<Motion>", movePad)

# set window title
root.wm_title("Pong Game")

print("Startup Pong")

# show window
root.mainloop()