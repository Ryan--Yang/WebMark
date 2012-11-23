import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class Kraken(Benchmark):
    def __init__(self, driver, logf, appmode=False):
        Benchmark.__init__(self, driver, logf, appmode)

    @property
    def name(self):
        return "Kraken"

    @property
    def metric(self):
        return "ms"
        
    def run(self):
        self.open("http://krakenbenchmark.mozilla.org/kraken-1.1/driver.html")
        time.sleep(120)
        wait.WebDriverWait(self.driver, 6000, 60).until(lambda x: x.current_url.lower().find("results") != -1)
        elem = self.driver.find_element_by_id("console")
        str = elem.text
        pos = str.find("Total:")+len("Total:")
        str = str[pos:].strip()
        pos = str.find("ms")
        return float(str[:pos])