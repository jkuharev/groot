# groot
Groot is a plant. Plants need water.
In this project, I have implemented an IOT hard- and software solution that allows me to monitor soil moisture on multiple plants.

## Logics
### Short version
A series of resistive soil moisture sensors report values to ESP8266. ESP reports to a MQTT server periodically.

### Long version
**Wiring**: 
Series of resistive moisture sensors connected to the common ground of ESP but get powered on-demand by different ESP pins.
They report values muxed via diodes to the ADC pin.

**Soft-Logics**:

- boot.py
  - connect to an existing Wifi-AP
  - get current time from NTP
  - set all IO pins to low
  - start webrepl
  - turn on garbage collection
- main.py
  - create unique board identifier
  - create MQTT client
  - define ADC and sensor power pins
  - connect to MQTT server
  - read deep sleep time from MQTT
  - read ADC control value having all pins off
  - publish control value to MQTT
  - for each sensor
    - switch pin on
    - read ADC
    - publish value to MQTT
  - publish default deep sleep time if deep sleep time was 0
  - disconnect from MQTT server
  - fall into deep sleep in case the deep sleep time is more than 0
    -  otherwise we just stay on for WEBREPL
- cfg.py
  - configure all your inputs here
    - wifi connection details
    - NTP server
    - default sleep time
    - MQTT server details
    - sensor pins  

## Hardware
ESP8266, resistive moisture sensors, diodes, resistor, wires, connectors

## Software
Micropython, Wifi connection, multimuxed ADC sensor read, MQTT

## References

- Micropython Firmware: [https://micropython.org/download/esp8266/]
- MQTT Client: [https://github.com/micropython/micropython-lib/tree/master/umqtt.simple]

