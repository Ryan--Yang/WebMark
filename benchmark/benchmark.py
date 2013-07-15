import os
from selenium.webdriver.support.wait import WebDriverWait
import sys
import time
from common.util import LOGGER
from common.util import PROJECT_PATH

class Benchmark(object):
    poll_frequency = 90
    def __init__(self, driver, browser, case):
        self.driver = driver
        self.browser = browser
        self.case = case
        self.case.metric = self.CONFIG['metric']

        config_path = self.CONFIG['path']
        if case.path == 'external':
            self.path = config_path['external']
        elif case.path == 'internal':
            self.path = 'file:///' + PROJECT_PATH + 'third_party/WebBench/' + config_path['internal']
        else:
            self.path = self.case.path

        run_times = self.case.run_times
        for i in range(run_times):
            self._start()
            self.config()
            WebDriverWait(self.driver, self.case.timeout, self.poll_frequency).until(self.has_finished)
            self.case.add_result(round(self.get_result(), 2))
        self.case.log_result()

    def _start(self):
        LOGGER.info('start')
        self.driver.maximize_window()
        self.driver.get(self.path)
        WebDriverWait(self.driver, self.case.timeout, self.poll_frequency).until(self.has_started)

    def has_started(self, driver):
        return True

    def config(self):
        pass

    def has_finished(self, driver):
        time.sleep(3)
        return True

    def get_result(self):
        return 0.0