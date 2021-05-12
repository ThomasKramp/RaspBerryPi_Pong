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

        # Kijk voor botsingen
        if leftPos + self.xSpeed <= 0 or rightPos + speedX >= scrWidth:
            speedX = -speedX
        if topPos + self.ySpeed <= 0 or bottomPos + speedY >= scrHeight:
            speedY = -speedY
        
        #bij het aanraken van een speler
        for paddle in paddles:
            if(self.isTouchingBottom(paddle)):
                self.ySpeed = -self.ySpeed
        
            if(self.isTouchingTop(paddle)):
                self.ySpeed = -self.ySpeed
        
            if(self.isTouchingLeft(paddle)):
                self.xSpeed = -self.xSpeed
        
            if(self.isTouchingRight(paddle)):
                self.xSpeed = -self.xSpeed

        # Beweeg de bal
        self.coords = (leftPos, topPos, rightPos, bottomPos)
        self.speed = (speedX, speedY)

        # Start de functie opnieuw op
        # self.canvas.after(50, self.moveBall, paddles)

    def isTouchingBottom(self, obs):
        (left, top, right, bottom) = self.coords
        (obsleft, obstop, obsright, obsbottom) = obs.coords
        (speedX, speedY) = self.speed
        
        b = (bottom > obsbottom)
        t = (top + speedY < obsbottom)
        l = (right > obsleft)
        r = (left < obsright)

        return (b and t and l and r)

    def isTouchingTop(self, obs):
        (left, top, right, bottom) = self.coords
        (obsleft, obstop, obsright, obsbottom) = obs.coords
        (speedX, speedY) = self.speed
        
        b = (bottom + speedY > obstop)
        t = (top < obstop)
        l = (right > obsleft)
        r = (left < obsright)

        return (b and t and l and r)

    def isTouchingLeft(self, obs):
        (left, top, right, bottom) = self.coords
        (obsleft, obstop, obsright, obsbottom) = obs.coords
        (speedX, speedY) = self.speed
        
        b = (bottom > obstop)
        t = (top < obsbottom)
        l = (left < obsleft)
        r = (right + speedX > obsleft)

        return (b and t and l and r)

    def isTouchingRight(self, obs):
        (left, top, right, bottom) = self.coords
        (obsleft, obstop, obsright, obsbottom) = obs.coords
        (speedX, speedY) = self.speed
        
        b = (bottom > obstop)
        t = (top < obsbottom)
        l = (left + speedX < obsright)
        r = (right > obsright)

        return (b and t and l and r)