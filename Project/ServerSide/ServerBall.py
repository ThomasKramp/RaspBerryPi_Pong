class Ball(object):

    def __init__(self, scrDimen):
        # Dimensies van het scherm bijhouden
        self.scrDimen = (scrHeight, scrWidth) = scrDimen

        # Coordinaten van de bal instellen
        # coords = (X-begin, Y-begin, X-end, Y-end)
        self.coords = (scrWidth / 2 - 10, scrHeight / 2 - 10, scrWidth / 2 + 10, scrHeight / 2 + 10)

        # Snelheid van de bal instellen
        self.speed = (speedX, speedY) = (7, 7)

    def moveBall(self, paddles):
        # Huidige positie ophalen
        (leftPos, topPos, rightPos, bottomPos) = self.coords
        (scrHeight, scrWidth) = self.scrDimen
        (speedX, speedY) = self.speed

        # Kijk voor botsingen met scherm
        if leftPos + self.xSpeed <= 0 or rightPos + speedX >= scrWidth:
            speedX = -speedX
        if topPos + self.ySpeed <= 0 or bottomPos + speedY >= scrHeight:
            speedY = -speedY
        
        # Aanraken van een speler
        for paddle in paddles:
            if(self.isTouchingLeft(paddle)):
                self.xSpeed = -self.xSpeed

            if(self.isTouchingTop(paddle)):
                self.ySpeed = -self.ySpeed

            if(self.isTouchingRight(paddle)):
                self.xSpeed = -self.xSpeed
        
            if(self.isTouchingBottom(paddle)):
                self.ySpeed = -self.ySpeed

        # Beweeg de bal
        leftPos = leftPos + speedX
        topPos = topPos + speedY
        rightPos = rightPos + speedX
        bottomPos = bottomPos + speedY

        # Bewaar de verandering
        self.coords = (leftPos, topPos, rightPos, bottomPos)
        self.speed = (speedX, speedY)

        # Start de functie opnieuw op
        # self.canvas.after(50, self.moveBall, paddles)

    def isTouchingLeft(self, obs):
        (left, top, right, bottom) = self.coords
        (obsleft, obstop, obsright, obsbottom) = obs.coords
        (speedX, speedY) = self.speed
        
        l = (left < obsleft)
        t = (top < obsbottom)
        r = (right + speedX > obsleft)
        b = (bottom > obstop)

        return (l and t and r and b)

    def isTouchingTop(self, obs):
        (left, top, right, bottom) = self.coords
        (obsleft, obstop, obsright, obsbottom) = obs.coords
        (speedX, speedY) = self.speed
        
        l = (right > obsleft)
        t = (top < obstop)
        r = (left < obsright)
        b = (bottom + speedY > obstop)

        return (l and t and r and b)

    def isTouchingRight(self, obs):
        (left, top, right, bottom) = self.coords
        (obsleft, obstop, obsright, obsbottom) = obs.coords
        (speedX, speedY) = self.speed
        
        l = (left + speedX < obsright)
        t = (top < obsbottom)
        r = (right > obsright)
        b = (bottom > obstop)

        return (l and t and r and b)
        
    def isTouchingBottom(self, obs):
        (left, top, right, bottom) = self.coords
        (obsleft, obstop, obsright, obsbottom) = obs.coords
        (speedX, speedY) = self.speed
        
        l = (right > obsleft)
        t = (top + speedY < obsbottom)
        r = (left < obsright)
        b = (bottom > obsbottom)

        return (l and t and r and b)
