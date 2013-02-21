import time
from benchmark import Benchmark

class DynamicCubemap(Benchmark):
    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Dynamic Cubemap"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://webglsamples.googlecode.com/hg/dynamic-cubemap/dynamic-cubemap.html"
        
    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 300

    def start(self, driver):
        if driver.name.find("internet explorer") !=-1:
            raise WebMarkException("internet explorer does not support WebGLCube")
            
    def get_result(self, driver):
        time.sleep(300)
        str = self.driver.find_element_by_id("fps").text
        str = str.strip()
        return float(str)