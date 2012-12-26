import time
from benchmark import Benchmark

class Arkanoid(Benchmark):
    RESULT = 'return document.getElementById("twattext").value'

    def __init__(self):
        Benchmark.__init__(self)

    @property
    def name(self):
        return "Arkanoid"

    @property
    def metric(self):
        return "fps"

    @property
    def default_url(self):
        return "http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/Arkanoid/"

    @property
    def default_timeout(self):
        return 1500

    @property
    def expect_time(self):
        return 0

    def start(self, driver):
        time.sleep(5)
        driver.find_elements_by_tag_name("li")[0].click()


    def chk_finish(self, driver):
        return driver.execute_script(self.RESULT) != ""

    def get_result(self, driver):
        str = driver.execute_script(self.RESULT)
        start = str.find(":") + 1	
        end = str.find("MinFPS:")		
        str = str[start:end].strip()		
        print str
        fps = float(str)
        return round(fps, 2)