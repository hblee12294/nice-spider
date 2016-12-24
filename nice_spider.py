import sys
import signal
import queue
import requests
import threading
import time
from bs4 import BeautifulSoup


# Base directories, replace them with your own directories
results_directory = r'D:\Program\GitHub\Nice_Spider\results'
pics_directory = r'D:\Program\GitHub\Nice_Spider\pics'

# Fake header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'} 

# Nice url
base_url = r'www.oneniceapp.com'

# Thread communication settings
mutex = threading.Lock()
is_exit = False

user_url_queue = queue.Queue()



# Obtain pictures and sources from tag page
# sources：图片页链接  pics：图片链接
class Nice(object):
	
	def __init__(self, url):
		self.original_url = url
		self.sources = []
		self.pics = []
		self.f_sources = open(results_directory + r'\sources.txt', 'a+')
		self.f_pics = open(pics_directory + r'\pics.txt', 'a+')

	def download(self):
		res = requests.get(self.original_url, headers = headers)
		soup = BeautifulSoup(res.text, 'html.parser')
		blocks = soup.find_all("li", attrs={'class': 'loading-block'})

		for block in blocks:
			self.sources.append(block.a['href'].strip())
			self.pics.append(block.img['src'].strip())

	def save(self):
		global user_url_queue
		for source in self.sources:
			user_url_queue.push(source)

		# just for test, meanningless
		for source in self.sources:
			self.f_sources.write(source + '\r\n')

		for pic in self.pics:
			self.f_pics.write(pic + '\r\n')

		self.f_sources.close()
		self.f_pics.close()



# Get user info and download images from homepage
# 
class Page_Downloader(threading.Thread):

	def __init__(self, queue):
		threading.Thread.__int__(self)
		self.user_queue = queue
		self.total_users = []
		self.f_users = open(results_directory + r'\users.txt', 'a+')

	def download(self, url):
		res = requests.get(url)
		soup = BeautifulSoup(res.text)



	def run(self):
		global is_exit
		while not is_exit:
			user = self.user_url_queue.get()
			url = base_url + user
			





def handler(signum, frame):
	global is_exit
	is_exit = True
	print('Receive a signal %d, is_exit = %d' % (signum, is_exit))
	sys.exit(0)


def main():

	if len(sys.argv) < 2:
		print('Usage: python nice_spider.py url')
		sys.is_exit
	url = sys.argv[1]

	nice = Nice(url)
	nice.download()
	nice.save()

	signal.signal(signal.SIGINT, handler)
	signal.signal(signal.SIGTERM, handler)

	threads = []
	NUM_WORKERS = 5
	for i in range(NUM_WORKERS):
		downloader = Page_Downloader(user_url_queue)
		downloader.setDaemon(True)
		downloader.start()
		threads.append(downloader)

	while True:
		for thread in threads:
			if not thread.isAlive():
				break
			time.sleep(1)


if __name__ == '__main__':
	main()