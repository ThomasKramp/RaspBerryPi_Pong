#!/usr/bin/python3
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from time import sleep
from Led import LedHW
from Button import ButtonHW
import json


GPIO.setmode(GPIO.BCM)


def subscribes():
    global client
    #Al de topics waarop we moeten luisteren
    client.subscribe("/player1/server/coords")
    client.subscribe("/player2/server/coords")
    client.subscribe("/ball/coords")
    client.subscribe("/server/start")
    client.subscribe("/server/startnext")
    client.subscribe("/server/player")
    client.subscribe("/server/selectplayer")    

def playerLeft():
    global GreenLedL,GreenLedR, RedLedL, RedLedR
    GreenLedL.On()
    RedLedL.Off()
    GreenLedR.Off()
    RedLedR.On()

def playerRight():
    global GreenLedL,GreenLedR, RedLedL, RedLedR
    GreenLedL.Off()
    RedLedL.On()
    GreenLedR.On()
    RedLedR.Off()

# Alle afhandelingen van MQTT
def on_message(clients, userdata, message):
    global coordsPlayer1, Pad1, coordsPlayer2, Pad2, coordsBall, Ball, YellowLed, btnStart,broker_address,client,playerSelector, hasStarted
    #print(userdata)

    if(userdata == "initial"):
        if("/server/player" in message.topic):
            print(message.payload)
            x = message.payload.decode("utf-8") 
            print(x)
            playerSelector = int(x)
            name = ""
            if(playerSelector == 1):
                print("verander client name naar 'Player1'")
                name = "Player1"
            elif(playerSelector == 2):
                print("verander client name naar 'Player2'")
                name = "Player2"
            elif(playerSelector == 3):
                print("verander client name naar 'Watcher'")
                name = "Watcher"

            client.loop_stop() #stop de loop
            sleep(0.5)
            client = mqtt.Client(client_id=name,clean_session=True, userdata="inGame", protocol=mqtt.MQTTv31) #create new instance
            client.on_message=on_message #attach function to callback
            client.connect(host=broker_address,port=1883) #connect to broker
            client.loop_start() #start the loop
            subscribes()
    else:
        if("/server/start" in message.topic): #Wanneer de server de start heeft ontvangen kunnen we deze knop verwijderen
            btnStart.destroy()
            hasStarted = True

        if("/server/startnext" in message.topic):
            YellowLed.Toggle()
            print("Led On Off")

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

def isr(channel):
    global hasStarted
    if(channel == 27):
        print("BTN Up")
        PaddleUp()
    if(channel == 22):
        print("BTN Down")
        PaddleDown()
    if(channel == 5 and hasStarted == True):
        print("BTN Speed")
        PaddleSpeed()
    elif (channel == 5 and hasStarted == False):
        Start()
        hasStarted = True

hasStarted = False

#Aanmaken knopjes
BTNUP = Button(GPIO, 27, isr)
BTNDOWN = Button(GPIO, 22, isr)
BTNSPEED = Button(GPIO, 5, isr)
#Aanmaken leds
RedLedR = LedHW(GPIO, 17)
RedLedL = LedHW(GPIO, 11)
GreenLedR = LedHW(GPIO, 10)
GreenLedL = LedHW(GPIO, 0)
YellowLed = LedHW(GPIO, 9)

broker_address="192.168.35.206" 
client = mqtt.Client(client_id="Client2",clean_session=True, userdata="initial", protocol=mqtt.MQTTv31) #create new instance
client.on_message=on_message #attach function to callback
client.connect(host=broker_address,port=1883) #connect to broker
client.loop_start() #start the loop

subscribes()

#Initial startup fase wanneer we geen verbinding hebben met de Game Engine
speed = False
playerSelector = 0
client.publish("/client/player",1) #Eerste initiatie naar server toe om speler te worden