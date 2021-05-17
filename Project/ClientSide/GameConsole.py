import tkinter as tk
from Paddle import Paddle
from Ball import Ball
from Led import Led, LedColors
from Button import Button
from Label import Label

import paho.mqtt.client as mqtt

from time import sleep
import json

def subscribes():
    global client
    #Al de topics waarop we moeten luisteren
    client.subscribe("/player1/server/coords")
    client.subscribe("/player2/server/coords")
    client.subscribe("/ball/coords") 

# Alle afhandelingen van MQTT
def on_message(clients, userdata, message):
    global coordsPlayer1, Pad1, coordsPlayer2, Pad2, coordsBall, Ball, YellowLed, btnStart,broker_address,client,playerSelector
    #print(userdata)
    if("/player1/server/coords" in message.topic):
        Pad1.move(json.loads(message.payload))

    if("/player2/server/coords" in message.topic):
        Pad2.move(json.loads(message.payload))

    if("/ball/coords" in message.topic):
        print(message.payload)
        Ball.move(json.loads(message.payload))

broker_address="192.168.35.206" 
client = mqtt.Client(client_id="Client",clean_session=True, userdata="initial", protocol=mqtt.MQTTv31) #create new instance
client.on_message=on_message #attach function to callback
client.connect(host=broker_address,port=1883) #connect to broker
client.loop_start() #start the loop

subscribes()


scrHeight = 600
scrWidth = 500

coordsPlayer1 = (10,scrHeight/2-50,20,scrHeight/2+50) #De coördinaten van de speler1
coordsPlayer2 = (scrWidth-20,scrHeight/2-50,scrWidth-10,scrHeight/2+50) #De coördinaten van de speler2
coordsBall = (scrWidth / 2 - 10, scrHeight / 2 - 10, scrWidth / 2 + 10, scrHeight / 2 + 10) #De coördinaten van de bal

root = tk.Tk()
canvas = tk.Canvas( root, height = scrHeight, width = scrWidth)

#Aanmaak paddles en bal
Pad1 = Paddle(canvas, coordsPlayer1, "black")
Pad2 = Paddle(canvas, coordsPlayer2, "black")
Ball = Ball(canvas, coordsBall, "black")

#Aanmaken van scores etc.
pointsLB = Label(canvas, (0,0),"0")

canvas.pack()

root.mainloop()