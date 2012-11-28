import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class GUIMark2VectorChart(Benchmark):
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "GUIMark2VectorChart"

    @property
    def metric(self):
        return "fps"
        
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/vectorchart/guimark2vectorchart.html")
        time.sleep(5)	

        elem = self.driver.find_element_by_tag_name("input")
        elem.click()		
        time.sleep(300)
        elem = self.driver.find_element_by_id("results")
        str = elem.text
        start = str.find(":") + 1
        end = str.find("fps")		
        str = str[start:end].strip()
        print str
        fps = float(str)
        return round(fps, 2)	