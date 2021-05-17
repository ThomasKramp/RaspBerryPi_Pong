class Paddle(object):

    # Coordinaten in het begin doorsturen bij nieuw spel
    coords = (0, 0, 0, 0)
    speed = (0, 0)
    side = ""

    def __init__(self, scrDimen, side):
        # Dimensies van het scherm bijhouden
        self.scrDimen = (scrHeight, scrWidth) = scrDimen

        self.side = side
        # Coordinaten van het pad instellen
        if side == "Left":
            # coords = (X-begin, Y-begin, X-end, Y-end)
            self.coords = (10, scrHeight / 2 - 50, 20, scrHeight / 2 + 50)
        if side == "Right":
            self.coords = (scrWidth - 20, scrHeight / 2 - 50, scrWidth - 10, scrHeight / 2 + 50)

        # Snelheid van paddle instellen
        self.speed = 5

    def movePaddle(self, movement):
        # Huidige positie ophalen
        (leftPos, topPos, rightPos, bottomPos) = self.coords
        (scrHeight, scrWidth) = self.scrDimen

        # check de positie en input
        if movement == "down" and bottomPos + self.speed <= scrHeight:
            topPos = topPos + self.speed
            bottomPos = bottomPos + self.speed
        elif movement == "up" and topPos - self.speed >= 0:
            topPos = topPos - self.speed
            bottomPos = bottomPos - self.speed
        
        # Positie aanpassen
        self.coords = (leftPos, topPos, rightPos, bottomPos)
        print(self.coords)

    def changeSpeed(self):
        # Stel de huidige snelheid in
        if self.speed == 5:
            self.speed = 20
        else:
            self.speed = 5

    def resetPaddle(self):        
        # Reset de plaats van de paddle
        (scrHeight, scrWidth) = self.scrDimen
        (leftPos, topPos, rightPos, bottomPos) = self.coords
        topPos = scrHeight / 2 - 50
        bottomPos = scrHeight / 2 + 50
        self.coords = (leftPos, topPos, rightPos, bottomPos)