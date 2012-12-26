import time
from benchmark import Benchmark

class RShadow(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "RShadow"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/rshadow/rshadow.html"

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