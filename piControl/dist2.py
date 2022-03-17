import time
import board
import adafruit_hcsr04

# alternative distance sensor library from adafruit

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D27, echo_pin=board.D22)
while True:
    try:
        print(str(sonar.distance))
    except RuntimeError:
        print("retry")
    time.sleep(2)
