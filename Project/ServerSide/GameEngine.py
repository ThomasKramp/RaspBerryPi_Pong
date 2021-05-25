import paho.mqtt.client as mqtt
from threading import Thread, enumerate
from time import sleep
import random
import json

from ServerPaddle import Paddle
from ServerBall import Ball
from ServerPlayer import Player

def subscribes():
    global client
    #Al de topics waarop we moeten luisteren
    client.subscribe("/player1/client/up")
    client.subscribe("/player1/client/down")
    client.subscribe("/player1/client/fast")

    client.subscribe("/player2/client/up")
    client.subscribe("/player2/client/down")
    client.subscribe("/player2/client/fast")

    client.subscribe("/client/start")
    client.subscribe("/client/player")

def on_message(clients, userdata, message):
    global paddle1, paddle2, start
    # print(message.payload)
    # print(json.loads(message.payload))
    # Publish moet in json formaat

    # threads = enumerate()
    # if len(threads) >= 5:
    #     while threads[5].is_alive():
    #         pass
    
    if "/player1/client/up" in message.topic:
        # Thread(target=movePaddle, args=[player1, "up"]).start()
        movePaddle(player1, "up")
    
    if "/player1/client/down" in message.topic:
        # Thread(target=movePaddle, args=[player1, "down"]).start()
        movePaddle(player1, "down")
    
    if "/player1/client/fast" in message.topic:
        # Thread(target=changePaddleSpeed, args=[player1]).start()
        changePaddleSpeed(player1)
    
    if "/player2/client/up" in message.topic:
        # Thread(target=movePaddle, args=[player2, "up"]).start()
        movePaddle(player2, "up")
    
    if "/player2/client/down" in message.topic:
        # Thread(target=movePaddle, args=[player2, "down"]).start()
        movePaddle(player2, "down")
    
    if "/player2/client/fast" in message.topic:
        # Thread(target=changePaddleSpeed, args=[player2]).start()
        changePaddleSpeed(player2)
    
    if "/client/start" in message.topic:
        print("start")
        client.publish("/server/start", "Start")
        client.publish("/player1/server/coords", json.dumps(paddle1.coords))
        client.publish("/player2/server/coords", json.dumps(paddle2.coords))
        client.publish("/ball/coords", json.dumps(ball.coords))
        start = True
        ball.goalAtPaddle = "Setup"
    
    if "/client/player" in message.topic:
        if player1.isSet == False:
            player1.isSet = True
            client.publish("/server/player", 1)
            client.publish("/server/selectplayer", True)
            print("Player 1 selected")
        else:
            if player2.isSet == False:
                paddle2.isSet = True
                client.publish("/server/player", 2)
                client.publish("/server/selectplayer", True)
                print("Player 2 selected")
            else:
                client.publish("/server/player", 3)
                print("Watcher Added")

def signalStart():
    global client
    print("start")
    client.publish("/player1/server/coords", json.dumps(player1.paddle.coords))
    client.publish("/player2/server/coords", json.dumps(player2.paddle.coords))
    client.publish("/ball/coords", json.dumps(ball.coords))
    for x in range(3):
        client.publish("/server/startnext", "On")
        # print("On")
        sleep(1)
        client.publish("/server/startnext", "Off")
        # print("Off")
        sleep(1)
    sleep(1)
    # gameThreads[games].start()
    # gameThreads[games].join()

def movePaddle(player, message):
    global client
    print(player.name + " " + message)
    player.paddle.movePaddle(message)
    client.publish("/" + player.name + "/server/coords", json.dumps(player.paddle.coords))

def changePaddleSpeed(player):
    global client
    print(player.name + " fast")
    player.paddle.changeSpeed()
    client.publish("/" + player.name + "/server/speed", player.paddle.speed)

def addScore(ball, winner, loser):
    if loser.paddle.side == ball.goalAtPaddle:
        if(ball.bounces == 0):
            winner.points = winner.points + (5)
        else:
            winner.points = winner.points + (ball.bounces * 5)
        client.publish("/" + winner.name + "/points", winner.points)
        print(winner.name + "scores")

def moveBall(ball, player1, player2):
    global client
    while ball.goalAtPaddle == "":
        ball.moveBall((player1.paddle, player2.paddle))
        client.publish("/ball/coords", json.dumps(ball.coords))
        # print(ball.coords)
        sleep(0.2)

scrDimen = (scrHeight, scrWidth) = (500, 500)
stop = start = False
games = 0

paddle1 = Paddle(scrDimen, "Left")
player1 = Player(paddle1, "player1")

paddle2 = Paddle(scrDimen, "Right")
player2 = Player(paddle2, "player2")

ball = Ball(scrDimen)
# gameThreads = []
# for _ in range(11):
#     ballThread = Thread(target=moveBall, args=[ball, player1, player2])
#     gameThreads.append(ballThread)

broker_address="127.0.0.1"
client = mqtt.Client(client_id="server",clean_session=True, userdata="", protocol=mqtt.MQTTv31) #create new instance
client.on_message=on_message #attach function to callback
client.connect(host=broker_address,port=1883) #connect to broker
client.loop_start() #start the loop
subscribes()

while stop == False:
    if start == True:
        client.publish("/server/bounces", ball.bounces)
        if ball.goalAtPaddle == "":
            ball.moveBall((player1.paddle, player2.paddle))
            client.publish("/ball/coords", json.dumps(ball.coords))
            # print(ball.coords)
            sleep(0.1)
        else:
            # wacht tot vorige thread volledig gedaan is
            # while gameThreads[games].is_alive():
            #    pass
            # Huidige posities
            print("Left paddle at " + str(paddle1.side))
            print("Right paddle at " + str(paddle2.side))
            print("Player 1 at " + str(player1.paddle.side))
            print("Player 2 at " + str(player2.paddle.side))
            # Geeft de juiste speler de punten
            addScore(ball, player1, player2)
            addScore(ball, player2, player1)
            
            willy = random.randint(1, 2)
            print("Willy is " + str(willy))
            if willy == 1 or games == 0:
                player1.paddle = paddle1
                player2.paddle = paddle2
                client.publish("/server/selectplayer", True)
            else:
                player1.paddle = paddle2
                player2.paddle = paddle1
                client.publish("/server/selectplayer", False)
            
            # Reset de coordinaten van alle objecten
            ball.resetBall()
            player1.paddle.resetPaddle()
            player2.paddle.resetPaddle()
            # Kijkt na hoeveel games er geweest zijn
            games += 1
            if games <= 10:
                signalStart()
                print("Player 1 selected")
                print("Start Game " + str(games))
            else:
                if player1.points > player2.points:
                    print("player 1 wins")
                elif player1.points < player2.points:
                    print("player 2 wins")
                else:
                    print("draw")
                stop = True

#try:
#	while True:
#        pass
#except KeyboardInterrupt:
#	pass