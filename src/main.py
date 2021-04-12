from umqttsimple import MQTTClient
import ubinascii
import machine
from machine import Pin
from machine import ADC
import utime
import time

delayPerIteration = 3
deepSleepMinDefault = 10
deepSleepMin = deepSleepMinDefault

clientID = b"esp8266_" + ubinascii.hexlify(machine.unique_id())
client = MQTTClient(clientID, "192.168.0.xxxx", user="mqtt", password="xxxx", port=1883)

# create ADC object on ADC pin
adc = ADC(0)

# D5:14,D6:12,D7:13
# A=12, B=14, C=13 # because I messed when soldering
pins = [ Pin(12, Pin.OUT), Pin(14, Pin.OUT), Pin(13, Pin.OUT) ]

# 
def readSensors() :
	t = utime.localtime()
	stmp = "{:04d}.{:02d}.{:02d} {:02d}:{:02d}:{:02d}".format( t[0],t[1],t[2],t[3]+2,t[4],t[5] )
	print("	current time stamp: " + stmp)
	res = []
	print("	switching off all sensors ... ")
	for p in pins :
		p.off()
	valueOff = str( adc.read() )
	print("	sensor off value: " + valueOff)
	client.publish("groot/valueOff", valueOff )
	for i in range(0, len(pins)) :
		p = pins[i]
		p.on()
		v = adc.read()
		print("	sensor " + str(i+1) + " value: " + str( v ) )
		client.publish("groot/moisture" + chr(65+i), str( v ))
		res.append(v)
		p.off()
	client.publish("groot/lastUpdate", stmp)
	return res
#
def onMessage(topic, msg) :
	global deepSleepMin
	print("Topic: %s, Message: %s" % (topic, msg))
	try :
		deepSleepMin = int(msg)
		print("deepSleepMinutes from MQTT = " + str(deepSleepMin) )
	except :
		print("failed to convert MQTT message to float: " + str(msg))
#

client.connect()
client.set_callback(onMessage)
client.subscribe(b"groot/deepSleepMinutes")
client.check_msg()

for i in range(1, 4) :
	print("------------------------------------------------------------")
	print("iteration {:g}".format(i))
	readSensors()
	time.sleep(delayPerIteration)
	print("------------------------------------------------------------")
#

client.check_msg()
client.disconnect()

deepSleepMS= deepSleepMin * 60 * 1000

if deepSleepMin > 0 :
	print("going to deep sleep for {:g} minutes.".format(deepSleepMin))
	time.sleep(1)
	machine.deepsleep( deepSleepMS )
else :
	print("deep sleep off. Please set MQTT/groot/deepSleepMin > 0 and restart manually.")
	client.connect()
	client.publish("groot/deepSleepMinutes", str(deepSleepMinDefault) )
	client.disconnect()
#