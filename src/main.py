from cfg import cfg
from umqttsimple import MQTTClient
import ubinascii
import machine
from machine import Pin
from machine import ADC
import utime
import time

delayPerIteration = 3
deepSleepMinutes = cfg['defaultSleepMinutes']

clientID = b"esp8266_" + ubinascii.hexlify( machine.unique_id() )
client = MQTTClient(clientID, cfg['mqttServer'], user=cfg['mqttUser'], password=cfg['mqttPass'], port=cfg['mqttPort'])

# create ADC object on ADC pin
adc = ADC(0)

# D5:14,D6:12,D7:13 
# A=12, B=14, C=13 # because I messed when soldering
pins = [Pin(i, Pin.OUT) for i in cfg['sensorPins']]

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
	client.publish(cfg['mqttPath'] + "/valueOff", valueOff )
	for i in range(0, len(pins)) :
		p = pins[i]
		p.on()
		v = adc.read()
		print("	sensor " + str(i+1) + " value: " + str( v ) )
		client.publish(cfg['mqttPath'] + "/moisture" + chr(65+i), str( v ))
		res.append(v)
		p.off()
	client.publish(cfg['mqttPath'] + "/lastUpdate", stmp)
	return res
#

def onMessage(topic, msg) :
	global deepSleepMinutes
	print("Topic: %s, Message: %s" % (topic, msg))
	try :
		deepSleepMinutes = int(msg)
		print("deepSleepMinutes from MQTT = " + str(deepSleepMinutes) )
	except :
		print("failed to convert MQTT message to float: " + str(msg))
#

try :
	client.connect()
	client.set_callback(onMessage)
	client.subscribe(bytes(cfg['mqttPath'] + "/deepSleepMinutes","ascii"))
	# we make 3 iterations to read sensors and publish results
	for i in range(1, 4) :
		# read mqqt input
		client.check_msg()
		print("------------------------------------------------------------")
		print("iteration {:g}".format(i))
		readSensors()
		time.sleep(delayPerIteration)
		print("------------------------------------------------------------")
	# set default value for deep sleep delay
	if deepSleepMinutes < 1 :
		client.publish(cfg['mqttPath'] + "/deepSleepMinutes", str(cfg['defaultSleepMinutes']) )
	client.disconnect()
except Exception as e: 
	print(e)

deepSleepMS= deepSleepMinutes * 60 * 1000

# deep sleep on 
if deepSleepMinutes > 0 :
	print("going to deep sleep for {:g} minutes.".format(deepSleepMinutes))
	time.sleep(1)
	machine.deepsleep( deepSleepMS )
#