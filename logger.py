"""
Logs events into files
"""

import os
import datetime
import atexit
from mss import mss
from PIL import Image
from intervaltimer import IntervalTimer


class Logger:
	def __init__(self, settings):
		self.m_settings = settings

		self.logStart()  # Log Start
		atexit.register(self.logClose)  # Log Close

		self.logScreen()

		self.m_intervalTimer = IntervalTimer(self.m_settings['screenshots_interval'], self.logScreen)
		self.m_intervalTimer.start()

	@staticmethod
	def now():
		return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	@staticmethod
	def year():
		return datetime.datetime.now().strftime('%Y')

	@staticmethod
	def month():
		return datetime.datetime.now().strftime('%m')

	@staticmethod
	def day():
		return datetime.datetime.now().strftime('%d')

	@staticmethod
	def time():
		return datetime.datetime.now().strftime('%H.%M.%S')

	def logStart(self):
		self.log("\n" + self.now() + ' -> ')

	def logClose(self):
		self.log(self.now())

	def logScreen(self):
		path = os.path.join(self.m_settings['log_path'], 'screenshots/')

		# Year folder
		path += self.year() + '/'
		if not os.path.isdir(path):
			os.mkdir(path)

		# Month folder
		path += self.month() + '/'
		if not os.path.isdir(path):
			os.mkdir(path)

		# Day folder
		path += self.day() + '/'
		if not os.path.isdir(path):
			os.mkdir(path)

		# Filename
		path += self.time() + '.jpg'

		with mss() as sct:
			monitor = sct.monitors[0]  # 0 = all-in-one monitors
			img = sct.grab(monitor)
			img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
			img.thumbnail((10000, self.m_settings['img_max_height']), Image.BICUBIC)
			img.save(path, 'JPEG', optimize=True, quality=self.m_settings['img_compression'])

	def log(self, message):
		with open(self.m_settings['log_path'] + '/log.txt', 'a') as f:
			f.write(message)
