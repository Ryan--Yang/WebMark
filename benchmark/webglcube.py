import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class WebGLCube(Benchmark):
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "WebGLCube"

    @property
    def metric(self):
        return "fps"
        
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/webGL/webglcube/webgl_Cube.html")
        time.sleep(300)	

        elem = self.driver.find_element_by_id("FPS")
        str = elem.text
        start = str.find(":") + 1	
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)	