# -*- coding: utf-8 -*-
from flask import Flask
import datetime
from config import config
import socket
import struct
from traceback import print_exc
import threading
import time

app = Flask(__name__)
state = 1
@app.route('/')
def index():
	return str(datetime.datetime.now())

@app.route("/getState")
def getState():
	return str(state)

@app.route("/setState/<int:value>")
def setState(value=None):
	global state
	state = value
	return str(state)

DEFAULT_PORT = 7
def send_magic_packet(addr):
   # create socket
   with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
       s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
       # parse address
       mac_ = addr.upper().replace("-", "").replace(":", "")
       if len(mac_) != 12:
           raise Exception("invalid MAC address format: {}".format(addr))
       buf_ = b'f' * 12 + (mac_ * 20).encode()
       # encode to magic packet payload
       magicp = b''
       for i in range(0, len(buf_), 2):
           magicp += struct.pack('B', int(buf_[i:i + 2], 16))

       # send magic packet
       print("sending magic packet for: {}".format(addr))
       s.sendto(magicp, ('<broadcast>', DEFAULT_PORT))

def deamon():
	while True:
		if state == 2:
			print("send_magic_packet")
			try:
				send_magic_packet(config.mac)
			except:
				print_exc()
		time.sleep(config.minterval)

if __name__ == "__main__":
	d = threading.Thread(target=deamon)
	d.start()
	app.run(debug=config.debug,host=config.host,port=config.port)