import machine
import utime
from umqtt.simple import MQTTClient

# MQTT Configuration
mqtt_broker = "YOUR_BROKER_IP"
mqtt_topic = "pico2/control"

# Sound Sensor Configuration
sound_pin = machine.Pin(0, machine.Pin.IN)

# RGB LED Configuration
red_pin = machine.Pin(1, machine.Pin.OUT)
green_pin = machine.Pin(2, machine.Pin.OUT)
blue_pin = machine.Pin(3, machine.Pin.OUT)

# Push Button Configuration
button_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

# Buzzer Configuration
buzzer_pin = machine.Pin(5, machine.Pin.OUT)

# MQTT Setup
client = MQTTClient("pico2", mqtt_broker)

def sound_level():
    return sound_pin.value()

def control_rgb(color):
    red_pin.off()
    green_pin.off()
    blue_pin.off()

    if color == "red":
        red_pin.on()
    elif color == "green":
        green_pin.on()
    elif color == "blue":
        blue_pin.on()

def button_pressed():
    return not button_pin.value()

def main_loop():
    while True:
        level = sound_level()
        print("Sound Level:", level)
        client.publish(mqtt_topic, str(level))

        if button_pressed():
            print("Button Pressed")
            control_rgb("red")
            buzzer_pin.on()
        else:
            control_rgb("green")
            buzzer_pin.off()

        utime.sleep(0.1)

try:
    client.connect()
    print("Connected to MQTT broker")
    main_loop()
finally:
    client.disconnect()
    print("Disconnected from MQTT broker")
