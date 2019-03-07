


#Hardware Platform: FireBeetle-ESP32
#Result: input MQTTlibrary and remote controls LED by mqtt communication.

from umqtt.simple import MQTTClient

from machine import ADC,Pin
import network
import time
import math

adc0=ADC(Pin(36)) 
adc2=ADC(Pin(35))#create ADC object
adc1=ADC(Pin(39))
counter=0
SSID="Ranga"
PASSWORD="12345678"

led=Pin(2, Pin.OUT, value=0)

SERVER = "192.168.43.210"
CLIENT_ID = "ommm"
TOPIC = b"om"
username='you'
password='yaa'
state = 0
c=None
def datasampling(counter):
  data1=[]
  data2=[]
  data3=[]
  maxidata1=[]
  maxidata2=[]
  for i in range(0,2000):
    data1.append(adc0.read())
    data2.append(adc2.read())
    data3.append(adc1.read())
  for j in range(0,len(data1),50):
    aa=data1[j:j+50]
    bb=data2[j:j+50]
    maxiaa=0
    maxibb=0
    for k in range(0,len(aa)):
        if (aa[maxiaa]<aa[k]):
            maxiaa=k
        if (bb[maxibb]<bb[k]):
            maxibb=k
    maximumdata1=aa[maxiaa]
    maximumdata2=bb[maxibb]
    maxidata1.append(maximumdata1)
    maxidata2.append(maximumdata2)
  avg_maxidata1=sum(maxidata1)/len(maxidata1)
  avg_maxidata2=sum(maxidata2)/len(maxidata2)
  
  avg_data3=sum(data3)/len(data3)
  rms_current=avg_maxidata1/math.sqrt(2)
  rms_voltage=avg_maxidata2/math.sqrt(2)
  
  #print("maximum data1 {} maximum data2 {} avergae data3 {}".format(maxidata1,maxidata2,avg_data3))
  #print("rms_current and voltage are {} {}".format(rms_current,rms_voltage))
  #time.sleep(0.001)
  
  return counter,rms_current,rms_voltage,avg_data3

  
  
def sub_cb(topic, msg):
  global state
  print((topic, msg))
  if msg == b"on":
    led.value(1)
    state = 0
    print("1")
  elif msg == b"off":
    led.value(0)
    state = 1
    print("0")
  elif msg == b"toggle":
    # LED is inversed, so setting it to current state
    # value will make it toggle
    led.value(state)
    state = 1 - state
def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)         #create a wlan object
  wlan.active(True)                         #Activate the network interface
  wlan.disconnect()                         #Disconnect the last connected WiFi
  wlan.connect(ssid,passwd)                 #connect wifi
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(0.0001)

    
#Catch exceptions,stop program if interrupted accidentally in the 'try'
try:
  connectWifi(SSID,PASSWORD)
  server=SERVER
  c = MQTTClient(CLIENT_ID, server,0,username,password)     #create a mqtt client
  c.set_callback(sub_cb)                    #set callback
  c.connect()                               #connect mqtt
  c.subscribe(TOPIC)                        #client subscribes to a topic
  print("Connected to %s, subscribed to %s topic" % (server, TOPIC))

  while True:
    a=datasampling(counter)
    print(a)
   
    #time.sleep(3)
    c.publish('hello','{}'.format(a))
    c.check_msg() 
    #time.sleep(0.001)#wait message 
    
    counter+=1
    #time.sleep(0.01)
finally:
  if(c is not None):
    c.disconnect()
  wlan.disconnect()
  wlan.active(False)


