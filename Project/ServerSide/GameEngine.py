import paho.mqtt.client as mqtt
from time import sleep
import json

from ServerPaddle import Paddle
from ServerBall import Ball

broker_address="127.0.0.1"
scrDimen = (scrHeight, scrWidth) = (600, 500)
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

def on_message(clients, userdata, message):
    global paddle1, paddle2, start
    #print(message.payload)
    #print(json.loads(message.payload))
    # Publish moet in json formaat
    if "/player1/client/up" in message.topic:
        print("Player 1 up")
        paddle1.movePaddle("up")
        print(paddle1.coords)
        client.publish("/player1/server/coords", json.dumps(paddle1.coords))
    
    if "/player1/client/down" in message.topic:
        print("Player 1 down")
        paddle1.movePaddle("down")
        print(paddle1.coords)
        client.publish("/player1/server/coords", json.dumps(paddle1.coords))
    
    if "/player1/client/fast" in message.topic:
        print("Player 1 fast")
        paddle1.changeSpeed()
        print(paddle1.speed)
        client.publish("/player1/server/speed", paddle1.speed)
    
    if "/player2/client/up" in message.topic:
        print("Player 2 up")
        paddle2.movePaddle("up")
        print(paddle2.coords)
        client.publish("/player2/server/coords", json.dumps(paddle2.coords))
    
    if "/player2/client/down" in message.topic:
        print("Player 2 down")
        paddle2.movePaddle("down")
        print(paddle2.coords)
        client.publish("/player2/server/coords", json.dumps(paddle2.coords))
    
    if "/player2/client/fast" in message.topic:
        print("Player 2 fast")
        paddle2.changeSpeed()
        print(paddle2.speed)
        client.publish("/player2/server/speed", paddle2.speed)
    
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
            client.publish("/server/player", 1)
            print("Player 1 selected")
        else:
            if paddle2.isSet == False:
                paddle2.isSet = True
                client.publish("/server/player", 2)
                print("Player 2 selected")
            else:
                print("Watcher Added")

def signalStart():
    global client
    for x in range(3):
        client.publish("/server/startNext", "On")
        print("On")
        sleep(1)
        client.publish("/server/startNext", "Off")
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
            # Geeft de juiste speler de punten
            if ball.goal == "Right":
                paddle1.points += ball.bounces * 5
                client.publish("/player1/points", paddle1.points)
                print("Player 1 scores")
            if ball.goal == "Left":
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