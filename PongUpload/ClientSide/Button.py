import tkinter as tk

class Button(object):
    def __init__(self, canvas, coords, fill, text, command):
        self.canvas = canvas
        self.button = tk.Button(canvas, text=text,command=command)
        self.button.place(x=coords[0], y=coords[1])

    def destroy(self):  #verwijderd een element 
        self.button.destroy()

class ButtonHW(object):
    def __init__(self, GPIO, pin, isr):
        self.GPIO = GPIO
        self.pin = pin
        self.isr = isr
        self.GPIO.setup(self.pin, GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
        self.GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.isr, bouncetime=200)
    
    def RmInter(self):
        self.GPIO.remove_event_detect(self.pin)
    
    

if __name__  == "__main__":
    def x():
        global xb
        if(xb == 5):
            button.destroy()
        print(xb)
        xb = xb + 1
    
    xb = 0
    scrHeight = 500
    scrWidth = 500

    root = tk.Tk()
    canvas = tk.Canvas(root, height=scrHeight, width=scrWidth)

    button = Button(canvas, (10, 50), "green","Start", x)


    canvas.pack()

    root.mainloop()