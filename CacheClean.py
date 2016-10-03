#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from operator import itemgetter

import os
import time
import math
import LogMaster
import datetime
import Queue
import ConfigParser
import copy

from threading import Thread, Event, Lock
from multiprocessing import Process

__author__ = "Yiğit Can BAŞALMA"
__license__ = "GPL"
__version__ = "2.0"
__email__ = "yigit.basalma@gmail.com"

total = 0
real_list = []

class Cleaner(object):
        def __init__(self, path, max_size, min_size):
		global total, real_list
                self.logger = LogMaster.Logger()
                self.tmp_list = Queue.Queue()
                self.real_list = real_list
                self.total = total
		self.controller_list = [i[0] for i in self.real_list]
                self.start_time = time.time()
                self.path = path
                self.min_size = min_size
                self.max_size = max_size
                self.lock = Lock()
	
        def Consumer(self, path):
                try:
                        for i in os.listdir(path):
                                if os.path.isfile(os.path.join(path, i))\
				and os.path.join(path, i) not in self.controller_list:
                                        size = os.path.getsize(os.path.join(path, i))
                                        s = math.ceil((size * 4) / 1024) if size <= 1024 else math.ceil(size / 1024)
                                        self.real_list.append((os.path.join(path, i), \
						size, os.stat(os.path.join(path, i)).st_ctime))
                                        self.total += s
                except OSError:
                        pass

        def Producer(self):
                while True:
                        self.lock.acquire()
                        self.Consumer(self.tmp_list.get())
                        self.lock.release()
                        self.tmp_list.task_done()

        def FoundAndCollect(self):
                for i in range(100):
                        t = Thread(target=self.Producer)
                        t.daemon = True
                        t.start()
                [self.tmp_list.put("{0}/{1}/{2}".format(self.path, i, e)) for i in os.listdir(self.path) \
                        if os.path.isdir(os.path.join(self.path, i)) for e in os.listdir(os.path.join(self.path, i))]
                self.tmp_list.join()
                self.Destroyer()

        def Destroyer(self):
                ers_size = 0
                total, bulk = self.total, self.real_list
                if total >= self.max_size:
                        msg = "{0} KB cache klasörü toplam boyutu.Silme işlemi başlıyor.Hesaplama süresi {1:2f}".\
				format(total, time.time() - self.start_time)
                        self.logger.LogSave("Cache Admin","INFO",msg)
                        start = time.time()
                        sorted(bulk, key=lambda ctime: ctime[2], reverse=False)
                        while True:
                                if os.path.exists(bulk[-1][0]):
                                        os.unlink(bulk[-1][0])
                                        if bulk[-1][1] <= 1024:
                                                total -= math.ceil((bulk[-1][1] *4) / 1024)
                                                ers_size += math.ceil((bulk[-1][1] *4) / 1024)
                                        else:
                                                total -= math.ceil(bulk[-1][1] / 1024)
                                                ers_size += math.ceil(bulk[-1][1] / 1024)
                                        del bulk[-1]
                                if total < self.min_size:
                                        runtime = time.time() - start
                                        msg = "{0} KB cache silindi.Çalışma süresi {1:2f} S".format(ers_size,runtime)
                                        self.logger.LogSave("Cache Admin","INFO",msg)
                                        break
                else:
                        timer = time.time() - self.start_time
                        msg = "{0} KB cache klasörü toplam boyutu.Silme işlemi gerektirmiyor.\
Toplam hesaplama zamanı {1:2f}".format(total,timer)
                        self.logger.LogSave("Cache Admin","INFO",msg)

def caller(cache_path, m_size, mn_size):
	with open("pid", "a") as pid:
                pid.write("{0}\n".format(str(os.getpid())))
	a = Cleaner(cache_path, m_size, mn_size)
	a.FoundAndCollect()

def main():
	if os.path.exists("pid"):
		os.unlink("pid")
	with open("pid", "w") as pid:
                pid.write("{0}\n".format(str(os.getpid())))
	while True:
		config = ConfigParser.ConfigParser()
		config.read(os.path.join(os.getcwd(), "config.cfg"))
		cache_path, m_size, mn_size = config.get("env","cahce_path"), int(config.get("env","max_size")), int(config.get("env","min_size"))
		p = Process(target=caller, args=(cache_path, m_size, mn_size, ))
		p.start()
		p.join()
		with open("pid", "w") as pid:
                	pid.write("{0}\n".format(str(os.getpid())))
		time.sleep(float(config.get("env","delay_second")))

if __name__ == "__main__":
	main()
