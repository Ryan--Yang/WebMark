﻿import time
from selenium.webdriver.support import wait
from common.exceptions import WebMarkException
from benchmark import Benchmark

class Peacekeeper(Benchmark):
    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "Peacekeeper%s" % self.name_common_ext()

    @property
    def metric(self):
        return "score"

    @property
    def extra_chrome_args(self):
        return ['--always-authorize-plugins']

    def _chk_finished(self, driver):
        href = driver.current_url.lower()
        if href.find("results") != -1 or href.find("error") != -1:
            return href
        return None      

    def run(self):
        self.open("http://peacekeeper.futuremark.com/run.action")
        time.sleep(270)
        href = wait.WebDriverWait(self.driver, 600, 60).until(self._chk_finished)
        if href.find("results") != -1 :
            elem = self.driver.find_element_by_class_name("your-score")
            str = elem.text
            return int(str)
        else:
            raise WebMarkException(self.name + " : An error occured during your benchmark run.")