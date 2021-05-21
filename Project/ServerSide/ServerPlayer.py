class Player(object):

    isSet = False
    name = "player"
    points = 0
    paddle = {}

    def __init__(self, paddle, name):
        # Paddle toekenen aan player
        self.paddle = paddle
        self.name = name