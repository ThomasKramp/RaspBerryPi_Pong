import tkinter as tk
from Object.Paddle_Client import Paddle
from Object.Ball_Client import Ball
from Object.Led import Led, LedColors
from Object.Button import Button

import paho.mqtt.client as mqtt
#import paho.mqtt.subscribe as subscribe
import time
import json

def subscribes():
    global client
    #Al de topics waarop we moeten luisteren
    client.subscribe("/player1/server/coords")
    client.subscribe("/player2/server/coords")
    client.subscribe("/bal/coords")
    client.subscribe("/server/start")
    client.subscribe("/server/startnext")
    client.subscribe("/server/player")
    client.subscribe("/server/selectplayer")    

def playerLeft():
    global GreenLedL,GreenLedR, RedLedL, RedLedR
    GreenLedL.On();
    RedLedL.Off();
    GreenLedR.Off();
    RedLedR.On();

def playerRight():
    global GreenLedL,GreenLedR, RedLedL, RedLedR
    GreenLedL.Off();
    RedLedL.On();
    GreenLedR.On();
    RedLedR.Off();

# Alle afhandelingen van MQTT
def on_message(clients, userdata, message):
    global coordsPlayer1, Pad1, coordsPlayer2, Pad2, coordsBall, Ball, YellowLed, btnStart, playerSelector, playerSelectorSet,broker_address,client
    print(userdata)

    if(userdata == "initial"):
        if("/server/player" in message.topic):
            print(message.payload)
            x = message.payload.decode("utf-8") 
            print(x)
            if(x == "False" and playerSelector < 3 and playerSelectorSet == False): # Als de player al bestond en de playerSelector is kleiner dan 3
                playerSelector = playerSelector + 1
                client.publish("/client/player",playerSelector)
            else:

                playerSelectorSet = True
                client.loop_stop() #stop de loop
                name = ""
                if(playerSelector == 1):
                    print("verander client name naar 'Player1'")
                    name = "Player1"
                elif(playerSelector == 2):
                    print("verander client name naar 'Player2'")
                    name = "Player2"
                else:
                    print("verander client name naar 'Watcher'")
                    name = "Watcher"

                
                client = mqtt.Client(client_id=name,clean_session=True, userdata="inGame", protocol=mqtt.MQTTv31) #create new instance
                client.on_message=on_message #attach function to callback
                client.connect(host=broker_address,port=1883) #connect to broker
                client.loop_start() #start the loop
                subscribes()
    else:
        if("/player1/server/coords" in message.topic):
        #     print(message.payload)
        #    a = json.loads(message.payload)
        #    print(a[0])
        #    coordsPlayer1 = a
        #    Pad1.move(coordsPlayer1)
        #    print(coordsPlayer1)
            Pad1.move(json.loads(message.payload))

        if("/player2/server/coords" in message.topic):
        #   print(message.payload)
        #   a = json.loads(message.payload)
        #   print(a[0])
        #   coordsPlayer1 = a
        #   Pad2.move(coordsPlayer1)
        #   print(coordsPlayer1)
            Pad2.move(json.loads(message.payload))

        if("/bal/coords" in message.topic):
            Ball.move(json.loads(message.payload))

        if("/server/start" in message.topic): #Wanneer de server de start heeft ontvangen kunnen we deze knop verwijderen
            btnStart.destroy()

        if("/server/startnext" in message.topic):
            YellowLed.Toggle()
        if("server/selectplayer" in message.topic):
            print(message.payload)
            x = message.payload.decode("utf-8") 
            if(x == "False" and playerSelector == 1 or x == "True" and playerSelector == 2):
                playerRight()

            if(x == "False" and playerSelector == 2 or x == "True" and playerSelector == 1):
                playerLeft()

def PaddleUp():
    #Stuur True naar MQTT
    global client

    if(playerSelector == 1):
        client.publish("/player1/client/up","True")
    elif(playerSelector == 2):
        client.publish("/player2/client/up","True")
    else:
        print("Enkel kijken")

def PaddleSpeed():
    #Stuur True naar MQTT
    global client, speed    
    if speed:
        speed = False
    else:
        speed = True

    if(playerSelector == 1):
        client.publish("/player1/client/fast",speed)
    elif(playerSelector == 2):
        client.publish("/player2/client/fast",speed)
    else:
        print("Enkel kijken")

def PaddleDown():
    #Stuur True naar MQTT
    global client

    if(playerSelector == 1):
        client.publish("/player1/client/down","True")
    elif(playerSelector == 2):
        client.publish("/player2/client/down","True")
    else:
        print("Enkel kijken")

def Start():
    print("Start")
    client.publish("/client/start","True")

broker_address="127.0.0.1" 
client = mqtt.Client(client_id="Client2",clean_session=True, userdata="initial", protocol=mqtt.MQTTv31) #create new instance
client.on_message=on_message #attach function to callback
client.connect(host=broker_address,port=1883) #connect to broker
client.loop_start() #start the loop

subscribes()


scrHeight = 600
scrWidth = 500

#Initial startup fase wanneer we geen verbinding hebben met de Game Engine
speed = False
coordsPlayer1 = (10,scrHeight/2-50,20,scrHeight/2+50) #De coördinaten van de speler1
coordsPlayer2 = (scrWidth-20,scrHeight/2-50,scrWidth-10,scrHeight/2+50) #De coördinaten van de speler2
coordsBall = (scrWidth / 2 - 10, scrHeight / 2 - 10, scrWidth / 2 + 10, scrHeight / 2 + 10) #De coördinaten van de bal

#Selectie variabelen
#Deze variabelen zal 1 blijven als de server een True heeft geantwoord op topic /server/player
#Deze variabelen zal 2 blijven als de server een True heeft geantwoord op topic /server/player bij een response van False wanneer we op de topic /client/player een 1 hadden gestuurd
#Deze variabelen zal een 3 zijn wanneer er al 2 players actief zijn.
playerSelector = 1 
playerSelectorSet = False;

client.publish("/client/player",playerSelector) #Eerste initiatie naar server toe om speler te worden

root = tk.Tk()
canvas = tk.Canvas( root, height = scrHeight, width = scrWidth)

Pad1 = Paddle(canvas, coordsPlayer1, "black")
Pad2 = Paddle(canvas, coordsPlayer2, "black")
Ball = Ball(canvas, coordsBall, "black")
# Start de functie opnieuw op
canvas.pack()

#Aanmaken knopjes
btn1Up = Button(canvas, (scrWidth - (scrWidth-20),scrHeight - 30), "white","Up", PaddleUp)
btn1Speed = Button(canvas, (scrWidth - (scrWidth-50),scrHeight - 30), "white","Speed", PaddleSpeed)
btn1Down = Button(canvas, (scrWidth - (scrWidth-100),scrHeight - 30), "white","Down", PaddleDown)
#Aanmaken leds
GreenLedL = Led(canvas,(scrWidth - (scrWidth-20),scrHeight - 50,scrWidth - (scrWidth-40),scrHeight - 70), LedColors[2],LedColors[3])
RedLedL = Led(canvas,(scrWidth - (scrWidth-50),scrHeight - 50,scrWidth - (scrWidth-70),scrHeight - 70), LedColors[4],LedColors[5])

#Aanmaken knopjes
btn2Up = Button(canvas, (scrWidth - 140,scrHeight - 30), "white","Up", PaddleUp)
btn2Speed = Button(canvas, (scrWidth - 110,scrHeight - 30), "white","Speed", PaddleSpeed)
btn2Down = Button(canvas, (scrWidth - 60,scrHeight - 30), "white","Down", PaddleDown)
#Aanmaken leds
GreenLedR = Led(canvas,(scrWidth - 40 ,scrHeight - 50,scrWidth -60,scrHeight - 70), LedColors[2],LedColors[3])
RedLedR = Led(canvas,(scrWidth - 70,scrHeight - 50,scrWidth - 90,scrHeight - 70), LedColors[4],LedColors[5])

#Aanmaken waarschuw led en start knop
YellowLed = Led(canvas,(scrWidth/2-10,scrHeight - 50,scrWidth/2+10,scrHeight - 70), LedColors[0],LedColors[1])
btnStart = Button(canvas, (scrWidth/2-20,scrHeight - 30), "Green","Start", Start)

canvas.pack()

root.mainloop()