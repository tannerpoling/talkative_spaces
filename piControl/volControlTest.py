#!/usr/bin/env python3

import alsaaudio

# from piControl.distSensor import *
from email.mime import audio
from time import sleep
from gpiozero import DistanceSensor
# from playsound import playsound # to play audio files easily

import pygame

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # If value outside of range, apply ceiling
    if (value > leftMax): 
        value = leftMax
    if (value < leftMin):
        value = leftMin

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

audio_fn = "../media/abomunist.wav"
m = alsaaudio.Mixer()
# playsound(audio_fn)
# current_volume = m.getvolume()

pygame.mixer.init()
# pygame.mixer.music.load(audio_fn)
# pygame.mixer.music.play()
my_sound = pygame.mixer.Sound(audio_fn)
my_sound.play()
my_sound.set_volume(1.0)

while(1):
    print("Distance sensor read %.1f cm." % (dist_sensor.distance * 100))
    dist = dist_sensor.distance * 100
    new_volume = int(translate_inverse(dist, 15.0, 40.0, 0, 100))
    # pygame.mixer.music.set_volume(new_volume)
    my_sound.set_volume(new_volume)
    sleep(0.1)
    m.setvolume(new_volume)