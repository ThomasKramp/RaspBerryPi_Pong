import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json

from ServerPaddle import Paddle
from ServerBall import Ball

broker_address="127.0.0.1"
scrDimen = (scrHeight, scrWidth) = (600, 500)
paddle1 = Paddle(scrDimen, True)
paddle2 = Paddle(scrDimen, False)
coordsBall = Ball(scrDimen)

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
    global paddle1, paddle2
    #print(message.payload)
    #print(json.loads(message.payload))
    # Publish moet in json formaat
    if "/player1/client/up" in message.topic:
        print("Player 1 up")
        paddle1.movePaddle("up")
        print(paddle1.coords)
        client.publish("/player1/server/up", json.dumps(paddle1.coords))
    
    if "/player1/client/down" in message.topic:
        print("Player 1 down")
        paddle1.movePaddle("down")
        print(paddle1.coords)
        client.publish("/player1/server/down", json.dumps(paddle1.coords))
    
    if "/player1/client/fast" in message.topic:
        print("Player 1 fast")
        paddle1.changeSpeed()
        print(paddle1.speed)
        client.publish("/player1/server/fast", paddle1.speed)
    
    if "/player2/client/up" in message.topic:
        print("Player 2 up")
        paddle2.movePaddle("up")
        print(paddle2.coords)
        client.publish("/player2/server/up", json.dumps(paddle2.coords))
    
    if "/player2/client/down" in message.topic:
        print("Player 2 down")
        paddle2.movePaddle("down")
        print(paddle2.coords)
        client.publish("/player2/server/down", json.dumps(paddle2.coords))
    
    if "/player2/client/fast" in message.topic:
        print("Player 2 fast")
        paddle2.changeSpeed()
        print(paddle2.speed)
        client.publish("/player2/server/fast", paddle2.speed)
    
    if "/client/start" in message.topic:
        print("start")
    
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

client = mqtt.Client(client_id="server",clean_session=True, userdata="", protocol=mqtt.MQTTv31) #create new instance
client.on_message=on_message #attach function to callback
client.connect(host=broker_address,port=1883) #connect to broker
client.loop_start() #start the loop
subscribes()

try:
	while True:
		pass
except KeyboardInterrupt:
	pass