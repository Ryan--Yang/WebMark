import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class CrazyCube(Benchmark):
    _SUITES = {
        "transform" : "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/crazycube/crazycube.html",
        "transition" : "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/crazycube/crazycube.html",
        "animation" : "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/crazycube/crazycube.html"
    }

    def __init__(self, driver, logf, appmode=False, suite = 'transform'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'transform', 'transition', 'animation'." % suite)
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "CrazyCube %s%s" % (self.suite, self.name_common_ext())

    @property
    def metric(self):
        return "fps"

    @property
    def _url(self):
        return self._SUITES[self.suite.lower()]        

    def run(self):
        self.open(self._url)
        time.sleep(5)		
        ratio = self.driver.find_element_by_id(self.suite.lower())
        ratio.click()		
        time.sleep(300)
        elem = self.driver.find_element_by_id("FPS")
        str = elem.text
        start = str.find(":") + 1
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)	