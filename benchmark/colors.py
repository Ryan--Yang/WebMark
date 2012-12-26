import time
from benchmark import Benchmark

class Colors(Benchmark):
    RESULT_LEN = 'return result.length'
    RESULT = 'return result[1][1]'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Colors"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/colors/colors.html"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 30

    def chk_finish(self, driver):
        return driver.execute_script(self.RESULT_LEN) == 2

    def get_result(self, driver):
        str = driver.execute_script(self.RESULT)
        start = str.find(":") + 1	
        end = str.find("fps")	
        str = str[start:end].strip()		
        print str
        fps = float(str)
        return round(fps, 2)	