import time
from benchmark import Benchmark

class UniSelectors(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "UniSelectors"

    @property
    def metric(self):
        return "ms"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/uniselectors/uniselectors.html"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 60

    def chk_finish(self, driver):
        return driver.find_element_by_id("output").text !=""

    def get_result(self, driver):
        str = driver.find_element_by_id("output").text		
        start = str.find(":") + 1	
        end = str.find("ms")		
        str = str[start:end].strip()			
        print str
        res = float(str)
        return round(res, 2)