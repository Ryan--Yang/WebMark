import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class Asteroids(Benchmark):
    RESULT = 'return document.getElementById("results").innerHTML'
	
    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "Asteroids%s" % self.name_common_ext()

    @property
    def metric(self):
        return "score"
        
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/asteroids/asteroids.html")
        time.sleep(5)
        elem = self.driver.find_element_by_id("canvas")
        elem.click()
		
        wait.WebDriverWait(self.driver, 3600, 30).until(lambda x: x.execute_script(self.RESULT) != "")
        str = self.driver.execute_script(self.RESULT)
        start = str.find(":") + 1	
        end = str.find("<br>")		
        str = str[start:end].strip()		
        print str
        fps = float(str)
        return round(fps, 2)