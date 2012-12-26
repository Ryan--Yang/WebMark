import time
from common.exceptions import WebMarkException
from benchmark import Benchmark

class CrazyCube(Benchmark):
    _SUITES = ("transform", "transition", "animation")

    def __init__(self, suite = 'transform'):
        if suite in self._SUITES:
            self.suite = suite
        else:
            raise WebMarkException("Unsupported suite %s, "
            "should be one of 'transform', 'transition', 'animation'." % suite)
            
        Benchmark.__init__(self)

    @property
    def name(self):
        return "CrazyCube %s" % self.suite

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/crazycube/crazycube.html"

    @property
    def default_timeout(self):
        return 600

    @property
    def expect_time(self):
        return 300
        
    def start(self, driver):
        time.sleep(5)	
        driver.find_element_by_id(self.suite.lower()).click()

    def get_result(self, driver):
        str = driver.find_element_by_id("FPS").text
        start = str.find(":") + 1
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)