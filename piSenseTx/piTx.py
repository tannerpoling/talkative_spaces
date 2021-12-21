#!/usr/bin/env python3

import time
import board
import digitalio
import adafruit_si4713

# SI4743 RDS FM transmitter

# ***** VARS *****
# Tx frequency in 50kHz steps
FREQUENCY_KHZ = 102300  # 102.300mhz

# *****************