import time


class Profiler(object):
    def __init__(self):
        self._startTime = time.time()

    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        self.res_time = time.time() - self._startTime
        print("Elapsed time: {:.3f} sec".format(self.res_time))

    def start(self):
        self._startTime = time.time()

    def get_time(self):
        return time.time() - self._startTime