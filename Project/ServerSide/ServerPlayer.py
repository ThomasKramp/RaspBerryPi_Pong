class Player(object):

    isSet = False
    points = 0
    paddle = {}

    def __init__(self, paddle):
        # Paddle toekenen aan player
        self.paddle = paddle