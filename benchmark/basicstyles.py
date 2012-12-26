import time
from common.exceptions import WebMarkException
from benchmark import Benchmark

class BasicStyles(Benchmark):
    _SUITES = {
        "text" : "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/attrChange/text.html",
        "list" : "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/attrChange/list.html",
        "table" : "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/attrChange/table.html"
    }

    def __init__(self, suite = 'text'):
        if self._SUITES.has_key(suite.lower()):
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'text', 'list', 'table'." % suite)
        Benchmark.__init__(self)

    @property
    def name(self):
        return "BasicStyles %s" % self.suite

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return self._SUITES[self.suite.lower()]      

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 120

    def get_result(self, driver):
        str = driver.find_element_by_id("FPS").text
        start = str.find(":") + 1
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)	