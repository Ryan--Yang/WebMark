import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class Arkanoid(Benchmark):
    RESULT = 'return document.getElementById("twattext").value'

    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "Arkanoid"

    @property
    def metric(self):
        return "fps"
        
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/canvas2D/Arkanoid/")
        time.sleep(5)
        elem = self.driver.find_elements_by_tag_name("li")
        elem[0].click()
        wait.WebDriverWait(self.driver, 3600, 30).until(lambda x: x.execute_script(self.RESULT) != "")
        str = self.driver.execute_script(self.RESULT)
        start = str.find(":") + 1	
        end = str.find("MinFPS:")		
        str = str[start:end].strip()		
        print str
        fps = float(str)
        return round(fps, 2)