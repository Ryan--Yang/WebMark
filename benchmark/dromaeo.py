import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class Dromaeo(Benchmark):
    _SUITES = {
        "all javascript tests" : "http://dromaeo.com/?dromaeo|sunspider|v8",
        "all dom tests" : "http://dromaeo.com/?dom|jslib|cssquery"
    }
    def __init__(self, driver, logf, suite = 'All JavaScript Tests'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'All JavaScript Tests', 'All DOM Tests'." % suite)
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "Dromaeo(%s)" % self.suite

    @property
    def metric(self):
        return "runs/second"

    @property
    def _url(self):
        return self._SUITES[self.suite.lower()]        

    def run(self):
        self.open(self._url)
        pause = self.driver.find_element_by_id("pause")
        wait.WebDriverWait(self.driver, 60, 3).until(lambda x: pause.get_attribute("value") == "Run")
        pause.click()
        time.sleep(200)
        elem = self.driver.find_element_by_id("timebar")
        wait.WebDriverWait(self.driver, 1600, 120).until(lambda x: elem.text.find("Total") != -1)
        str = elem.text
        pos1 = str.find(":") + 1
        pos2 = str.find("runs/s")
        str = str[pos1:pos2].strip()
        return float(str)