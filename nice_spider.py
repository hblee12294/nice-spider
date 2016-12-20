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
		self.f_sources = open(results_directory + '\sources.txt', 'a+')
		self.f_pics = open(pics_directory + '\pics.txt', 'a+')

	def download(self):
		res = requests.get(self.original_url, headers = headers)
		soup = BeautifulSoup(res.text, 'html.parser')
		blocks = soup.find_all("li", attrs={'class': 'loading-block'})

		for block in blocks:
			self.sources.append(block.a['href'].strip())
			self.pics.append(block.img['src'].strip())

	def save(self):
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


	def download(self, url):


	def run(self):




def main():

	if len(sys.argv) < 2:
		print('Usage: python nice_spider.py url')
		sys.is_exit
	url = sys.argv[1]

	nice = Nice(url)
	nice.download()
	nice.save()


if __name__ == '__main__':
	main()