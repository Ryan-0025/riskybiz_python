from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT) 
button = Pin(14, Pin.IN, Pin.PULL_UP)

led_state = False
prev_button_state = 1


while True:
    button_state = button.value()


    if prev_button_state == 1 and button_state == 0:
        led_state = not led_state
        led.value(led_state)
        sleep(0.05)


    prev_button_state = button_state
    sleep(0.01)
    