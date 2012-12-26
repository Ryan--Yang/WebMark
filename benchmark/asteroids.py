import time
from benchmark import Benchmark

class Asteroids(Benchmark):
    RESULT = 'return document.getElementById("results").innerHTML'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Asteroids"

    @property
    def metric(self):
        return "score"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/asteroids/asteroids.html"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 0

    def start(self, driver):
        time.sleep(5)
        driver.find_element_by_id("canvas").click()


    def chk_finish(self, driver):
        return driver.execute_script(self.RESULT) != ""

    def get_result(self, driver):
        str = driver.execute_script(self.RESULT)
        start = str.find(":") + 1	
        end = str.find("<br>")		
        str = str[start:end].strip()		
        print str
        fps = float(str)
        return round(fps, 2)