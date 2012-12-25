import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class Dromaeo(Benchmark):
    _SUITES = {
        "all javascript tests" : "%s?dromaeo|sunspider|v8",
        "all dom tests" : "%s?dom|jslib|cssquery"
    }
    def __init__(self, suite = 'All JavaScript Tests'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'All JavaScript Tests', 'All DOM Tests'." % suite)
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Dromaeo(%s)" % self.suite

    @property
    def metric(self):
        return "runs/second"

    @property
    def default_url(self):
        return self._SUITES[self.suite.lower()] % "http://dromaeo.com/"      

    @property
    def expect_time(self):
        return 600

    @property
    def default_timeout(self):
        return 1800

    def start(self, driver):
        pause = driver.find_element_by_id("pause")
        wait.WebDriverWait(driver, 120, 10).until(lambda x: pause.get_attribute("value") == "Run")
        pause.click()
        self.timebar = self.driver.find_element_by_id("timebar")

    def chk_finish(self, driver):
        return self.timebar.text.find("Total") != -1

    def get_result(self, driver):
        str = self.timebar.text
        pos1 = str.find(":") + 1
        pos2 = str.find("runs/s")
        str = str[pos1:pos2].strip()
        return float(str)
