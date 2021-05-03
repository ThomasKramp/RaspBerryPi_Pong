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

    def moveBall(self, paddles):
        # Huidige positie ophalen
        (leftPos, topPos, rightPos, bottomPos) = self.canvas.coords(self.ball)


        # Kijk voor botsingen
        if leftPos + self.xSpeed <= 0 or rightPos + self.xSpeed >= self.scrWidth:
            self.xSpeed = -self.xSpeed
        if topPos + self.ySpeed <= 0 or bottomPos + self.ySpeed >= self.scrHeight:
            self.ySpeed = -self.ySpeed
        
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
        self.canvas.move(self.ball, self.xSpeed, self.ySpeed)

        # Start de functie opnieuw op
        self.canvas.after(50, self.moveBall, paddles)


    def isTouchingLeft(self, obs):
        (left,top,right,bottom) = self.canvas.coords(self.ball)
        (obsleft,obstop,obsright,obsbottom) = self.canvas.coords(obs)
        
        a = (right + self.xSpeed > obsleft)
        b = (left < obsleft)
        c = (bottom > obstop)
        d = (top < obsbottom)

        return (a and b and c and d)

    def isTouchingRight(self, obs):
        (left,top,right,bottom) = self.canvas.coords(self.ball)
        (obsleft,obstop,obsright,obsbottom) = self.canvas.coords(obs)
        
        a = (left + self.xSpeed < obsright)
        b = (right > obsright)
        c = (bottom > obstop)
        d = (top < obsbottom)

        return (a and b and c and d)

    def isTouchingBottom(self, obs):
        (left,top,right,bottom) = self.canvas.coords(self.ball)
        (obsleft,obstop,obsright,obsbottom) = self.canvas.coords(obs)
        
        a = (top + self.ySpeed < obsbottom)
        b = (bottom > obsbottom)
        c = (right > obsleft)
        d = (left < obsright)

        return (a and b and c and d)

    def isTouchingTop(self, obs):
        (left,top,right,bottom) = self.canvas.coords(self.ball)
        (obsleft,obstop,obsright,obsbottom) = self.canvas.coords(obs)
        
        a = (bottom + self.ySpeed > obstop)
        b = (top < obstop)
        c = (right > obsleft)
        d = (left < obsright)

        return (a and b and c and d)