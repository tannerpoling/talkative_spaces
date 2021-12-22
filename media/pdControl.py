#!/usr/bin/env python3

import os

# https://guitarextended.wordpress.com/2012/11/03/make-python-and-pure-data-communicate-on-the-raspberry-pi/

class pdController:

	def __init__():
		return 1

	def send2Pd(message=''):
		os.system("echo '" + message + "' | pdsend 3000")

	def playAudio():
		message = "0 1;" #ID = 0, message = 1 (hopefully generate bang!)
		send2Pd(message)

	def setVolume(vol=0):
		message = '1 ' + str(vol) + ';'
		send2Pd(message)