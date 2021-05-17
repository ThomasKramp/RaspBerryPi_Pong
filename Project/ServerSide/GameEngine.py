import paho.mqtt.client as mqtt
from time import sleep
import random
import json

from ServerPaddle import Paddle
from ServerBall import Ball

broker_address="192.168.35.206"
scrDimen = (scrHeight, scrWidth) = (500, 500)
paddle1 = Paddle(scrDimen, True)
paddle2 = Paddle(scrDimen, False)
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

def checkPaddle(paddle, message):
    if paddle.player == 1:
        if "/player1/client/up" in message.topic:
            print("Player 1 up")
            paddle.movePaddle("up")
            print(paddle.coords)
            client.publish("/player1/server/coords", json.dumps(paddle.coords))
        
        if "/player1/client/down" in message.topic:
            print("Player 1 down")
            paddle.movePaddle("down")
            print(paddle.coords)
            client.publish("/player1/server/coords", json.dumps(paddle.coords))
        
        if "/player1/client/fast" in message.topic:
            print("Player 1 fast")
            paddle.changeSpeed()
            print(paddle.speed)
            client.publish("/player1/server/speed", paddle.speed)
    
    if paddle.player == 2:
        if "/player2/client/up" in message.topic:
            print("Player 2 up")
            paddle.movePaddle("up")
            print(paddle.coords)
            client.publish("/player2/server/coords", json.dumps(paddle.coords))
        
        if "/player2/client/down" in message.topic:
            print("Player 2 down")
            paddle.movePaddle("down")
            print(paddle.coords)
            client.publish("/player2/server/coords", json.dumps(paddle.coords))
        
        if "/player2/client/fast" in message.topic:
            print("Player 2 fast")
            paddle.changeSpeed()
            print(paddle.speed)
            client.publish("/player2/server/speed", paddle.speed)

def on_message(clients, userdata, message):
    global paddle1, paddle2, start
    # print(message.payload)
    # print(json.loads(message.payload))
    # Publish moet in json formaat
    
    checkPaddle(paddle1, message)
    checkPaddle(paddle2, message)
    
    if "/client/start" in message.topic:
        print("start")
        signalStart()
        client.publish("/server/start", "Start")
        client.publish("/player1/server/coords", json.dumps(paddle1.coords))
        client.publish("/player2/server/coords", json.dumps(paddle2.coords))
        client.publish("/ball/coords", json.dumps(ball.coords))
        start = True
    
    if "/client/player" in message.topic:
        if paddle1.isSet == False:
            paddle1.isSet = True
            paddle1.player = 1
            client.publish("/server/player", 1)
            client.publish("/server/selectplayer", True)
            print("Player 1 selected")
        else:
            if paddle2.isSet == False:
                paddle2.isSet = True
                paddle2.player = 200
                client.publish("/server/player", 2)
                client.publish("/server/selectplayer", True)
                print("Player 2 selected")
            else:
                client.publish("/server/player", 3)
                print("Watcher Added")
        sleep(5)

def signalStart():
    global client
    for x in range(3):
        sleep(1)
        client.publish("/server/startnext", "On")
        print("On")
        sleep(1)
        client.publish("/server/startnext", "Off")
        print("Off")
        sleep(1)

client = mqtt.Client(client_id="server",clean_session=True, userdata="", protocol=mqtt.MQTTv31) #create new instance
client.on_message=on_message #attach function to callback
client.connect(host=broker_address,port=1883) #connect to broker
client.loop_start() #start the loop
subscribes()

while stop == False:
    if start == True:
        if ball.goal == "":
            ball.moveBall((paddle1, paddle2))
            print(ball.coords)
            client.publish("/ball/coords", json.dumps(ball.coords))
            sleep(1)
        else:
            willy = random.randint(1, 3)
            print("Willy is " + str(willy))
            if willy == 1:
                paddle1.player = 1
                paddle2.player = 2
                client.publish("/server/selectplayer", True)
            else:
                paddle1.player = 2
                paddle2.player = 1
                client.publish("/server/selectplayer", False)

            # Geeft de juiste speler de punten
            if ball.goal == "Left":
                paddle1.points += ball.bounces * 5
                client.publish("/player1/points", paddle1.points)
                print("Player 1 scores")
            if ball.goal == "Right":
                paddle2.points += ball.bounces * 5
                client.publish("/player2/points", paddle2.points)
                print("Player 2 scores")
            
            # Reset de coordinaten van alle objecten
            ball.resetBall()
            paddle1.resetPaddle()
            paddle2.resetPaddle()

            # Kijkt na hoeveel games er geweest zijn
            games += 1
            if games < 10:
                signalStart()
                print("Start Game " + str(games + 1))
            else:
                stop = True

#try:
#	while True:
#        pass
#except KeyboardInterrupt:
#	pass