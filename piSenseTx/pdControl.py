#!/usr/bin/env python3

import os

# https://guitarextended.wordpress.com/2012/11/03/make-python-and-pure-data-communicate-on-the-raspberry-pi/

class pdController:

    def __init__(self):
        print("init pd control!")

    def send2Pd(self, message=''):
        os.system("echo '" + message + "' | pdsend 3000")

    def playAudio(self):
        message = "0 1;" #ID = 0, message = 1 (hopefully generate bang!)
        self.send2Pd(message)

    def setVolume(self, vol=0):
        message = '1 ' + str(vol) + ';'
        self.send2Pd(message)
