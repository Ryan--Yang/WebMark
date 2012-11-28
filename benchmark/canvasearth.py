import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class CanvasEarth(Benchmark):
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "CanvasEarth"

    @property
    def metric(self):
        return "fps"
        
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/canvasearth/canvas_earth.html")
        time.sleep(30)
        elem = self.driver.find_element_by_id("FPS")
        str = elem.text
        start = str.find(":") + 1
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)	