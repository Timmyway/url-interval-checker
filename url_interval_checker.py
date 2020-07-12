import requests
from timeit import timeit
import time
import logging
from datetime import datetime
from threading import Thread

class Interval(object):
	"""docstring for Interval"""
	def __init__(self, action, try_counter=3):
		super(Interval, self).__init__()		
		self.action = action
		self.try_counter = try_counter

	def run(self):		
		self.action()		

	def run_inside_thread(self):
		print('Start running thread')
		threads = [Thread(target=self.run) for i in range(self.try_counter)]
		for t in threads:
			t.start()
					


class URLChecker(object):
	"""docstring for URLChecker"""
	def __init__(self, href, src=None):
		super(URLChecker, self).__init__()
		self.href = href
		self.src = src
		self.logger = logging
		self.critical_time = 30
		self.logger.basicConfig(filename='checker-log.log', level=logging.DEBUG)

	def basicConfig(self, critical_time=30, href=None, src=None):
		self.critical_time = critical_time
		if href:
			self.href = href
		if src:
			self.src = src
		
	def check(self, what='href'):
		start = timeit()
		try:
			if what == 'href':
				url_to_check = self.href
			else:
				url_to_check = self.src
			r = requests.get(url_to_check, allow_redirects=False)
			self.logger.info(f'Logging time: {self.getNow()}')
			self.logger.debug(f'Elapsed time by requests module: {r.elapsed}')
			elapsed_time = timeit() - start
			self.logger.info(f'Status code: {r.status_code} | Elapsed time: {elapsed_time}\n\n')
		except Exception as e:
			self.logger.warning(e)
		if elapsed_time > self.critical_time:
			self.logger.warning(f'CRITICAL: page loading time has exceeded 30 seconds')

	@staticmethod
	def getNow():
		now = datetime.now()		
		return now.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
	checker = URLChecker('https://rl.lagendadesventesprivees.eu?h=ed6a836cbea00f14f2a0ba81bf71cd75',
		'https://image.lagendadesventesprivees.eu/pf2E2Zr1kc/6xPa5rGY.png'
	)
	timing = 60 * 30
	counter = 0
	max_counter = 40
	interval_href = Interval(lambda: checker.check('href'))
	interval_src = Interval(lambda: checker.check('src'))
	while counter < max_counter or datetime.now() > datetime(2020, 7, 13, 8, 0):
		print('I am awake...work now...')
		interval_href.run_inside_thread()
		interval_src.run_inside_thread()
		print('I am going to sleep...')
		time.sleep(timing)
		counter += 1