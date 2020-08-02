# -*- coding: utf-8 -*-

import time
import subprocess
import signal
import requests
import sys
from config import config
import os
import threading

class PM_Daemon:
	"""
	ifttt連携してPCの電源を管理するのが目的
	10秒おきにサーバーにリクエストの状態を問い合わせ、それに応じてスリープに入れる
	"""
	def __init__(self):
		self.delay = config.delay #十秒後にスリープに入るってこと
		requests.get(config.serverURL + "/setState/3")
	def sleeping(self):
		#スタンバイ状態にする
		time.sleep(self.delay)
		requests.get(config.serverURL + "/setState/1")
		Application.SetSuspendState(PowerState.Suspend, False, False)
	def daemon(self):
		while True:
			try:
				r = requests.get(config.serverURL + "/getState")
				print(r.text)
				if int(r.text) == 0 or int(r.text) == 1:
					self.sleeping()
				elif int(r.text) == 2:
					requests.get(config.serverURL + "/setState/3")
			except requests.ConnectionError:
				print("requests.ConnectionError")
			finally:
				time.sleep(config.interval)


if __name__ == "__main__":
	if len(sys.argv) >= 2 and (sys.argv[1] == "server" or sys.argv[1] == "debug"):
		server = subprocess.Popen(["python","module1.py"],shell=False)
	if len(sys.argv) < 2 or sys.argv[1] == "client" or sys.argv[1] == "debug":
		import clr
		clr.AddReference("System.Windows.Forms")
		from System.Windows.Forms import Application,PowerState
		d = PM_Daemon()
	try:
		if  len(sys.argv) >= 2 and sys.argv[1] == "server":
			while True:
				time.sleep(config.interval)
		else:
			d.daemon()
	finally:
		if  len(sys.argv) >= 2 and (sys.argv[1] == "server" or sys.argv[1] == "debug"):
			server.send_signal(signal.CTRL_C_EVENT)