import paho.mqtt.client as mqtt
from threading import Thread
from time import sleep
import random
import json

from ServerPaddle import Paddle
from ServerBall import Ball
from ServerPlayer import Player

def MQTT():
    global client
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
        global player1, player2, ball, start
        # print(message.payload)
        # print(json.loads(message.payload))
        # Publish moet in json formaat
        
        if "/player1/client/up" in message.topic:        
            movePaddle(player1, "up")
        
        if "/player1/client/down" in message.topic:
            movePaddle(player1, "down")
        
        if "/player1/client/fast" in message.topic:
            changePaddleSpeed(player1)
        
        if "/player2/client/up" in message.topic:
            movePaddle(player2, "up")
        
        if "/player2/client/down" in message.topic:
            movePaddle(player2, "down")
        
        if "/player2/client/fast" in message.topic:
            changePaddleSpeed(player2)
        
        if "/client/start" in message.topic:
            print("start")
            client.publish("/server/start", "Start")
            client.publish("/player1/server/coords", json.dumps(player1.paddle.coords))
            client.publish("/player2/server/coords", json.dumps(player2.paddle.coords))
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
                    player2.isSet = True
                    client.publish("/server/player", 2)
                    client.publish("/server/selectplayer", True)
                    print("Player 2 selected")
                else:
                    client.publish("/server/player", 3)
                    print("Watcher Added")

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
    
    broker_address="192.168.1.4"
    client.on_message=on_message #attach function to callback
    client.connect(host=broker_address,port=1883) #connect to broker
    client.loop_start() #start the loop
    subscribes()

def Game():
    global start, stop, player1, player2, ball, client
    def addScore(ball, winner, loser):
        if loser.paddle.side == ball.goalAtPaddle:
            if(ball.bounces == 0):
                winner.points = winner.points + (5)
            else:
                winner.points = winner.points + (ball.bounces * 5)
            client.publish("/" + winner.name + "/points", winner.points)
            print(winner.name + "scores")

    def signalStart(player1, player2, ball):
        global client
        print("start")
        client.publish("/server/start", "Start")
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

    games = 0
    leftPaddle = player1.paddle
    rightPaddle = player2.paddle

    while stop == False:
        if start == True:
            client.publish("/server/bounces", ball.bounces)
            if ball.goalAtPaddle == "":
                ball.moveBall((player1.paddle, player2.paddle))
                client.publish("/ball/coords", json.dumps(ball.coords))
                # print(ball.coords)
                sleep(0.1)
            else:
                # Huidige posities
                print("Player 1 at " + str(player1.paddle.side))
                print("Player 2 at " + str(player2.paddle.side))
                # Geeft de juiste speler de punten
                addScore(ball, player1, player2)
                addScore(ball, player2, player1)
                
                willy = random.randint(1, 2)
                print("Willy is " + str(willy))
                if willy == 1 or games == 0:
                    player1.paddle = leftPaddle
                    player2.paddle = rightPaddle
                    client.publish("/server/selectplayer", True)
                else:
                    player1.paddle = rightPaddle
                    player2.paddle = leftPaddle
                    client.publish("/server/selectplayer", False)
                
                # Reset de coordinaten van alle objecten
                ball.resetBall()
                player1.paddle.resetPaddle()
                player2.paddle.resetPaddle()

                # Kijkt na hoeveel games er geweest zijn
                games += 1
                if games <= 10:
                    signalStart(player1, player2, ball)
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

scrDimen = (scrHeight, scrWidth) = (500, 750)
stop = start = False

player1 = Player(Paddle(scrDimen, "Left"), "player1")
player2 = Player(Paddle(scrDimen, "Right"), "player2")
ball = Ball(scrDimen)

client = mqtt.Client(client_id="server",clean_session=True, userdata="", protocol=mqtt.MQTTv31) #create new instance

mqttJob = Thread(target=MQTT)
gameJob = Thread(target=Game)

mqttJob.start()
gameJob.start()