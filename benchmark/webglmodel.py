import time
from common.exceptions import WebMarkException
from benchmark import Benchmark

class WebGLModel(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "WebGLModel"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/webGL/webglmodel/webgl_Model.html"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 300

    def start(self, driver):
        if driver.name.find("internet explorer") !=-1:
            raise WebMarkException("internet explorer does not support WebGLModel")

    def get_result(self, driver):
        elem = driver.find_element_by_id("FPS")
        str = elem.text
        start = str.find(":") + 1	
        str = str[start:].strip()
        print str
        fps = float(str)
        return round(fps, 2)