import sys
import time
import threading
import Queue
from exceptions import WebMarkException, WebMarkTimeoutException

class MyThread(threading.Thread):
    def __init__(self, target=None,
                 args=(), kwargs=None):
        threading.Thread.__init__(self, target=target, args=args, kwargs=kwargs) 
    def run(self):
        threading.Thread.run(self)

class Timeout(object): 
    def __init__(self, function, limit):
        """Initialize instance in preparation for being called."""
        if limit <= 0:
            raise ValueError()
        self.__limit = limit
        self.__function = function
        self.__process = None
        self.__queue = None

    def call(self, *args, **kwargs):
        self.__queue = Queue.Queue(1)
        args = (self.__queue, self.__function) + args
        self.__process = MyThread(target=self._target,
                                                 args=args,
                                                 kwargs=kwargs)
        self.__process.setDaemon(True)
        self.__process.start()
        self.__process.join(self.__limit)
        if self.__process.is_alive():
            raise WebMarkTimeoutException('Timeout')
        if self.__queue.empty():
            raise WebMarkException('Get result failed.')
        rs = self.__queue.get()
        if not rs[0]:
            raise WebMarkException(rs[1])
        return rs[1]

    def _target(self, queue, function, *args, **kwargs):
        try:
            queue.put((True, function(*args, **kwargs)))
        except:
            queue.put((False, sys.exc_info()[1])) 

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, value):
        if value <= 0:
            raise ValueError()
        self.__limit = value
