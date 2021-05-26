import tkinter as tk

LedColors = ["yellow", "yellow4","green2", "green4","red", "red4"]

class Led(object):
    def __init__(self, canvas, coords, colorOn ,colorOff):
        self.canvas = canvas
        self.led = self.canvas.create_oval(coords, fill=colorOff)
        self.colorOn = colorOn
        self.colorOff = colorOff
        self.toggle = False
        self.canvas.pack()

    def Toggle(self):
        if(self.toggle == False):
            if __name__  == "__main__":
                print("On")
            self.On()
            self.toggle = True
        else:
            if __name__  == "__main__":
                print("Off")
            self.Off()
            self.toggle = False

    def On(self):
        self.canvas.itemconfig(self.led, fill=self.colorOn)
        if __name__  == "__main__":
            print("On")

    def Off(self):
        self.canvas.itemconfig(self.led, fill=self.colorOff)
        if __name__  == "__main__":
            print("Off")

class LedHW(object):
    def __init__(self, GPIO, pin):
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin
        self.GPIO = GPIO
        self.toggle = False

    def Toggle(self):
        if(self.toggle == False):
            if __name__  == "__main__":
                print("On")
            self.On()
            self.toggle = True
        else:
            if __name__  == "__main__":
                print("Off")
            self.Off()
            self.toggle = False

    def On(self):
        self.GPIO.output(self.pin, True)
        if __name__  == "__main__":
            print("On")

    def Off(self):
        self.GPIO.output(self.pin, False)
        if __name__  == "__main__":
            print("Off")


if __name__  == "__main__":

    scrHeight = 500
    scrWidth = 500

    root = tk.Tk()
    canvas = tk.Canvas(root, height=scrHeight, width=scrWidth)

    ledR = Led(canvas, (10, 50, 30, 70), LedColors[2],LedColors[3])

    canvas.pack()

    #Button wordt vervangen door MQTT bericht
    button = tk.Button(root, text="Start",command=lambda: ledR.Toggle())
    button.pack(side="bottom")

    root.mainloop()
