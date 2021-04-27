import tkinter as tk
from time import sleep

screenW = 500
screenH = 500
player1Padx0, player1Pady0 ,player1Padx1 , player1Pady1 = 20, 0 ,30 ,60
player2Padx0, player2Pady0 ,player2Padx1 , player2Pady1 = 470, 0 ,480 ,60

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
    if(PlayerDefine == "R"):
        y=event.y - player1Pady1/2

        print("Links")

        if(y < screenH - player1Pady1 and y > 0):
            canvas.coords(player1, player1Padx0,player1Pady0 + y,player1Padx1,player1Pady1 + y)
        elif (y > screenH - player1Pady1):
            canvas.coords(player1, player1Padx0,player1Pady0 + (screenH - player1Pady1),player1Padx1,player1Pady1 + (screenH - player1Pady1))
        elif(y < 0):
            canvas.coords(player1, player1Padx0,player1Pady0,player1Padx1,player1Pady1)

    else:
        y=event.y - player1Pady1/2

        print("Links")

        if(y < screenH - player2Pady1 and y > 0):
            canvas.coords(player2, player2Padx0,player2Pady0 + y,player2Padx1,player2Pady1 + y)
        elif (y > screenH - player2Pady1):
            canvas.coords(player2, player2Padx0,player2Pady0 + (screenH - player2Pady1),player2Padx1,player2Pady1 + (screenH - player2Pady1))
        elif(y < 0):
            canvas.coords(player2, player2Padx0,player2Pady0,player2Padx1,player2Pady1)


def mouseOverEvent(event):
    print(event.y)

root = tk.Tk()
root.geometry('500x530')    #instellen van window size
root.resizable(False, False)    #instellen dat width en height niet kan veranderd worden
root.config(bg='goldenrod')
canvas = tk.Canvas(root, width=screenW, height=screenH,bg="sky blue")
#Een vierkant maken
player1 = canvas.create_rectangle(player1Padx0,player1Pady0,player1Padx1,player1Pady1,fill="grey18")
player2 = canvas.create_rectangle(player2Padx0,player2Pady0,player2Padx1,player1Pady1,fill="grey18")
canvas.pack()

startButton = tk.Button(root, text="Switch player",command=clickedStart)    #zal Hello printen in de button en bij drukken knop -> naar event methode
startButton.pack(side="bottom")

canvas.bind("<Motion>", movePad)

# set window title
root.wm_title("Pong Game")

print("Startup Pong")

# show window
root.mainloop()