import sys
import signal
import queue
import requests
import threading
import time
from bs4 import BeautifulSoup

# directories, please replace it with your directories
results_directory = r'D:\Program\GitHub\Nice_Spider\results'
pics_directory = r'D:\Program\GitHub\Nice_Spider\pics'

# fake header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'} 

# sources：图片页链接， pics：图片链接

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
			self.f_sources.write(source + '\r\n')

		for pic in self.pics:
			self.f_pics.write(pic + '\r\n')

		self.f_sources.close()
		self.f_pics.close()



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