import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class Octane(Benchmark):
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "Octane"

    @property
    def metric(self):
        return "score"
        
    def run(self):
        self.open("http://octane-benchmark.googlecode.com/svn/latest/index.html")
        time.sleep(1)
        self.driver.find_element_by_id("run-octane").click()
        elem = self.driver.find_element_by_id("main-banner")
        time.sleep(90)
        wait.WebDriverWait(self.driver, 1200, 30).until(lambda x: elem.text.find("Score:") != -1)
        str = elem.text
        pos = str.find(":") + 1
        str = str[pos:].strip()
        return int(str)