import tkinter as tk

# maak scherm
scrWidth = 750
scrHeight = 500

root = tk.Tk()

# maak canvas & padd
canvas = tk.Canvas( root, width = scrWidth, height = scrHeight)
padd = canvas.create_rectangle(100, scrHeight/2 + 35, 110, scrHeight/2 - 35, fill='black')
canvas.pack()

# beweeg padd
ySpeed = 3
def movePadd():
    global ySpeed, scrHeight
    canvas.move(padd, 0, ySpeed)
    (leftPos, topPos, rightPos, bottomPos) = canvas.coords(padd)
    if topPos + ySpeed <= 0 or bottomPos + ySpeed >= scrHeight:
        ySpeed = -ySpeed
    canvas.after(50, movePadd)

# maak knop
button = tk.Button ( root, text = "Start", command = movePadd() )
button.pack()

# voer code uit
root.mainloop()