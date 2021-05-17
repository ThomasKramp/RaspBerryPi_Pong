class Ball(object):

    coords = (0, 0, 0, 0)
    speed = (0, 0)
    bounces = 0
    goalAtPaddle = ""

    def __init__(self, scrDimen):
        # Dimensies van het scherm bijhouden
        self.scrDimen = (scrHeight, scrWidth) = scrDimen

        # Coordinaten van de bal instellen
        # coords = (X-begin, Y-begin, X-end, Y-end)
        self.coords = (scrWidth / 2 - 10, scrHeight / 2 - 10, scrWidth / 2 + 10, scrHeight / 2 + 10)

        # Snelheid van de bal instellen
        self.speed = (speedX, speedY) = (31, 31)

    def moveBall(self, paddles):
        # Huidige positie ophalen
        (leftPos, topPos, rightPos, bottomPos) = self.coords
        (scrHeight, scrWidth) = self.scrDimen
        (speedX, speedY) = self.speed
        
        # Aanraken van een speler
        for paddle in paddles:
            if(self.isTouchingLeft(paddle)):
                speedX = -speedX
                # Telt aantal kaatsingen tellen
                self.bounces += 1
                print("Bounce back left")

            if(self.isTouchingTop(paddle)):
                speedY = -speedY

            if(self.isTouchingRight(paddle)):
                speedX = -speedX
                # Telt aantal kaatsingen tellen
                self.bounces += 1
                print("Bounce back right")
        
            if(self.isTouchingBottom(paddle)):
                speedY = -speedY
                
        
        # Kijk voor botsingen met scherm
        if topPos + speedY <= 0 or bottomPos + speedY >= scrHeight:
            speedY = -speedY

        if leftPos + speedX <= 0 or rightPos + speedX >= scrWidth:
            # Waar is de goal
            if leftPos + speedX <= 0:
                self.goalAtPaddle = "Left"
            if rightPos + speedX >= scrWidth:
                self.goalAtPaddle = "Right"
            speedX = -speedX

        # Beweeg de bal
        if self.goalAtPaddle == "":
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

    def resetBall(self):
        # Versnelt de bal bij elk nieuw spel
        (speedX, speedY) = self.speed
        speedX += 5
        speedY += 5
        self.speed = (speedX, speedY)
        
        # Reset de plaats van de bal
        (scrHeight, scrWidth) = self.scrDimen
        self.coords = (scrWidth / 2 - 10, scrHeight / 2 - 10, scrWidth / 2 + 10, scrHeight / 2 + 10)

        # Reset de variabelen
        self.bounces = 0
        self.goalAtPaddle = ""