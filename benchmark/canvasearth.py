import time
from benchmark import Benchmark

class CanvasEarth(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "CanvasEarth"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/canvasearth/canvas_earth.html"

    @property
    def default_timeout(self):
        return 360

    @property
    def expect_time(self):
        return 0

    def start(self, driver):
        time.sleep(300)

    def get_result(self, driver):
        elem = driver.find_element_by_id("FPS")
        str = elem.text
        start = str.find(":") + 1
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)	