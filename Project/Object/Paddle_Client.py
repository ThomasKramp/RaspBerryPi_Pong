import paho.mqtt.client as client

class Paddle(object):

    leftPos = rightPos = 0

    def __init__(self, canvas, coords, color):
        # Canvas maken om mee te werken
        self.canvas = canvas

        # De paddle zelf aanmaken
        self.paddle = self.canvas.create_rectangle(coords, fill=color)

    def move(self,coords):
        self.canvas.coords(self.paddle, coords[0],coords[1],coords[2],coords[3])