import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import json

from ServerPaddle import Paddle
from ServerBall import Ball

broker_address="192.168.255.206"
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
    if "/player1/client/up" in message.topic:
        print("up1")
        paddle1.movePaddle("up")
        print(paddle1.coords)
        client.publish("/player1/server/up", paddle1.coords)
    
    if "/player1/client/down" in message.topic:
        print("down1")
        paddle1.movePaddle("down")
        print(paddle1.coords)
        client.publish("/player1/server/down", paddle1.coords)
    
    if "/player1/client/fast" in message.topic:
        print("fast1")
        paddle1.changeSpeed()
        print(paddle1.speed)
        client.publish("/player1/server/fast", paddle1.speed)
    
    if "/player2/client/up" in message.topic:
        print("up2")
        paddle2.movePaddle("up")
        print(paddle2.coords)
        client.publish("/player2/server/up", paddle2.coords)
    
    if "/player2/client/down" in message.topic:
        print("down2")
        paddle2.movePaddle("down")
        print(paddle2.coords)
        client.publish("/player2/server/down", paddle2.coords)
    
    if "/player2/client/fast" in message.topic:
        print("fast2")
        paddle2.changeSpeed()
        print(paddle2.speed)
        client.publish("/player2/server/fast", paddle2.speed)
    
    if "/client/start" in message.topic:
        print("start")
    
    if "/client/player" in message.topic:
        print("player")
    


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