import time
from benchmark import Benchmark

class GUIMark2VectorChart(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "GUIMark2VectorChart"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/vectorchart/guimark2vectorchart.html"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 0

    def start(self, driver):
        time.sleep(5)	
        driver.find_element_by_tag_name("input").click()		
        time.sleep(300)

    def get_result(self, driver):
        elem = self.driver.find_element_by_id("results")
        str = elem.text
        start = str.find(":") + 1
        end = str.find("fps")		
        str = str[start:end].strip()
        print str
        fps = float(str)
        return round(fps, 2)	