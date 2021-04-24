from cfg import cfg

# connect wifi
try :
	import network
	wlan = network.WLAN(network.STA_IF)
	if not wlan.isconnected():
		print('connecting to network...')
		wlan.active(True)
		wlan.connect( cfg['wifiName'], cfg['wifiPass'] )
		while not wlan.isconnected():
			pass
	print('network config:', wlan.ifconfig())
except :
	print("wifi connection failed")

# get time
try :
	import ntptime
	ntptime.host = cfg['ntpServer']
	ntptime.settime()
except:
	print("ntp update failed")

# NodeMCU label to ESP8266 pin number:
# l2p = {"D0":16,"D1":5,"D2":4,"D3":0,"D4":2,"D5":14,"D6":12,"D7":13,"D8":15,"D9":3,"D10":1}

# make sure that all pins are really low
# don't touch WAKE pin due to weird results (it might reset)
from machine import Pin
pins = [Pin(i, Pin.OUT) for i in [5,4,0,2,14,12,13,15,3,1]] 
offs = [p.off() for p in pins]

import webrepl
webrepl.start()

import gc
gc.collect()
