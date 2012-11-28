import time
from selenium.webdriver.support import wait
from benchmark import Benchmark

class PageRender(Benchmark):
    IS_Complete = 'return allComplete'

    def __init__(self, driver, logf):
        Benchmark.__init__(self, driver, logf)

    @property
    def name(self):
        return "PageRender"

    @property
    def metric(self):
        return "s"
        
    def run(self):
        self.open("http://pnp.sh.intel.com/benchmarks/WRTBench-git/htmlRendering/PageRender/iterations_rev11_new.html")
        time.sleep(5)
		
        wait.WebDriverWait(self.driver, 3600, 5).until(lambda x: x.execute_script(self.IS_Complete))
        elem = self.driver.find_element_by_xpath("//div/p")
        str = elem.text
        pos = str.find("The Final Result is") + len("The Final Result is")
        str = str[pos:].strip()
        print str
        res = float(str)
        return round(res, 2)
		