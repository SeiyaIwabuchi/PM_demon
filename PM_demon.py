# -*- coding: utf-8 -*-

import time
import subprocess
import signal
import threading
import requests
import sys

class PM_Daemon:
	"""
	ifttt連携してPCの電源を管理するのが目的
	10秒おきにサーバーにリクエストの状態を問い合わせ、それに応じてスリープに入れる
	"""
	def __init__(self):
		self.delay = 10 #十秒後にスリープに入るってこと
	def sleeping(self):
		#スタンバイ状態にする
		time.sleep(self.delay)
		requests.get("http://127.0.0.1:8080/setState/1")
		Application.SetSuspendState(PowerState.Suspend, False, False)
	def daemon(self):
		while True:
			try:
				r = requests.get("http://127.0.0.1:8080/getState")
				print(r.text)
				if int(r.text) == 0:
					self.sleeping()
				elif int(r.text) == 2:
					requests.get("http://127.0.0.1:8080/setState/3")
			except requests.ConnectionError:
				print("requests.ConnectionError")
			finally:
				time.sleep(10)


if __name__ == "__main__":
	if sys.argv[1] == "server" or sys.argv[1] == "debug":
		server = subprocess.Popen(["python","module1.py"],shell=True)
	if sys.argv[1] == "client" or sys.argv[1] == "debug":
		import clr
		clr.AddReference("System.Windows.Forms")
		from System.Windows.Forms import Application,PowerState
		d = PM_Daemon()
	try:
		if  sys.argv[1] == "server":
			while True:
				pass
		else:
			d.daemon()
	finally:
		if  sys.argv[1] == "server" or sys.argv[1] == "debug":
			server.send_signal(signal.CTRL_C_EVENT)