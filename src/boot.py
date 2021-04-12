def joinAP(SSID, PWD):
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.active(True)
        wlan.connect(SSID, PWD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
#
def exitAP():
	import network
	wlan = network.WLAN(network.STA_IF)
	wlan.active(False)
# 
def startAP(SSID, PWD):
	import network
	ap = network.WLAN(network.AP_IF)
	ap.active(True)
	ap.config(essid=SSID, password=PWD)
#
def stopAP():
	import network
	ap = network.WLAN(network.AP_IF)
	ap.active(False)
#

joinAP('WiFi AP', 'WiFi Password')

try :
	import ntptime
	ntptime.host = "1.europe.pool.ntp.org"
	ntptime.settime()
except:
	print("ntp update failed")

# make an array of available pins
from machine import Pin
def getPins(pins) :
	res = []
	for p in pins :
		res.append( Pin(p, Pin.OUT) )
	return res
#
# NodeMCU label to ESP8266 pin number
gpioL2P = {
	# "D0":16 # don't touch WAKE pin
	"D1":5
	,"D2":4
	,"D3":0
	,"D4":2
	,"D5":14
	,"D6":12
	,"D7":13
	,"D8":15
	,"D9":3
	,"D10":1
}
gpioPins = getPins( list( gpioL2P.values() ) )
for p in gpioPins :
	p.off()
#
# my sensor pins are D5:14,D6:12,D7:13

import webrepl
webrepl.start()

import gc
gc.collect()
