import machine
import utime
from umqtt.simple import MQTTClient

# MQTT Configuration
mqtt_broker = "YOUR_BROKER_IP"
mqtt_topic = "pico1/ultrasonic"

# Ultrasonic Sensor Configuration
trigger_pin = machine.Pin(0, machine.Pin.OUT)
echo_pin = machine.Pin(1, machine.Pin.IN)

# Push Button Configuration
button_pin = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

# Buzzer Configuration
buzzer_pin = machine.Pin(3, machine.Pin.OUT)

# LED Configuration
led_pin = machine.Pin(4, machine.Pin.OUT)

# MQTT Setup
client = MQTTClient("pico1", mqtt_broker)

def ultrasonic_distance():
    trigger_pin.on()
    utime.sleep_us(10)
    trigger_pin.off()

    while not echo_pin.value():
        pass
    start_time = utime    .ticks_us()

    while echo_pin.value():
        pass
    end_time = utime.ticks_us()

    duration = utime.ticks_diff(end_time, start_time)
    distance = duration / 58  # Calculate distance in centimeters

    return distance

def publish_distance(distance):
    client.publish(mqtt_topic, str(distance))

def button_pressed():
    return not button_pin.value()

def main_loop():
    while True:
        distance = ultrasonic_distance()
        print("Distance:", distance, "cm")
        publish_distance(distance)

        if button_pressed():
            print("Button Pressed")
            led_pin.on()
            buzzer_pin.on()
        else:
            led_pin.off()
            buzzer_pin.off()

        utime.sleep(0.1)

try:
    client.connect()
    print("Connected to MQTT broker")
    main_loop()
finally:
    client.disconnect()
    print("Disconnected from MQTT broker")


