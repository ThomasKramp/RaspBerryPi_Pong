import tkinter as tk

# maak scherm
scrWidth = 750
scrHeight = 500

root = tk.Tk()

# maak canvas & ball
canvas = tk.Canvas( root, width = scrWidth, height = scrHeight)
ball = canvas.create_oval(scrWidth/2 + 10, scrHeight/2 + 10, scrWidth/2 - 10, scrHeight/2 - 10, fill='black')
canvas.pack()

# beweeg ball
xSpeed = ySpeed = 3
def moveBall():
    global xSpeed, ySpeed, scrWidth, scrHeight
    canvas.move(ball, xSpeed, ySpeed)
    (leftPos, topPos, rightPos, bottomPos) = canvas.coords(ball)
    if leftPos + xSpeed <= 0 or rightPos + xSpeed >= scrWidth:
        xSpeed = -xSpeed
    if topPos + ySpeed <= 0 or bottomPos + ySpeed >= scrHeight:
        ySpeed = -ySpeed
    canvas.after(50, moveBall)

# maak knop
button = tk.Button ( root, text = "Start", command = moveBall )
button.pack()

# voer code uit
root.mainloop()
