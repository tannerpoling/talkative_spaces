#!/usr/bin/env python3

from time import sleep
from gpiozero import DistanceSensor
from pdControl import *

dist_sensor = DistanceSensor(echo=22, trigger=27, max_distance=4)

# pdcontrol = pdController()

print("Press CTRL-C to exit.\n")
pdcontrol.playAudio()
while True:
    print("Distance sensor read %.1f cm." % (dist_sensor.distance * 100))
    # pdcontrol.setVolume((dist_sensor.distance * 100 + 50) / 100)
    sleep(0.1)

    
