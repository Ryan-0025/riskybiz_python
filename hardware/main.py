from machine import Pin
from time import sleep

button = Pin(14, Pin.IN, Pin.PULL_UP)

was_pressed = False

while True:
    if button.value() == 0 and not was_pressed:
        # Button just pressed
        was_pressed = True
    elif button.value() == 1 and was_pressed:
        # Button was released after being pressed
        print("1")
        was_pressed = False
        sleep(0.05)  # Debounce after a full press
    
    sleep(0.01)  # Avoid busy loop