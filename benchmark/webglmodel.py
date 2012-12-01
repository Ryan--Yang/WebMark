import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class WebGLModel(Benchmark):
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "WebGLModel"

    @property
    def metric(self):
        return "fps"
        
    def run(self):
        if self.driver.name.find("internet explorer") !=-1:
            return 0

        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/webGL/webglmodel/webgl_Model.html")
        time.sleep(300)	

        elem = self.driver.find_element_by_id("FPS")
        str = elem.text
        start = str.find(":") + 1	
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)	