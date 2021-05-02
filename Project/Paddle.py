class Paddle(object):

    leftPos = rightPos = 0


    def __init__(self, canvas, scrDimen, leftPaddle, color):
        # Canvas maken om mee te werken
        self.canvas = canvas

        # Dimensies van het scherm bijhouden
        (self.scrHeight, scrWidth) = scrDimen

        # Coordinaten van het pad instellen
        if  leftPaddle:
            xRef = 100
            self.keys = ('s', 'd', 'f')
        else:
            xRef = scrWidth - 100
            self.keys = ('j', 'k', 'l')
        # coords = (X-begin, Y-begin, X-end, Y-end)
        coords = (xRef - 10, self.scrHeight / 2 - 50, xRef + 10, self.scrHeight / 2 + 50)

        # De paddle zelf aanmaken
        self.paddle = self.canvas.create_rectangle(coords, fill=color)

        # Snelheid van paddle instellen
        self.speed = 3
        
        (self.leftPos, topPos, self.rightPos, bottomPos) = self.canvas.coords(self.paddle)


    def movePaddle(self, event):
        # Huidige positie ophalen
        (self.leftPos, topPos, self.rightPos, bottomPos) = self.canvas.coords(self.paddle)

        # Stel de huidige snelheid in
        if event.char == self.keys[1]:
            if self.speed == 3:
                self.speed = 20
            else:
                self.speed = 3

        # check de positie en input
        if event.char == self.keys[0] and bottomPos + self.speed <= self.scrHeight:
            self.canvas.move(self.paddle, 0, self.speed)
        elif event.char == self.keys[2] and topPos - self.speed >= 0:
            self.canvas.move(self.paddle, 0, -self.speed)