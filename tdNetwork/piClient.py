#!/usr/bin/env python3
import socket
import pickle

# Client to connect to TouchDesigner. This runs on the Pi side.
# NOTE: Make sure pyServer is running in TouchDeisgner before
# starting this script!

# class being named tdClient is confusing but I'm lazy!!!!!

class tdClient:
    # client to send data to touchdesigner via tcp/ip

    # default_hostname = 'localhost'
    default_hostname = '10.0.0.4'
    default_port = 7000

    # initialize client. connects to given hostname and port upon init
    def __init__(self, hostname = default_hostname, port = default_port):
        self.hostname = hostname
        self.port = port

    # return 1 if ok, 0 if bad -> use call in if statement
    def initialize(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.s.connect((hostname, port))
        except (BlockingIOError, InterruptedError):
            return 0
        confirm_msg = self.s.recv(1024)
        print("confirmation: " + str(confirm_msg.decode("utf-8")))
        print("Client is connected to TouchDesigner!")
        return 1

    # lazy method for sending data
    def sendData(self, data):
        data_encode = pickle.dumps(data)
        self.s.send(data_encode)
