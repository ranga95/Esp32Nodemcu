"""
import paho.mqtt.client as mqtt
import time as t
mqttc = mqtt.Client("p")
mqttc.connect("192.168.43.210")
mqttc.username_pw_set("you","yaa")
"""
import pandas as pd
import paho.mqtt.client as mqtt #import the client1
import time
############
l=[]
#r=[{"ranga","ram"}]
#df=pd.DataFrame(columns=["SlNo","Current","Voltage","Sensor"])

df=[]
print(df)
def on_message(client, userdata, message):
    #print("message received " ,str(message.payload.decode("utf-8")))
    msg=str(message.payload.decode("utf-8"))
    msg=msg[1:-1]
    
    #print(msg)
    msg=msg.split(',')
    msg=list(msg)
    print(msg)
    df.append(msg)
    
    print(type(msg))
    
    #df.append({"SlNo":msg[0],"Current":msg[1],"Voltage":msg[2],"Sensor":msg[3]})
    print(df)
    time.sleep(1)
    
  
########################################
broker_address="192.168.43.210"
#broker_address="iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.username_pw_set("you","yaa")
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","helloe")
client.subscribe("hello")
"""
for i in range(0,10):
    #print("Publishing message to topic","om")
    client.publish("om","on")
    client.on_message=on_message 
    #time.sleep(1)
    client.publish("om","off")
"""
    
    

#client.loop_stop() #stop the loop
