#!/usr/bin/python3

import paho.mqtt.client as client #import the client1
import paho.mqtt.subscribe as subscribe #import the client1
import time

def on_message(client, userdata, message):

    if("KrampElsermansPong/y" in message.topic):
        
        print("message received " ,str(message.payload.decode("utf-8")))
	    
        print("message topic=",message.topic)
	    
        print("message qos=",message.qos)
	    
        print("message retain flag=",message.retain)

broker_address="127.0.0.1" 
client = client.Client(client_id="ServerClient",clean_session=False, userdata=None, protocol=client.MQTTv31) #create new instance
client.on_message=on_message #attach function to callback
client.connect(host=broker_address,port=1883) #connect to broker
client.loop_start() #start the loop
#subscribe.callback(on_message, "KrampElsermansPong/y", hostname=broker_address)
client.subscribe("KrampElsermansPong/y")

time.sleep(10)
client.publish("KrampElsermansPong/x","yes")

time.sleep(2)
client.publish("KrampElsermansPong/x","yes")
time.sleep(2)
client.publish("KrampElsermansPong/x","yes")
time.sleep(2)
client.publish("KrampElsermansPong/x","yes")

client.loop_stop() #stop the loop
