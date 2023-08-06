import time
from threading import Thread, Event
from pyformance.registry import global_registry


class Reporter(object):

    def __init__(self, registry=None, reporting_interval=30, clock=None):
        self.registry = registry or global_registry()
        self.reporting_interval = reporting_interval
        self.clock = clock or time
        self._stopped = Event()
        self._loop_thread = Thread(target=self._loop)
        self._loop_thread.setDaemon(True)

    def start(self):
        if not self.is_running():
            self._loop_thread.start()
            return True
        return False

    def stop(self):
        self._stopped.set()

    def is_running(self):
        return self._stopped.is_set()

    def _loop(self):
        while not self._stopped.is_set():
            self.report_now(self.registry)
            time.sleep(self.reporting_interval)
        # self._stopped.clear()

    def report_now(self, registry=None, timestamp=None):
        raise NotImplementedError(self.report_now)
