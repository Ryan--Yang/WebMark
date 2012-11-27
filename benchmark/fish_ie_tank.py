import time
from selenium.webdriver.support import wait
from common.exceptions import WebMarkException
from benchmark import Benchmark

class FishIETank(Benchmark):
    fishes = (1, 10, 20, 50, 100, 250, 500, 1000)
    def __init__(self, driver, logf, appmode=False, offline=False, fishNumber=20):
        if fishNumber in self.fishes:
            self.fishNumber = fishNumber
        else:
            raise WebMarkException("Unsupported fish number %d, "
            "should be one of (1, 10, 20, 50, 100, 250, 500, 1000)" % fishNumber)
            
        Benchmark.__init__(self, driver, logf, appmode, offline)

    @property
    def name(self):
        return "FishIE Tank(%s%d fish)" % (self.name_common_ext(True), self.fishNumber)

    @property
    def metric(self):
        return "fps"

    @property
    def _url(self):
        if self.offline:
            return self.webbench_path + 'microsoft/testdrive/Performance/FishIETank/Default.html'
        return "http://ie.microsoft.com/testdrive/Performance/FishIETank/Default.html"

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
        self.open(self._url)
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