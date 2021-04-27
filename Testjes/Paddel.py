import tkinter as tk

screenW = 500
screenH = 500
player1Padx0, player1Pady0 ,player1Padx1 , player1Pady1 = 20, 0 ,30 ,60
player2Padx0, player2Pady0 ,player2Padx1 , player2Pady1 = 470, 0 ,480 ,60

class padCoords():
    x0=0
    x1=0
    y0=0
    y1=0
    objId=0
    curx0=0
    cury0=0
    curx1=0
    cury1=0

player1 = padCoords();
player1.x0, player1.x1, player1.y0, player1.y1 = 20, 30, 0, 60
player2 = padCoords();
player2.x0, player2.x1, player2.y0, player2.y1 = 470, 480, 0, 60

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
        y=event.y - player1.y1/2

        #print("Rechts")

        if(y < screenH - player1.y1 and y > 0):
            canvas.coords(player1.objId, player1.x0,player1.y0 + y,player1.x1,player1.y1 + y)
        elif (y > screenH - player1.y1):
            canvas.coords(player1.objId, player1.x0,player1.y0 + (screenH - player1.y1),player1.x1,player1.y1 + (screenH - player1.y1))
        elif(y < 0):
            canvas.coords(player1.objId, player1.x0,player1.y0,player1.x1,player1.y1)

    else:
        y=event.y - player1.y1/2

        #print("Links")

        if(y < screenH - player2.y1 and y > 0):
            canvas.coords(player2.objId, player2.x0,player2.y0 + y,player2.x1,player2.y1 + y)
        elif (y > screenH - player2.y1):
            canvas.coords(player2.objId, player2.x0,player2.y0 + (screenH - player2.y1),player2.x1,player2.y1 + (screenH - player2.y1))
        elif(y < 0):
            canvas.coords(player2.objId, player2.x0,player2.y0,player2.x1,player2.y1)

    print(player1.cury0)
    
    [player1.curx0, player1.cury0, player1.curx1, player1.cury1] = canvas.coords(player1.objId)
    [player2.curx0, player2.cury0, player2.curx1, player2.cury1] = canvas.coords(player2.objId)



def mouseOverEvent(event):
    print(event.y)

root = tk.Tk()
root.geometry('500x530')    #instellen van window size
root.resizable(False, False)    #instellen dat width en height niet kan veranderd worden
root.config(bg='goldenrod')
canvas = tk.Canvas(root, width=screenW, height=screenH,bg="sky blue")
#Een vierkant maken
player1.objId = canvas.create_rectangle(player1.x0,player1.y0,player1.x1,player1.y1,fill="grey18")
player2.objId = canvas.create_rectangle(player2.x0,player2.y0,player2.x1,player1.y1,fill="grey18")
canvas.pack()

startButton = tk.Button(root, text="Switch player",command=clickedStart)    #zal Hello printen in de button en bij drukken knop -> naar event methode
startButton.pack(side="bottom")

canvas.bind("<Motion>", movePad)

# set window title
root.wm_title("Pong Game")

print("Startup Pong")

# show window
root.mainloop()