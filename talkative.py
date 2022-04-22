#!/usr/bin/env python3

from talkative_spaces.piControl.volControlTest import translate_inverse
from tdNetwork.piClient import *
from piControl.radioTx import *
import piControl.audioControl as AC
from time import sleep
from gpiozero import DistanceSensor
# from pdControl import *
import board 
import alsaaudio # for mixer control
from playsound import playsound # to play audio files easily

# main file: everything is run from here

# radio tx doesn't need loop -> no threading
# only getting distance, updating variables, sending over client
# (socket doesn't need loop either)

# TODO
# * basic structure
#   * get distance, create delta, figure out constants / vars / etc
#   * determine how to format when sending over tcp/ip to touch
# * integrate pure data

# NOTE
# * pretty sure numpy columns can be addressed by 'name'
#   -> format:
#       dist | delta | output volume
#        x   |   y   |     z
#   hopefully can just use Table DAT -> select using column name
# * this file should tie all modules together + contain system-level config
# * worry about volume, etc. once know how puredata will work


# ***** CONFIG VARS / CONSTANTS *****
# radio config
radio_freq = 91000   # 91.000 mhz
radio_pin = board.D5 # pi digital pin 5
radio_power = 115 # dBuV

# GPIO pins used on rpi (unverified)
dist_echo_pin = 22
dist_trig_pin = 27
poll_delay = 0.1   # delay between dist sensor polls

# network config (unverified)
server_hostname = 'TAN-LAP'
server_port = 7000

# misc constants
dist_min = 2
dist_max = 60
vol_min = 10
vol_max = 100
audio_fn = "media/abom.mp3"
# ************************

# ***** DEBUG/SYSTEM VARS *****
en_server = False
first_loop = True
prev_dist = None
cur_dist = None
delta_dist = None
audio_control = None
base_volume = 0
volume_multiplier = 0
output_volume = 0
# ************************


# distance in cm
def getDistance(dist_sensor):
    return dist_sensor.distance * 100



# ***** START *****
print("0")
if __name__ == "__main__":

    # init distance sensor
    dist_sensor = DistanceSensor(echo=22, trigger=27, max_distance=4)
    print("2")
    # init server
    if (en_server):
        client = tdClient(server_hostname, server_port)
        if (not client.initialize()):
            print("TCP client failed to connect")
            quit()

    # init radio
    print("3")
    pi_radio = radioInit(radio_freq, radio_pin, radio_power)
    print("getting radio status")
    getRadioStatus(pi_radio)
    print("4")

    # init audio
    mixer = alsaaudio.Mixer()
    playsound(audio_fn)

    # init system variables
    cur_dist = getDistance(dist_sensor)
    first = True
    loop = 1

    sleep(poll_delay)
    # start main loop
    while(True):
        print("loop: " + str(loop))
        if (first):
            # init distance variable stuff
            first = False
            prev_dist = cur_dist
            cur_dist = getDistance(dist_sensor)
            delta_dist = 0
            audio_control = AC.AudioControl()
            sleep(poll_delay)
        
        # check and update movement state
        cur_dist = getDistance(dist_sensor)
        audio_control.updateDistState(cur_dist)

        # update output volume:
        #  base_volume is controlled by position
        #  volume_multiplier is controlled by movement
        #  output_volume is the final output to our radio
        base_volume = int(translate_inverse(cur_dist, dist_min, dist_max, vol_min, vol_max))
        volume_multiplier = audio_control.getAudioUpdate();
        output_volume = base_volume * volume_multiplier;
        mixer
        
        sleep(poll_delay)




