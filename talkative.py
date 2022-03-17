#!/usr/bin/env python3

from tdNetwork.piClient import *


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


# ***** VARS *****
# delay between dist sensor polls
poll_delay = 0.5

# GPIO pins used on rpi (unverified)
dist_echo_pin = 22
dist_trig_pin = 27

# network config (unverified)
server_hostname = 'TAN-LAP'
server_port = 7000
# *****************





# ***** START *****

# init radio tx
# init distance sensor
# init server
client = tdClient(server_hostname, server_port)
if (not client.initialize()):
    print("TCP client failed to connect")
    quit()


