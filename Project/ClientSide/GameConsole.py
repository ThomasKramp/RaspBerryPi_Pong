import paho.mqtt.client as mqtt
import tkinter as tk
from Paddle import Paddle
from Ball import Ball
from Label import Label

from time import sleep
import json

def subscribes():
    global client
    #Al de topics waarop we moeten luisteren
    client.subscribe("/player1/server/coords")
    client.subscribe("/player2/server/coords")
    client.subscribe("/ball/coords") 
    client.subscribe("/player2/points")
    client.subscribe("/player1/points")
    client.subscribe("/server/bounces")

# Alle afhandelingen van MQTT
def on_message(clients, userdata, message):
    global Pad1, Pad2, Ball, points1, points2, ticks
    #print(userdata)
    if("/player1/server/coords" in message.topic):
        Pad1.move(json.loads(message.payload))

    if("/player2/server/coords" in message.topic):
        Pad2.move(json.loads(message.payload))

    if("/ball/coords" in message.topic):
        #print(message.payload)
        Ball.move(json.loads(message.payload))

    if("/player2/points" in message.topic):
        points2.changeText("player2: ", json.loads(message.payload))
    if("/player1/points" in message.topic):
        points1.changeText("player1: ", json.loads(message.payload))
    if("/server/bounces" in message.topic):
        ticks.changeText("ticks: ", json.loads(message.payload))
        

broker_address="192.168.1.4"
client = mqtt.Client(client_id="Client2",clean_session=True, userdata="initial", protocol=mqtt.MQTTv31) #create new instance
client.on_message=on_message #attach function to callback
client.connect(host=broker_address,port=1883) #connect to broker
client.loop_start() #start the loop

subscribes()


scrHeight = 500
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
points1 = Label(canvas, (scrWidth/2-30,0),"player2: 0")
points2 = Label(canvas, (scrWidth/2-30,30),"player1: 0")
ticks = Label(canvas, (scrWidth/2-30, 60),"ticks: 0")

canvas.pack()

root.mainloop()