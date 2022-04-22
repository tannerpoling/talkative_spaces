#!/usr/bin/env python3

import alsaaudio
# from piControl.distSensor import *
from time import sleep
from gpiozero import DistanceSensor
from playsound import playsound # to play audio files easily

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # If value outside of range, apply ceiling
    if (value > leftMax): 
    	value = leftMax

    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def translate_inverse(value, leftMin, leftMax, rightMin, rightMax):
    return rightMax - translate(value, leftMin, leftMax, rightMin, rightMax)

dist_sensor = DistanceSensor(echo=22, trigger=27, max_distance=4)

audio_fn = "../media/abom.mp3"
m = alsaaudio.Mixer()
playsound(audio_fn)
current_volume = m.getvolume()

while(1):
	print("Distance sensor read %.1f cm." % (dist_sensor.distance * 100))
	dist = dist_sensor.distance * 100
	new_volume = int(translate(dist, 2, 60, 10, 100))
	m.setvolume(new_volume)
	sleep(0.5)

