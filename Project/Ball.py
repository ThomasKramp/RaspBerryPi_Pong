class Ball(object):
    def __init__(self, canvas, scrDimen):
        # Canvas maken om mee te werken
        self.canvas = canvas

        # Dimensies van het scherm bijhouden
        (self.scrHeight, self.scrWidth) = scrDimen

        # Coordinaten van het pad instellen
        # coords = (X-begin, Y-begin, X-end, Y-end)
        coords = (self.scrWidth / 2 - 10, self.scrHeight / 2 - 10, self.scrWidth / 2 + 10, self.scrHeight / 2 + 10)

        # De paddle zelf aanmaken
        self.ball = self.canvas.create_oval(coords, fill='black')

        # Snelheid van paddle instellen
        self.xSpeed = self.ySpeed = 7

    def moveBall(self):
        # Huidige positie ophalen
        (leftPos, topPos, rightPos, bottomPos) = self.canvas.coords(self.ball)

        # Beweeg de bal
        self.canvas.move(self.ball, self.xSpeed, self.ySpeed)

        print(leftPad)
        # Kijk voor botsingen
        if leftPos + self.xSpeed <= 0 or rightPos + self.xSpeed >= self.scrWidth:
            self.xSpeed = -self.xSpeed
        if topPos + self.ySpeed <= 0 or bottomPos + self.ySpeed >= self.scrHeight:
            self.ySpeed = -self.ySpeed
        
        # Start de functie opnieuw op
        self.canvas.after(50, self.moveBall)