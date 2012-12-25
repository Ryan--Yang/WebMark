import time
from common.exceptions import WebMarkException
from benchmark import Benchmark

class Peacekeeper(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Peacekeeper"

    @property
    def metric(self):
        return "score"

    @property
    def default_url(self):
        return "http://peacekeeper.futuremark.com/run.action"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 270

    def chk_finish(self, driver):
        href = driver.current_url.lower()
        return href.find("results") != -1 or href.find("error") != -1

    def get_result(self, driver):
        href = driver.current_url.lower()
        if href.find("results") != -1 :
            elem = self.driver.find_element_by_class_name("your-score")
            str = elem.text
            return int(str)
        else:
            raise WebMarkException(self.name + " : An error occured during your benchmark run.")
