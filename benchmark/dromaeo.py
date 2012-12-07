import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class Dromaeo(Benchmark):
    _SUITES = {
        "all javascript tests" : "%s?dromaeo|sunspider|v8",
        "all dom tests" : "%s?dom|jslib|cssquery"
    }
    def __init__(self, driver, logf, appmode=False, offline=False, suite = 'All JavaScript Tests'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'All JavaScript Tests', 'All DOM Tests'." % suite)
        Benchmark.__init__(self, driver, logf, appmode, offline)

    @property
    def name(self):
        return "Dromaeo(%s%s)" % (self.name_common_ext(True), self.suite)

    @property
    def metric(self):
        return "runs/second"

    @property
    def _url(self):
        if self.offline:
            path = self.webbench_path + "dromaeo/index.html"
            return self._SUITES[self.suite.lower()] % path
        return self._SUITES[self.suite.lower()] % "http://dromaeo.com/"      

    def run(self):
        self.open(self._url)
        time.sleep(60)

        pause = self.driver.find_element_by_id("pause")
        wait.WebDriverWait(self.driver, 600, 30).until(lambda x: pause.get_attribute("value") == "Run")
        pause.click()

        elem = self.driver.find_element_by_id("timebar")
        wait.WebDriverWait(self.driver, 1800, 60).until(lambda x: elem.text.find("Total") != -1)

        str = elem.text
        pos1 = str.find(":") + 1
        pos2 = str.find("runs/s")
        str = str[pos1:pos2].strip()
        return float(str)