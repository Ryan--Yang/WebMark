import time
from benchmark import Benchmark

class SkewScale(Benchmark):
    RESULT_LEN = 'return result.length'
    RESULT = 'return result[1][1]'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "SkewScale"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/skewscale/skewscale.html"

    @property
    def default_timeout(self):
        return 600

    @property
    def expect_time(self):
        return 300

    def get_result(self, driver):
        str = driver.find_element_by_id("FPS").text
        start = str.find(":") + 1
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)	