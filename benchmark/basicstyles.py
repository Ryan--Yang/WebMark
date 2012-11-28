import time
from selenium.webdriver.support import wait
from benchmark import Benchmark
from common.exceptions import WebMarkException

class BasicStyles(Benchmark):
    _SUITES = {
        "text" : "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/attrChange/text.html",
        "list" : "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/attrChange/list.html",
        "table" : "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/attrChange/table.html"
    }

    def __init__(self, driver, logf, suite = 'text'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'text', 'list', 'table'." % suite)
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "BasicStyles %s" % self.suite

    @property
    def metric(self):
        return "fps"

    @property
    def _url(self):
        return self._SUITES[self.suite.lower()]        

    def run(self):
        self.open(self._url)
        time.sleep(300)
        elem = self.driver.find_element_by_id("FPS")
        str = elem.text
        start = str.find(":") + 1
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)	