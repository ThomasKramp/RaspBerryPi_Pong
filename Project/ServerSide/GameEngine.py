import paho.mqtt.client as mqtt
from time import sleep
import random
import json

from ServerPaddle import Paddle
from ServerBall import Ball
from ServerPlayer import Player

broker_address="192.168.60.206"
scrDimen = (scrHeight, scrWidth) = (500, 500)
paddle1 = Paddle(scrDimen, "Left")
paddle2 = Paddle(scrDimen, "Right")
player1 = Player(paddle1)
player2 = Player(paddle2)
ball = Ball(scrDimen)
stop = start = False
games = 0

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
    
    if "/player1/client/up" in message.topic:
        print("Player 1 up")
        player1.paddle.movePaddle("up")
        client.publish("/player1/server/coords", json.dumps(player1.paddle.coords))
    
    if "/player1/client/down" in message.topic:
        print("Player 1 down")
        player1.paddle.movePaddle("down")
        client.publish("/player1/server/coords", json.dumps(player1.paddle.coords))
    
    if "/player1/client/fast" in message.topic:
        print("Player 1 fast")
        player1.paddle.changeSpeed()
        client.publish("/player1/server/speed", player1.paddle.speed)
    
    if "/player2/client/up" in message.topic:
        print("Player 2 up")
        player2.paddle.movePaddle("up")
        client.publish("/player2/server/coords", json.dumps(player2.paddle.coords))
    
    if "/player2/client/down" in message.topic:
        print("Player 2 down")
        player2.paddle.movePaddle("down")
        client.publish("/player2/server/coords", json.dumps(player2.paddle.coords))
    
    if "/player2/client/fast" in message.topic:
        print("Player 2 fast")
        player2.paddle.changeSpeed()
        client.publish("/player2/server/speed", player2.paddle.speed)
    
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
            # print(ball.coords)
            client.publish("/ball/coords", json.dumps(ball.coords))
            sleep(1)
        else:
            print("Left paddle at " + str(paddle1.side))
            print("Right paddle at " + str(paddle2.side))
            print("Player 1 at " + str(player1.paddle.side))
            print("Player 2 at " + str(player2.paddle.side))

            # Geeft de juiste speler de punten
            if player1.paddle.side == ball.goalAtPaddle:
                if(ball.bounces == 0):
                    player2.points += 1 * 5
                else:
                    player2.points = player2.points + (ball.bounces * 5)
                client.publish("/player2/points", player2.points)
                print("Player 2 scores")
            if player2.paddle.side == ball.goalAtPaddle:
                if(ball.bounces == 0):
                    player1.points = player1.points + (5)
                else:
                    player1.points = player1.points + (ball.bounces * 5)
                client.publish("/player1/points", player1.points)
                print("Player 1 scores")
            
            willy = random.randint(1, 2)
            print("Willy is " + str(willy))
            if willy == 1:
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
                stop = True

#try:
#	while True:
#        pass
#except KeyboardInterrupt:
#	pass