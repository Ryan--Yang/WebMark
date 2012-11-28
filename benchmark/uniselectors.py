import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class UniSelectors(Benchmark):
    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "UniSelectors"

    @property
    def metric(self):
        return "ms"
        
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/css/uniselectors/uniselectors.html")
        time.sleep(5)
        elem = self.driver.find_element_by_id("output")
        wait.WebDriverWait(self.driver, 1200, 10).until(lambda x: elem.text)
        str = elem.text		
        start = str.find(":") + 1	
        end = str.find("ms")		
        str = str[start:end].strip()			
        print str
        res = float(str)
        return round(res, 2)