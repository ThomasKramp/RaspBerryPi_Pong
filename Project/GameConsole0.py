import tkinter as tk
from Object.Paddle2 import Paddle
from Object.Ball import Ball
from Object.Led import Led, LedColors
from Object.Button import Button

import paho.mqtt.client as client
import paho.mqtt.subscribe as subscribe
import time
import json

# Alle afhandelingen van MQTT
def on_message(client, userdata, message):
    if("/player0/server/y" in message.topic):
        print(message.payload)
    if("/player0/server/x" in message.topic):
        print(message.payload[2])
        a = json.loads(message.payload)
        print(a["x0"])
    # if("/player0/server/x1" in message.topic):
    #     print(message.payload)
    # if("/player0/server/y1" in message.topic):
    #     print(message.payload)


def movePaddleUp():
    #Stuur True naar MQTT
    global client
    client.publish("/player0/client/up","true")



#mqttTopicsPlayer0Paddle = ["/player0/server/x0","//player0/server/y0","/player0/server/x1","/player0/server/y1","/player0/client/up","/player0/client/down","/player0/client/fast",""]
broker_address="127.0.0.1" 
client = client.Client(client_id="Client",clean_session=False, userdata=None, protocol=client.MQTTv31) #create new instance
client.on_message=on_message #attach function to callback
client.connect(host=broker_address,port=1883) #connect to broker
client.loop_start() #start the loop
client.subscribe("/player0/server/x")


scrHeight = 500
scrWidth = 500

root = tk.Tk()
canvas = tk.Canvas( root, height = scrHeight, width = scrWidth)

Pad1 = Paddle(canvas, (10,scrHeight/2-50,20,scrHeight/2+50), "black")
Pad2 = Paddle(canvas, (scrWidth-20,scrHeight/2-50,scrWidth-10,scrHeight/2+50), "black")
Ball = Ball(canvas, (scrHeight, scrWidth))
# Start de functie opnieuw op
canvas.pack()

btn0Up = Button(canvas, (scrWidth - (scrWidth-20),scrHeight - 30), "white","Up", movePaddleUp)
#btn0Down = Button(canvas, (scrWidth - (scrWidth-20),scrHeight - 30), "white","Up", movePaddleUp)
#btn0Speed

root.mainloop()