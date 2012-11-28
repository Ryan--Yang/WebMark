import time
from selenium.webdriver.support import wait
from common.exceptions import WebMarkException
from benchmark import Benchmark

class Aquarium(Benchmark):
    fishes = (1, 10, 50, 100, 250, 500, 1000)
    def __init__(self, driver, logf, fishNumber=50):
        if fishNumber in self.fishes:
            self.fishNumber = fishNumber
        else:
            raise WebMarkException("Unsupported fish number %d, "
            "should be one of (1, 10, 50, 100, 250, 500, 1000)" % fishNumber)
            
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "Aquarium(%d fish)" % self.fishNumber

    @property
    def metric(self):
        return "fps"

    @property
    def _order_number(self):
        for i in range(len(self.fishes)):
            if self.fishNumber == self.fishes[i]:
                return i
        
    def _set_fish_number_on_page(self):
        time.sleep(3)
        control = "setSetting" + str(self._order_number)
        fish_elems = self.driver.find_element_by_id(control)
        fish_elems.click()
        time.sleep(1)

    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/webGL/fishtank/aquarium/aquarium.html")
        self._set_fish_number_on_page()	
        elem = self.driver.find_element_by_id("fps")	
        fps = 0.0        
        for i in range(1,16):
            time.sleep(30)
            str = elem.text
            print str			
            fps += (int(str) - fps) / i
        return round(fps, 2)