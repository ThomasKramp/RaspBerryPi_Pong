class Ball(object):
    def __init__(self, canvas, coords, color):
        # Canvas maken om mee te werken
        self.canvas = canvas

        # De paddle zelf aanmaken
        self.ball = self.canvas.create_oval(coords, fill=color)

    def move(self,coords):
        self.canvas.coords(self.ball, coords[0],coords[1],coords[2],coords[3])