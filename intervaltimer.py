import threading
import time


class IntervalTimer:
	def __init__(self, interval, callback, *args, **kwargs):
		"""
		:param interval: Interval in seconds
		:param callback:
		"""
		self.m_timer = None  # Reference to the current Timer
		self.m_interval = interval
		self.m_callback = callback
		self.m_isRunning = False
		self.m_args = args
		self.m_kwargs = kwargs

	def setInterval(self, interval):
		self.m_interval = interval

	def setCallback(self, callback):
		self.m_callback = callback

	def step(self):
		self.m_isRunning = False
		self.m_callback(*self.m_args, **self.m_kwargs)
		self.start()  # Program next step

	def start(self):
		if not self.m_isRunning:  # If not already running
			self.m_timer = threading.Timer(self.m_interval, self.step)
			# self.m_timer.daemon = True
			self.m_timer.start()
			self.m_isRunning = True

	def stop(self):
		if self.m_timer is not None:
			self.m_timer.cancel()
		self.m_timer = None
		self.m_isRunning = False


if __name__ == '__main__':
	def clbk():
		print('step')
	timer = IntervalTimer(3, clbk)
	timer.start()
	print('Letting it run for 20s...')
	time.sleep(20)
	print('Waiting is over, kill the timer')
	timer.stop()
