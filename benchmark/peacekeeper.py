import time
from selenium.webdriver.support import wait
from common.exceptions import WebMarkException
from benchmark import Benchmark

class Peacekeeper(Benchmark):
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "Peacekeeper"

    @property
    def metric(self):
        return "score"

    def _chk_finished(self, driver):
        href = driver.current_url.lower()
        if href.find("results") != -1 or href.find("error") != -1 :
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