import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class FishIETank(Benchmark):
    fishes = (1, 10, 20, 50, 100, 250, 500, 1000)
    def __init__(self, driver, logf, fishNumber=20):
        if fishNumber in self.fishes:
            self.fishNumber = fishNumber
        else:
            raise TypeError("Unsupported fish number, please set it to one of (1, 10, 20, 50, 100, 250, 500, 1000)")
            
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "FishIE Tank(%d fish)" % self.fishNumber

    @property
    def metric(self):
        return "fps"

    @property
    def _order_number(self):
        for i in range(len(self.fishes)):
            if self.fishNumber == self.fishes[i]:
                return i * 2 + 2
        
    def _set_fish_number_on_page(self):
        time.sleep(3)
        fish_elems = self.driver.find_elements_by_class_name("control")
        fish_elems[self._order_number].click()
        time.sleep(1)

    def run(self):
        self.driver.get("http://ie.microsoft.com/testdrive/Performance/FishIETank/Default.html")
        self._set_fish_number_on_page()
        elem = self.driver.find_element_by_id("fpsCanvas")
        fps = 0.0        
        for i in range(1,16):
            time.sleep(20)
            str = elem.get_attribute("title").lower()
            start = str.find("at") + 2
            end = str.find("fps")
            str = str[start:end].strip()
            fps += (int(str) - fps) / i
        return round(fps, 2)