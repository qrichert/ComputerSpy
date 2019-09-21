"""
Logs events into files
"""

import os
import datetime
import atexit
from mss import mss
from PIL import Image
import io
import requests
from intervaltimer import IntervalTimer


class Logger:
	def __init__(self, settings):
		self.m_settings = settings

		self.m_saveLocally = False

		if 'save_locally' in self.m_settings and self.m_settings['save_locally'] is True:
			self.m_saveLocally = True

			# Create log folders ('/log' and '/log/screenshots')
			os.makedirs(os.path.join(settings['log_path'], 'screenshots/'), exist_ok=True)

		self.m_httpPostToRemoteServer = False

		if 'http_post_to' in self.m_settings and self.m_settings['http_post_to']:
			self.m_httpPostToRemoteServer = True

		self.m_httpPostUsePassword = False

		if 'http_post_password' in self.m_settings and self.m_settings['http_post_password'] is not None:
			self.m_httpPostUsePassword = True

		self.m_httpPostUseInstance = False

		if 'http_post_instance' in self.m_settings and self.m_settings['http_post_instance'] is not None:
			self.m_httpPostUseInstance = True

		self.logStart()  # Log Start
		atexit.register(self.logClose)  # Log Close

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

	# I/O

	def writeStartClose(self, message):
		with open(self.m_settings['log_path'] + '/log.txt', 'a') as f:
			f.write(message)

	def postStartClose(self, log):
		postData = {}

		postData['log_start_close'] = log

		if self.m_httpPostUsePassword:
			postData['password'] = self.m_settings['http_post_password']

		if self.m_httpPostUseInstance:
			postData['instance'] = self.m_settings['http_post_instance']

		with requests.Session() as session:
			session.post(self.m_settings['http_post_to'], data=postData)

	def writeScreenshot(self, imgBuffer, fileName):
		path = os.path.join(self.m_settings['log_path'], 'screenshots/')

		# Create folders
		path += self.year() + '/' + self.month() + '/' + self.day() + '/'
		os.makedirs(path, exist_ok=True)

		path += fileName

		with open(path, 'wb') as f:
			f.write(imgBuffer.getvalue())

	def postScreenshot(self, imgBuffer, fileName):
		postData = {}

		if self.m_httpPostUsePassword:
			postData['password'] = self.m_settings['http_post_password']

		if self.m_httpPostUseInstance:
			postData['instance'] = self.m_settings['http_post_instance']

		postFiles = {}

		postFiles['screenshot'] = (
			fileName,
			imgBuffer.getvalue(),
			'image/jpeg'
		)

		with requests.Session() as session:
			session.post(self.m_settings['http_post_to'], data=postData, files=postFiles)

	# Logging

	def logStart(self):
		log = "\n" + self.now() + ' -> '  # Add \n here because if it doesn't close correctly, next would be on wrong line

		if self.m_saveLocally:
			self.writeStartClose(log)

		if self.m_httpPostToRemoteServer:
			self.postStartClose(log)

	def logClose(self):
		log = self.now()

		if self.m_saveLocally:
			self.writeStartClose(log)

		if self.m_httpPostToRemoteServer:
			self.postStartClose(log)

	def logScreen(self):
		# Filename
		fileName = self.time() + '.jpg'

		with mss() as sct:
			monitor = sct.monitors[0]  # 0 = all-in-one monitors
			img = sct.grab(monitor)
			img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
			img.thumbnail((10000, self.m_settings['img_max_height']), Image.BICUBIC)

			with io.BytesIO() as output:
				# Save into IO buffer
				img.save(output, 'JPEG', optimize=True, quality=self.m_settings['img_compression'])

				if self.m_saveLocally:
					self.writeScreenshot(output, fileName)

				if self.m_httpPostToRemoteServer:
					self.postScreenshot(output, fileName)
