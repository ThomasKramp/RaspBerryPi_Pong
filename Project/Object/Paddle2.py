class Paddle(object):

    leftPos = rightPos = 0

    def __init__(self, canvas, coords, color):
        # Canvas maken om mee te werken
        self.canvas = canvas

        # De paddle zelf aanmaken
        self.paddle = self.canvas.create_rectangle(coords, fill=color)

        self.speed  = 3

    def moveUp(self):
        self.canvas.move(self.paddle, 0, self.speed)