import sys
import signal
import queue
import requests
import threading
import time
from bs4 import BeautifulSoup

mutex = threading.Lock()
is_exit = False

class Nice(threading.Tread)
	
	def __init__(self, queue):
		self.user_queue = queue
		self.total_user = []
		self.total_url = []
		self.f_user = open(user.txt, 'a+')
		self.f_source - open(user.source, 'a+')