class Paddle(object):

    # Coordinaten in het begin doorsturen bij nieuw spel
    isSet = False
    coords = (0, 0, 0, 0)
    speed = (0, 0)
    points = 0
    player = 0

    def __init__(self, scrDimen, leftPaddle):
        # Dimensies van het scherm bijhouden
        self.scrDimen = (scrHeight, scrWidth) = scrDimen

        # Coordinaten van het pad instellen
        if  leftPaddle:
            # coords = (X-begin, Y-begin, X-end, Y-end)
            self.coords = (10, scrHeight / 2 - 50, 20, scrHeight / 2 + 50)
        else:
            self.coords = (scrWidth - 20, scrHeight / 2 - 50, scrWidth - 10, scrHeight / 2 + 50)

        # Snelheid van paddle instellen
        self.speed = 3

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

    def changeSpeed(self):
        # Stel de huidige snelheid in
        if self.speed == 3:
            self.speed = 20
        else:
            self.speed = 3

    def resetPaddle(self):        
        # Reset de plaats van de paddle
        (scrHeight, scrWidth) = self.scrDimen
        (leftPos, topPos, rightPos, bottomPos) = self.coords
        topPos = scrHeight / 2 - 50
        bottomPos = scrHeight / 2 + 50
        self.coords = (leftPos, topPos, rightPos, bottomPos)