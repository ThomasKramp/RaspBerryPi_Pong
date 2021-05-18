import tkinter as tk

screenW = 500
screenH = 500

class Bol(object):
    def __init__(self, canvas, coords, fill):   
        self.canvas = canvas
        self.bol = self.canvas.create_oval(coords, fill=fill)
        self.moveY = 4
        self.moveX = 7
        self.x0 = coords[0]
        self.y0 = coords[1]
        self.x1 = coords[2]
        self.y1 = coords[3]


    def CheckCollision(self, players):
        global screenW, screenH
        (left,top,right,bottom) = self.canvas.coords(self.bol)

        if(top + self.moveY <= 0 or bottom + self.moveY >= screenH):
            self.moveY = -self.moveY
        if(left + self.moveX <= 0 or right + self.moveX >= screenW):
            self.moveX = -self.moveX

        #bij het aanraken van een speler
        for player in players:
            if(self.isTouchingBottom(player)):
                self.moveY = -self.moveY
        
            if(self.isTouchingTop(player)):
                self.moveY = -self.moveY
        
            if(self.isTouchingLeft(player)):
                self.moveX = -self.moveX
        
            if(self.isTouchingRight(player)):
                self.moveX = -self.moveX


        self.MoveBol()

    def MoveBol(self):
        self.canvas.move(self.bol, self.moveX ,self.moveY)

    def StopBol(self):
        self.moveY = 0
        self.moveX = 0
        self.canvas.coords(self.bol, self.x0,self.y0,self.x1,self.y1)

    def isTouchingLeft(self, obs):
        (left,top,right,bottom) = self.canvas.coords(self.bol)
        (obsleft,obstop,obsright,obsbottom) = self.canvas.coords(obs)
        
        a = (right + self.moveX > obsleft)
        b = (left < obsleft)
        c = (bottom > obstop)
        d = (top < obsbottom)

        return (a and b and c and d)

    def isTouchingRight(self, obs):
        (left,top,right,bottom) = self.canvas.coords(self.bol)
        (obsleft,obstop,obsright,obsbottom) = self.canvas.coords(obs)
        
        a = (left + self.moveX < obsright)
        b = (right > obsright)
        c = (bottom > obstop)
        d = (top < obsbottom)

        return (a and b and c and d)

    def isTouchingBottom(self, obs):
        (left,top,right,bottom) = self.canvas.coords(self.bol)
        (obsleft,obstop,obsright,obsbottom) = self.canvas.coords(obs)
        
        a = (top + self.moveY < obsbottom)
        b = (bottom > obsbottom)
        c = (right > obsleft)
        d = (left < obsright)

        return (a and b and c and d)

    def isTouchingTop(self, obs):
        (left,top,right,bottom) = self.canvas.coords(self.bol)
        (obsleft,obstop,obsright,obsbottom) = self.canvas.coords(obs)
        
        a = (bottom + self.moveY > obstop)
        b = (top < obstop)
        c = (right > obsleft)
        d = (left < obsright)

        return (a and b and c and d)

def start():
    global players
    bol.CheckCollision(players)
    bol1.CheckCollision(players)
    canvas.after(20, start)

root = tk.Tk()
root.geometry('500x530')    #instellen van window size
root.resizable(False, False)    #instellen dat width en height niet kan veranderd worden
root.config(bg='goldenrod')
canvas = tk.Canvas(root, width=screenW, height=screenH,bg="sky blue")

# een object maken
players = (canvas.create_rectangle(50,60,70,90,fill="red"),
canvas.create_rectangle(80,200,120,150,fill="green"),
canvas.create_rectangle(300,400,350,420,fill="blue"),
canvas.create_rectangle(380,450,430,520,fill="blue"),
canvas.create_rectangle(150,200,200,240,fill="yellow"))
#players = (canvas.create_rectangle(50,60,70,90,fill="red"))

#een bol maken
bol = Bol(canvas, (10,10,30,30), "black")
bol1 = Bol(canvas, (80,80,100,100), "blue")
canvas.pack()

startButton = tk.Button(root, text="Switch player", command=start)    #zal Hello printen in de button en bij drukken knop -> naar event methode
startButton.pack(side="bottom")


# set window title
root.wm_title("Pong Game")

print("Startup Pong")

# show window
root.mainloop()